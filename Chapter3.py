import os
import sys
import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# INIT PYGAME (AUDIO ONLY)
pygame.mixer.init()

# VIDEO PROCESSING (MOVIEPY)
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

try:
    video = VideoFileClip("Jadoo.mp4")

    video.write_videofile("result.mp4", audio=True)

    short_video = video.subclip(0, 10)
    short_video.write_videofile("short_result.mp4", audio=True)

    combined = concatenate_videoclips([video, short_video])
    combined.write_videofile("combined_result.mp4", audio=True)

    reversed_video = short_video.fx(vfx.time_mirror)
    reversed_video.write_videofile("reversed_result.mp4", audio=True)

    sped_up = short_video.fx(vfx.speedx, 2)
    sped_up.write_videofile("sped_up_result.mp4", audio=True)

except Exception as e:
    print("Video Error:", e)

# GUI TKINTER
root = tk.Tk()
root.title("Multimedia Application")
root.geometry("400x500")

# TAMPILKAN GAMBAR
try:
    image = Image.open("foto1.jpg")
    image = image.resize((300, 200))
    photo = ImageTk.PhotoImage(image)

    label_img = tk.Label(root, image=photo)
    label_img.pack(pady=10)
except:
    tk.Label(root, text="Gambar tidak ditemukan").pack()

# AUDIO PLAYER (STABIL)
current_audio = None

def play_music():
    global current_audio
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
    )
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        current_audio = file_path

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

# BUTTON AUDIO
tk.Label(root, text="Audio Player", font=("Arial", 14, "bold")).pack(pady=10)

btn_play = tk.Button(root, text="▶ Play Audio", width=20, command=play_music)
btn_play.pack(pady=5)

btn_pause = tk.Button(root, text="⏸ Pause", width=20, command=pause_music)
btn_pause.pack(pady=5)

btn_resume = tk.Button(root, text="⏯ Resume", width=20, command=resume_music)
btn_resume.pack(pady=5)

btn_stop = tk.Button(root, text="⏹ Stop", width=20, command=stop_music)
btn_stop.pack(pady=5)

# EXIT BUTTON
btn_exit = tk.Button(root, text="❌ Exit", width=20, command=root.destroy)
btn_exit.pack(pady=20)

# START GUI
root.mainloop()

pygame.mixer.quit()
sys.exit()
