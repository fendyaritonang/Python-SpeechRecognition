from ctypes import *
from contextlib import contextmanager
import pyaudio
import wave
import speech_recognition as sr

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
        pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)

with noalsaerr():
	r = sr.Recognizer();
	mic = sr.Microphone();

microphoneList = sr.Microphone.list_microphone_names();
print(microphoneList);
