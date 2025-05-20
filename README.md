# Motion-Extraction <!-- CTRL SHIFT V to preview md in vscode -->
With a very simple trick you can extract the motion of a video. Uses python3 and OpenCV to compare current frame of the video to a previous frame to see where changes have been made in the frames (and any changes indicate motion).
> Inspired by <a href="https://youtu.be/NSS6yAMZF78"> this </a> video by Posy

### NOTE: Recommend to only test on shorter videos (ie: not greater than 5 minutes) -- current program converts in REAL TIME 
- IE: 5 hour video = at least 5 hours to convert

### How to run this program (Easy Way):
- 1) Make sure you have python 3 downloaded, installed and on path
- 2) Move your target MP4 video into the same directory as the `motion_Extraction.py` file
- 5) Run the easy install program with the command `python Install_and_Run_Program.py --video 'yourVideo.mp4'` 
    * you NEED to provide the video title as an argument
    * this will automatically create a new virtual environment, install all the pip packages and then run the extraction program
- 6) If you want to see the extraction overlay, type `yes`. If you do not, type `no`
- 7) If you just want the frame compared to the previous one, then type `PREVIOUS`. If you want a larger delay, type `CUSTOM` (you will the be prompted to enter your custom frame delay)
- 8) Your output will be created in a subfolder within the `OUTPUTS` folder, enjoy!

### How to run this program (Long Way):
- 1) Make sure you have python 3 downloaded, installed and on path
- 2) Use the activateVirEnv.txt to create a virtual environment
- 3) Make sure you `pip install -r requirements.txt` to install all the needed packages
- 4) Move your target MP4 video into the same directory as the `motion_Extraction.py` file
- 5) Run the program with the command `python motion_Extraction.py yourVideo.mp4` 
    - you NEED to provide the video title as an argument
- 6) If you want to see the extraction overlay, type `yes`. If you do not, type `no`
- 7) If you just want the frame compared to the previous one, then type `PREVIOUS`. If you want a larger delay, type `CUSTOM` (you will the be prompted to enter your custom frame delay)
- 8) Your output will be created in a subfolder within the `OUTPUTS` folder, enjoy!

### Ideas:
- [DONE] maybe combine the two while loops?
- [DONE] invert then immediatly overlay?
- [DONE] check pervious frame in one video then x frames back in another video (shows slower movement)
- cut videos larger than like 3 minutes into chunks of 1 minutes, store in folder [check multiprocessing attempt folder]
- then use threading to individually loop through and invert videos
- then you can paste it together at the end

### Resources used:
- Motion Extraction tutorial (attempt...): https://youtu.be/woj4vfMLpao
- Python OpenCV – cv2.flip() method: https://www.geeksforgeeks.org/python-opencv-cv2-flip-method/
- Adding (blending) two images using OpenCV : https://docs.opencv.org/3.4/d5/dc4/tutorial_adding_images.html
- How to split a video in parts using Python?: https://stackoverflow.com/questions/65570944/how-to-split-a-video-in-parts-using-python
- multiprocessing — Process-based parallelism: https://docs.python.org/3/library/multiprocessing.html
