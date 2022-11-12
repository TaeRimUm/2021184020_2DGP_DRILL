# fill here
import pico2d
import game_framework
import logo_state
import play_state
import item_state
import add_delete_boy

import play_state_Boy_move

pico2d.open_canvas()
game_framework.run(logo_state)
game_framework.run(play_state)
#game_framework.run(item_state)
#game_framework.run(play_state_Boy_move)


pico2d.close_canvas()
