Speech Recognition on Raspbian (tested on Raspbian Buster 4.19)

=== Things you need to have ==
- Microphone
- Raspberry Pi with Raspbian Buster 4.19
- Internet connection for Raspberry Pi

=== Preparation ===
1. sudo apt-get update
2. sudo apt-get install git
3. git clone https://github.com/fendyaritonang/Python-SpeechRecognition
4. cd Python-SpeechRecognition/
5. sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev espeak
6. pip3 install pyaudio SpeechRecognition pyttsx3
7. sudo apt-get install flac
8. Attach your microphone and execute the following command to check if you have audio input device
   arecord -l
9. If it's listed, execute the following:
    python3 checkMicrophone.py
10. It should list all the available audio input. Yours should be hw:1, 0
11. Execute the following command to adjust audio output and input volume 
    alsamixer
12. The first one should be your audio output device. Pls adjust the volumn by clicking up/down arrow
13. To adjust audio input device, press F6 and select your microphone. Then adjust the volume using up/down arrow
14. To exit from mixer, press Esc
15. Test the recording using the following command. Record duration is 5 seconds and it will record to test.wav
    arecord -f dat -r 60000 -D plughw:1,0 -d 5 test.wav
16. Play the recording using the following command
    aplay test.wav
17. If everything is good, now we're ready for the speech SpeechRecognition.

=== Start Speech Recognition ===
Execute the following command to start the speech SpeechRecognition
python3 recordaudioloop.py

=== How it works ===
You need to say hello to activate speech recognition. The same like siri which you need to call siri to activate speech command.
After you say hello, the program will say "Yes, how can I help". Then you can continue to tell what you need to do.
The activation keyword, greeting reply and list of recognized command can be changed in recordaudioloop.py, line 30 until 35.
You can register your actual command in line 117. For example if you tell the program "off", you can write code to do anything
Code example:
if textresult == "off":
    print("You just said Off");