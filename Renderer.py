import numpy as np
import math
import cv2
import mediapipe as mp
from PlanarRobot import PlanarRobot
from Landmarker import PoseDetection


class Renderer:
    '''Render the planar robot manipulator along with the pose landmarks'''
    def __init__(self, length, canvasBot, canvasImg, videoPath):
        self.lm = PoseDetection(model_path='models/pose_landmarker_lite.task', canvas=canvasImg)
        self.bot = PlanarRobot([length]*2, canvasBot)

        self.counter = 0
        self.cap = cv2.VideoCapture(videoPath)

        # Check if camera opened successfully
        if (self.cap.isOpened()== False): 
            print('Error opening video stream or file')

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(f'Video frame rate: {self.fps}')


    def run(self):
        
        ret, frame = self.cap.read()
        if ret == True:
            frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
        
            # Calculate the timestamp for each frame.
            time_stamp = int(self.counter*1000/self.fps)

            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            pose_landmarker_result = self.lm.landmarker.detect_for_video(mp_image, time_stamp)
            self.counter += 1

            # Display the resulting frame
            if len(pose_landmarker_result.pose_landmarks):
                self.lm.draw_landmarks_on_image(frame, pose_landmarker_result)
                self.bot.mimickArm(pose_landmarker_result.pose_landmarks)

        # Call update_frame after 20 ms (to get ~50 FPS)
        self.lm.canvas.after(20, self.run)


    def releaseVideo(self):
        self.cap.release()
        print('Released the video capture')