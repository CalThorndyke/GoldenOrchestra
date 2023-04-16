import adafruit_mpr121
import board
import busio
import logging
import pprint
from subprocess import Popen
import threading
import time

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)


def get_sound_for_pin(i: int) -> str:
    if i in range(5):
        return "./Dizi.wav"
    else:
        return "./Guzheng.wav"


def play_sound_for_pin(i: int) -> Popen:
    return Popen(["aplay", get_sound_for_pin(i)])


def is_touched(i: int):
    return mpr121[i].value


def sensor_detection_thread(i: int):
    logging.info(f"STARTING THREAD FOR PIN {i}")
    while True:
        if is_touched(i):
            logging.info(f"DETECTED TOUCH FOR PIN {i}")

            process = play_sound_for_pin(i)

            logging.info(pprint.pformat(process))
            logging.info(f"PID: {process.pid}")

            if is_touched(i):
                logging.info(f"PIN {i} ACTIVE")
            if poll:
                logging.info(f"PROCESS ID {poll}")

            while is_touched(i) or process.poll():
                time.sleep(0.25)

            logging.info(f"PIN {i} READY TO RECIEVE EVENTS AGAIN")


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("APPLICATION BOOTED")

threads = []

for i in range(12):
    thread = threading.Thread(target=sensor_detection_thread, args=(i,))
    thread.start()
