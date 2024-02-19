# Motion-Extraction
With a very simple trick you can extract the motion of a video. Uses python and OpenCV
> Inspired by <a href="https://youtu.be/NSS6yAMZF78"> this </a> video by Posy

#### NOTE: Recommend to only test on shorter videos (ie: not greater than 5 minutes) -- current program converts in REAL TIME (5 hour video = at least 5 hours to convert)

<!-- CTRL SHIFT V to preview md in vscode -->
### Ideas:
- maybe combine the two while loops?
- invert then immediatly overlay?
- check pervious frame in one video then x frames back in another video (shows slower movement)
- cut videos larger than like 3 minutes into chunks of 1 minutes, store in folder [check multiprocessing attempt folder]
- then use threading to individually loop through and invert videos
- then you can paste it together at the end

### Resources used:
- Motion Extraction tutorial (attempt...): https://youtu.be/woj4vfMLpao
- Python OpenCV – cv2.flip() method: https://www.geeksforgeeks.org/python-opencv-cv2-flip-method/
- Adding (blending) two images using OpenCV : https://docs.opencv.org/3.4/d5/dc4/tutorial_adding_images.html
- How to split a video in parts using Python?: https://stackoverflow.com/questions/65570944/how-to-split-a-video-in-parts-using-python
