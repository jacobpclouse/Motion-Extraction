# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import cv2
import os
import sys
import datetime
from pathlib import Path


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
OUTPUT_FOLDER = 'OUTPUTS' # folder where all the output files should be stored


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print("Dedicated to Peter Zlomek and Harley Alderson III")

# --- Function to create a folder if it does not exist ---
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

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

# --- Function to look for and delete specific videos ---
def delete_videos():
    videos = [
        "Out60_video.mp4",
        "output_video.mp4",
        # "slowed_inverted_video.mp4"
    ]

    for video in videos:
        try:
            os.remove(video)
            print(f"Deleted {video}")
        except FileNotFoundError:
            print(f"{video} not found, skipping deletion")

# --- Function to take target video name in from the command line ---
def returnVid():
    incomingVid = sys.argv[1]
    return incomingVid


# --- Function to invert previous frame and compare to present ---
def invertVideoFunc(inputVideoName):
    # Open the video file
    # video_capture = cv2.VideoCapture('input_video.mp4')
    video_capture = cv2.VideoCapture(inputVideoName)

    # Get the frame rate of the input video
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Get the codec of the input video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Define output video writer
    output_video = cv2.VideoWriter(f'Out{fps}_video.mp4', fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))))
    Out60_video = cv2.VideoWriter('Out60_video.mp4', fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))))

    # Read the first frame
    success, frame1 = video_capture.read()

    # Loop through the video frames
    while success:
        # Read the next frame
        success, frame2 = video_capture.read()

        if success:
            # Invert the colors of the second frame
            inverted_frame = cv2.bitwise_not(frame2)

            # Apply 50% transparency to the inverted frame
            overlay = cv2.addWeighted(frame1, 0.5, inverted_frame, 0.5, 0)

            # Write the overlaid frame to the output video
            output_video.write(overlay)
            Out60_video.write(overlay)

            # # Display the overlaid frame
            # cv2.imshow('Overlay', overlay)
            
            # # Press 'q' to quit
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            # # Update the previous frame
            # frame1 = frame2

    # Release video capture and writer objects
    video_capture.release()
    output_video.release()
    Out60_video.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()



# -- Function to specify frame 'delay' -- aka compare present frame to user specfied frame 
# think of like long exposure in camera - i want to compare present frame to 30 frames ago to see slower movements
def variableExposureInvertFunc(inputVideoName, numFramesToCompareTo):
    # Open the video file
    video_capture = cv2.VideoCapture(inputVideoName)

    # Get the frame rate of the input video
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Get the codec of the input video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Define output video writer
    output_video = cv2.VideoWriter(f'Out_{fps}fps_video--@{numFramesToCompareTo}_frame_delay.mp4', fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))))
    Out60_video = cv2.VideoWriter(f'Out_60fps_video--@{numFramesToCompareTo}_frame_delay.mp4.mp4', fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))))

    # Read the first frame
    # success, frame1 = video_capture.read()

# -----------
    # Initialize frame buffer
    # frame_buffer = [frame1] * numFramesToCompareTo
    frame_buffer = []

    # Read the first x number of frames into an array
    for _ in range(numFramesToCompareTo):
        success, frame1 = video_capture.read()
        if success:
            frame_buffer.append(frame1)
        else:
            break

    # Display the number of frames read
    print(f"Number of frames read: {len(frame_buffer)}")
# -----------

    currentFramePos = numFramesToCompareTo + 1

    # Loop through the video frames
    while success:
        # incriment current frame
        currentFramePos = currentFramePos + 1

        # Read the next frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, currentFramePos)
        success, nextFrame = video_capture.read()

        if success:
            # Store the current frame in the buffer
            frame_buffer.pop(0)
            frame_buffer.append(nextFrame)

            # Get the frame five frames back
            frame_to_compare = frame_buffer[0]

            # Invert the colors of the current frame
            inverted_frame = cv2.bitwise_not(nextFrame)

            # Apply 50% transparency to the inverted frame
            overlay = cv2.addWeighted(frame_to_compare, 0.5, inverted_frame, 0.5, 0)

            # Write the overlaid frame to the output video
            output_video.write(overlay)
            Out60_video.write(overlay)

            # Display the overlaid frame
            cv2.imshow('Overlay', overlay)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release video capture and writer objects
    video_capture.release()
    output_video.release()
    Out60_video.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
delete_videos()

thisVideo = returnVid()



# Get the number of CPU cores -- in future can use this to apply muliprocessing
num_cpu_cores = os.cpu_count()
print("Number of CPU cores:", num_cpu_cores)

# invertVideoFunc(thisVideo)