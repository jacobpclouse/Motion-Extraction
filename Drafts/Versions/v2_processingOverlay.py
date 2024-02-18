import cv2
import os
import sys
import multiprocessing

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

def returnVid():
    incomingVid = sys.argv[1]
    return incomingVid



def invertVideoFunc(inputVideoName):
    # Open the video file
    # video_capture = cv2.VideoCapture('input_video.mp4')
    video_capture = cv2.VideoCapture(inputVideoName)

    # Get the frame rate of the input video
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Get the codec of the input video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # # Define output video writer
    # output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))))
    # Out60_video = cv2.VideoWriter('Out60_video.mp4', fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))))
        # Define output video writer
    normalOutput = f'output_video-bitrate_{bitrate}-{inputVideoName}'
    at60FPSOutput = f'Out60_video-bitrate_{bitrate}-{inputVideoName}'

    # Increase the bitrate for better quality
    bitrate = 5000000  # Adjust bitrate as needed

    output_video = cv2.VideoWriter(normalOutput, fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))), bitrate)
    Out60_video = cv2.VideoWriter(at60FPSOutput, fourcc, 60, (int(video_capture.get(3)), int(video_capture.get(4))), bitrate)

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

            # Update the previous frame
            frame1 = frame2

    # Release video capture and writer objects
    video_capture.release()
    output_video.release()
    Out60_video.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# MAIN

# delete_videos()

# thisVideo = returnVid()



if __name__ == "__main__":
    # Get the number of CPU cores
    num_cpu_cores = os.cpu_count()
    print("Number of CPU cores:", num_cpu_cores)

    # creating processes 
    p1 = multiprocessing.Process(target=invertVideoFunc, args=("grass.mp4",)) 
    p2 = multiprocessing.Process(target=invertVideoFunc, args=("waves.mp4",))

    print("ID of main process: {}".format(os.getpid())) 

    # starting processes 
    p1.start() 
    p2.start() 

    # process IDs 
    print("ID of process p1: {}".format(p1.pid)) 
    print("ID of process p2: {}".format(p2.pid)) 

    # wait until processes are finished 
    p1.join() 
    p2.join() 

    # both processes finished 
    print("Both processes finished execution!") 

    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive()))
