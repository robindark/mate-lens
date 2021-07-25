from PIL import Image as im
import mss
import numpy as np
import socket

URL = "matelight.cbrp3.c-base.org"
UDP_PORT = 1337

def send_array(data, hostname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (hostname, UDP_PORT))

if __name__ == "__main__":

    with mss.mss() as sct:

        # Get information of monitor
        monitor_number = 0
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        lenswidth = 1920
        lensheight = 768

        monitor = {
            "top": mon["top"] + int((mon["height"] - lensheight) / 2),
            "left": mon["left"] + int((mon["width"] - lenswidth) / 2),
            "width": lenswidth,
            "height": lensheight,
            "mon": monitor_number,
        }

        while True:
            sct_img = sct.grab(monitor)
            image_resized = np.array(im.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").resize((40, 16)))
            send_array(image_resized, URL)
            