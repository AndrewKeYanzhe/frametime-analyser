vid = "F:/ReLive/2020.10.14-21.51.mp4"

from moviepy.editor import VideoFileClip
filepath = "output.avi"
clip = VideoFileClip(vid)

for f in clip.iter_frames(True):
    np_array_frame = f