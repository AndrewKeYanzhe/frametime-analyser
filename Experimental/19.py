# -*- coding: utf-8 -*-

import vlc
import time 
import cv2

def mspf(mp):
    """Milliseconds per frame"""
    return int(1000 /60)


if __name__ == "__main__":
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("F:/ReLive/2020.09.18-22.33.mp4")
    player.set_media(media)

    player.play()

    """Play 800th frames"""
    new_time = 800 * mspf(player)
    player.set_time(new_time)

    time.sleep(10)