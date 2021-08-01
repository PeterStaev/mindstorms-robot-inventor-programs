# LEGO type:advanced slot:4 autostart
from util.rotation import rotate_hub_display_to_value
from runtime import VirtualMachine
from mindstorms import Motor, MotorPair, MSHub, ColorSensor
from mindstorms.control import wait_for_seconds
from util.print_override import spikeprint
import hub

print = spikeprint

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
happy_animation = [
    "77077:00000:97097:79079:00000",
    "77077:00000:79079:97097:00000",
]
ms_hub = MSHub()

left_hand = Motor("B")
right_hand = Motor("F")

wheels = MotorPair("A", "E")


async def on_start(vm, stack):
    ms_hub.status_light.on("black")
    rotate_hub_display_to_value("3")

    # Calibrate
    left_hand.run_to_position(0)
    right_hand.run_to_position(0)

    cool_frames = [hub.Image(frame) for frame in cool_animation]
    vm.system.display.show(cool_frames[0])
    await vm.system.sound.play_async("/extra_files/1234")

    vm.system.display.show(cool_frames,
                           clear=False,
                           delay=200,
                           loop=True,
                           fade=1)

    reset_hands()

    play_the_drums(12, 4, 50)

    vm.system.display.show(cool_frames,
                           clear=False,
                           delay=125,
                           loop=True,
                           fade=1)
    play_the_drums(12, 4, 70)

    reset_hands()

    for i in range(8):
        left_hand.start_at_power(50)
        right_hand.start_at_power(50)
        wait_for_seconds(0.1)

        left_hand.start_at_power(-50)
        right_hand.start_at_power(-50)
        wait_for_seconds(0.1)

    left_hand.stop()
    right_hand.stop()

    happy_frames = [hub.Image(frame) for frame in happy_animation]
    vm.system.display.show(happy_frames,
                           clear=False,
                           delay=125,
                           loop=True,
                           fade=1)
    vm.system.sound.play("/extra_files/Yes")

    left_hand.run_to_position(0)
    right_hand.run_to_position(0)

    # Drum blasters
    left_hand.run_to_position(60)
    right_hand.run_to_position(335)

    wheels.move(5, "cm", speed=50)
    wheels.move(-50, "degrees", steering=100, speed=50)

    for i in range(3):
        right_hand.start_at_power(40)
        wait_for_seconds(0.13)
        right_hand.start_at_power(-40)
        wait_for_seconds(0.13)

    right_hand.run_to_position(300)

    # Hit the blaster
    left_hand.run_to_position(335)

    left_hand.run_to_position(25)
    wheels.move(100, "degrees", steering=100, speed=50)

    for i in range(3):
        left_hand.start_at_power(40)
        wait_for_seconds(0.13)
        left_hand.start_at_power(-40)
        wait_for_seconds(0.13)

    left_hand.run_to_position(60)

    # Hit the blaster
    right_hand.run_to_position(25)

    right_hand.run_to_position(345)

    blinking_frames = [hub.Image(frame) for frame in blinking_animation]
    vm.system.display.show(blinking_frames,
                           clear=False,
                           delay=125,
                           loop=True,
                           fade=1)

    wheels.move(-50, "degrees", steering=100, speed=50)
    wheels.move(-8, "cm", speed=50)

    left_hand.run_to_position(15)

    # raise SystemExit


def play_the_drums(iterations, rhythm, tempo):
    timeout = 0.2 * (50.0 / tempo)
    for i in range(iterations):
        if (i + 1) % rhythm == 0:
            right_hand.start_at_power(tempo)

        left_hand.start_at_power(tempo)
        wait_for_seconds(timeout)

        if (i + 1) % rhythm == 0:
            right_hand.start_at_power(-tempo)

        left_hand.start_at_power(-tempo)
        wait_for_seconds(timeout)

        if (i + 1) % rhythm == 0:
            right_hand.stop()

    left_hand.stop()


def reset_hands():
    left_hand.run_to_position(15)
    right_hand.run_to_position(345)


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "drum_master")
    vm.register_on_start("drum_master|onstart", on_start)
    return vm