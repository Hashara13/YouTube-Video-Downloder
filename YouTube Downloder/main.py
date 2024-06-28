import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube
import threading

def download_video(url, save_path, file_format, progress_var, status_label):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        
        if file_format == "MP4":
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            highest_res_stream = streams.get_highest_resolution()
        elif file_format == "MP3":
            streams = yt.streams.filter(only_audio=True, file_extension="mp4")
            highest_res_stream = streams.first()
            highest_res_stream.download(output_path=save_path, filename_prefix="audio_")
        else:
            streams = yt.streams.filter(file_extension=file_format.lower())
            highest_res_stream = streams.first()
        
        highest_res_stream.download(output_path=save_path)
        status_label.config(text="Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    progress_var.set(percentage_completed)

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showerror("Error", "Please select a folder to save the video")
        return

    file_format = format_combobox.get()
    if not file_format:
        messagebox.showerror("Error", "Please select a format")
        return

    status_label.config(text="Downloading...")
    download_thread = threading.Thread(target=download_video, args=(url, save_path, file_format, progress_var, status_label))
    download_thread.start()

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x350")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TCombobox", font=("Helvetica", 12))

url_label = ttk.Label(root, text="YouTube URL:")
url_label.pack(pady=10)
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=10)

format_label = ttk.Label(root, text="Select Format:")
format_label.pack(pady=10)
format_combobox = ttk.Combobox(root, values=["MP4", "MP3", "WEBM", "3GP"])
format_combobox.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, padx=20, fill=tk.X)

status_label = ttk.Label(root, text="")
status_label.pack(pady=10)

download_button = ttk.Button(root, text="Download", command=start_download)
download_button.pack(pady=20)

root.mainloop()
