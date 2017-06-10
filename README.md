# Sonar Distance

This module provides a class `SonarDistance` that can be used
to continuously read distances using two SRF04 sonar distance sensors.

It is designed to work with two SRF04's that both send out a ping at the
same time. The time between sending and the first return of the echo is
recorded at both sensors.

It works in a background fashion and sends sonar pings continuously,
capturing echo's. The user can read the most recently collected
return-time at both the sensors.

## usage example
```python
import pigpio
from sonar_distance import SonarDistance

GPIO_SR_TRIGGER = 25
GPIO_SR_ECHO_L = 5
GPIO_SR_ECHO_R = 24

pi = pigpio.pi()
if not pi.connected:
   exit()

sonar = SonarDistance(pi, GPIO_SR_TRIGGER, GPIO_SR_ECHO_L, GPIO_SR_ECHO_R)
s = SonarDistance()
s.start()

while True:
     d = s.get_distance()
     print d
     time.sleep(1)

s.stop()
```