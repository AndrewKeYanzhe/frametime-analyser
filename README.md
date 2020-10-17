# Frametime Analyser
Frametime Analyser is a tool that detects duplicate frames in game footage to calculate FPS and frametimes.

![GitHub is not loading my RDR2 Gif :(](/Media/RDR2.gif)

It is inspired by Digital Foundry's FPSGui tool:

[![GitHub is not loading the Digital Foundry Gif :(](/Media/DF.gif)](https://youtu.be/niQfeglwDZ4?t=986)

## Setup

Frametime Analyser requires the following prerequisites

* Python 2.7.14
* OpenCV 4.2.0
* Numpy 1.14.3
* Matplotlib 2.2.5

## Usage

1. Clone this repo
2. Open `Frametime Analyser.py` in a text editor and set `file_path` to the location of your video
3. Run `Frametime Analyser.py`

Notes
* Input video must be encoded at 60 FPS
* OpenCV decodes video in software, so a fast CPU is recommended. i7-3770 is sufficient for H.264 1080p. H.265 or higher resolutions would require a faster CPU

## Technical Overview

Key processing steps
1. Calculate absolute difference of each pixel relative to previous frame
2. Calculate the average difference across the whole frame, giving the value `frame_diff`
3. Compare `frame_diff` with the exponential moving average of `frame_diff`. If `frame_diff` is significantly lower than the moving average (suggesting a duplicate frame), the frame is counted as a duplicate

## Limitations

* Frametime Analyser assumes the input video is encoded at a constant frame rate of 60 FPS, with dropped frames encoded as duplicate frames
* Frametime Analyser does not account for screen tearing. V-Sync should be enabled when recording the game footage.
