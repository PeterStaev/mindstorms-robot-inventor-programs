# LEGO type:advanced slot:3 autostart
from util.rotation import rotate_hub_display_to_value
from runtime import VirtualMachine
from mindstorms import Motor, MotorPair, MSHub, ColorSensor
from mindstorms.control import wait_for_seconds
import hub
import math

looking_animation = [
    "77077:00000:77077:97097:00000",
    "77077:00000:77077:79079:00000",
]
angry_animation = [
    "90009:09090:00000:97097:00000",
    "90009:09090:00000:79079:00000",
    "90009:09090:00000:97097:00000",
    "90009:09090:00000:79079:00000",
]
scared_animation = [
    "00000:00000:99099:99099:00000",
    "00000:99900:99900:99909:00000",
    "00000:99900:99900:99909:00000",
    "00000:00000:99099:99099:00000",
    "00000:00999:00999:90999:00000",
    "00000:00999:00999:90999:00000",
]
happy_animation = [
    "77077:00000:97097:79079:00000",
    "77077:00000:79079:97097:00000",
]
ms_hub = MSHub()

left_hand = Motor("B")
right_hand = Motor("F")

wheels = MotorPair("A", "E")

color_sensor = ColorSensor("C")


async def on_start(vm, stack):
    ms_hub.status_light.on("black")
    rotate_hub_display_to_value("3")
    blinking_frames = [hub.Image(frame) for frame in looking_animation]
    vm.system.display.show(blinking_frames,
                           clear=False,
                           delay=1000,
                           loop=True,
                           fade=1)

    # Calibrate
    left_hand.run_to_position(0)
    right_hand.run_to_position(0)

    while True:
        color = color_sensor.get_color()
        if not color is None:
            stacks = vm.broadcast(color)
            while any(stack.is_active() for stack in stacks):
                yield

            ms_hub.status_light.on("black")
            vm.system.display.show(blinking_frames,
                                   clear=False,
                                   delay=1000,
                                   loop=True,
                                   fade=1)

        yield


async def on_red(vm, stack):
    ms_hub.status_light.on("red")

    angry_frames = [hub.Image(frame) for frame in angry_animation]
    vm.system.display.show(angry_frames,
                           clear=False,
                           delay=1000,
                           loop=False,
                           fade=1)

    vm.system.sound.play("/extra_files/No")

    wheels.move(10, speed=60)


async def on_blue(vm, stack):
    ms_hub.status_light.on("blue")

    scared_frames = [hub.Image(frame) for frame in scared_animation]
    vm.system.display.show(scared_frames,
                           clear=False,
                           delay=round(1000 / 8),
                           loop=True,
                           fade=1)

    vm.system.sound.play("/extra_files/Scared")

    wheels.move(-20, speed=80)

    wait_for_seconds(1)


async def on_green(vm, stack):
    ms_hub.status_light.on("green")

    happy_frames = [hub.Image(frame) for frame in happy_animation]
    vm.system.display.show(happy_frames,
                           clear=False,
                           delay=round(1000 / 8),
                           loop=True,
                           fade=1)

    vm.system.sound.play("/extra_files/Chuckle")
    wheels.move(14 * math.pi, "cm", steering=100, speed=80)
    vm.system.sound.play("/extra_files/Chuckle")
    wheels.move(14 * math.pi, "cm", steering=-100, speed=80)


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "fav_color")
    vm.register_on_start("fav_color|onstart", on_start)
    vm.register_on_broadcast("fav_color|red", on_red, "red")
    vm.register_on_broadcast("fav_color|blue", on_blue, "blue")
    vm.register_on_broadcast("fav_color|green", on_green, "green")
    return vm