# Installation Tutorial For Gaussian Splatting

| **Total file size** | **7GB** |
|---|---|
|**VRAM**|**24GB**|

## step 1: setting up the environment

Install [Pinokio](https://pinokio.computer/), we wrote a pinokio file where you **just need 1 click to install all of the dependencies**. 
Then open up Pinokio, go to the top right button "Discover" 
Copy the link of this repository, paste the link at the side that says "enter git URL"
And press download
You can find "Project_Final.git" in your Pinokio list (if you didn't change the save name). 
Press **Install** to download all the dependencies in a conda env

## step 2: Structure from Motion (SfM) with COLMAP

### Extra step for inputs that are videos
This step is for custom inputs. If you have a video, please extract it into image frames. This can be done with FFMPEG. Below is a template for the ffmpeg command.
```
ffmpeg -i input_data/file.mp4 -r 1/1 input_data/$filename%03d.png
```

Now, with a collection of images of a scene, you would need to put the **set** of input images into the `input_data/<your_image_collection>/input` folder. Eg. `fern/input`

Taking 2 collections (fern and toy_truck) of input images as an example, below is the File Structure **requirements** before running `convert.py`. You would need to create these folders.
```
📂gaussian-splatting-Windows.git/ # this is root
├── 📂input_data/
│	├── 📂fern/
│	│	├── 📂input/
│	│	│	├── 🖼️image1.jpg
│	│	│	├── 🖼️image2.jpg
│	│	│	│...
│	├── 📂toy_truck/
│	│	├── 📂input/
│	│	│	├── 🖼️image1.jpg
│	│	│	├── 🖼️image2.jpg
│	│	│	│...
│ │...
│...
```

Now, using `fern` as an example, 
```
python convert.py -s input_data/fern --colmap_executable COLMAP-3.8-windows-cuda\COLMAP.bat
```
Below is the template:
```
python convert.py -s <your_input_dir> --colmap_executable COLMAP-3.8-windows-cuda\COLMAP.bat
```

## step 3: Train/optimize the images

This step is pretty straight forward, you just got to run the below command (using `fern` as an example):
```
python train.py -s input_data/fern
```
Below is the template:
```
python train.py -s <input_dir>
```

## step 4: View the result!
Go to the `output` folder, and you can see some randomly generated folder name. You can rename this to anything you want, like the scene name and the times it was ran.

```
📂gaussian-splatting-Windows.git/ # this is root
├── 📂output/ 
│	├── 📂a2973a46-9/ <--
│ │	├── 📂point_cloud/
│ │	│	└── ...
│ │	├── 📜cameras.json/
│ │	├── 📜cfg_args/
│ │	└── 📜input.ply/
│ │...
│...
```

So I'll rename mine from `a2973a46-9` -> `fern`

Now, using the below command with `fern` as an example, you can view it in 3D.
```
start viewers/bin/SIBR_GaussianViewer_app.exe . -m output\fern
```
Below would be a template
```
start viewers/bin/SIBR_GaussianViewer_app.exe . -m <output_folder>
```

## The tutorial ends here. 

The following are a copy of the original repository for references.

This tutorial is made by the team at bycloud AI, feel free to support our endevour in making installation tutorials here! 


- *Something is broken, how did this happen?* We tried hard to provide a solid and comprehensible basis to make use of the paper's method. We have refactored the code quite a bit, but we have limited capacity to test all possible usage scenarios. Thus, if part of the website, the code or the performance is lacking, please create an issue. If we find the time, we will do our best to address it.
