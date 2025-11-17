import cv2
import socket
import struct
import threading
import time
import numpy as np

CAMERAS = {
    "Cam1": 5600,
    "Cam2": 5601,
    "Cam3": 5602
}

RETRY_DELAY = 5
BUFFER_SIZE = 4096

last_frames = {name: None for name in CAMERAS.keys()}


def receive_stream(name, port):
    global last_frames
    window_name = f"{name} - Stream"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("127.0.0.1", port))
            print(f"✅ Conectado a {name} en puerto {port}")

            data = b""
            payload_size = struct.calcsize(">L")

            while True:
                while len(data) < payload_size:
                    packet = sock.recv(BUFFER_SIZE)
                    if not packet:
                        raise ConnectionError("Conexión cerrada por el servidor")
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]

                while len(data) < msg_size:
                    packet = sock.recv(BUFFER_SIZE)
                    if not packet:
                        raise ConnectionError("Conexión cerrada por el servidor")
                    data += packet

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                if frame is not None:
                    last_frames[name] = frame

        except (ConnectionRefusedError, ConnectionError, socket.timeout):
            print(f"⚠️ {name}: sin conexión en puerto {port}, reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
        finally:
            try:
                sock.close()
            except:
                pass


def main():
    threads = []
    for cam_name, cam_port in CAMERAS.items():
        t = threading.Thread(target=receive_stream, args=(cam_name, cam_port), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            for cam_name in CAMERAS.keys():
                frame = last_frames.get(cam_name)
                if frame is not None:
                    cv2.imshow(f"{cam_name} - Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
