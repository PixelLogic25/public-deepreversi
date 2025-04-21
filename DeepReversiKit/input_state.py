import numpy as np
import tensorflow as tf
import reversi_game as rg
from reversi_env import ReversiEnv
from model import DualNetworkAgent



class InputState:

    def __init__(self) -> None:
        pass
    
    def get_input_state(self,board:rg,row_state):
        move_list = board.possible_move
        tmp_rg = rg.ReversiGame(board)

        res = [0] * 64
        max = -1
        max_moves =[]

        over = False

        for m in move_list:
            if 0<m and m<64:

                tmp = tmp_rg.make_move(m)

                if tmp=='':
                    count = tmp_rg.count_not_turn_stones()
                    if max<count:
                        max_moves=[m]
                        max = count
                    elif max==count:
                        max_moves.append(m)

                else:
                    pass
            else :
                over = True

        if over :
            pass
        else:
            for i in max_moves:
                res[i] = 1
        return res









    