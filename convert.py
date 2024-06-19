import os
import logging
import shutil
from argparse import ArgumentParser

def setup_parser():
    parser = ArgumentParser("Colmap converter")
    parser.add_argument("--no_gpu", action='store_true')
    parser.add_argument("--skip_matching", action='store_true')
    parser.add_argument("--source_path", "-s", required=True, type=str)
    parser.add_argument("--camera", default="OPENCV", type=str)
    parser.add_argument("--colmap_executable", default="", type=str)
    parser.add_argument("--resize", action="store_true")
    parser.add_argument("--magick_executable", default="", type=str)
    return parser

def execute_command(command, error_message):
    exit_code = os.system(command)
    if exit_code != 0:
        logging.error(f"{error_message} with code {exit_code}. Exiting.")
        exit(exit_code)

def feature_extraction(args, colmap_command, use_gpu):
    feat_extracton_cmd = (
        f"{colmap_command} feature_extractor "
        f"--database_path {args.source_path}/distorted/database.db "
        f"--image_path {args.source_path}/input "
        f"--ImageReader.single_camera 1 "
        f"--ImageReader.camera_model {args.camera} "
        f"--SiftExtraction.use_gpu {use_gpu}"
    )
    execute_command(feat_extracton_cmd, "Feature extraction failed")

def feature_matching(args, colmap_command):
    feat_matching_cmd = (
        f"{colmap_command} exhaustive_matcher "
        f"--database_path {args.source_path}/distorted/database.db "
    )
    execute_command(feat_matching_cmd, "Feature matching failed")

def create_distorted_model(args, colmap_command):
    create_model_cmd = (
        f"{colmap_command} mapper "
        f"--database_path {args.source_path}/distorted/database.db "
        f"--image_path {args.source_path}/input "
        f"--output_path {args.source_path}/distorted/sparse "
    )
    execute_command(create_model_cmd, "Creating sparse model failed")

def undistort_images(args, colmap_command):
    undistort_cmd = (
        f"{colmap_command} image_undistorter "
        f"--image_path {args.source_path}/input "
        f"--input_path {args.source_path}/distorted/sparse "
        f"--output_path {args.source_path} "
        f"--output_type COLMAP "
        f"--max_image_size 2000"
    )
    execute_command(undistort_cmd, "Image undistortion failed")

def convert_model(args, colmap_command):
    convert_model_cmd = (
        f"{colmap_command} model_converter "
        f"--input_path {args.source_path}/sparse "
        f"--output_path {args.source_path}/sparse "
        f"--output_type TXT"
    )
    execute_command(convert_model_cmd, "Model conversion failed")

def move_sparse_files(args):
    files = os.listdir(os.path.join(args.source_path, "sparse"))
    os.makedirs(os.path.join(args.source_path, "sparse/0"), exist_ok=True)
    for file in files:
        if file == '0':
            continue
        source_file = os.path.join(args.source_path, "sparse", file)
        destination_file = os.path.join(args.source_path, "sparse", "0", file)
        shutil.move(source_file, destination_file)

def resize_images(args, magick_command):
    print("Copying and resizing...")
    os.makedirs(args.source_path + "/images_2", exist_ok=True)
    os.makedirs(args.source_path + "/images_4", exist_ok=True)
    os.makedirs(args.source_path + "/images_8", exist_ok=True)
    files = os.listdir(args.source_path + "/images")
    for file in files:
        source_file = os.path.join(args.source_path, "images", file)
        resize_and_copy_image(source_file, args.source_path + "/images_2", "50%", magick_command)
        resize_and_copy_image(source_file, args.source_path + "/images_4", "25%", magick_command)
        resize_and_copy_image(source_file, args.source_path + "/images_8", "12.5%", magick_command)
    print("Done.")

def resize_and_copy_image(source_file, destination_path, resize_percentage, magick_command):
    destination_file = os.path.join(destination_path, os.path.basename(source_file))
    shutil.copy2(source_file, destination_file)
    resize_cmd = f"{magick_command} mogrify -resize {resize_percentage} {destination_file}"
    execute_command(resize_cmd, f"{resize_percentage} resize failed")

def main():
    parser = setup_parser()
    args = parser.parse_args()
    colmap_command = f'"{args.colmap_executable}"' if args.colmap_executable else "colmap"
    magick_command = f'"{args.magick_executable}"' if args.magick_executable else "magick"
    use_gpu = 1 if not args.no_gpu else 0

    if not args.skip_matching:
        os.makedirs(args.source_path + "/distorted/sparse", exist_ok=True)
        feature_extraction(args, colmap_command, use_gpu)
        feature_matching(args, colmap_command)
        create_distorted_model(args, colmap_command)

    undistort_images(args, colmap_command)
    convert_model(args, colmap_command)
    move_sparse_files(args)

    if args.resize:
        resize_images(args, magick_command)

if __name__ == "__main__":
    main()

