# -*- coding: utf-8 -*-
"""
Created on 2020-06-20 12:13:13
@Author: ZHAO Lingfeng
@Version : 0.0.1
"""
import time
import ctypes

import mouse
from mouse._winmouse import *

SPEED1 = 0.02
SPEED2 = 0.1
try:
    with open("setting.txt") as f:
        SPEED1, SPEED2 = map(float, f.read().splitlines())

except Exception as e:
    ...

clicked = False
click_time = 0.02
user32 = ctypes.WinDLL("user32", use_last_error=True)


def callback(event):
    if isinstance(event, mouse.ButtonEvent):
        if event.button == "x" or event.button == "x2":
            global clicked, click_time
            click_time = SPEED1 if event.button == "x" else SPEED2
            clicked = event.event_type == "down" or event.event_type == "double"


def click():
    # press
    user32.mouse_event(0x2, 0, 0, 0, 0)
    time.sleep(0.05)
    # release
    user32.mouse_event(0x4, 0, 0, 0, 0)


def listen(queue):
    def low_level_mouse_handler(nCode, wParam, lParam):

        global previous_button_event

        struct = lParam.contents
        # Can't use struct.time because it's usually zero.
        t = time.time()
        x_button = False
        if wParam == WM_MOUSEMOVE:
            event = MoveEvent(struct.x, struct.y, t)
        elif wParam == WM_MOUSEWHEEL:
            event = WheelEvent(struct.data / (WHEEL_DELTA * (2 << 15)), t)
        elif wParam in buttons_by_wm_code:
            type, button = buttons_by_wm_code.get(wParam, ("?", "?"))
            if wParam >= WM_XBUTTONDOWN:
                button = {0x10000: X, 0x20000: X2}[struct.data]
                x_button = True
            event = ButtonEvent(type, button, t)

            if (event.event_type == DOWN) and previous_button_event is not None:
                # https://msdn.microsoft.com/en-us/library/windows/desktop/gg153548%28v=vs.85%29.aspx?f=255&MSPPError=-2147217396
                if (
                    event.time - previous_button_event.time
                    <= GetDoubleClickTime() / 1000.0
                ):
                    event = ButtonEvent(DOUBLE, event.button, event.time)

            previous_button_event = event
        else:
            # Unknown event type.
            return CallNextHookEx(NULL, nCode, wParam, lParam)

        queue.put(event)
        return -1 if x_button else CallNextHookEx(NULL, nCode, wParam, lParam)

    WH_MOUSE_LL = c_int(14)
    mouse_callback = LowLevelMouseProc(low_level_mouse_handler)
    mouse_hook = SetWindowsHookEx(WH_MOUSE_LL, mouse_callback, NULL, NULL)

    # Register to remove the hook when the interpreter exits. Unfortunately a
    # try/finally block doesn't seem to work here.
    atexit.register(UnhookWindowsHookEx, mouse_hook)

    msg = LPMSG()
    while not GetMessage(msg, NULL, NULL, NULL):
        TranslateMessage(msg)
        DispatchMessage(msg)


def main():
    mouse._os_mouse.listen = listen
    print("Starting hooking")
    print(f"侧键1: {1/SPEED1:.2f}Hz, 侧键2:  {1/SPEED2:.2f}Hz")
    mouse.hook(callback)

    while 1:
        if clicked:
            print("开始点击")
            while 1:
                click()
                if not clicked:
                    break
                time.sleep(click_time)
            print("停止点击")


if __name__ == "__main__":
    main()
