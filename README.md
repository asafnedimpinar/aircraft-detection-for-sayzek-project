# aircraft-detection-for-sayzek-project
🚀 AI-Powered Air and Ground Target Detection and Classification System

This project is designed to detect and classify air and ground targets in real-time from camera or video feeds.
It uses Ultralytics YOLOv8 for object detection and a custom-trained ResNet50 model for aircraft type classification.

🔍 Features

Real-time detection from live camera or video input

Separate detection models for air and ground targets

Aircraft type classification using a ResNet50-based model

YOLOv8-based fast and accurate object detection

Modular Python structure (separate files for model loading, classification, and main control)

Easy model switching and input source selection

🧠 Model Overview

YOLOv8 Model (Ground and Air Detection)

Used for detecting ground and aerial objects in frames.

ResNet50 Classifier (Aircraft Recognition)

Classifies detected aircraft into predefined categories.

🗂️ Project Structure
AI_Target_Detection/
│
├── Main/
│   ├── land_airborne_model_selection.py     # Main runnable script
│
├── Airplane_classifier/
│   ├── aircraft_classifier.py               # Handles aircraft classification
│   ├── model/aircraft_model.h5              # Trained ResNet50 model
│   ├── model/aircraft_labels.json           # Label file for aircraft classes
│
├── Image_Detector/
│   ├── dynamic_model_detection.py           # YOLOv8 detection pipeline
│
├── Live_Detector/
│   ├── realtime_camera_detection.py         # Real-time camera input handler
│
├── model_loader.py                          # Loads YOLOv8 models for air/ground targets
└── requirements.txt
