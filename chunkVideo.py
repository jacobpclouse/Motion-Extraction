from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

# https://stackoverflow.com/questions/65570944/how-to-split-a-video-in-parts-using-python

OUTPUT_FOLDER = 'OUTPUTS'

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

# from moviepy.editor import VideoFileClip

def cut_video(input_file, output_prefix, chunk_duration):
    video_clip = VideoFileClip(input_file)
    total_duration = video_clip.duration
    start_time = 0
    end_time = min(chunk_duration, total_duration)

    chunk_number = 1
    while start_time < total_duration:
        # Extract subclip
        subclip = video_clip.subclip(start_time, end_time)
        
        # Define output file name
        output_file = f"{output_prefix}_part{chunk_number}.mp4"
        
        # Save subclip to file
        subclip.write_videofile(output_file, codec="libx264")
        
        # Update start and end times for next iteration
        start_time = end_time
        end_time = min(start_time + chunk_duration, total_duration)
        
        chunk_number += 1

    video_clip.close()

# Example usage
input_file = "OLD\CHUNK\Field with Wind, Swallows, & Windchimes - Happy Summer moments 4K NO LOOP.mp4"
output_prefix = "output_chunk"
number_of_chunks = 4

create_folder_if_not_exists(OUTPUT_FOLDER)

current_duration = VideoFileClip(input_file).duration
print(f"Duration: {current_duration}")
chunk_duration = current_duration / number_of_chunks
print(f"Chunk Size: {chunk_duration}")

# chunk_duration = 60  # seconds

# Join various path components
fullPath_outputPrefix = os.path.join(OUTPUT_FOLDER,output_prefix)
print(fullPath_outputPrefix)

cut_video(input_file, fullPath_outputPrefix, chunk_duration)

