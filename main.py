import os
import adafruit_mpr121
import board
import busio
import logging
from subprocess import Popen, DEVNULL
import threading
import time

END_ON_RELEASE = True

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)


def get_sound_for_pin(i: int) -> str:
    if i in range(5):
        return "Dizi.wav"
    else:
        return "Guzheng.wav"


def play_sound_for_pin(i: int) -> Popen:
    return Popen(["aplay", f"{os.environ['WAV_DIR']}/{get_sound_for_pin(i)}"], stdout=DEVNULL)


def is_touched(i: int):
    return mpr121[i].value


def sensor_detection_thread(i: int):
    logging.info(f"STARTING THREAD FOR PIN {i}")

    while True:
        if is_touched(i):
            logging.info(f"DETECTED TOUCH FOR PIN {i}")

            process = play_sound_for_pin(i)

            if END_ON_RELEASE:
                while is_touched(i):
                    time.sleep(0.25)
                process.kill()
            else:
                while is_touched(i) or process.poll() is None:
                    time.sleep(0.25)

            logging.info(f"PIN {i} READY TO RECIEVE EVENTS AGAIN")

        time.sleep(0.25)


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("APPLICATION BOOTED")

threads = []

for i in range(12):
    thread = threading.Thread(target=sensor_detection_thread, args=(i,))
    thread.start()
