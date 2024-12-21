"""
renderer.py

This module defines the `Renderer` class, which integrates the functionalities of a
planar robot manipulator with pose landmark detection from a video stream.
"""

import cv2
import mediapipe as mp
from land_marker import PoseDetection
from planar_robot import PlanarRobot


class Renderer:
    """Render the planar robot manipulator along with the pose landmarks"""

    def __init__(self, length, canvas_bot, canvas_img, video_path):
        self.lm = PoseDetection(
            model_path="models/pose_landmarker_lite.task", canvas=canvas_img
        )
        self.bot = PlanarRobot([length] * 2, canvas_bot)

        self.counter = 0
        self.cap = cv2.VideoCapture(video_path)

        # Check if camera opened successfully
        if self.cap.isOpened() is False:
            print("Error opening video stream or file")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(f"Video frame rate: {self.fps}")

    def run(self):
        """
        Capture a frame from the video stream, process it to detect pose landmarks, and
        update the visualisation of the robot's arm based on the detected pose.
        """

        ret, frame = self.cap.read()
        if ret is True:
            frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))

            # Calculate the timestamp for each frame.
            time_stamp = int(self.counter * 1000 / self.fps)

            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            )

            pose_landmarker_result = self.lm.landmarker.detect_for_video(mp_image, time_stamp)
            self.counter += 1

            # Display the resulting frame
            if len(pose_landmarker_result.pose_landmarks):
                self.lm.draw_landmarks_on_image(frame, pose_landmarker_result)
                self.bot.mimick_arm(pose_landmarker_result.pose_landmarks)

        # Call update_frame after 20 ms (to get ~50 FPS)
        self.lm.canvas.after(20, self.run)

    def release_video(self):
        """Release the video capture resource"""
        self.cap.release()
        print("Released the video capture")
    