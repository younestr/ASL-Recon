import os
import cv2
import speech_recognition as sr
from pydub import AudioSegment
import random
import numpy as np
from PIL import Image, ImageTk
import customtkinter as ctk

ASL_FOLDER = "C:\\Users\\hp\\Downloads\\MachineLearning\\Sign-Language-To-Text-and-Speech-Conversion-master\\AtoZ_3.1"

def create_asl_mapping(folder):
    mapping = {}
    for i in range(26):
        letter = chr(i + 97)
        letter_folder = os.path.join(folder, letter.upper())
        mapping[letter] = [os.path.join(letter_folder, f"{j}.jpg") for j in range(180)]
    return mapping

asl_mapping = create_asl_mapping(ASL_FOLDER)

def prepare_voice_file(path: str) -> str:
    if os.path.splitext(path)[1] == '.wav':
        return path
    elif os.path.splitext(path)[1] in ('.mp3', '.m4a', '.ogg', '.flac'):
        audio_file = AudioSegment.from_file(path, format=os.path.splitext(path)[1][1:])
        wav_file = os.path.splitext(path)[0] + '.wav'
        audio_file.export(wav_file, format='wav')
        return wav_file
    else:
        raise ValueError(f'Unsupported audio format: {os.path.splitext(path)[1]}')

def transcribe_audio(audio_data, language) -> str:
    r = sr.Recognizer()
    text = r.recognize_google(audio_data, language=language)
    return text

def write_transcription_to_file(text, output_file) -> None:
    with open(output_file, 'w') as f:
        f.write(text)

def speech_to_text(input_path: str, output_path: str, language: str) -> str:
    wav_file = prepare_voice_file(input_path)
    with sr.AudioFile(wav_file) as source:
        audio_data = sr.Recognizer().record(source)
        text = transcribe_audio(audio_data, language)
        write_transcription_to_file(text, output_path)
        print('Transcription:')
        print(text)
        return text

def get_asl_gesture(text):
    gestures = []
    for char in text.lower():
        if char in asl_mapping:
            gesture_path = random.choice(asl_mapping[char])
            gestures.append(gesture_path)
        elif char == ' ':
            gestures.append(' ')  # Add space as a gesture
    return gestures

def convert_to_pil_image(cv2_img):
    color_converted = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)
    return pil_image

def render_asl_skeleton(gestures, panel):
    # Load a sample gesture image to get the size
    sample_image_path = asl_mapping['a'][0]
    sample_image = cv2.imread(sample_image_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = sample_image.shape

    # Create a blank white image with the same size as the sample image
    blank_image = np.ones((height, width, channels), np.uint8) * 255

    for gesture_path in gestures:
        if gesture_path == ' ':
            display_image = blank_image
        elif os.path.isfile(gesture_path):
            skeleton_image = cv2.imread(gesture_path, cv2.IMREAD_UNCHANGED)
            if skeleton_image is not None:
                display_image = skeleton_image
            else:
                print(f"Image at path {gesture_path} could not be read.")
                continue
        else:
            print(f"Image at path {gesture_path} not found.")
            continue

        pil_image = convert_to_pil_image(display_image)
        img = ImageTk.PhotoImage(pil_image)
        panel.configure(image=img)
        panel.image = img
        panel.update()
        if gesture_path == ' ':
            panel.after(2000)  # Display blank image for 2 seconds
        else:
            panel.after(1000)  # Display each gesture for 1 second

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title("Sign Language To Text Conversion")
    app.geometry("1000x600")

    # Configure grid layout
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=1)
    app.grid_rowconfigure(3, weight=1)
    app.grid_rowconfigure(4, weight=1)
    app.grid_rowconfigure(5, weight=1)
    app.grid_rowconfigure(6, weight=1)

    def on_start():
        input_path = input_entry.get()
        output_path = output_entry.get()
        language = language_entry.get()

        if not os.path.isfile(input_path):
            result_label.configure(text='Error: File not found.')
            return
        else:
            try:
                text = speech_to_text(input_path, output_path, language)
                result_label.configure(text=f'Transcription: {text}')
                asl_gestures = get_asl_gesture(text)
                render_asl_skeleton(asl_gestures, skeleton_panel)
            except Exception as e:
                result_label.configure(text=f'Error: {e}')

    # Left side input fields
    input_frame = ctk.CTkFrame(app)
    input_frame.grid(row=1, column=0, rowspan=5, padx=10, pady=20, sticky="nsew")

    ctk.CTkLabel(input_frame, text="Sign Language To Text Conversion", font=("Courier", 20, "bold")).pack(pady=10)

    ctk.CTkLabel(input_frame, text="Enter the path to an audio file (WAV, MP3, M4A, OGG, or FLAC):").pack(pady=5)
    input_entry = ctk.CTkEntry(input_frame, width=300)
    input_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Enter the path to the output file:").pack(pady=5)
    output_entry = ctk.CTkEntry(input_frame, width=300)
    output_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Enter the language code (e.g. en-US):").pack(pady=5)
    language_entry = ctk.CTkEntry(input_frame, width=300)
    language_entry.pack(pady=5)

    start_button = ctk.CTkButton(input_frame, text="Start", command=on_start)
    start_button.pack(pady=20)

    # Right side panel for skeleton image
    skeleton_frame = ctk.CTkFrame(app)
    skeleton_frame.grid(row=1, column=1, rowspan=5, padx=10, pady=20, sticky="nsew")

    skeleton_label = ctk.CTkLabel(skeleton_frame, text="ASL Skeleton will appear here", font=("Courier", 16))
    skeleton_label.pack(pady=10)

    skeleton_panel = ctk.CTkLabel(skeleton_frame, width=400, height=300, fg_color=("white", "white"))  # Adjust the color for light and dark themes
    skeleton_panel.pack(padx=20, pady=20, fill='both', expand=True)






    # Result label
    result_label = ctk.CTkLabel(app, text=" ")
    result_label.grid(row=6, column=0, columnspan=3, pady=10)

    app.mainloop()
