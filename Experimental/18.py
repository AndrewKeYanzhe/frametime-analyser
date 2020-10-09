import vlc
import time

# player = vlc.MediaPlayer("F:/ReLive/2020.09.18-22.33.mp4")
# player.play()

# while True:
#      pass

instance = vlc.Instance('--no-xlib --quiet')
player = instance.media_player_new()
media = instance.media_new("F:/ReLive/2020.09.18-22.33.mp4")
player.set_media(media)
player.play()
# mfps = int(1000 / (player.get_fps() or 25))
mfps = int(1000 / 60)
player.set_time(0) # start at 30 seconds
player.pause()
t = player.get_time()
# for iter in range(30):
while True:
	# pass:
    t += mfps
    player.set_time(t)
    if player.get_state() == 6: #6 is stopped, 3 is playing
        player.pause()
    time.sleep(0.5)