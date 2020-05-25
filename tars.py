from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from gtts import gTTS
import speech_recognition as sr 
from pygame import mixer
import random
import re
import webbrowser
import smtplib
import time


def talk(audio):
  print(audio)
  for line in audio.splitlines():
    text_to_speech = gTTS(text=audio, lang='en-us')
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

  if 'open google and search' in command:
    reg_ex = re.search('open google (.*)', command)
    search_for = command.split('search', 1)[1]
    url = 'https://google.com'
    if reg_ex:
      subgoogle = reg_ex.group(1)
      url = url + 'r/' + subgoogle
  
    talk('Okay!')
    driver =  webdriver.Chrome()
    driver.get('https://google.com')
    search = driver.find_element_by_name('q')
    search.send_keys(str(search_for))
    search.send_keys(Keys.RETURN)

    print('Done')

  elif 'email' or 'gmail' in command:
    talk('What is the subject?')
    time.sleep(3)
    subject = myCommand()
    talk('What should I say?')
    time.sleep(3)
    message = myCommand()
    content = 'Subject: {}\n\n{}'.format(subject, message)
    
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('your_email', 'your_password')

    mail.sendmail('FROM', 'TO', content)

    mail.close()

    talk('Email sent!')
  
  else:
    error = random.choice(errors)
    talk(error)


talk('TARS is ready!')

#loop to continue executing multiple commands
while True:
  tars(myCommand())