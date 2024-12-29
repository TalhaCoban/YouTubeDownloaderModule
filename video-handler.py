import yt_dlp
import urllib
import json
import os
from models.video import Video
from ydl_options import YDLOptions


class VideoHandler:

    basePath = os.getcwd()
    outdir = os.path.join(basePath, "outputs")

    def __init__(self, url):
        self.url = url
        if not os.path.exists(os.path.join(self.basePath, "outputs")):
            os.mkdir(os.path.join(self.basePath, "outputs"))
        self.getVideoInfo()

    def changeDir(self, to_outputs):
        if to_outputs:
            os.chdir(self.outdir)
        else:
            os.chdir(self.basePath)
            
    def del_file(self, filename):
        if os.path.exists(os.path.join(self.outdir, filename)):
            os.remove(os.path.join(self.outdir, filename))

    def getVideoInfo(self):
        ydl_opts = YDLOptions.getSearchOptions()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            with open("info_dict.json", "w", encoding="utf-8") as file:
                json.dump(info_dict, file, indent=4)
            self.video = Video(**info_dict)
    
    def downloadToDisk(self, ydl_opts: dict):
        self.del_file(ydl_opts["outtmpl"])
        self.changeDir(True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        self.changeDir(False)

    def streamAudio(self, url):
        with urllib.request.urlopen(url) as audio_stream:
            while chunk := audio_stream.read(1024 * 8):  # Read in 8KB chunks
                yield chunk
    
    



if __name__ == "__main__":
    from prettytable import PrettyTable
    url = "https://www.youtube.com/watch?v=qCT5b7gGz-c"

    # url="https://www.youtube.com/watch?v=ZrQJaLemaoE"
    
    url = "https://www.youtube.com/watch?v=Z1IA_75pOgA&ab_channel=TateMcRaeVEVO"
    
    videoHandler = VideoHandler(url)

    table2 = PrettyTable()
    table2.field_names = ["format_id", "ext", "resolution", "format_note", "acodec", "vcodec"]
    for format in videoHandler.video.getAllVideoFormats():
        table2.add_row([format.format_id, format.ext, format.resolution, format.format_note, format.acodec, format.vcodec])
    print("\nvideo formats\n", table2)

    table3 = PrettyTable()
    table3.field_names = ["format_id", "ext", "resolution", "format_note", "acodec", "vcodec"]
    for format in videoHandler.video.getAllAudioFormats("394"):
        table3.add_row([format.format_id, format.ext, format.resolution, format.format_note, format.acodec, format.vcodec])
    print("\naudio formats\n", table3)
    
    
    print(videoHandler.video.findAudioFormatById("140").url)
    print(videoHandler.video.findAudioFormatById("140").filesize)
    

    ydlOptions = YDLOptions(videoHandler.video)
    # ydlOptions.setVideoFormat("394")
    ydlOptions.setAudioFormat("140")
    audio_url = ydlOptions.audioFormat.url
    # ydlOptions.setTitle("deneme.380")

    
    # videoHandler.downloadToDisk(ydl_opts)
    
    
  