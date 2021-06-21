'''
Created on June 14, 2021

@author: Cody Peterson
'''

import speech_recognition as sr
from chatBot import chatBot

def main():
    
    # Assign NLP
    r = sr.Recognizer()
    
    # Machine Response
    #bot = chatBot();
    resp = ""
 
    while resp != "-1":
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
     
            print("Please say something")
     
            audio = r.listen(source)
     
            print("Recognizing Now .... ")
     
     
            # Recognize speech using google
            inp = r.recognize_google(audio)
            
            try:
                print("You have said \n" + inp)
                print("Audio Recorded Successfully \n ")
     
     
            except Exception as e:
                print("Error :  " + str(e))
     
     
     
     
            # Write audio
            with open("recorded.wav", "wb") as f:
                f.write(audio.get_wav_data())
                
            # Get Machine Response
            resp = "-1" #bot.chat(inp)

if __name__ == '__main__':
    main()