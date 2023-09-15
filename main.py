import time
from machine import Pin, PWM


pin_8 = PWM(Pin(8)) 
pin_8.freq(1000)


for i in range(0, 1024):
    pin_8.duty(i)
    time.sleep_ms(1)
for i in range(1023, -1, -1):
    pin_8.duty(i)
    time.sleep_ms(1)
