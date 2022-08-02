from faulthandler import dump_traceback
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import cv2
import easygui
import os
import glob

def show_the_video(filename):
    cap = cv2.VideoCapture(filename)
    while(cap.isOpened()):
        ret, frame = cap.read()
        print(frame, ret)
        if ret:
            frame = cv2.resize(frame, (300, 300), fx=0.7, fy=0.7)
            cv2.imshow("frame", frame)
            cv2.setWindowProperty("frame", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    
def get_length(filename):
    clip = VideoFileClip(filename)
    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    return duration, fps, (width, height)


def from_duration_to_intervals(durata_complessiva, durata_intervalli):
    tuple_durata = []
    for i in range(0,int(durata_complessiva),durata_intervalli):
        tuple_durata.append((i,(i+durata_intervalli)))
    return tuple_durata


clipLength = 30 # seconds

if __name__ == '__main__':
    
    for file in os.listdir("toElaborate"):
        file_name=file.split('.')[0]
        intervalli=from_duration_to_intervals(get_length(f"toElaborate/{file}")[0],clipLength)
        ultima_clip_elaborata = 0
        try:
            list_of_files = glob.glob(f'Elaborated/{file_name}/*.mp4') # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            print(f"Ultima clip elaborata: {latest_file}")
            ultima_clip_elaborata = int(latest_file.split('.')[0].split('_')[1])
        except Exception as ex:
            os.mkdir(f"Elaborated/{file_name}")   
        index = ultima_clip_elaborata + 1
        print(os.getcwd())
        labels = []
        for intervallo in intervalli[index:]:
            ffmpeg_extract_subclip(f"toElaborate/{file}", intervallo[0], intervallo[1], targetname=f"Elaborated/{file_name}/{file_name}_{index}.mp4")
            show_the_video(f"Elaborated/{file_name}/{file_name}_{index}.mp4")
            label = easygui.enterbox("Label?")
            with open(f'./Elaborated/{file_name}/label.txt','a+') as flabel:
                flabel.write(f"{file_name}_{index}.mp4\t{label}\n")
            index += 1
        
    