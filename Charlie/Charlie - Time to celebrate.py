# LEGO type:advanced slot:2 autostart
from util.rotation import rotate_hub_display_to_value
from runtime import VirtualMachine
from mindstorms import Motor, MotorPair, MSHub
from mindstorms.control import wait_for_seconds
import hub
import math

blinking_animation = [
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:00000:77077:00000",
    "77077:00000:00000:00000:00000",
    "77077:00000:00000:88088:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
    "77077:00000:99099:99099:00000",
]

ms_hub = MSHub()


# start test
async def on_start(vm, stack):
    ms_hub.status_light.on("black")
    rotate_hub_display_to_value("3")
    blinking_frames = [hub.Image(frame) for frame in blinking_animation]
    vm.system.display.show(blinking_frames,
                           clear=False,
                           delay=round(1000 / 8),
                           loop=True,
                           fade=1)

    left_hand = Motor("B")
    right_hand = Motor("F")

    # Calibrate
    left_hand.run_to_position(0)
    right_hand.run_to_position(0)

    vm.system.sound.play("/extra_files/Humming")
    for i in range(2):
        right_hand.run_for_degrees(-100, 50)
        right_hand.run_for_degrees(100, 50)

        left_hand.run_for_degrees(100, 50)
        left_hand.run_for_degrees(-100, 50)

    left_turn = MotorPair("B", "E")
    right_turn = MotorPair("A", "F")

    vm.system.sound.play("/extra_files/Humming")
    for i in range(2):
        right_turn.move(100, "degrees", steering=100, speed=50)
        right_turn.move(-100, "degrees", steering=100, speed=50)

        left_turn.move(100, "degrees", steering=-100, speed=50)
        left_turn.move(-100, "degrees", steering=-100, speed=50)

    wheels = MotorPair("A", "E")
    wheels.move(14 * math.pi, "cm", steering=100, speed=80)
    wheels.move(14 * math.pi, "cm", steering=-100, speed=80)

    right_hand.run_to_position(270, direction="counterclockwise")
    wait_for_seconds(1)
    right_hand.run_for_seconds(1, 50)

    await vm.system.sound.play_async("/extra_files/Tadaa")

    wait_for_seconds(1)
    right_hand.run_to_position(0, direction="counterclockwise")


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "charlie")
    vm.register_on_start("charlie|onstart", on_start)
    return vm
