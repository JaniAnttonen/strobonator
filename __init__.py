import badge
import ugfx
import time
import appglue
import _thread


class Strobonator:
    def __init__(self):
        self.strobonator_on = True
        self.delay = 50.0
        self.color = [255, 255, 255]
        _thread.start_new_thread(self.run, ())

    def run(self):
        latch = False
        while True:
            if latch or self.strobonator_on == False:
                badge.backlight(0)
                badge.led(6, 0, 0, 0)
                latch = False
            else:
                badge.backlight(255)
                badge.led(6, self.color[0], self.color[1], self.color[2])
                latch = True
            time.sleep(self.delay / 1000)

    def change_color(self, forward):
        if forward:
            if self.color == [255, 255, 255]:
                self.color = [255, 0, 0]
            elif self.color == [255, 0, 0]:
                self.color = [0, 255, 0]
            elif self.color == [0, 255, 0]:
                self.color = [0, 0, 255]
            else:
                self.color = [255, 255, 255]
        else:
            if self.color == [255, 255, 255]:
                self.color = [0, 0, 255]
            elif self.color == [0, 0, 255]:
                self.color = [0, 255, 0]
            elif self.color == [0, 255, 0]:
                self.color = [255, 0, 0]
            else:
                self.color = [255, 255, 255]

    def press_start(self, button_pressed):
        if button_pressed:
            if self.strobonator_on:
                self.strobonator_on = False
            else:
                self.strobonator_on = True

    def press_down(self, button_pressed):
        if self.delay > 10 and button_pressed:
            self.delay -= 10

    def press_up(self, button_pressed):
        if self.delay < 1000 and button_pressed:
            self.delay += 10

    def press_left(self, button_pressed):
        if button_pressed:
            self.change_color(False)

    def press_right(self, button_pressed):
        if button_pressed:
            self.change_color(True)


def main():
    strobonator = Strobonator()
    ugfx.input_attach(ugfx.BTN_START, strobonator.press_start)
    ugfx.input_attach(ugfx.JOY_UP, strobonator.press_up)
    ugfx.input_attach(ugfx.JOY_DOWN, strobonator.press_down)
    ugfx.input_attach(ugfx.JOY_LEFT, strobonator.press_left)
    ugfx.input_attach(ugfx.JOY_RIGHT, strobonator.press_right)


ugfx.input_init()
ugfx.input_attach(ugfx.BTN_B, lambda pushed: appglue.home()
                  if pushed else False)

_thread.start_new_thread(main, ())
