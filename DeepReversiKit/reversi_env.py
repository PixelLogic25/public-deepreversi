import numpy as np
try:
    import DeepReversiKit.reversi_game as rg
except:
    import reversi_game as rg
import random
import tensorflow as tf
import math

try:
    from reward_bits import Reward_bits
except:
    from DeepReversiKit.reward_bits import Reward_bits


try:
    import flip_buffer as fb
except:
    import DeepReversiKit.flip_buffer as fb


class ReversiEnv:
    def __init__(self,input_state_size,cpu_state_size,model_pass = None,magic_numbers = None):

        self.flip_buffer = fb.FlipBuffer()
        self.game = rg.ReversiGame(flip_stone_buffer=self.flip_buffer)
        self.input_state_size = input_state_size
        self.cpu_state_size = cpu_state_size
        if not model_pass == None:
            self.cpu_model = tf.keras.models.load_model(model_pass)
        else:
            self.cpu_model = None

        self.reward_kun = Reward_bits()

        self.rng = np.random.default_rng()

        self.magic_numbers = magic_numbers



    def reset(self):
        self.game.reset()
        self.reward_kun.reset()
        
        return self.game.return_int_board(), self.game.turn
    
    def get_valid_moves(self):
        
        return self.game.possible_move


    
    #旧式の学習時に使用する、一手だけの最善手取得
    def cpu_move(self,random_per = None,add_lie_pred_multi = None):

        #CPUモデルがない時はランダムな手を返す
        if self.cpu_model == None:
            tmp_index = random.randint(0,len(self.game.possible_move)-1)
            action = self.game.possible_move[tmp_index] 
            self.game.make_move(action)

            return self.game.game_end
        
            

        input_state = self.standardization_old()
        if not input_state is None:
            value_pred = self.cpu_model(np.reshape(input_state, [len(self.game.possible_move),self.cpu_state_size ]),training=False)
            value_pred = value_pred.numpy()

            tmp_index = -1

            if random_per == None:
                random_per = 0.1
            if add_lie_pred_multi ==None:
                add_lie_pred_multi = 0.0


            if random.random()<random_per:
                tmp_index = random.randint(0,len(value_pred)-1)
            else:
                if not add_lie_pred_multi ==0.0:
                    add = self.rng.random((len(value_pred),1)) * add_lie_pred_multi
                    value_pred += add


                tmp_index = np.argmax(value_pred)
                

            action = self.game.possible_move[tmp_index] 

            self.game.make_move(action)

            #学習をするときはコメントで消して
            #self.reward_kun.check_reward(self.game,False)


        return self.game.game_end


    

    """
    Args:
    action (Number): Description of parameter `x`.
    possible_best_res(list): 着手可能数が一番少なくさせるような手のリスト
    """
    def step(self, action, index , possible_best_res):
        
        # Assume action is a valid move index
        if action in self.game.possible_move:
            before_board = rg.ReversiGame(self.game,none_history=True,none_possible_move=True,flip_stone_buffer=self.flip_buffer)#あとでflip_bufferを追加しまくる
            #self.game.print_board()
            result = self.game.make_move(action)

            #報酬を計算
            reward,before_reward = self.calculate_reward(action,before_board,possible_best_res)
            done = (result == 'end')
            
            return reward, done, {},before_reward
        else:
            return -1, False, {}  # Penalty for invalid move

    def is_game_over(self):
        return 66 in self.game.possible_move  # Using 66 as the game-end indicator


    def standardization(self):
        
        
        valid_moves = self.game.possible_move
        tmp_board = rg.ReversiGame(self.game,none_history=True,none_possible_move=True,flip_stone_buffer=self.flip_buffer)
        
        tmp_board_state = tmp_board.return_int_board()
        stone_count_res = []
        board_res=[]
        
        tmp_board_res = []
        possible_len_list = []
        max_possible = 1
        
        turn_stone_num = tmp_board.count_turn_stones()
        not_turn_stone_num = tmp_board.count_not_turn_stones()
        
        if 66 in valid_moves or 77 in valid_moves :
            return None
        
        
        tmp_turn = -1 if self.game.turn else 1
        for m in valid_moves:

            #一手打つ
            tmp_board.make_move(m)

            #打った後も自分のターンなら1            
            next_turn_num = 1 if tmp_board.turn == self.game.turn else -1


            next_turn_stone_num = tmp_board.count_turn_stones()
            next_not_turn_stone_num = tmp_board.count_not_turn_stones()

            #打つ前の盤面と打った後の盤面、打つ前のターン、打った後のターンのリストを作る
            tmp_board_res.append(tmp_board_state + tmp_board.return_int_board() + [tmp_turn] + [next_turn_num]+[turn_stone_num]+[not_turn_stone_num]+[next_turn_stone_num]+[next_not_turn_stone_num])
            
            if next_turn_num == -1:
                possible_len_list.append(len(tmp_board.possible_notgomi_move) )
            else:
                #相手のターンでないなら相手の着手可能数は0
                possible_len_list.append(0)

            #一手打つ時の最大着手可能数を調べる
            if next_turn_num == -1 and max_possible<len(tmp_board.possible_notgomi_move):
                max_possible = len(tmp_board.possible_notgomi_move)
                

            tmp_board.back()

        possible_best_res = []
        tmp_min = 999999

        #相手の最大着手可能数を１とした着手可能数を追加
        #基本的には0に近いほうがいい手
        for i,p in enumerate(possible_len_list):
            
            board_res.append(tmp_board_res[i] + [p/max_possible])

            if p<tmp_min:
                possible_best_res = [valid_moves[i]]
                tmp_min = p
            elif p == tmp_min:
                possible_best_res.append(valid_moves[i])
        
        
        return board_res,possible_best_res

        #return stone_count_res
        #return [[stone_count_res[i],stone_count_max_res] for i in range(len(valid_moves))]#board_res


    def standardization_old(self):
        
        
        valid_moves = self.game.possible_move
        tmp_board = rg.ReversiGame(self.game,none_history=True,none_possible_move=True,flip_stone_buffer=self.flip_buffer )
        
        tmp_board_state = tmp_board.return_int_board()
        stone_count_res = []
        board_res=[]
        
        tmp_board_res = []
        possible_len_list = []
        max_possible = 1

        turn_stone_num = tmp_board.count_turn_stones()
        not_turn_stone_num = tmp_board.count_not_turn_stones()
        
        if 66 in valid_moves or 77 in valid_moves :
            return None
        
        
        tmp_turn = -1 if self.game.turn else 1
        for m in valid_moves:

            #一手打つ
            tmp_board.make_move(m)

            #打った後も自分のターンなら1            
            next_turn_num = 1 if tmp_board.turn == self.game.turn else -1
        
            next_turn_stone_num = tmp_board.count_turn_stones()
            next_not_turn_stone_num = tmp_board.count_not_turn_stones()

            #打つ前の盤面と打った後の盤面、打つ前のターン、打った後のターンのリストを作る
            tmp_board_res.append(tmp_board_state + tmp_board.return_int_board() + [tmp_turn] + [next_turn_num]+[turn_stone_num]+[not_turn_stone_num]+[next_turn_stone_num]+[next_not_turn_stone_num])
            
            #旧式のインプット（石の個数を入力していない）
            #tmp_board_res.append(tmp_board_state + tmp_board.return_int_board() + [tmp_turn] + [next_turn_num])
            if next_turn_num == -1:
                possible_len_list.append(len(tmp_board.possible_notgomi_move) )
            else:
                #相手のターンでないなら相手の着手可能数は0
                possible_len_list.append(0)

            #一手打つ時の最大着手可能数を調べる
            if next_turn_num == -1 and max_possible<len(tmp_board.possible_notgomi_move):
                max_possible = len(tmp_board.possible_notgomi_move)
                

            tmp_board.back()

        possible_best_res = []
        tmp_min = 999999

        #相手の最大着手可能数を１とした着手可能数を追加
        #基本的には0に近いほうがいい手
        for i,p in enumerate(possible_len_list):
            
            board_res.append(tmp_board_res[i] + [p/max_possible])

            if p<tmp_min:
                possible_best_res = [valid_moves[i]]
                tmp_min = p
            elif p == tmp_min:
                possible_best_res.append(valid_moves[i])
        
        
        return board_res
    

    def calculate_reward(self,action,before_board,possible_best_res):
        #盤面の評価を行う関数。
        # 打ったあとに通る。
        #学習中のモデルのみがここを呼び出す
        res = []
        max = -1



        res_reward = 0

        if self.game.game_end:
            
            if self.game.count_turn_stones() < self.game.count_not_turn_stones():
                return self.magic_numbers.lose_reward,0.0
            else:
                return self.magic_numbers.win_reward,0.0
        else:
            res_reward,before_reward = self.reward_kun.check_reward(self.game,before_board.turn)

            if possible_best_res and not action in possible_best_res:
                res_reward += self.magic_numbers.possible_num_best_reward
            #res_reward = 0.0
            
        
        return res_reward,before_reward

        


