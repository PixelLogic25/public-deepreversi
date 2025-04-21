import os


# 現在のワークスペース（カレントディレクトリ）のパスを取得
current_workspace = os.getcwd()
print("Current workspace:", current_workspace)

import numpy as np
import tensorflow as tf
import reversi_game as rg
from reversi_env import ReversiEnv,Reward_bits
from model import DualNetworkAgent
from input_state import InputState

import memory as m
from tensorflow.python.client import device_lib

import math
import random
import time
import magic_number



def display_count_clear():
    display_data.clear()
    display_data.append([])
    display_data.append([])

def print_procces_time(end):
    global before
    if before == 0:
        pass
    else:
        print(f"Execution time: {end - before} seconds")
    
    before = end
    




def generate_masks(moves):
    # ここで各状態に対するマスクを生成するロジックを実装
    # 例: 有効な着手可能位置に1, それ以外に0をセット

    # statesはバッチ内のゲームの状態を含むNumPy配列
    masks = np.zeros((len(moves),1, 64))  # 仮に64がアクションサイズ（盤面の位置数）
    for i, move in enumerate(moves):
        # ここで各stateに基づいて有効な着手位置を計算
        # 例としてランダムに有効な位置を選ぶ
        masks[i, 0 , move] = 1  # 有効な位置に対してマスクを1に設定


    
    return masks

'''
# 学習率のスケジューラーを定義
def lr_scheduler(fit_count):
    
    e = 10

    t = (fit_count/4 - e)
    if -1<t : t=-1


    lr = 10**t
    
    return lr
   ''' 
'''
bbb = tf.test.is_gpu_available()
aaaaa = tf.test.gpu_device_name()
if aaaaa:
    print('GPU found:', tf.test.gpu_device_name())
else:
    print('No GPU found')
'''

before = 0
if __name__ == "__main__":


    magic_numbers = magic_number.MagicNumber()

    #debug_ = debug.Debug()
    display_data=[]
    
    EPISODES = 900000
    #EPISODES = 1000  # LR Range Test用にエピソード数を減少
    BATCH_SIZE = 60  # バッチサイズを設定


    state_size = 131+4
    cpu_state_size = 131+4
    action_size = 1

    #env = ReversiEnv(state_size,cpu_state_size,model_pass= f'model_files/gen11_3.h5',magic_numbers = magic_numbers)
    env = ReversiEnv(state_size,cpu_state_size,model_pass=None,magic_numbers = magic_numbers)
    #env = ReversiEnv(state_size,cpu_state_size,model_pass= f'model_files/final_model_gen7_5.h5',magic_numbers = magic_numbers)


    agent = DualNetworkAgent(state_size, action_size , load_file_pass=None)
    #agent = DualNetworkAgent(state_size, action_size , load_file_pass=f'model_files/gen11_3.h5')
    #agent = DualNetworkAgent(state_size, action_size , load_file_pass=f'model_files/model_108832.h5')

    #agent = DualNetworkAgent(state_size, action_size , load_file_pass=None)
    memory = m.Memory(agent.gamma)  # 経験を保存するリスト


    #
    # 学習率と損失を記録するリスト

    loss_list = []


    inp = InputState()

    display_count_clear()

    fit_count=0


    #initial_learning_rate = 0.1
    #optimizer = tf.keras.optimizers.Adam(learning_rate=initial_learning_rate)

    rnd = np.random.default_rng()

    random_action_per = 0.1
    add_lie_random = 0.1
    cpu_add_lie_random = 0.1

    print_procces_time(time.time())

    cpu_turn = True


    pass_per = 0.8
    pass_set_count = 10 
    pass_count = 0

    #start = time.time()
    rng = np.random.default_rng()

    
    for e in range(EPISODES):

        #意図的に遅くしてCPU使用率を下げる。CPUのファンがうるさい場合使用してください
        #time.sleep(0.1)

        state, _ = env.reset()
        done = False

        cpu_turn = not cpu_turn

        while not done:
            
            for i in range(60):
                #cpuのターンなら打ってもらう
                if cpu_turn ==env.game.turn:
                    #env.game.print_board()
                    done = env.cpu_move(random_per=1.0/60.0,add_lie_pred_multi=cpu_add_lie_random)
                else:
                    break
            
            
            if done:
                tmp_reward = None
                #メモリのrewardを最後の部分を書き換える
                if env.game.count_not_turn_stones() < env.game.count_turn_stones():
                    tmp_reward = magic_numbers.lose_reward
                else:
                    tmp_reward = magic_numbers.win_reward
                #env.game.print_board()
                memory.insert_last_reward(tmp_reward)
                break


            #モデルへの入力を取得
            state , len_possible = env.standardization()

            #モデルからの出力を得る
            value_pred = agent.model(np.reshape(state, [len(env.game.possible_move), state_size]),training=False)
            value_pred = value_pred.numpy()

            #ランダムな値を加える
            add = rng.random((len(value_pred),1)) * add_lie_random
            value_pred += add

            tmp_index = -1
            if random.random()<random_action_per:
                tmp_index = random.randint(0,len(value_pred)-1)
            else:
                tmp_index = np.argmax(value_pred)

            action = env.game.possible_move[tmp_index] 
            state = state[tmp_index]

            #env.game.print_board()
            #print(f'CPU_turn:{cpu_turn}')

            #選んだ手に対しての報酬と、次の盤面へ更新
            reward, done, _ , before_reward= env.step(action,tmp_index, len_possible)
            
            # 経験をメモリに保存
            memory.add(state, reward,before_reward)

            
            if done:
                break
            
        last = memory.onegame_rewards[len(memory.onegame_rewards)-1]

        display_data[0].append(last)
        memory.compile_onegame(agent.gamma,agent.other_gamma)

        if e % magic_numbers.train_every_n_episodes==0:
            #print(f'100局終了:{(time.time()-start)}')
            indices = []
            indices = range(len(memory.main_memory))

            batch = [memory.main_memory[i] for i in indices]  # バッチを選択
            states, rewards = zip(*batch)

            tmp_s = []
            for s in states:
                tmp_s.append(np.reshape(s,[1,len(s)]))

            states = tmp_s

            agent.model.fit(np.vstack(states), np.vstack(rewards), verbose=0,epochs=1)
            #print(f'fit終了:{(time.time()-start)}')
            #start = time.time()
            memory.reset() # メモリをクリア
            fit_count+=1
            #lr_scheduler(fit_count)

            ng_count = 0
            ok_count = 0
            su_count = 0
            for i in display_data[0]:
                if i==magic_numbers.lose_reward:
                    ng_count +=1
                elif i==magic_numbers.draw_reward:
                    ok_count +=1
                elif i==magic_numbers.win_reward:
                    su_count+=1

            tmp_per = ng_count / (ng_count + ok_count + su_count)
            if 0.7<tmp_per:
                random_action_per = 6/60.0
                add_lie_random = 0.20
                cpu_add_lie_random = 0.22
            elif 0.6<tmp_per:
                random_action_per = 3/60.0
                add_lie_random = 0.15
                cpu_add_lie_random = 0.17
            elif 0.5<tmp_per:
                random_action_per = 2/60.0
                add_lie_random = 0.10
                cpu_add_lie_random = 0.12
            elif 0.4<tmp_per:
                random_action_per= 1/60.0
                add_lie_random = 0.10
                cpu_add_lie_random = 0.07
            elif 0.3<tmp_per:
                random_action_per=0.7/60.0
                add_lie_random = 0.10
                cpu_add_lie_random = 0.06
            elif 0.2< tmp_per :
                random_action_per=0.7/60.0
                add_lie_random = 0.10
                cpu_add_lie_random = 0.04
            else:
                random_action_per=0.5/60.0
                add_lie_random = 0.10
                cpu_add_lie_random = 0.02
            #random_action_per = #(ok_count+su_count)/(ng_count+ok_count+su_count)


            print(f"Episode: {e+1}/{EPISODES}, win:{su_count} win:{ok_count} lose:{ng_count}")
            #print(f"Episode: {e+1}/{EPISODES}, draw:{ok_count} lose:{ng_count}")
            if pass_per <= 1.0 - tmp_per:
                pass_count +=1
                if pass_set_count<=pass_count:
                    break
            else:
                pass_count = 0


            display_count_clear()


            
            

        # Save the model every 100 episodes
        if (e + 1) % 10000 == 0:
            agent.model.save(f'model_files/model_{e+1}.h5')
            print(f'Model saved after episode {e+1}')


    #print(loss_list)

    # Save the final model
    agent.model.save('model_files/final_model.h5')
    print('Final model saved.')
    
