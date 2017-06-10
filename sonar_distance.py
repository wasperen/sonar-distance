#!/usr/bin/env python
import time
import threading


class SonarDistance:

    def __init__(self, pi, trigger, echo_left, echo_right):
        self.pi = pi
        self.trigger = trigger
        self.echo_left = echo_left
        self.echo_right = echo_right

        self.trigger_ticks = {
            echo_left: pi.get_current_tick(),
            echo_right: pi.get_current_tick()
        }

        self.echo_ticks = {
            echo_left: pi.get_current_tick(),
            echo_right: pi.get_current_tick()
        }

        self.distance = (0,0)

        self.lock = threading.Lock()
        self.thread = None
        self.pinging = False

        pi.set_mode(trigger, pigpio.OUTPUT)
        pi.set_mode(echo_left, pigpio.INPUT)
        pi.set_mode(echo_right, pigpio.INPUT)

        self.left_cb = pi.callback(echo_left, pigpio.EITHER_EDGE, self._cb)
        pi.set_watchdog(echo_left, 50)
        self.right_cb = pi.callback(echo_right, pigpio.EITHER_EDGE, self._cb)
        pi.set_watchdog(echo_right, 50)

    def __del__(self):
        self.pi.left_cb.cancel()
        self.pi.right_cb.cancel()
        self.pi.set_watchdog(self.echo_left, 0)
        self.pi.set_watchdog(self.echo_right, 0)

    def _all_echos_in(self):
        return self.echo_ticks[self.echo_left] is not None and \
            self.echo_ticks[self.echo_right] is not None

    def _cb(self, gpio, level, tick):
        if level == 0 or level == 2:
            self.lock.acquire()
            if self.echo_ticks[gpio] is None:
                self.echo_ticks[gpio] = tick
            if self._all_echos_in():
                self.distance = (
                    pigpio.tickDiff(self.trigger_ticks[self.echo_left], self.echo_ticks[self.echo_left]),
                    pigpio.tickDiff(self.trigger_ticks[self.echo_right], self.echo_ticks[self.echo_right])
                )
            self.lock.release()

        if level == 1:
            self.lock.acquire()
            self.trigger_ticks[gpio] = tick
            self.lock.release()

    def _trigger(self):
        while self.pinging:
            if self._all_echos_in():
                self.lock.acquire()
                self.echo_ticks[self.echo_left] = None
                self.echo_ticks[self.echo_right] = None
                self.lock.release()

                self.pi.gpio_trigger(self.trigger, 10, 1)
            time.sleep(0.1)

    def get_distance(self):
        self.lock.acquire()
        result = self.distance
        self.lock.release()
        return result

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target = self._trigger)
            self.thread.setDaemon(True)
            self.pinging = True
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.pinging = False
            self.thread = None

if __name__ == "__main__":
    import pigpio

    TRIGGER = 25
    ECHO_L = 5
    ECHO_R = 24

    pi = pigpio.pi()
    if not pi.connected:
       exit()

    sonar = SonarDistance(pi, TRIGGER, ECHO_L, ECHO_R)
    sonar.start()
    while True:
        try:
            d = sonar.get_distance()
            print d
            time.sleep(1)

        except KeyboardInterrupt:
            break