import pybullet as p
import pybullet_data
import os
import time
import config
from robot import Panda
from cameras import ExternalCamera, OnboardCamera
import matplotlib.pyplot as plt


# create simulation and place camera
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.resetDebugVisualizerCamera(cameraDistance=config.cameraDistance, 
                                cameraYaw=config.cameraYaw,
                                cameraPitch=config.cameraPitch, 
                                cameraTargetPosition=config.cameraTargetPosition)

# add additional cameras
external_camera = ExternalCamera()
onboard_camera = OnboardCamera()

# load the objects
urdfRootPath = pybullet_data.getDataPath()
plane = p.loadURDF(os.path.join(urdfRootPath, "plane.urdf"), basePosition=[0, 0, -0.625])
table = p.loadURDF(os.path.join(urdfRootPath, "table/table.urdf"), basePosition=[0.5, 0, -0.625])
cube = p.loadURDF(os.path.join(urdfRootPath, "cube_small.urdf"), basePosition=[0.6, -0.2, 0.05])

# load the robot and set its home position
panda = Panda(basePosition=config.baseStartPosition,
                baseOrientation=p.getQuaternionFromEuler(config.baseStartOrientationE),
                jointStartPositions=config.jointStartPositions)

# run simluation
timestep = 0
while True:
    # record images to "images" folder
    if timestep % 10 == 0:
        # we use the robot's state to position the onboard camera
        state = panda.get_state()
        image1 = external_camera.get_image()
        image2 = onboard_camera.get_image(ee_position=state["ee-position"], ee_quaternion=state["ee-quaternion"])
        plt.imsave('images/' + str(timestep) + '-1.png', image1)
        plt.imsave('images/' + str(timestep) + '-2.png', image2)
    p.stepSimulation()
    time.sleep(config.control_dt)
    timestep += 1