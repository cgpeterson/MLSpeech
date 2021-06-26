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
    bot = chatBot()
    print("Chat Bot Initialized")
    inputChk = True
    resp = "Empty"
    inp = "Hello"
    
    print("Would you like to enable input checker? (can only be set now)\n")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Please say something")
        audio = r.listen(source, timeout=8, phrase_time_limit=8)

    print("Recognizing Now .... ")

    # Recognize speech using google
    try:
        inp = r.recognize_google(audio)
    except:
        inp = input("I'm sorry I didn't hear anything. Please type out what you said.\n")
        
    # Enable input checking
    if (inp[0].lower() != 'y'):
        print("input checking disabled")
        inputChk = False
    else:
        print("input checking enabled")
 
    # Chat Loop
    while resp != "-1":
        # Clear listening input
        audio = None
        
        # Listen
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Please say something")
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
     
        print("Recognizing Now .... ")
 
        # Recognize speech using google
        try:
            inp = r.recognize_google(audio)
            
            # Check if correct input
            if inputChk == True:
                print("is '%s' what you said\n" % (inp))
                
                # Listen
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    print("Please say something")
                    audio = r.listen(source, timeout=8, phrase_time_limit=8)
            
                print("Recognizing Now .... ")
            
                # Recognize speech using google
                try:
                    yn = r.recognize_google(audio)
                except:
                    yn = input("I'm sorry I didn't hear anything. Please type out what you said.\n")
                if (yn[0].lower() != 'y'):
                    inp = input("I'm sorry for the confusion. Please type out what you said.\n")
                    
        except:
            inp = input("I'm sorry I didn't hear anything. Please type out what you said.\n")
        
        try:
            if inp.lower() == "quit" or inp.lower() == "end" or inp.lower() == "stop":
                break;
            print("You: " + inp)     
 
        except Exception as e:
            print("Error :  " + str(e))
 
        # Write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())
            
        
            
        # Get Machine Response
        resp = bot.chat(str(inp))
        if resp != "-1":
            print("CodyBot: " + resp)
                
    print("Shutting Down")
    bot.reset()

if __name__ == '__main__':
    main()