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

## Limitations

* Frametime Analyser assumes the input video is encoded at a constant frame rate of 60 FPS, with dropped frames encoded as duplicate frames
* Frametime Analyser does not account for screen tearing in the game recording. V-Sync should be enabled when recording the footage.

