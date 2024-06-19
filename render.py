import torch
from scene import Scene
import os
from tqdm import tqdm
import torchvision
from utils.general_utils import safe_state
from argparse import ArgumentParser
from arguments import ModelParams, PipelineParams, get_combined_args
from gaussian_renderer import render, GaussianModel


def save_images(rendering, gt, render_path, gts_path, idx):
    render_filename = os.path.join(render_path, f"{idx:05d}.png")
    gt_filename = os.path.join(gts_path, f"{idx:05d}.png")
    torchvision.utils.save_image(rendering, render_filename)
    torchvision.utils.save_image(gt, gt_filename)


def setup_directories(model_path, name, iteration):
    render_path = os.path.join(model_path, name, f"ours_{iteration}", "renders")
    gts_path = os.path.join(model_path, name, f"ours_{iteration}", "gt")
    os.makedirs(render_path, exist_ok=True)
    os.makedirs(gts_path, exist_ok=True)
    return render_path, gts_path


def render_views(views, gaussians, pipeline, background, render_path, gts_path):
    for idx, view in enumerate(tqdm(views, desc="Rendering progress")):
        rendering = render(view, gaussians, pipeline, background)["render"]
        gt = view.original_image[:3, :, :]
        save_images(rendering, gt, render_path, gts_path, idx)


def render_set(model_path, name, iteration, views, gaussians, pipeline, background):
    render_path, gts_path = setup_directories(model_path, name, iteration)
    render_views(views, gaussians, pipeline, background, render_path, gts_path)


def render_sets(dataset, iteration, pipeline, skip_train, skip_test):
    with torch.no_grad():
        gaussians = GaussianModel(dataset.sh_degree)
        scene = Scene(dataset, gaussians, load_iteration=iteration, shuffle=False)
        background_color = [1, 1, 1] if dataset.white_background else [0, 0, 0]
        background = torch.tensor(background_color, dtype=torch.float32, device="cuda")

        if not skip_train:
            render_set(dataset.model_path, "train", scene.loaded_iter, scene.getTrainCameras(), gaussians, pipeline, background)
        if not skip_test:
            render_set(dataset.model_path, "test", scene.loaded_iter, scene.getTestCameras(), gaussians, pipeline, background)


def main():
    parser = ArgumentParser(description="Testing script parameters")
    model = ModelParams(parser, sentinel=True)
    pipeline = PipelineParams(parser)
    parser.add_argument("--iteration", default=-1, type=int)
    parser.add_argument("--skip_train", action="store_true")
    parser.add_argument("--skip_test", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = get_combined_args(parser)

    print("Rendering " + args.model_path)
    safe_state(args.quiet)
    render_sets(model.extract(args), args.iteration, pipeline.extract(args), args.skip_train, args.skip_test)


if __name__ == "__main__":
    main()
