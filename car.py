from machine import Pin, PWM
import time

# 定义控制引脚
in1 = Pin(1, Pin.OUT)
in2 = Pin(0, Pin.OUT)
ena = PWM(Pin(2))  # 使用 PWM 控制电机速度

in3 = Pin(8, Pin.OUT)
in4 = Pin(9, Pin.OUT)
enb = PWM(Pin(10))

def motor_forward(speed=1023):
    ena.duty(speed)
    in1.off()
    in2.on()
    enb.duty(speed)
    in4.on()
    in3.off()

    time.sleep(1)
    motor_stop()

def motor_backward(speed=1023):
    ena.duty(speed)
    in1.on()
    in2.off()
    enb.duty(speed)
    in3.on()
    in4.off()
    time.sleep(1)
    motor_stop()

def turn_left(speed=1023):
    ena.duty(speed)  # 设置左边电机的速度
    in1.on()         # 左边电机后退
    in2.off()
    
    enb.duty(speed)  # 设置右边电机的速度
    in3.off()        # 右边电机前进
    in4.on()
    
    time.sleep(1)    # 持续转动1秒，你可以根据需要调整
    motor_stop()

def turn_right(speed=1023):
    ena.duty(speed)  # 设置左边电机的速度
    in1.off()        # 左边电机前进
    in2.on()
    
    enb.duty(speed)  # 设置右边电机的速度
    in3.on()         # 右边电机后退
    in4.off()
    
    time.sleep(1)    # 持续转动1秒，你可以根据需要调整
    motor_stop()

def motor_stop():
    in1.off()
    in2.off()
    in3.off()
    in4.off()

# 测试
if __name__ == '__main__':
    motor_forward()
    motor_backward()
    motor_stop()
