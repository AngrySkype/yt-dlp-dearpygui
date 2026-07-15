import yt_dlp
import dearpygui.dearpygui as dpg
from pydub import AudioSegment
from pydub.playback import play

audio = AudioSegment.from_mp3("Sounds/finish.mp3")

URL = ""
TYPE = ["Video","Audio"]
RESOLUTION = ["2160", "1440", "1080", "720", "480"]
BITRATES = ["64","128","192","320"]
output_dir = 'SavedFiles'

def notification(message: str, modal: bool = True):
    with dpg.window(label="Notification", modal=modal,autosize=True):
        dpg.add_text(message)

def progress_hook(d):
    if d['status'] == 'downloading':
        dpg.configure_item("progress",show=True)
        percent = d.get('_percent_str', '0%')
        try:
            progress = float(percent.strip().replace("%","")) / 100
            dpg.set_value("progress", progress)
        except ValueError:
            notification(message="Error")
    elif d['status'] == 'finished':
        notification(message=f"Download Finished!")
        dpg.configure_item("progress",show=False)
        play(audio)

ydl_opts = {
    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    'progress_hooks': [progress_hook],
    'writethumbnail': False,
}

def resolution_list(sender, data):
    ydl_opts["format"] = f"bestvideo[height<={data}]+bestaudio/best"

def bitrate_list(sender, data):
    if ydl_opts.get("postprocessors"):
        ydl_opts["postprocessors"][0]["preferredquality"] = data
    

def codec_list(sender, data):
    if data == TYPE[0]:
        dpg.configure_item("bitrate",show=False)
        dpg.configure_item("resolution",show=True)
        ydl_opts["format"] = "bestvideo+bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "webm",
        }]
    elif data == TYPE[1]:
        dpg.configure_item("bitrate",show=True)
        dpg.configure_item("resolution",show=False)
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

def search_bar(sender,app_data):
    global URL
    URL = app_data
    print(f"url : ", URL)

def analyze_button():
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(URL, download=False)
            uploader, duration, like, comment = f"Uploader: {info['uploader']}", f"Duration: {info['duration']} seconds", f"Like: {info['like_count']}", f"Comments: {info['comment_count']}"
            s_n = uploader, duration, like, comment
            dpg.set_value("analyze_title_result", f"Title: {info['title']}")
            dpg.set_value("analyze_result",'\n'.join(s_n))
    except Exception as e:
        notification(message=f"{e}")


def download_button():
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])
    except Exception as e:
        notification(message=f"{e}")

def main():
    dpg.create_context()
    with dpg.window(tag="f"):
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="Url", callback=search_bar, hint="Enter a YouTube URL...")
                dpg.add_button(label="Analyse",callback=analyze_button)

            dpg.add_input_text(readonly=True, tag="analyze_title_result")
            dpg.add_input_text(readonly=True,height=100,multiline=True,tag="analyze_result")
            
            dpg.add_progress_bar(default_value=0.0,tag="progress",show=False)
            dpg.add_combo(label="Bitrate", tag="bitrate", items=BITRATES,callback=bitrate_list,show=False)
            dpg.add_combo(label="Resolution", tag="resolution", items=RESOLUTION,callback=resolution_list,show=False)
        
            with dpg.group(horizontal=True):
                dpg.add_combo(label="Type",items=TYPE,callback=codec_list)
                dpg.add_button(label="Download",callback=download_button)

            #dpg.add_checkbox(label="DownloadThumbnail")


    dpg.create_viewport(title='juicy', width=600, height=300)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("f", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()

#[x] - progress bar appear only when download is clicked
#[x] - being able to change codec from combolist
#[x] - add more info to analyze input
#[x] - add finished sound
#[x] - choose codec
#[x] - choose bitrate
#[x] - choose resolution
#[] - show thumbnail
