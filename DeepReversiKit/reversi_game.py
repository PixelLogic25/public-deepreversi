
import numpy as np
import copy


try:
    import flip_buffer
except:
    import DeepReversiKit.flip_buffer

class ReversiBoardHistoryData:
    def __init__(self,reversi_game):
        self.player_board = reversi_game.player_board
        self.opponent_board = reversi_game.opponent_board
        self.turn = reversi_game.turn
        #self.pass_count = reversi_game.pass_count
        self.possible_move = reversi_game.possible_move
        self.game_end = reversi_game.game_end
        #self.turn_count = reversi_game.turn_count  
        self.turn_num = reversi_game.turn_num
        



class History:


    def __init__(self):
        self.count = 0
        self.history = []

    def add(self,rg):
        if self.count+1<len(self.history):
            del self.history[self.count+1:]
        self.history.append(ReversiBoardHistoryData(rg))
        self.count = len(self.history)-1
    
    def back(self):
        if len(self.history)<=0:
            return None
        
        if self.count<=0:
            return None
        
        self.count -= 1    

        return self.history[self.count]


    def foward(self):

        
        if self.count>=len(self.history)-1:
            return None
        self.count += 1


        return self.history[self.count]
    
    def deepcopy(self):
        res = History()
        res.count = self.count
        res.history = self.history

        return res 
    

class ReversiGame:

    def __init__(self, board=None , none_possible_move = True , none_history = True , player=None , opponent=None , turn = None , flip_stone_buffer = None) -> None:

        self.history = None
        self.possible_move =[]
        self.possible_notgomi_move = []

        self.gomi_move_list = [1,6,8,9,14,15,48,49,54,55,57,62]

        self.game_end = False
        #self.turn_count = 0
        self.turn_num=0

        self.flip_stone_buffer = flip_stone_buffer

        if board is None:
            if player is None:
                self.player_board = int(0x0000000810000000)  # プレイヤーの初期配置
                self.opponent_board = int(0x0000001008000000)  # 相手の初期配置
                self.turn = True
                #self.turn_count = 0
                #self.pass_count = 0
                self.update_possible_moves()
                
                self.history = History()
                self.history.add(self)

                self.turn_num=0
            else:
                self.player_board = player
                self.opponent_board = opponent
                self.turn = turn
                if not none_possible_move:
                    self.update_possible_moves()

                

            

        else:
            self.player_board = board.player_board  # プレイヤーの初期配置
            self.opponent_board = board.opponent_board # 相手の初期配置
            self.turn = board.turn
            #self.pass_count = board.pass_count
            self.game_end = board.game_end
            self.turn_num=board.turn_num
            #self.turn_count = 0

            if not none_history:
                self.history = board.history.deepcopy()
                #self.turn_count = board.turn_count
            else:
                self.history = History()
                self.history.add(self)
                #self.turn_count+=1

            if not none_possible_move:
                
                self.update_possible_moves()

    def recoverry(self,historyData):
        self.player_board = historyData.player_board
        self.opponent_board = historyData.opponent_board
        self.turn = historyData.turn
        self.possible_move = historyData.possible_move
        self.game_end = historyData.game_end
        self.turn_num=historyData.turn_num
        #self.turn_count = historyData.turn_count  


    def reset(self):
        self.player_board = int(0x0000000810000000)  # プレイヤーの初期配置
        self.opponent_board = int(0x0000001008000000)  # 相手の初期配置
        self.turn = True
        #self.pass_count = 0
        self.update_possible_moves()
        
        #self.turn_count = 0
        self.game_end = False

        self.history = History()
        self.history.add(self)

        self.turn_num = 0


    def count_turn_stones(self):
        """盤面上の黒石と白石の数をそれぞれカウントして返すメソッド"""
        now_turn_player_stone = bin(self.player_board).count('1')
        return now_turn_player_stone
    
    def count_not_turn_stones(self):

        now_not_turn_player_stone = bin(self.opponent_board).count('1')
        return now_not_turn_player_stone

        

    def return_str_board(self):


        result_int = self.return_int_board()

        return ",".join(str(num) for num in result_int)

    def return_int_board(self):

        np1 = self.convert_int_to_bitlist(self.player_board)
        np2 = self.convert_int_to_bitlist(self.opponent_board)

        if self.turn :
            result_int_list = np2 - np1
        else:
            result_int_list = np1 - np2

        '''
        int_array1 = [(self.player_board  >> i) & 1 for i in range(64)]
        int_array2 = [(self.opponent_board  >> i) & 1 for i in range(64)]

        result_int = []
        if self.turn :
            result_int = [a - b for a, b in zip(int_array2, int_array1)]
        else:
            result_int = [a - b for a, b in zip(int_array1, int_array2)]
        '''

        return result_int_list.tolist()
    #bitを格納する整数型の変数を0と1のリストに変換する
    def convert_int_to_bitlist(self,int_value):
        res = np.unpackbits(
            np.array([int_value], dtype=np.uint64).byteswap().view(np.uint8)
        )[::-1]

        return res.astype(np.int8)

    def generate_by_str(self,str_board):
        list_str = str_board.split(',')

        
        int_array1 = [1 if list_str[i] == '-1' else 0 for i in range(64)]
        int_array2 = [1 if list_str[i] == '1' else 0 for i in range(64)]
            
        bit1 =0
        bit2 =0
        
        for i in range(64):
            reverse = 63 - i
            bit1 += int_array1[reverse] * (2 ** i)
            bit2 += int_array2[reverse] * (2 ** i)

        self.history = []

        self.game_end = False


        self.player_board = bit1  # プレイヤーの初期配置
        self.opponent_board = bit2  # 相手の初期配置
        self.turn = True
        #self.pass_count = 0


        self.update_possible_moves()

        #self.print_board()

        return
    def print_board(self):
        board_representation = self.player_board | self.opponent_board  # 総合盤面
        for y in range(8):
            for x in range(8):
                if self.player_board & (1 << (y * 8 + x)):
                    if self.turn:
                        print("X", end="")
                    else:
                        print("O", end="")
                elif self.opponent_board & (1 << (y * 8 + x)):
                    if self.turn:
                        print("O", end="")
                    else:
                        print("X", end="")
                else:
                    print(".", end="")  # 空マス
            print()
        print()

    def print_board_row(self,board):
        
        for y in range(8):
            for x in range(8):
                if board & (1 << (y * 8 + x)):
                    print("●", end="")
                else:
                    print("○", end="")
            print()
        print()

    def flip_stones(self, move):

        flip_mask = 0

        if self.flip_stone_buffer is not None:
            flip_mask = self.flip_stone_buffer.get_flip_mask(move,self.player_board,self.opponent_board)

            

                    

            return flip_mask



        # マスクを用いて各方向の確認と石をひっくり返す処理を行う
        directions = [1, -1, 8, -8, 7, -7, 9, -9] # 8方向
        

        for d in directions:
            mask = 0
            n = move
            while True:
                if (d == -1 or d == 7 or d==-9 ) and n % 8 == 0: break
                if (d == 1 or d == -7 or d==9 )  and n % 8 == 7: break
                n += d
                if not (0 <= n < 64): break  # 盤面外に出たかのチェック
                if (self.opponent_board & (1 << n)) == 0: break  # 相手の石ではない場合は停止

                mask |= (1 << n)
        
            # 自分の石に到達したかのチェック
            if 0 <= n < 64 and (self.player_board & (1 << n)) != 0:
                flip_mask |= mask  # 相手の石をひっくり返す

                

        return flip_mask

    #
    def possible_flip_stones(self,move):
        if self.flip_stone_buffer is not None:
            return self.flip_stone_buffer.get_possible(move,self.player_board,self.opponent_board)


        # マスクを用いて各方向の確認と石をひっくり返す処理を行う
        directions = [1, -1, 8, -8, 7, -7, 9, -9] # 8方向

        for d in directions:
            n = move
            flag = False
            while True:
                if (d == -1 or d == 7 or d==-9 ) and n % 8 == 0: break
                if (d == 1 or d == -7 or d==9 )  and n % 8 == 7: break
                n += d
                if not (0 <= n < 64): break  # 盤面外に出たかのチェック
                if (self.opponent_board & (1 << n)) == 0: break  # 相手の石ではない場合は停止
                flag = True
                
        
            # 自分の石に到達したかのチェック
            if flag and 0 <= n < 64 and (self.player_board & (1 << n)) != 0:
                return True

        return False
    def make_move(self, move):

        if 63<move :
            return ''
        flip_mask = self.flip_stones(move)

        # 石をひっくり返して新しい盤面を返す
        if flip_mask != 0:

            #今の状態の盤面をhistoryへ代入
            #if self.turn_count < len(self.history):
            #    del self.history[self.turn_count:]

            self.player_board ^= (1 << move) | flip_mask
            self.opponent_board ^= flip_mask
            
            self.change_turn()
            self.update_possible_moves()

            self.history.add(self)
            self.turn_num+=1

            #self.turn_count+=1

            
            if self.possible_move[0]==77:

                self.change_turn()
                self.update_possible_moves()
                self.turn_num+=1

                if self.possible_move[0]==77 :
                    self.game_end = True
                    return 'end'
                return ''


        return ''

    def change_turn(self):
        tmp = self.player_board
        self.player_board = self.opponent_board
        self.opponent_board = tmp

        self.turn = not(self.turn)



    def update_possible_moves(self):
        self.possible_move = []
        self.possible_notgomi_move = []
        player_board = int(self.player_board)
        opponent_board = int(self.opponent_board)
        
        # ビット演算
        empty_board = (~(player_board | opponent_board)) & 0xFFFFFFFFFFFFFFFF
        for move in range(64):  # 盤面上のすべてのマスをチェック
            if empty_board & (1 << move):#空きマスすべてに対して行う
                if self.possible_flip_stones(move):
                    self.possible_move.append(move)

                    if not move in self.gomi_move_list:
                        self.possible_notgomi_move.append(move)




        if len(self.possible_move)==0:
            self.possible_move = [77]#パスを意味する
            return


            
        return
    
    
    def valid_moves_total(self):


        return len(self.possible_move)

    def back(self):
        tmp = self.history.back()
        if not tmp==None:
            self.recoverry(tmp)
    def foward(self):
        tmp = self.history.foward()
        if not tmp==None:
            self.recoverry(tmp)

    def print_valid_moves(self):
        board = 0
        for move in self.possible_move:
            board |= (1 << move)
            print(move)
        
        self.print_board_row(board)