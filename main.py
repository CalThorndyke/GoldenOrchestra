import board
import busio
import os
import time

# Import MPR121 module.
import adafruit_mpr121

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)


def get_sound_for_pin(i: int) -> str:
    if i in range(5):
        return "Dizi.mp3"
    else:
        return "Guzheng.mp3"


def play_sound_for_pin(i: int):
    os.system(f"aplay ./{get_sound_for_pin(i)}")


def is_touched(i: int):
    return mpr121[i].value


print("STARTED")

# Loop forever testing each input and printing when they're touched.
while True:
    for i in range(11):
        if is_touched():
            print("DETECTED TOUCH")
            play_sound_for_pin(i)

            while is_touched():
                time.sleep(0.25)

            print("RELEASED TOUCH")

    time.sleep(0.25)  # Small delay to keep from spamming output messages.
