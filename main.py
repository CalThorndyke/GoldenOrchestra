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


def play_sound():
    os.system("aplay ./sound.wav")


def is_touched():
    return any(mpr121[i].value for i in range(12))


print("STARTED")

# Loop forever testing each input and printing when they're touched.
while True:
    if is_touched():
        print("DETECTED TOUCH")
        play_sound()

        while is_touched():
            time.sleep(0.25)

        print("RELEASED TOUCH")

    time.sleep(0.25)  # Small delay to keep from spamming output messages.
