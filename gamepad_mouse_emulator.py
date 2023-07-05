import subprocess
import evdev
from evdev import UInput, ecodes as e

GAMEPAD_NAME = "USB Gamepad"
BTN_TRIGGER = 288
BTN_THUMB = 289
BTN_THUMB2 = 290
BTN_TOP = 291
BTN_TOP2 = 292
BTN_PINKIE = 293
BTN_BASE = 294
BTN_BASE2 = 295
BTN_BASE3 = 296
BTN_BASE4 = 297
ABS_X = 0
ABS_Y = 1

class GamepadMouseEmulator:
    def __init__(self):
        self.ui = UInput({
            e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE],
            e.EV_REL: [e.REL_X, e.REL_Y],
        }, name="Emulated Mouse")
        self.device_path = None

    def find_gamepad(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if GAMEPAD_NAME in device.name:
                self.device_path = device.path
                break

    def start_emulation(self):
        if self.device_path is None:
            print("USB Gamepad not found.")
            return

        device = evdev.InputDevice(self.device_path)
        print("Gamepad found. Starting emulation...")
        for event in device.read_loop():
            self.emulate_mouse_event(event)

    def emulate_mouse_event(self, event):
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == ABS_X:
                print("Horizontal: ", event.value - 127)
                self.ui.write(e.EV_REL, e.REL_X, event.value - 127)
                self.ui.syn()
            elif event.code == ABS_Y:
                print("Vertical: ", event.value - 127)
                self.ui.write(e.EV_REL, e.REL_Y, event.value - 127)
                self.ui.syn()

        elif event.type == evdev.ecodes.EV_KEY:
            if event.code == BTN_BASE2 or event.code == BTN_BASE:
                print("Left Click!")
                self.ui.write(e.EV_KEY, e.BTN_LEFT, event.value)
                self.ui.syn()
            elif event.code == BTN_TOP2 or event.code == BTN_PINKIE:
                print("Right Click!")
                self.ui.write(e.EV_KEY, e.BTN_RIGHT, event.value)
                self.ui.syn()
            elif event.code == BTN_TRIGGER:
                print("YouTube!")
                subprocess.Popen(["google-chrome", "https://www.youtube.com"])
            elif event.code == BTN_THUMB:
                print("Volume Up!")
                subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
            elif event.code == BTN_THUMB2:
                print("Mute!")
                subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "toggle"])
            elif event.code == BTN_TOP:
                print("Volume Down!")
                subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
            elif event.code == BTN_BASE3:
                print("Extra Button 4!")
                subprocess.Popen(["subl"])
            elif event.code == BTN_BASE4:
                print("Extra Button 5!")
                subprocess.Popen(["konsole"])

if __name__ == "__main__":
    try:
        gamepad_emulator = GamepadMouseEmulator()
        gamepad_emulator.find_gamepad()
        gamepad_emulator.start_emulation()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
