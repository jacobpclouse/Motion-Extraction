# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import cv2
import os
import sys
import datetime


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
OUTPUT_FOLDER_NAME = 'OUTPUTS'  # folder where all the output files should be stored
show_live_output = True  # show live output

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
    print("Dedicated to Mary Clouse, Stephen Frost, and Harley Alderson III")

# --- Function to create a folder if it does not exist ---
def createFolderIfNotExists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":", "_")
    current_datetime = current_datetime.replace(".", "-")
    current_datetime = current_datetime.replace(" ", "_")

    return current_datetime

# --- Function to take target video name in from the command line ---
def returnVid():
    incomingVid = sys.argv[1]
    return incomingVid


# --- Function to invert previous frame and compare to present ---
def invertVideoFunc(inputVideoName, outputFolder):
    # Open the video file
    # video_capture = cv2.VideoCapture('input_video.mp4')
    video_capture = cv2.VideoCapture(inputVideoName)

    # Get the frame rate of the input video
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Get the codec of the input video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Define output video writer
    namePathOrigFPS = os.path.join(
        outputFolder, f'Out_{fps}fps_video--@DEFAULT_1_frame_delay.mp4')
    namePath60FPS = os.path.join(
        outputFolder, f'Out_60fps_video--@DEFAULT_1_frame_delay.mp4')
    originalFPS_OutVideo = cv2.VideoWriter(namePathOrigFPS, fourcc, fps, (int(
        video_capture.get(3)), int(video_capture.get(4))))
    modified60FPS_OutVideo = cv2.VideoWriter(
        namePath60FPS, fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))))

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
            originalFPS_OutVideo.write(overlay)
            modified60FPS_OutVideo.write(overlay)

            # maybe ask user if they want to see this?

            if show_live_output == True:
                # Display the overlaid frame
                # cv2.imshow('Overlay', overlay)
                cv2.imshow('DEFAULT 1 frame Delay - Overlay', overlay)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Update the previous frame
            frame1 = frame2

    # Release video capture and writer objects
    video_capture.release()
    originalFPS_OutVideo.release()
    modified60FPS_OutVideo.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# -- Function to specify frame 'delay' -- aka compare present frame to user specfied frame
# think of like long exposure in camera - i want to compare present frame to 30 frames ago to see slower movements
def variableExposureInvertFunc(inputVideoName, outputFolder, numFramesToCompareTo):
    # Open the video file
    video_capture = cv2.VideoCapture(inputVideoName)

    # Get the frame rate of the input video
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Get the codec of the input video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    namePathOrigFPS = os.path.join(
        outputFolder, f'Out_{fps}fps_video--@{numFramesToCompareTo}_frame_delay.mp4')
    namePath60FPS = os.path.join(
        outputFolder, f'Out_60fps_video--@{numFramesToCompareTo}_frame_delay.mp4')

    # Define output video writer
    originalFPS_OutVideo = cv2.VideoWriter(namePathOrigFPS, fourcc, fps, (int(
        video_capture.get(3)), int(video_capture.get(4))))
    modified60FPS_OutVideo = cv2.VideoWriter(
        namePath60FPS, fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))))

# -----------
    # Initialize frame buffer
    frame_buffer = []

    # Read the first x number of frames into an array
    for _ in range(numFramesToCompareTo):
        success, frame1 = video_capture.read()
        if success:
            frame_buffer.append(frame1)
        else:
            break

    # Display the number of frames read
    print(f"DELAY BUFFER: Number of frames read: {len(frame_buffer)}")
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
            overlay = cv2.addWeighted(
                frame_to_compare, 0.5, inverted_frame, 0.5, 0)

            # Write the overlaid frame to the output video
            originalFPS_OutVideo.write(overlay)
            modified60FPS_OutVideo.write(overlay)

            if show_live_output == True:
                # Display the overlaid frame
                cv2.imshow(
                    f'CUSTOM {numFramesToCompareTo} frame Delay - Overlay', overlay)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # Release video capture and writer objects
    video_capture.release()
    originalFPS_OutVideo.release()
    modified60FPS_OutVideo.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# create outputs Folder
createFolderIfNotExists(OUTPUT_FOLDER_NAME)

if len(sys.argv) < 2:
    raise ValueError(
        "ERROR: You need to provide the name of your target video as an argument when you run your code!")
else:
    # use function to get argument from command line
    thisVideo = returnVid()
    # used to grab date and time to create output folder
    currentDateTime = defang_datetime()

    # # Get the number of CPU cores -- in future can use this to apply muliprocessing
    # num_cpu_cores = os.cpu_count()
    # print("Number of CPU cores:", num_cpu_cores)

# do they want to see the output live? Or run it headless?
    user_input = input(
        "Do you want to see live output from the motion extraction process? (yes/no): ")

    if user_input.lower() == "no":
        show_live_output = False
    elif user_input.lower() != "yes":
        print("Invalid input. Defaulting to live output.")

    # Now, you can use show_live_output throughout your code
    print("Show live output:", show_live_output)


# choose what kind of delay you want for your extraction:
    chooseInvert = input(
        "What kind of Invert do you want: PREVIOUS or CUSTOM? ")
    print(chooseInvert.upper())
    print('\n')

    # Catch statement to prevent invalid selections
    while chooseInvert == '':
        chooseInvert = input(
            "Can't be left blank, please input either PREVIOUS or CUSTOM: ")

    # execute PREVIOUS Invert
    if chooseInvert.upper() == 'PREVIOUS':
        # create subfolder name to house output
        subFolderName = f"Motion_Extraction--PREVIOUS_OPTION--From_{currentDateTime}"
        pathSubfolder = os.path.join(OUTPUT_FOLDER_NAME, subFolderName)

        # create subfolder
        createFolderIfNotExists(pathSubfolder)

        # execute function
        invertVideoFunc(thisVideo, pathSubfolder)

        # at end, print my logo
        myLogo()

    # execute CUSTOM Invert ****
    elif chooseInvert.upper() == 'CUSTOM':

        # choose fps delay:
        fpsDelay = input("How many frames delayed do you want? ")
        while fpsDelay == '' or not fpsDelay.isdigit():
            fpsDelay = input(
                "Can't be left blank and needs to be a valid number: ")

        # create subfolder name to house output
        subFolderName = f"Motion_Extraction--CUSTOM_@{fpsDelay}_Frame_Delay--From_{currentDateTime}"
        pathSubfolder = os.path.join(OUTPUT_FOLDER_NAME, subFolderName)

        # create subfolder
        createFolderIfNotExists(pathSubfolder)

        # execute function
        variableExposureInvertFunc(thisVideo, pathSubfolder, int(fpsDelay))

        # at end, print my logo
        myLogo()

    # if nonsense, end the script
    else:
        print("Response Not Recognized, Ending Program...")

