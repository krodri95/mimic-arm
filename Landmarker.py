import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from tkinter import *
import numpy as np
from PIL import Image, ImageTk
import cv2

class PoseDetection():
    def __init__(self, model_path, canvas):
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Create a pose landmarker instance with the video mode:
        options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO)

        # Initialize the landmarker
        self.landmarker = PoseLandmarker.create_from_options(options)

        self.canvas = canvas
        self.image = None


    def draw_landmarks_on_image(self, rgb_image, detection_result):
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)
        rows, cols = annotated_image.shape[:2]

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])

        solutions.drawing_utils.draw_landmarks( annotated_image,
                                                pose_landmarks_proto,
                                                solutions.pose.POSE_CONNECTIONS,
                                                solutions.drawing_styles.get_default_pose_landmarks_style())
        # Mask the face
        cv2.ellipse(annotated_image,(int(pose_landmarks_list[0][0].x*cols), int(pose_landmarks_list[0][0].y*rows)),
                    (50,70),0,0,360,(200,200,200),-1)

        self.image = ImageTk.PhotoImage(Image.fromarray(annotated_image[:,:,::-1]))
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)