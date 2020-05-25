from gtts import gTTS
import speech_recognition as sr 
from pygame import mixer
import random

def talk(audio):
  print(audio)
  for line in audio.splitlines():
    text_to_speech = gTTS(text=audio, lang='en-uk')
    text_to_speech.save('audio.mp3')
    mixer.init()
    mixer.music.load('audio.mp3')
    mixer.music.play()

def myCommand():
  r = sr.Recognizer()

  with sr.Microphone() as source:
    print('TARS is ready...')
    r.pause_threshold = 2
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)
    print('dirgraça')

  try:
    command = r.recognize_google(audio).lower()
    print('you said: ' + command + '\n')

  except sr.UnknownValueError:
    print('Your last command couldn\'t be heard')
    command = myCommand()

  return command

def tars(command):
  errors = [
    'I don\'t know what you mean',
    'Excuse me?',
    'Can you repeat it please'
  ]

  if 'hello' in command:
    talk('Hello! I\'m TARS. How can I help you')
  
  else:
    error = random.choice(errors)
    talk(error)


talk('TARS is ready!')

#loop to continue executing multiple commands
while True:
  tars(myCommand())