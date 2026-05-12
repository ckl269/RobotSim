import pybullet as p
import time
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -50)
p.configureDebugVisualizer(p.COV_ENABLE_KEYBOARD_SHORTCUTS, 0)

plane = p.loadURDF("plane.urdf")
robot = p.loadURDF("r2d2.urdf", [0, -1, 1])
robot2 = p.loadURDF("r2d2.urdf", [0, 1, 1])

for i in range(p.getNumJoints(robot)):
    info = p.getJointInfo(robot, i)
    print(i, info[1].decode(), "type:", info[2])

robot_joints = {
    robot: {
        "arm": 8,
        "left_gripper": 9,
        "right_gripper": 11
    },
    robot2: {
        "arm": 8,
        "left_gripper": 9,
        "right_gripper": 11
    },
}

speed = 2
arm_speed = 1
gripper_speed = 0.05

joint_positions = {
    robot: {"arm": 0, "gripper": 0},
    robot2: {"arm": 0, "gripper": 0},
}

while p.isConnected():
    p.stepSimulation()
    time.sleep(1 / 241)

    keys = p.getKeyboardEvents()

    vx1, vy1, vx2, vy2 = 0, 0, 0, 0

    if keys.get(ord("a"), 0) & p.KEY_IS_DOWN:
        vx1 = speed
    if keys.get(ord("d"), 0) & p.KEY_IS_DOWN:
        vx1 = -speed
    if keys.get(ord("w"), 0) & p.KEY_IS_DOWN:
        vy1 = speed
    if keys.get(ord("s"), 0) & p.KEY_IS_DOWN:
        vy1 = -speed

    if keys.get(ord("q"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot]["arm"] -= arm_speed
    if keys.get(ord("e"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot]["arm"] += arm_speed

    if keys.get(ord("z"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot]["gripper"] += gripper_speed
    if keys.get(ord("c"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot]["gripper"] -= gripper_speed

    if keys.get(p.B3G_LEFT_ARROW, 0) & p.KEY_IS_DOWN:
        vx2 = speed
    if keys.get(p.B3G_RIGHT_ARROW, 0) & p.KEY_IS_DOWN:
        vx2 = -speed
    if keys.get(p.B3G_UP_ARROW, 0) & p.KEY_IS_DOWN:
        vy2 = speed
    if keys.get(p.B3G_DOWN_ARROW, 0) & p.KEY_IS_DOWN:
        vy2 = -speed

    if keys.get(ord("j"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot2]["arm"] -= arm_speed
    if keys.get(ord("l"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot2]["arm"] += arm_speed

    if keys.get(ord("n"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot2]["gripper"] += gripper_speed
    if keys.get(ord("m"), 0) & p.KEY_IS_DOWN:
        joint_positions[robot2]["gripper"] -= gripper_speed

    p.resetBaseVelocity(robot, linearVelocity=[vx1, vy1, 0])
    p.resetBaseVelocity(robot2, linearVelocity=[vx2, vy2, 0])

    for r in (robot, robot2):
    # limit arm and gripper movement
        joint_positions[r]["arm"] = max(-0.4, min(0.4, joint_positions[r]["arm"]))
        joint_positions[r]["gripper"] = max(0, min(0.5, joint_positions[r]["gripper"]))

    # extend/retract arm
        p.setJointMotorControl2(
            r,
            robot_joints[r]["arm"],
            p.POSITION_CONTROL,
            targetPosition=joint_positions[r]["arm"],
            force=500
        )

    # left gripper
        p.setJointMotorControl2(
            r,
            robot_joints[r]["left_gripper"],
            p.POSITION_CONTROL,
            targetPosition=joint_positions[r]["gripper"],
            force=100
        )

        # right gripper moves opposite direction
        p.setJointMotorControl2(
            r,
            robot_joints[r]["right_gripper"],
            p.POSITION_CONTROL,
            targetPosition=-joint_positions[r]["gripper"],
            force=100
        )