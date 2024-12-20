import pyttsx3

engine = pyttsx3.init()

# RATE
rate = engine.getProperty('rate')   # getting details of current speaking rate
print(rate)                         # printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate

# VOLUME
volume = engine.getProperty('volume')   # getting to know current volume level (min=0 and max=1)
print(volume)                           # printing current volume level
engine.setProperty('volume', 1.0)       # setting up volume level between 0 and 1


def convert_text_to_speech(text, output_file):
    engine.say(text)
    engine.save_to_file(text, output_file)
    engine.runAndWait()

index =0
while True:
    user_input = input("Enter text to convert to speech (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    index += 1
    # output_file = input("Enter output file name: ")
    output_file = f"output_{index}.wav"
    convert_text_to_speech(user_input, output_file)

engine.stop()