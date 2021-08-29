# LEGO type:advanced slot:5 autostart

from util.rotation import rotate_hub_display_to_value
from runtime import VirtualMachine
from mindstorms import Motor, MotorPair
from mindstorms.control import wait_for_seconds
import hub

cool_animation = [
    "00000:77077:99999:99099:00000",
    "77000:00077:99999:99099:00000",
    "00000:77077:99999:99099:00000",
    "77000:00077:99999:99099:00000",
    "00000:77077:00000:99999:99099",
    "00077:77000:99999:99099:00000",
    "00000:77077:00000:99999:99099",
    "00077:77000:99999:99099:00000",
]

left_hand = Motor("B")
right_hand = Motor("F")
hands = MotorPair("B", "F")


async def on_start(vm, stack):
    hub.led(0)

    rotate_hub_display_to_value("3")

    # Calibrate
    left_hand.run_to_position(0)
    right_hand.run_to_position(0)

    cool_frames = [hub.Image(frame) for frame in cool_animation]

    vm.system.display.show(cool_frames,
                           clear=False,
                           delay=200,
                           loop=True,
                           fade=1)

    vm.system.sound.play("/extra_files/Yipee")

    hands.set_default_speed(100)

    for i in range(3):
        hands.move(80, "degrees")

        wait_for_seconds(0.2)

        hands.move(-80, "degrees")

    vm.system.sound.play("/extra_files/Like")


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "skiboard_time")
    vm.register_on_start("skiboard_time|onstart", on_start)
    return vm
