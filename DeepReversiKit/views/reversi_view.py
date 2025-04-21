from flask import Blueprint
from flask import render_template, jsonify, request , Response,current_app

#import web_deep_reversi_app.reversi_game as rg


try:
    from model import DualNetworkAgent
except:
    from DeepReversiKit.model import DualNetworkAgent


import numpy as np
#import tensorflow as tf
#from web_deep_reversi_app.reversi_env import ReversiEnv



#from collections.abc import Iterable

import json
import os
import sys
import time
import gzip


reversi_bp = Blueprint('reversi', __name__)


# モジュールレベルでグローバルに初期化
dual_network_agent = None

def initialize_agent():
    global dual_network_agent
    if dual_network_agent is None:
        state_size=131
        action_size = 1
        dual_network_agent = DualNetworkAgent(state_size, action_size , load_file_pass='DeepReversiKit/model_files/final_model_gen_9_13.h5')  # 初期化処理を一度だけ実行

# アプリケーション起動時に初期化
def setup_app(app):
    @app.before_request
    def setup_agent():
        initialize_agent()

@reversi_bp.route('/')
def deep_reversi():
    client_ip = request.remote_addr
    current_app.logger.info(f"Accessed /top from {client_ip}")
    return render_template('deeplearning_reversi.html')


# 現在の作業ディレクトリを確認します
current_working_directory = os.getcwd()

print(f'現在の作業ディレクトリ(リバーシ): {current_working_directory}')



#agent = DualNetworkAgent(state_size, action_size , load_file_pass='web_deep_reversi_app/model_files/final_model_gen_9_13.h5')

#いずれCPUのターンはhtmlのほうで設定できるようにする
cpu_turn = False


ONE_INPUT_SPAN = 44
MAX_NODES = 8000

rng = np.random.default_rng()

# データをgzip圧縮するヘルパー関数
def gzip_compress(data):
    return gzip.compress(data.encode('utf-8'))

#board = rg.ReversiGame()





def is_check_passed(data):
    #割り切れないならだめ
    if len(data)%ONE_INPUT_SPAN!=0:
        return False

    #評価値を計算する局面の数
    node_num = int(len(data)/ONE_INPUT_SPAN)
    if MAX_NODES < node_num :
        return False
    

    return True






@reversi_bp.route('/move', methods=['POST'])
def move():

    #print(f'受信 agent memory:{get_deep_sizeof(agent)}')
    #start_time = time.time()
    compressed_data = request.get_data()
    data = list(gzip.decompress(compressed_data))

    int_list = None
    res_list = None
    nodes_num = int(len(data)/ONE_INPUT_SPAN)

    error = False
    if is_check_passed(data):

        client_ip = request.remote_addr
        current_app.logger.info(f"Post /move check success from {client_ip}")

        #print(input_array[0].tolist())
        #print(input_array[1].tolist())
        #print(input_array[2].tolist())
        
        #受信したデータからモデルに入力する形に変換
        input_array = data_to_model_input_data(data)
        #評価値を得る
        value_pred = dual_network_agent.model(np.array(input_array),training=False)
        value_pred = value_pred.numpy()

    
        #返信用の送信データを作る。100万倍して切り捨てた評価値を返す

        value_pred*=1000*1000
        int_list = np.floor(value_pred).astype(int).tolist()
        res_list = [item[0] for item in int_list]

    else:
        #ダミーの値を返す
        res_list = rng.integers(-100000,100000, size=nodes_num).astype(int).tolist()
        error = True

        client_ip = request.remote_addr
        current_app.logger.info(f"Post /move check failed from {client_ip}")
        pass

    #print(res_list)

    data = {
        "success": True,
        "evals": res_list,  # 評価値だけ返却
        "error": error
    }
    
    # JSONとしてエンコードし、gzip圧縮
    json_data = json.dumps(data)
    compressed_data = gzip_compress(json_data)
    
    # レスポンスの設定
    response = Response(compressed_data, content_type='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = str(len(compressed_data))
    
    #print('処理時間:',str(time.time()-start_time))
    return response

 #受信したデータからモデルに入力する形に変換
def data_to_model_input_data(data):

    # 'data' は解凍されたバイトデータ
    # バイトデータから盤面、ターンを取得

    '''
    受信するデータの順番と大きさ

    前の盤面の黒石 64bit
    前の盤面の白の石 64bit
    現在の盤面の黒の石 64bit
    現在の盤面の白の石 64bit
    現在の手番 8bit
    一手前の手番と今の手番が同じなら1、違うなら-1 8bit
    「着手可能数÷最大着手可能数」を100万倍した整数 32bit  
    '''
    input_array = []
    
    #受信したデータからモデルに入力する形に変換
    count=0


    byte_array = np.array(data, dtype=np.uint8)

    for i in range(int(len(data)/ONE_INPUT_SPAN)):

        #前の盤面のstateをnpリストに変換
        before_board_list = get_np_by_bit(byte_array,count,8).astype(np.int32)
        count+=8
        before_board_list = get_np_by_bit(byte_array,count,8).astype(np.int32) - before_board_list
        count+=8

        #現在の盤面のStateをnpリストに変換
        board_list = get_np_by_bit(byte_array,count,8).astype(np.int32)
        count+=8
        board_list = get_np_by_bit(byte_array,count,8).astype(np.int32) - board_list
        count+=8


        #現在の手番を取得
        turn = get_np_by_bit(byte_array,count+3,1).astype(np.int32)
        if turn[0] == 0:
            turn[0] = -1
        turn = np.array([turn[0]]).astype(np.int32)
        count+=4

        #一手前の手番と今の手番が同じかどうかを取得
        turn_state = get_np_by_bit(byte_array,count+3,1).astype(np.int32)
        if turn_state[0] == 0:
            turn_state [0]= -1
        turn_state= np.array([turn_state[0]]).astype(np.int32)




        count+=4

        #「着手可能数÷最大着手可能数」を100万倍した整数を取得
        # リストを文字列に変換し、2進数として解釈して整数に変換
        #possible_state = int(''.join(map(str, get_list_by_bit(data,count,4))), 2)
        possible_state = np.array([convert_to_int(byte_array,count)/(1000*1000)]).astype(np.float64)

        count+=4

    

        input_array.append(np.concatenate((before_board_list,board_list,turn,turn_state,possible_state)))

    return input_array

# 連続する4つを取り出し、それを1つの整数に変換する関数
def convert_to_int(data, start_index):
    # 連続する4つのデータを取り出し
    chunk = data[start_index:start_index + 4]
    # 32ビットの整数に変換
    value = (chunk[0] << 24) | (chunk[1] << 16) | (chunk[2] << 8) | chunk[3]
    return np.int32(value)


# 指定した位置から任意の数の要素ごとに変換する関数
def convert_segment(array, start_index, segment_size=8):
    # 指定位置から8つの要素をスライスしてunpackbits
    segment = array[start_index:start_index + segment_size]


    return np.flip(np.unpackbits(segment))


def get_np_by_bit(data,ofset,byte_length):
    
    # 指定位置から8つの要素をスライスしてunpackbits
    segment = data[ofset:ofset + byte_length]
    return np.flip(np.unpackbits(segment))



def get_list_by_bit(data,ofset,byte_length):
    #byteをintのlist([0,1,0,1,1,0...])に変換
    count = ofset
    bit = data[count]
    count+=1
    for j in range(byte_length-1):
        bit = (bit<<8) | data[count]
        count+=1

    return int_to_bit_list(bit,byte_length*8)
    



def int_to_bit_list(number, bit_length):
    # number を bin() で 2進数文字列に変換し、プレフィックス '0b' を除去
    binary_string = bin(number)[2:]
    
    # 指定のビット長までゼロ埋め（上位の桁が不足している場合）
    padded_binary_string = binary_string.zfill(bit_length)
    
    # 各文字を整数に変換してリストにする
    bit_list = [int(bit) for bit in padded_binary_string]
    
    return bit_list



def get_deep_sizeof(obj, seen=None):
    """オブジェクト全体のメモリ使用量を再帰的に計算する"""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0  # 循環参照を防ぐ
    seen.add(obj_id)

    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(get_deep_sizeof(k, seen) + get_deep_sizeof(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_deep_sizeof(i, seen) for i in obj)
    elif hasattr(obj, '__dict__'):  # クラスのインスタンスなど
        size += get_deep_sizeof(vars(obj), seen)
    elif hasattr(obj, '__slots__'):  # __slots__を使ったクラス
        size += sum(get_deep_sizeof(getattr(obj, slot), seen) for slot in obj.__slots__ if hasattr(obj, slot))
    
    return size