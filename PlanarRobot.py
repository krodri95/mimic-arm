import numpy as np
import math
from collections import namedtuple

MarkerBase = namedtuple('MarkerBase', ['x', 'y'])


class Marker(MarkerBase):
    '''Process the landmarker data and compute the joint angles'''
    def __sub__(self, vec):
        return Marker(self.x - vec.x, self.y - vec.y)
    
    def sign(self, vec):
        return math.acos((self.x * vec.x + self.y * vec.y)/(math.hypot(self.x, self.y)*math.hypot(vec.x, vec.y)))

    def angle(self, vec):
        # Note: the z-axis of image coordinate system is pointing inwards and that of the robot coordinate system is pointing outwards
        k_hat = -int(math.copysign(1, self.x * vec.y - self.y * vec.x))
        return math.acos((self.x * vec.x + self.y * vec.y)/(math.hypot(self.x, self.y)*math.hypot(vec.x, vec.y)))*k_hat


class PlanarRobot:
    '''Two-segment planar robot manipulator'''
    def __init__(self,lengths, canvas):
        self.l1, self.l2 = lengths
        self.theta1, self.theta2 = 0.0, 0.0
        self.p1 = self.l1*np.array([[1.0],[0.0]])
        self.p2 = self.p1 + self.l2*np.array([[1.0],[0.0]])

        self.drawItems = []
        self.imgw = int(canvas.__getitem__('width'))
        self.imgh = int(canvas.__getitem__('height'))
        self.canvas = canvas


    def updateParameters(self, angles):
        self.theta1, self.theta2 = angles
        self.p1 = self.l1*np.array([[math.cos(self.theta1)],[math.sin(self.theta1)]])
        self.p2 = self.p1 + self.l2*np.array([[math.cos(self.theta1+self.theta2)],[math.sin(self.theta1+self.theta2)]])
        self.clear()
        self.draw()
    

    def robot2img(self, x, y):
        '''
        Convert the robot frame coordinates to image coordinates.
        In the robot coordinate system, the x-axis points towards the right and the y-axis up whereas in the 
        image coordinate system the x-axis is to the right and the y-axis points down. The origin of the robot
        coordinate system is at the centre of the image.
        '''
        u = int(x + self.imgw//2)
        v = int(self.imgh//2 - y)
        return [u, v]


    def draw(self):
        s = self.robot2img(0,0)
        m = self.robot2img(self.p1[0], self.p1[1])
        e = self.robot2img(self.p2[0], self.p2[1])
        self.drawItems.append(self.canvas.create_line(s[0], s[1], m[0], m[1], fill="red",width=30))
        self.drawItems.append(self.canvas.create_line(m[0], m[1], e[0], e[1], fill="green",width=30))
        self.drawItems.append(self.canvas.create_oval(s[0]-10,s[1]-10,s[0]+10,s[1]+10,fill="black"))
        self.drawItems.append(self.canvas.create_oval(m[0]-10,m[1]-10,m[0]+10,m[1]+10,fill="black"))


    def clear(self):
        for item in self.drawItems:
            self.canvas.delete(item)
        self.drawItems = []


    def mimickArm(self, pose_landmarks):
        '''
        Compute the joint angles and update the parameters.
        '''
        # 11 - left shoulder
        # 12 - right shoulder
        # 13 - left elbow
        # 15 - left wrist

        rs = Marker(pose_landmarks[0][12].x*self.imgw, pose_landmarks[0][12].y*self.imgh)
        ls = Marker(pose_landmarks[0][11].x*self.imgw, pose_landmarks[0][11].y*self.imgh)
        le = Marker(pose_landmarks[0][13].x*self.imgw, pose_landmarks[0][13].y*self.imgh)
        lw = Marker(pose_landmarks[0][15].x*self.imgw, pose_landmarks[0][15].y*self.imgh)

        vec1 = ls - rs
        vec2 = le - ls
        vec3 = lw - le

        theta1 = vec1.angle(vec2)
        theta2 = vec2.angle(vec3)
        self.updateParameters([theta1,theta2])