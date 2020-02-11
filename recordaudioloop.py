from ctypes import *
from contextlib import contextmanager
import pyaudio
import wave
import speech_recognition as sr
import time

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

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 2 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

def recognize_speech_from_mic(recognizer, audio):
	# create pyaudio stream
	stream = audio.open(format = form_1,rate = samp_rate,channels = chans, input_device_index = dev_index,input = True, frames_per_buffer=chunk)
	print("recording")
	frames = []

	# loop through stream and append audio chunks to frame array
	for ii in range(0,int((samp_rate/chunk)*record_secs)):
		data = stream.read(chunk)
		frames.append(data)

	print("finished recording")

	# stop the stream, close it, and terminate the pyaudio instantiation
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# save the audio frames as .wav file
	wavefile = wave.open(wav_output_filename,'wb')
	wavefile.setnchannels(chans)
	wavefile.setsampwidth(audio.get_sample_size(form_1))
	wavefile.setframerate(samp_rate)
	wavefile.writeframes(b''.join(frames))
	wavefile.close()

	voiceTest  = sr.AudioFile(wav_output_filename);
	with voiceTest as source:
			audio = recognizer.record(source);

	response = {
		"success": True,
		"error": None,
		"transcription": None
	}

	try:
		response["transcription"] = recognizer.recognize_google(audio);
	except sr.RequestError:
		# API was unreachable or unresponsive
		response["success"] = False;
		response["error"] = "API unavailable";
	except sr.UnknownValueError:
		# speech was unintelligible
		response["error"] = "Unable to recognize speech";
	return response;

if __name__ == "__main__":
	recognizer = sr.Recognizer();
	while True:
		with noalsaerr():
			audioObj = pyaudio.PyAudio();
		result = recognize_speech_from_mic(recognizer, audioObj);
		if result["error"]:
			print(result["error"]);
			break;
		print(result["transcription"]);	
		time.sleep(0.1);


