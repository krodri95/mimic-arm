"""
pose_detection.py

A module for detecting and visualising human left arm pose landmarks using a pre-trained model. 
"""

from tkinter import *  # pylint: disable=unused-wildcard-import

import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from PIL import Image, ImageTk


class PoseDetection:
    """
    A class for detecting and visualizing pose landmarks in images.

    This class utilizes a pose detection model to identify landmarks on human poses
    in an image and display the results on a given canvas. It provides functionality
    to initialize a pose landmarker and annotate images with detected pose landmarks,
    while also masking specific areas like the face.

    Attributes:
        landmarker: An instance of the pose landmarker for detecting landmarks.
        canvas: A Tkinter canvas object where the annotated images are displayed.
        image: The current annotated image to be displayed on the canvas.

    Methods:
        __init__(model_path, canvas):
            Initializes the pose landmarker with the given model and canvas.

        draw_landmarks_on_image(rgb_image, detection_result):
            Draws pose landmarks on an RGB image and masks the face area.
    """

    def __init__(self, model_path, canvas):
        base_options = mp.tasks.BaseOptions
        pose_landmarker = mp.tasks.vision.PoseLandmarker
        pose_landmarker_options = mp.tasks.vision.PoseLandmarkerOptions
        vision_running_mode = mp.tasks.vision.RunningMode

        # Create a pose landmarker instance with the video mode:
        options = pose_landmarker_options(
            base_options=base_options(model_asset_path=model_path),
            running_mode=vision_running_mode.VIDEO,
        )

        # Initialize the landmarker
        self.landmarker = pose_landmarker.create_from_options(options)

        self.canvas = canvas
        self.image = None

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        """
        Draws pose landmarks and masks the face on the given RGB image.

        This function takes an input RGB image and a detection result containing pose landmarks, 
        visualises the left arm landmarks on the image, and masks the face region. 
        The annotated image is then displayed on a canvas.

        Args:
            rgb_image (np.ndarray): The input RGB image as a NumPy array.
            detection_result: The detection result containing pose landmarks.

        Returns:
            None
        """
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)
        rows, cols = annotated_image.shape[:2]

        # Loop through the detected poses to visualize.
        for pose_landmarks in pose_landmarks_list:
            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend(
                [landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                 for landmark in pose_landmarks]
            )

            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style(),
            )

            # Mask the face
            cv2.ellipse(
                annotated_image,
                (int(pose_landmarks_list[0][0].x*cols), int(pose_landmarks_list[0][0].y*rows)),
                (50,70),
                0,
                0,
                360,
                (200,200,200),
                -1
            )

            self.image = ImageTk.PhotoImage(Image.fromarray(annotated_image[:, :, ::-1]))
            self.canvas.create_image(0, 0, anchor=NW, image=self.image)
