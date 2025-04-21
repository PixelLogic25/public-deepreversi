from flask import render_template, jsonify, request , Response
from web_deep_reversi_app import app
import web_deep_reversi_app.reversi_game as rg

from web_deep_reversi_app.model import DualNetworkAgent
import numpy as np
import tensorflow as tf
from web_deep_reversi_app.reversi_env import ReversiEnv

import json
import os
import sys
import time
import gzip

import web_deep_reversi_app.reward_bits as rb
'''
# コマンドライン引数を取得します
args = sys.argv

# 最初の引数（スクリプト名）を除いた2番目の引数をディレクトリとして使用します
if len(args) > 1:
    new_working_directory = args[1]
    os.chdir(new_working_directory)
'''

# 現在の作業ディレクトリを確認します
current_working_directory = os.getcwd()
print(f'現在の作業ディレクトリ: {current_working_directory}')



#env = ReversiEnv(131,131,model_pass='web_deep_reversi_debug_app/model_files/final_model_gen9_3.h5')
env = ReversiEnv(131,131,model_pass='web_deep_reversi_app/model_files/model_138090.h5')
#env = ReversiEnv(129,model_pass='../model_files/model_314000.h5')
#いずれCPUのターンはhtmlのほうで設定できるようにする
cpu_turn = False


debug_reward_bits = rb.Reward_bits()
debug_reward_bits.reset()

#board = rg.ReversiGame()

@app.route('/deeplearning_reversi_debug')
def gebug_main():
    return render_template('deeplearning_reversi.html')



def get_stone_nums():
    if env.game.turn:
        b_num = env.game.count_turn_stones()
        w_num = env.game.count_not_turn_stones()
    else:
        b_num = env.game.count_not_turn_stones()
        w_num = env.game.count_turn_stones()

    return b_num,w_num

@app.route('/move', methods=['POST'])
def debugmove():
    global cpu_turn


    data = request.get_json()
    x = data['x']
    y = data['y']
    # リバーシのロジックを処理し、結果を返す

    #プレイヤーの手を反映させる
    env.game.make_move(x+y*8)


    ai_turn = env.game.turn



    for i in range(100):
        if cpu_turn is not None and env.game.turn == cpu_turn:
           
            env.cpu_move(random_per=0.0/60.0,add_lie_pred_multi=0.0)
            pass
        else:
            break

    nr,br =  debug_reward_bits.check_reward(env.game,ai_turn)
    print(f'現状の報酬{nr}相手の報酬{br}')


    b =  env.game.return_str_board()
    move_posible =  env.game.possible_move
    #env.game.print_board()
    turn =  env.game.turn
    
    b_num,w_num = get_stone_nums()

    return jsonify(result='success', b=b , move_posible = move_posible,turn = turn,b_num = b_num,w_num = w_num)



@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    reset = data['reset']
    back = data['back']
    foward = data['foward']

    if reset:
        env.reset()
        debug_reward_bits.reset()
    if back:
        env.game.back()

    if foward:
        env.game.foward()
        
    b = env.game.return_str_board()

    move_posible = env.game.possible_move
    env.game.print_board()

    turn = env.game.turn

    b_num,w_num = get_stone_nums()
    
    return jsonify(result='success', b=b , move_posible = move_posible,turn = turn,b_num = b_num,w_num = w_num)

@app.route('/moves_history', methods=['POST'])
def moves_history():
    data = request.get_json()
    moves = data['moves']
   

    env.game.reset()

    str_array:list = moves.split(',')
    
    for i in str_array:
        tmp = i.replace(' ','')
        tmp = int(tmp)
        env.game.make_move(tmp)

        
    b = env.game.return_str_board()

    move_posible = env.game.possible_move
    turn = env.game.turn

    b_num,w_num = get_stone_nums()

    return jsonify(result='success', b=b , move_posible = move_posible,turn = turn,b_num = b_num,w_num = w_num)

@app.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    str_board = data['board']
   

    env.game.generate_by_str(str_board)

        
    b = env.game.return_str_board()

    move_posible = env.game.possible_move
    turn = env.game.turn
    
    b_num,w_num = get_stone_nums()


    return jsonify(result='success', b=b , move_posible = move_posible,turn = turn,b_num = b_num,w_num = w_num)
