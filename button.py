from machine import Pin
import time

# 设置 pin5 为输入并启用内部上拉电阻
button = Pin(4, Pin.IN, Pin.PULL_UP)

while True:
    # 如果按钮按下，pin5 会读取为低电平
    if button.value() == 0:
        print("按钮已按下")
        time.sleep(0.2)  # 防抖动
    else:
        time.sleep(0.2)
