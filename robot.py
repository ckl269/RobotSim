import pybullet as p

import time

import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -50)


plane = p.loadURDF("plane.urdf")
robot = p.loadURDF("r2d2.urdf", [0, 0, 1])
#p.loadURDF("cube.urdf", [2, 0, 1])

while True:
    p.stepSimulation()
    time.sleep(1 / 241)

    keys = p.getKeyboardEvents()
    
    vx2=0
    vy2=0
    speed2 = 0.4

    if p.B3G_LEFT_ARROW in keys:
        vx2= speed2
    if p.B3G_RIGHT_ARROW in keys:
        vx2= -speed2
    if p.B3G_UP_ARROW in keys:
        vy2= speed2
    if p.B3G_DOWN_ARROW in keys:
        vy2= -speed2

    p.resetBaseVelocity(robot, linearVelocity=[vx2, vy2, 0])
