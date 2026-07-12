import yt_dlp
import dearpygui.dearpygui as dpg

URL = ""
CODEC = ["Video","Audio"]
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

ydl_opts = {
    'format': '',
    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    'progress_hooks': [progress_hook]
}

def codec_list(sender,data):
    if data == CODEC[0]:
        print(f"Codec selected : {CODEC[0]}")
        ydl_opts["format"] = 'best'
        
    if data == CODEC[1]:
        print(f"Codec selected : {CODEC[1]}")
        ydl_opts["format"] = 'bestaudio'

def search_bar(sender,app_data):
    global URL
    URL = app_data
    print(f"url : ", URL)

def analyze_button():
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        uploader, duration, like, comment = f"Uploader: {info['uploader']}", f"Duration: {info['duration']} seconds", f"Like: {info['like_count']}", f"Comments: {info['comment_count']}"
        s_n = uploader, duration, like, comment
        dpg.set_value("analyze_title_result", f"Title: {info['title']}")
        dpg.set_value("analyze_result",'\n'.join(s_n))


def download_button():
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])

def main():
    dpg.create_context()
    with dpg.window(tag="f"):
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="Url", callback=search_bar, hint="Enter a YouTube URL...")
                dpg.add_button(label="Analyse",callback=analyze_button)

            dpg.add_input_text(readonly=True, tag="analyze_title_result")
            dpg.add_input_text(readonly=True,height=100,multiline=True,tag="analyze_result")
            
            dpg.add_progress_bar(default_value=0.0,tag="progress",show=False)

            with dpg.group(horizontal=True):
                dpg.add_combo(label="Codec",items=CODEC,callback=codec_list)
                dpg.add_button(label="Download",callback=download_button)


    dpg.create_viewport(title='juicy', width=600, height=200)
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
#[] - show thumbnail
#[] - add finished sound