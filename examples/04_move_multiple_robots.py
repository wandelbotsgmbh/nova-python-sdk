from nova import Nova, ptp, jnt, Pose, Controller, speed_up_movement_controller
import asyncio
import numpy as np


async def main():
    nova = Nova()
    cell = nova.cell()
    ur = await cell.controller("ur")
    kuka = await cell.controller("kuka")

    await asyncio.gather(move_robot(ur), move_robot(kuka))


async def move_robot(controller: Controller):
    home_joints = (0, -np.pi / 4, -np.pi / 4, -np.pi / 4, np.pi / 4, 0)

    async with controller:
        motion_group = controller.get_motion_group()

        current_pose = await motion_group.tcp_pose("Flange")
        target_pose = current_pose @ Pose((100, 0, 0, 0, 0, 0))
        actions = [jnt(home_joints), ptp(target_pose), jnt(home_joints)]

        await motion_group.stream_run(
            actions, tcp="Flange", movement_controller=speed_up_movement_controller
        )


if __name__ == "__main__":
    asyncio.run(main())
