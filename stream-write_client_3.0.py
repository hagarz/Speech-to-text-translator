__author__ = 'Hagar Zemach'
#!/usr/bin/env python

import pyaudio
import socket


# # socket connection
# # Return a string containing the hostname of the machine where the Python interpreter is currently executing:
#HOST = socket.gethostname()
HOST = '127.0.0.1'
PORT = 5000

# Audio recording parameters
FORMAT = pyaudio.paInt16
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
CHANNELS = 1


# instantiate PyAudio
audio_interface = pyaudio.PyAudio()

audio_stream = audio_interface.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
)


def send_audio():
    print('listening and connecting...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as newSocket:
        newSocket.connect((HOST, PORT))
        frames = []
        while True:
            data = audio_stream.read(CHUNK)
            # Send data to the socket
            #  Unlike send(),
            # sendall() continues to send data from bytes until either all data has been sent or an error occurs.
            newSocket.sendall(data)




if __name__ == '__main__':
    send_audio()
