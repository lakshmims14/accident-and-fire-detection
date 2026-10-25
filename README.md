# Fire and Accident Detection using YOLOv8

A computer vision project that detects road accidents and fire/smoke in images and videos using custom-trained YOLOv8 models, with a Django web app and a MySQL database.

I built this project to learn how to train and test object detection models on custom datasets and to connect an AI model to a web application.

## Features

- Accident detection in videos using a custom-trained YOLOv8 model
- Fire and smoke detection in images and videos using a second YOLOv8 model
- Training scripts for both models, with dataset settings in YAML files
- Prediction scripts that run the trained models on new images and videos
- Django web app for [describe what the user can do, for example: uploading an image or video and viewing the detection result]
- MySQL database connected to the Django app to store [add what is stored, for example: user details or detection results]

## Tech Stack

- **AI / Computer Vision:** Python, YOLOv8 (Ultralytics)
- **Web app:** Django, HTML, CSS
- **Database:** MySQL
- **Datasets:** custom accident dataset, Roboflow fire and smoke dataset
- **Tools:** PyCharm, GitHub

## How It Works

1. A dataset of images is prepared and labelled for each task (accident, fire and smoke).
2. The dataset paths and class names are set in a YAML file (`car_accident.yaml`, `data.yaml`).
3. A YOLOv8 model is trained on each dataset using the training scripts.
4. The trained models are tested on new images and videos using the prediction scripts.
5. The Django web app connects the detection to a web interface, with data stored in MySQL.

## Project Structure

```
Accident/                              # Accident detection model
  train_yolov8.py                      # trains the accident model
  detect_accident.py                   # runs detection on videos
  car_accident.yaml                    # dataset configuration
fire-smoke-detection.v2-v2.yolov8/     # Fire and smoke detection model
  train.py                             # trains the fire and smoke model
  prediction.py                        # runs detection on images and videos
  data.yaml                            # dataset configuration
  prediction_result.jpg                # sample result
project/                               # Django web app
  app/  project/  static/  templates/  manage.py
```

## Dataset

- **Accident detection:** [describe your dataset: where the images came from and how many images, for example: "custom dataset of N images collected from ... and labelled with ..."]
- **Fire and smoke detection:** Roboflow dataset "fire-smoke-detection" (version 2, YOLOv8 format). [Add the dataset link and check its license on Roboflow, then credit the author here.]

## Note

This repository contains the source code, configuration files and sample results. The datasets, training outputs and large video files are not included because of GitHub's file size limits, so the project cannot be run directly from a copy of this repository. The code is shared to show how the project was built.

## Author

**Lakshmi MS** - Python Full Stack Developer (fresher)
[LinkedIn](https://www.linkedin.com/in/lakshmi-m-s-aa97a2293/) | [GitHub](https://github.com/lakshmims14)
