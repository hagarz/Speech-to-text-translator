
from __future__ import division
import os
import socket
from threading import Thread

import re
import sys
import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from six.moves import queue

from google.cloud import translate_v2 as translate
translate_client = translate.Client()

# put the path to GOOGLE_APPLICATION_CREDENTIALS here:
credential_path = r"[path].json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

HOST = '127.0.0.1'
PORT = 5000   # Port to listen on



class AudioStream(object):
    """
    audio stream as a generator yielding audio chunks
    """
    def __init__(self):
        self.buff = queue.Queue()
        self.closed = True
        self.transcript = None

    def __enter__(self):
        self.closed = False
        return self

    def generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        print("chunk is None")
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

    def write(self, data):
        """
        collect data from the audio stream, into the buffer.
        """
        self.buff.put(data)

    def __exit__(self, type, value, traceback):
        print('exiting...')
        self.closed = True
        self.buff.put(None)
        server.close()
        server.shutdown()



def listen_print_loop(responses):
    """
    Converts audio chunks to text

    Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            print('continue')
            continue
        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]

        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.

        transcript = result.alternatives[0].transcript
        #lang = translate_client.detect_language(transcript)

        target = 'he'
        transcript = translate_client.translate(transcript, target_language=target)['translatedText']

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def client_s(transcoder):
    """ Collect audio from stream and write it to buffer"""
    with clientsocket:

        # make it non-blocking
        clientsocket.setblocking(False)

        BlockingIOError_10035_count = 0
        while True:
            try:
                data = clientsocket.recv(CHUNK)
                transcoder.write(data)
                BlockingIOError_10035_count = 0
            except BlockingIOError:
                if BlockingIOError_10035_count < 5:
                    BlockingIOError_10035_count += 1
                    time.sleep(0.5)
                else:
                    print(
                        'BlockingIOError: [WinError 10035] '
                        'A non-blocking socket operation could not be completed immediately',
                        BlockingIOError_10035_count)
                    server.close()
                    server.shutdown()
                    break




def audio_streamer(transcoder_):
    """
    return the output of Google speech to text
    """

    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    #language_code = 'he-IL'  # a BCP-47 language tag
    language_code = 'en-US' # a BCP-47 language tag

    client = speech.SpeechClient()  # Instantiates a client
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with transcoder_ as transcoder:
        trans_gen = transcoder.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in trans_gen)

        responses = client.streaming_recognize(streaming_config, requests)
        # put the transcription responses to use
        listen_print_loop(responses)


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    # create a streaming socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # bind the socket to a host and a port
        server.bind((HOST, PORT))
        # enable a server to accept connections
        server.listen()

        # accept connections from outside
        # clientsocket is a new socket object usable to send and receive data on the connection,
        # and address is the address bound to the socket on the other end of the connection.
        clientsocket, address = server.accept()
        print('Connected by', address)

        Transcoder = AudioStream()
        # multi-threading
        socket_thread = Thread(target=client_s, args=(Transcoder,))
        audio_stream_thread = Thread(target=audio_streamer, args=(Transcoder,))
        socket_thread.start()
        audio_stream_thread.start()

