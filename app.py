import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image


models = {
    "Orange": YOLO("TRAINED MODEL\ORANGEbest.pt"),
    "Banana": YOLO("TRAINED MODEL\BANANAbest.pt"),
    "Pomegranate": YOLO("TRAINED MODEL\POMEGRANATEbest.pt"),
    "Papaya": YOLO("TRAINED MODEL\PAPAbest.pt"),
    "Mango": YOLO("TRAINED MODEL\MANGObest.pt"),
}


def predict_image(image, model):
    results = model(image)
    annotated_frame = results[0].plot() 
    return annotated_frame


def bgr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def predict_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        
        frame_rgb = bgr_to_rgb(frame)
        annotated_frame_rgb = bgr_to_rgb(annotated_frame)
       
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image(frame_rgb, caption="Original Frame")
            with col2:
                st.image(annotated_frame_rgb, caption="Predicted Frame")
    cap.release()


def webcam_detection(model):
    cap = cv2.VideoCapture(0)
    stframe1 = st.empty()
    stframe2 = st.empty()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        
        frame_rgb = bgr_to_rgb(frame)
        annotated_frame_rgb = bgr_to_rgb(annotated_frame)
        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                stframe1.image(frame_rgb, caption="Original Frame")
            with col2:
                stframe2.image(annotated_frame_rgb, caption="Predicted Frame")
    cap.release()


st.title("Multi-Fruits Ripeness Detection")


fruit = st.sidebar.selectbox("Select Fruit", list(models.keys()))


st.write(f"Selected Model: {fruit}")


option = st.radio(
    "Choose an input method:",
    ("Upload Image", "Upload Video", "Real-time Webcam")
)

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)
        model = models[fruit]
        annotated_image = predict_image(image, model)
        
        annotated_image_rgb = bgr_to_rgb(annotated_image)
        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original Image")
            with col2:
                st.image(annotated_image_rgb, caption="Predicted Image")

elif option == "Upload Video":
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
        model = models[fruit]
        st.write("Processing video...")
        predict_video("temp_video.mp4", model)

elif option == "Real-time Webcam":
    st.write("Starting webcam...")
    model = models[fruit]
    webcam_detection(model)
