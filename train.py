import os
import sys
import torch
from random import randint
from utils.loss_utils import l1_loss, ssim
from gaussian_renderer import render, network_gui
from scene import Scene, GaussianModel
from utils.general_utils import safe_state
from tqdm import tqdm
from utils.image_utils import psnr
from argparse import ArgumentParser
from arguments import ModelParams, PipelineParams, OptimizationParams

try:
    from torch.utils.tensorboard import SummaryWriter
    TENSORBOARD_FOUND = True
except ImportError:
    TENSORBOARD_FOUND = False

def prepare_output_and_logger(dataset):
    if TENSORBOARD_FOUND:
        log_dir = os.path.join("logs", str(uuid.uuid4()))
        return SummaryWriter(log_dir)
    return None

def setup_training_environment(dataset, opt, checkpoint):
    gaussians = GaussianModel(dataset.sh_degree)
    scene = Scene(dataset, gaussians)
    gaussians.training_setup(opt)
    first_iter = 0
    if checkpoint:
        model_params, first_iter = torch.load(checkpoint)
        gaussians.restore(model_params, opt)
    return gaussians, scene, first_iter

def prepare_background(dataset):
    bg_color = [1, 1, 1] if dataset.white_background else [0, 0, 0]
    return torch.tensor(bg_color, dtype=torch.float32, device="cuda")

def training_loop(opt, scene, gaussians, pipeline, background, tb_writer, testing_iterations, saving_iterations, checkpoint_iterations, debug_from):
    ema_loss_for_log = 0.0
    progress_bar = tqdm(range(1, opt.iterations + 1), desc="Training progress")
    for iteration in progress_bar:
        if network_gui.conn is None:
            network_gui.try_connect()
        while network_gui.conn is not None:
            net_image_bytes = None
            custom_cam, do_training, pipe_state = network_gui.get_remote_cmds()
            if not do_training:
                break

        train_step(scene, gaussians, pipeline, background, tb_writer, iteration, debug_from, ema_loss_for_log)
        
        if iteration in testing_iterations:
            l1_test, psnr_test = test_step(scene, gaussians, pipeline, background)
            if tb_writer:
                tb_writer.add_scalar('l1_test', l1_test, iteration)
                tb_writer.add_scalar('psnr_test', psnr_test, iteration)

        if iteration in saving_iterations:
            save_checkpoint(gaussians, iteration)

        if iteration in checkpoint_iterations:
            save_checkpoint(gaussians, iteration)

        progress_bar.set_postfix(loss=ema_loss_for_log)
        torch.cuda.empty_cache()

def train_step(scene, gaussians, pipeline, background, tb_writer, iteration, debug_from, ema_loss_for_log):
    scene_data = scene.get_training_batch()
    rendered = render(scene_data, gaussians, pipeline, background)
    loss = compute_loss(rendered, scene_data)
    gaussians.update(loss)

    if tb_writer:
        tb_writer.add_scalar('train_loss', loss, iteration)
    
    ema_loss_for_log = ema_loss_for_log * 0.99 + loss.item() * 0.01

    if iteration >= debug_from:
        print(f"Debugging at iteration {iteration}")

def test_step(scene, gaussians, pipeline, background):
    test_data = scene.get_test_batch()
    rendered = render(test_data, gaussians, pipeline, background)
    l1_test = l1_loss(rendered, test_data).item()
    psnr_test = psnr(rendered, test_data)
    return l1_test, psnr_test

def compute_loss(rendered, scene_data):
    return l1_loss(rendered, scene_data)

def save_checkpoint(gaussians, iteration):
    checkpoint_path = f"checkpoint_{iteration}.pt"
    torch.save((gaussians.state_dict(), iteration), checkpoint_path)

def main():
    parser = ArgumentParser(description="Training script parameters")
    model_params = ModelParams(parser)
    opt_params = OptimizationParams(parser)
    pipe_params = PipelineParams(parser)
    parser.add_argument('--ip', type=str, default="127.0.0.1")
    parser.add_argument('--port', type=int, default=6009)
    parser.add_argument('--debug_from', type=int, default=-1)
    parser.add_argument('--detect_anomaly', action='store_true', default=False)
    parser.add_argument("--test_iterations", nargs="+", type=int, default=[5000, 10000])
    parser.add_argument("--save_iterations", nargs="+", type=int, default=[5000, 10000])
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--checkpoint_iterations", nargs="+", type=int, default=[])
    parser.add_argument("--start_checkpoint", type=str, default=None)
    args = parser.parse_args(sys.argv[1:])
    args.save_iterations.append(opt_params.iterations)

    print("Optimizing " + args.model_path)
    safe_state(args.quiet)

    network_gui.init(args.ip, args.port)
    torch.autograd.set_detect_anomaly(args.detect_anomaly)

    tb_writer = prepare_output_and_logger(model_params.extract(args))
    gaussians, scene, first_iter = setup_training_environment(model_params.extract(args), opt_params.extract(args), args.start_checkpoint)
    background = prepare_background(model_params.extract(args))

    training_loop(opt_params.extract(args), scene, gaussians, pipe_params.extract(args), background, tb_writer, args.test_iterations, args.save_iterations, args.checkpoint_iterations, args.debug_from)

    print("\nTraining complete.")

if __name__ == "__main__":
    main()
