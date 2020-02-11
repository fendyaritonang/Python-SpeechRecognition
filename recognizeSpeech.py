import speech_recognition as sr

r = sr.Recognizer();

voiceTest  = sr.AudioFile('test1.wav');

with voiceTest as source:
	audio = r.record(source);

a = r.recognize_google(audio);

print(a);
