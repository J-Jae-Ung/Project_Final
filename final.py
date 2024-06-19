import subprocess
import os
import glob

def get_video_duration(input_file):
    try:
        # Use ffprobe to get the video duration
        ffprobe_command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        
        # Run the ffprobe command and capture the output
        result = subprocess.run(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        duration = float(result.stdout)
        return duration
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while getting video duration: {e}")
        return None

def run_ffmpeg(input_file, output_pattern, frame_rate):
    try:
        # Construct the ffmpeg command
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_file,
            '-r', str(frame_rate),
            output_pattern
        ]
        
        # Run the ffmpeg command
        subprocess.run(ffmpeg_command, check=True)
        print("FFmpeg command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running FFmpeg: {e}")

def run_convert_py(input_dir):
    try:
        # Run the convert.py script
        colmap_executable = "COLMAP-3.8-windows-cuda\\COLMAP.bat"
        convert_command = ['python', 'convert.py', '-s', input_dir, '--colmap_executable', colmap_executable]
        subprocess.run(convert_command, check=True)
        print("convert.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running convert.py: {e}")

def run_train_py(input_dir):
    try:
        # Run the train.py script
        train_command = ['python', 'train.py', '-s', input_dir]
        subprocess.run(train_command, check=True)
        print("train.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running train.py: {e}")

def get_latest_output_folder(output_base):
    output_folders = glob.glob(f'{output_base}/*/')
    if not output_folders:
        return None
    latest_folder = max(output_folders, key=os.path.getmtime)
    return latest_folder


if __name__ == "__main__":
    filename = input("Please enter the name of the MP4 file (without path or with .mp4 extension): ").strip()
    
    # Add .mp4 extension if not present
    if not filename.endswith('.mp4'):
        filename += '.mp4'
    
    # Derive the output base name by removing the extension
    base_name = os.path.splitext(filename)[0]
    
    input_file = f'input_data/{filename}'
    output_dir = f'input_data/{base_name}/input'
    output_pattern = f'{output_dir}/{base_name}%03d.png'
    input_dir = f'input_data/{base_name}'
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the video duration
    duration = get_video_duration(input_file)
    if duration is not None:
        # Set the frame rate based on the video duration
        if duration >= 10:
            frame_rate = 7
        else:
            frame_rate = 8
        
        print(f"Video duration: {duration} seconds. Using frame rate: {frame_rate}")
        
        run_ffmpeg(input_file, output_pattern, frame_rate)
        run_convert_py(input_dir)
        run_train_py(input_dir)


    # Get the latest output folder
        latest_output_folder = get_latest_output_folder('output')
        if latest_output_folder:
            new_folder_name = f'output/{base_name}'
            os.rename(latest_output_folder, new_folder_name)
            print(f"Renamed latest output folder to: {new_folder_name}")
        else:
            print("No output folders found.")



