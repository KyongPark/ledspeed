# -*- coding: utf-8 -*-
"""speedled.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VDH6w9vDAijyRBN617jOtPFW2zNsatQd
"""

import RPi.GPIO as GPIO
import smbus
import time


LED_PINS = {
    'green': [17, 27],
    'yellow': [22, 5],
    'red': [6, 13, 19]
}


GPIO.setmode(GPIO.BCM)
pwm_objects = {color: [] for color in LED_PINS}
for color in LED_PINS:
    for pin in LED_PINS[color]:
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 100)
        pwm.start(0)
        pwm_objects[color].append(pwm)

bus = smbus.SMBus(1)
MPU6050_ADDR = 0x68
bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)  # Power on MPU6050

def read_word_2c(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def convert_gyro_to_speed(gyro_xout):
    return abs(gyro_xout / 131.0)

def read_gyro_speed():

    gyro_xout = read_word_2c(0x43)
    speed_kmh = convert_gyro_to_speed(gyro_xout)
    return speed_kmh

def set_led_brightness(led_pins, duty_cycle):
    for pwm in led_pins:
        pwm.ChangeDutyCycle(duty_cycle)

def update_leds(speed_kmh):

    for color in pwm_objects:
        set_led_brightness(pwm_objects[color], 0)


    if speed_kmh <= 10:
        set_led_brightness(pwm_objects['green'][:1], 100)
    elif 10 < speed_kmh <= 15:
        set_led_brightness(pwm_objects['green'], 100)
    elif 16 <= speed_kmh <= 18:
        set_led_brightness(pwm_objects['green'], 100)
        set_led_brightness(pwm_objects['yellow'][:1], 100)
    elif 19 <= speed_kmh <= 20:
        set_led_brightness(pwm_objects['green'], 100)
        set_led_brightness(pwm_objects['yellow'], 100)
    elif 21 <= speed_kmh <= 22:
        set_led_brightness(pwm_objects['green'], 100)
        set_led_brightness(pwm_objects['yellow'], 100)
        set_led_brightness(pwm_objects['red'][:1], 100)
    elif 23 <= speed_kmh <= 24:
        set_led_brightness(pwm_objects['green'], 100)
        set_led_brightness(pwm_objects['yellow'], 100)
        set_led_brightness(pwm_objects['red'][:2], 100)
    elif speed_kmh >= 25:
        set_led_brightness(pwm_objects['green'], 100)
        set_led_brightness(pwm_objects['yellow'], 100)
        set_led_brightness(pwm_objects['red'], 100)

try:
    while True:
        speed_kmh = read_gyro_speed()
        update_leds(speed_kmh)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()