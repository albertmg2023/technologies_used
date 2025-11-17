import cv2
import subprocess
import numpy as np
import threading

def show_camera(tcp_url, width=640, height=480, window_name="Camera"):
    frame_size = width * height * 3
    proc = subprocess.Popen([
        "ffmpeg",
        "-i", tcp_url,
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-"
    ], stdout=subprocess.PIPE, bufsize=10**8)

    try:
        while True:
            raw = proc.stdout.read(frame_size)
            if len(raw) != frame_size:
                break
            frame = np.frombuffer(raw, np.uint8).reshape((height, width, 3))
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        proc.terminate()
        cv2.destroyWindow(window_name)

# URLs TCP de las dos cámaras
camera1_url = "tcp://127.0.0.1:5600"
camera2_url = "tcp://127.0.0.1:5601"

# Crear hilos seguros para cada cámara
t1 = threading.Thread(target=show_camera, args=(camera1_url, 640, 480, "Camara 1"))
t2 = threading.Thread(target=show_camera, args=(camera2_url, 640, 480, "Camara 2"))

t1.start()
t2.start()

t1.join()
t2.join()
