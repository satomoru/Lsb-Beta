import argparse
import base64
import os, sys
from pydub import AudioSegment
from pydub.generators import Sine
from pyfiglet import Figlet
from PIL import Image


satomoru = argparse.ArgumentParser()
satomoru.add_argument('--run', choices=['img-str', 'str-img', 'morse-audio','info','apk-img', 'img-apk', 'file-img'])
satomoru.add_argument('-img')
satomoru.add_argument('-txt')
satomoru.add_argument('-folder')
satomoru.add_argument('-name')
satomoru.add_argument('-music')
satomoru.add_argument('-apk')
args = satomoru.parse_args()

if args.run == 'img-str':
    with open(f'{args.img}', 'rb') as image2string:
        converted_string = base64.b64encode(image2string.read())
        print('converted: image to string\ncondition: succesed')

    with open(f'{args.name}', 'wb') as file:
        file.write(converted_string)

elif args.run == 'str-img':
    file = open(f'{args.txt}', 'rb')
    byte = file.read()
    print('converted: string to image\ncondition: succesed')
    decodeit = open(f'{args.name}', 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()

elif args.run == 'morse-audio':

    morse_code_mapping = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/'
    }


    def text_to_morse(text):
        morse_code = '-....'
        for char in text.upper():
            if char in morse_code_mapping:
                morse_code += morse_code_mapping[char] + ' '
        return morse_code.strip()


    def generate_audio(morse_code):
        dot_duration = 100
        dash_duration = 3 * dot_duration

        audio = AudioSegment.silent(duration=dot_duration)

        for symbol in morse_code:
            if symbol == '.':
                audio += Sine(1000).to_audio_segment(duration=dot_duration)
            elif symbol == '-':
                audio += Sine(1000).to_audio_segment(duration=dash_duration)
            elif symbol == ' ':
                audio += AudioSegment.silent(duration=dot_duration)
            elif symbol == '/':
                audio += AudioSegment.silent(duration=7 * dot_duration)

        return audio




    text = f'{args.txt}'
    morse_code = text_to_morse(text)

    audio = generate_audio(morse_code)
    audio_name = f'{args.name}'
    audio.export(audio_name, format="wav")

    print("\nconverted: text to morse audio\nconditation: succesed")
elif args.run == 'info':
    print('\033[32m')
    custom_fig = Figlet(font='graffiti')
    print(custom_fig.renderText('lsb-msb'))
    print('''
\033[31m-----
\033[32mhello bro my name 'LSB-MSB'
i'm steganograohic tool for hide data in files
\033[31m-----
\033[34mmy user guide
\033[31m-----
\033[32mimage to string convertor:\033[34m -img <image location> -name <name.txt>
\033[32mstring to image convertor:\033[34m -txt <txt file location> -name <name.jpg>
\033[32mtext to morse audio convertor:\033[34m -txt <here-text> -name  <name.mp3>
\033[31m-----
\033[32mhide apk to image: -img <image location>\033[34m -apk <apk location> -name <name.apk>
\033[31m-----
\033[32munhide apk an image:\033[34m -img <apk hidden image location> -name <name.apk>
\033[31m-----
\033[31m-----\033[39m

''')

elif args.run == 'apk-img':
    img = Image.open(f'{args.img}')
    with open(f'{args.apk}', 'rb') as apk_file:
        apk_data = apk_file.read()

    apk_bytes = bytes(apk_data)
    img.putdata(list(apk_bytes))
    img.save(f'{args.name}')
    print('converted: apk to image\nconditation: succes ')

elif args.run == 'img-apk':
    hidden_img = Image.open(f'{args.img}')
    hidden_data = hidden_img.tobytes()
    with open(f'{args.name}', 'wb') as PY_TO_PY:
        PY_TO_PY.write(hidden_data)

else:
    print('\033[32m')
    custom_fig = Figlet(font='graffiti')
    print(custom_fig.renderText('lsb-msb'))
    print('''
\033[31m-----
\033[32mhello bro my name 'LSB-MSB'
i'm steganograohic tool for hide data in files
\033[31m-----
\033[34mmy user guide
\033[31m-----
\033[32mimage to string convertor:\033[34m -img <image location> -name <name.txt>
\033[32mstring to image convertor:\033[34m -txt <txt file location> -name <name.jpg>
\033[32mtext to morse audio convertor:\033[34m -txt <here-text> -name  <name.mp3>
\033[31m-----
\033[32mhide apk to image: -img <image location>\033[34m -apk <apk location> -name <name.apk>
\033[31m-----
\033[32munhide apk an image:\033[34m -img <apk hidden image location> -name <name.apk>
\033[31m-----
\033[31m-----\033[39m

    ''')
