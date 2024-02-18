import cv2
import os
import sys
import multiprocessing
import datetime
from pathlib import Path

# --- Function to delete files inside directory (without deleting directory itself) ---
def emptyFolder(directoryPath):
    [f.unlink() for f in Path(directoryPath).glob("*") if f.is_file()] 


# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

def delete_videos():
    videos = [
        "Out60_video.mp4",
        "output_video.mp4",
    ]

    for video in videos:
        try:
            os.remove(video)
            print(f"Deleted {video}")
        except FileNotFoundError:
            print(f"{video} not found, skipping deletion")

def returnVid():
    incomingVid = sys.argv[1]
    return incomingVid

def invertVideoFunc(inputVideoName):
    video_capture = cv2.VideoCapture(inputVideoName)
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    normalOutput = f'output_video-{inputVideoName}'
    at60FPSOutput = f'Out60_video-{inputVideoName}'
    
    # Increase the bitrate for better quality
    bitrate = 5000000  # Adjust bitrate as needed

    output_video = cv2.VideoWriter(normalOutput, fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))), bitrate)
    Out60_video = cv2.VideoWriter(at60FPSOutput, fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))), bitrate)

    success, frame1 = video_capture.read()

    while success:
        success, frame2 = video_capture.read()
        if success:
            inverted_frame = cv2.bitwise_not(frame2)
            overlay = cv2.addWeighted(frame1, 0.5, inverted_frame, 0.5, 0)
            output_video.write(overlay)
            Out60_video.write(overlay)
            frame1 = frame2

    video_capture.release()
    output_video.release()
    Out60_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    num_cpu_cores = os.cpu_count()
    print("Number of CPU cores:", num_cpu_cores)

    p1 = multiprocessing.Process(target=invertVideoFunc, args=("grass.mp4",)) 
    p2 = multiprocessing.Process(target=invertVideoFunc, args=("waves.mp4",))

    print("ID of main process: {}".format(os.getpid())) 

    p1.start() 
    p2.start() 

    print("ID of process p1: {}".format(p1.pid)) 
    print("ID of process p2: {}".format(p2.pid)) 

    p1.join() 
    p2.join() 

    print("Both processes finished execution!") 

    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive()))
