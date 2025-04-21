import math
import copy

class FlipPossibleSplitBoardMask:
    def __init__(self,maskdata,start_move,direction,mask_bit):
        self.maskdata = maskdata
        self.start_move = start_move
        self.direction = direction
        self.bit_maskdata = mask_bit

class FlipBuffer:
    def __init__(self):


        print('高速な盤面生成のための準備に入ります')
        self.target_buffer = []

        self.target_mask = []


        self.move_to_leftup =[]
        self.move_to_rightup =[]
        
        #任意のマスから一番端まで左上へ進めたときにたどり着くマスから何番目に位置するかを格納
        self.move_to_base_leftup=[]

        #任意のマスから一番端まで右上へ進めたときにたどり着くマスから何番目に位置するかを格納
        self.move_to_base_rightup=[]


        #左上から数えて端につくまでに何個石が存在するか
        self.stones_num_leftup=[8,7,6,5,4,3,2,1,
                                7,8,7,6,5,4,3,2,
                                6,7,8,7,6,5,4,3,
                                5,6,7,8,7,6,5,4,
                                4,5,6,7,8,7,6,5,
                                3,4,5,6,7,8,7,6,
                                2,3,4,5,6,7,8,7,
                                1,2,3,4,5,6,7,8]
        
        self.stones_num_right=[1,2,3,4,5,6,7,8,
                                2,3,4,5,6,7,8,7,
                                3,4,5,6,7,8,7,6,
                                4,5,6,7,8,7,6,5,
                                5,6,7,8,7,6,5,4,
                                6,7,8,7,6,5,4,3,
                                7,8,7,6,5,4,3,2,
                                8,7,6,5,4,3,2,1]
        '''
        #左上から数えて端につくまでに何個石が存在するか
        self.stones_num_leftup=[7,6,5,4,3,2,1,0,
                                6,5,4,3,2,1,0,1,
                                5,4,3,2,1,0,1,2,
                                4,3,2,1,0,1,2,3,
                                3,2,1,0,1,2,3,4,
                                2,1,0,1,2,3,4,5,
                                1,0,1,2,3,4,5,6,
                                0,1,2,3,4,5,6,7]


        self.stones_num_right=[1,2,3,4,5,6,7,8,
                                2,3,4,5,6,7,8,7,
                                3,4,5,6,7,8,7,6,
                                4,5,6,7,8,7,6,5,
                                5,6,7,8,7,6,5,4,
                                6,7,8,7,6,5,4,3,
                                7,8,7,6,5,4,3,2,
                                8,7,6,5,4,3,2,1]

                                '''
        #盤面からひっくり返すときのデータに整形するとき使う。
        self.maskdata = [[-1] * 64 for i in range(4)]
        
        
        #1bitの全通りをリストで格納 [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,　～ 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]までサイズ65535。
        self.base_stone_pattern = [[] for i in range(6)]
        
        #1bitの全通りを整数値で格納 0000 0000 0000 0000　～ 1111 1111 1111 1111までサイズ65535。
        self.base_stone_pattern_row = [[] for i in range(6)]

        self.base_flip_possible_pattern = [[[] for j in range(8)] for i in range(6)] #base_stone_patternのうち、0の位置に石を置いてひっくり返すことができるものだけが格納されたリスト。
        self.base_flip_possible_flip_mask = [[[] for j in range(8)] for i in range(6)]#ひっくり返る場所に1のbitが入る。
        for i in range(64):
            x = i%8
            y = math.floor(i/8)
            
            #任意のマスから一番端まで左上へ進めたときにたどり着くマスを格納
            '''
            move_to_leftup = 0
            if y-x<0:
                move_to_leftup = (y-x)*8
            else:
                move_to_leftup = x-y
            self.move_to_leftup.append(move_to_leftup)
            '''
            self.move_to_leftup = [0,1,2,3,4,5,6,7,
                                   8,0,1,2,3,4,5,6,
                                   16,8,0,1,2,3,4,5,
                                   24,16,8,0,1,2,3,4,
                                   32,24,16,8,0,1,2,3,
                                   40,32,24,16,8,0,1,2,
                                   48,40,32,24,16,8,0,1,
                                   56,48,40,32,24,16,8,0]
            

            #任意のマスから一番端まで右上へ進めたときにたどり着くマスを格納
            '''
            move_to_rightup = 7
            if y+x>7:
                move_to_rightup = (y-x)
            else:
                move_to_rightup = (7-y+x)*8
            self.move_to_rightup.append(move_to_rightup)
            '''
            self.move_to_rightup = [0,1,2,3,4,5,6,7,
                                    1,2,3,4,5,6,7,15,
                                    2,3,4,5,6,7,15,23,
                                    3,4,5,6,7,15,23,31,
                                    4,5,6,7,15,23,31,39,
                                    5,6,7,15,23,31,39,47,
                                    6,7,15,23,31,39,47,55,
                                    7,15,23,31,39,47,55,63]

            #任意のマスから一番端まで左上へ進めたときにたどり着くマスから何番目に位置するかを格納
            self.move_to_base_leftup=[0,0,0,0,0,0,0,0,
                                      0,1,1,1,1,1,1,1,
                                      0,1,2,2,2,2,2,2,
                                      0,1,2,3,3,3,3,3,
                                      0,1,2,3,4,4,4,4,
                                      0,1,2,3,4,5,5,5,
                                      0,1,2,3,4,5,6,6,
                                      0,1,2,3,4,5,6,7]                                      

            
            '''
            move_to_base_leftup = y
            
            if y>x:
                move_to_base_leftup = x
            self.move_to_base_leftup.append(move_to_base_leftup)
            '''
            #任意のマスから一番端まで右上へ進めたときにたどり着くマスから何番目に位置するかを格納

            self.move_to_base_rightup= [0,0,0,0,0,0,0,0,
                                        1,1,1,1,1,1,1,0,
                                        2,2,2,2,2,2,1,0,
                                        3,3,3,3,3,2,1,0,
                                        4,4,4,4,3,2,1,0,
                                        5,5,5,4,3,2,1,0,
                                        6,6,5,4,3,2,1,0,
                                        7,6,5,4,3,2,1,0]
            '''
            move_to_base_rightup = y
            if y>7-x:
                move_to_base_rightup = 7-x
            self.move_to_base_rightup.append(move_to_base_rightup)
            '''

        self.generate_mask()
        #0000 0000 0000 0000　～ 1111 1111 1111 1111まで代入。
        for dim in range(6):
            bit_length = 6+dim*2
            for i in range(2**bit_length):
                self.base_stone_pattern[dim].append(self.int_to_bit_list(i,bit_length))
                self.base_stone_pattern_row[dim].append(i)

        #基礎の３～８マスにおけるひっくり返し可能の全パターンを生成
        
        for dim , dim_index in zip([3,4,5,6,7,8],range(6)):
            bit_length = dim*2
            for move in range(dim):
                self.base_flip_possible_pattern[dim_index][move] = {}
                self.base_flip_possible_flip_mask[dim_index][move] = {}
                for data,row in zip(self.base_stone_pattern[dim_index],self.base_stone_pattern_row[dim_index]):
                    player = data[0 : dim]
                    oppenet = data[dim: dim*2]

                    player_bit = row>>dim
                    oppenet_bit = row%(2**dim)
                    

                    
                    #同じマスに黒と白が置かれている不可能な状態
                    if (player_bit & oppenet_bit)!=0:
                        continue

                    #置く場所に石が存在する時点で置くことすらできないので帰宅
                    if player[move]==1 or oppenet[move]==1:
                        continue
                        
                    tmp_mask = [0]*dim #一方向にのみ使う ひっくり返せる場所に1
                    mask=[]
                    possible_flag = False

                    #xマイナス方向にチェック
                    #範囲外チェック
                    #お隣が相手の石でないならひっくり返せないので帰宅
                    if 0<move-1 and (player[move-1]==0 and oppenet[move-1]==1):

                        count = 1
                        #お隣の相手の石が途切れるまで続く
                        while(True):
                            move_i = move-count
                            if move_i<0:
                                break
                            
                            #ひっくり返せるときのためにmaskのbitを立て続ける
                            tmp_mask[move_i]=1

                            #自分の石に到達したのでひっくり返せると判断
                            if player[move_i]==1:
                                tmp_mask[move_i]=0
                                mask = copy.deepcopy(tmp_mask)
                                possible_flag = True
                                break

                            #相手の石が途切れたのでbreak
                            if oppenet[move_i]==0:
                                break

                            count+=1


                    #xプラス方向にチェック
                    #範囲外チェック
                    #お隣が相手の石でないならひっくり返せないので帰宅

                    tmp_mask = [0]*dim #一方向にのみ使う ひっくり返せる場所に1
                    if move+1<dim and (player[move+1]==0 and oppenet[move+1]==1):

                        count = 1
                        #お隣の相手の石が途切れるまで続く
                        while(True):
                            move_i = move+count
                            if dim<=move_i:
                                break
                            
                            #ひっくり返せるときのためにmaskのbitを立て続ける
                            tmp_mask[move_i]=1

                            #自分の石に到達したのでひっくり返せると判断
                            if player[move_i]==1:
                                tmp_mask[move_i]=0

                                if possible_flag:
                                    #すでにひっくり返すマスクが入っているとき
                                    mask = [d + tmp for d,tmp in zip(mask,tmp_mask)]
                                else:
                                    #はじめての代入
                                    mask = copy.deepcopy(tmp_mask)
                                    possible_flag=True

                                
                                break

                            #相手の石が途切れたのでbreak
                            if oppenet[move_i]==0:
                                break

                            count+=1

                    if len(mask)!=0:
                        self.base_flip_possible_flip_mask[dim_index][move][row] = mask
                        self.base_flip_possible_pattern[dim_index][move][row] = data


                    '''
                    for x in [-1,1]:#左右を考慮しないといけない

                        #範囲外チェック
                        if move+x<0 or dim<=move+x:
                            continue

                        #お隣が相手の石でないならひっくり返せないので帰宅
                        if player[move+x]==1 or oppenet[move+x]==0:
                            continue
                        
                        
                        if possible_flag:
                            #1週目でひっくり返せることが確定
                            #ひっくり返すデータとしてmaskに代入
                            mask = copy.deepcopy(tmp_mask)
                            possible_flag = False

                            #tmp_maskの内容を消す
                            tmp_mask = [0]*dim

                       
                        tmp_mask[move+x] = 1

                        count = 2

                        
                        #お隣の相手の石が途切れるまで続く
                        while(True):
                            move_i = move+(x*count)
                            if move_i<0 or dim<=move_i:
                                break
                            
                            #ひっくり返せるときのためにmaskのbitを立て続ける
                            tmp_mask[move_i]=1

                            #自分の石に到達したのでひっくり返せると判断
                            if player[move_i]==1:
                                possible_flag = True
                                tmp_mask[move_i]=0
                                break

                            #相手の石が途切れたのでbreak
                            if oppenet[move_i]==0:
                                break

                            count+=1

                    #一方向でも置けるならTrue
                    if len(mask)!=0 or possible_flag:
                        self.base_flip_possible_pattern[dim_index][move][row] = data
                        
                        #1回目はひっくり返せない場合
                        if len(mask)==0:
                            #空っぽのリスト作成
                            mask = [0]*dim

                        #2回目の方向でひっくり返せるとわかった、または1回目と2回目両方でひっくり返せるとわかったのでmask登録
                        if possible_flag:
                            #tmp_maskの内容をmaskに追加
                            mask = [mask[i] + tmp_mask[i] for i in range(dim)]
                        
                        self.base_flip_possible_flip_mask[dim_index][move][row] = mask


                    #この場所はおけるので登録

                '''
                    

        #最終的なひっくり返し可能かどうかのmaskを生成

        self.main_flip_possible_pattern =  [[{} for _ in range(4)] for _ in range(64)]
        self.main_flip_possible_flip_mask =  [[{} for _ in range(4)] for _ in range(64)]

        for move in range(64):
            for d,d_count in zip([1,8,9,7],range(4)):


                #各方角の端っこを取得
                n = -1
                if d_count==0:
                    n = math.floor(move/8)*8
                    small_move = move%8
                    dim = 8
                if d_count==1:
                    n = move%8
                    small_move = math.floor(move/8)
                    dim = 8
                if d_count==2:
                    n = self.move_to_leftup[move]
                    small_move = self.move_to_base_leftup[move]
                    dim = self.stones_num_leftup[move]
                if d_count==3:
                    n = self.move_to_rightup[move]
                    small_move = self.move_to_base_rightup[move]
                    dim = self.stones_num_right[move]

                dim_index = dim - 3
                if dim<3 or len(self.base_flip_possible_pattern[dim_index][small_move])==0:
                    continue

                for (pos_key,pos_value),(flp_key,flp_value) in zip(self.base_flip_possible_pattern[dim_index][small_move].items(),self.base_flip_possible_flip_mask[dim_index][small_move].items()):
                    res_possible = 0
                    res_flip=0
                    #tmp_debug = [[0] * 8 for i in range(8)]

                    #1盤面の64bitを生成
                    for color in [0,1]:
                        for count in range(dim):
                            add_index = n + d * count
                            #if 63<add_index:
                                #break
                            res_flip |= flp_value[count] << add_index
                            res_possible |= pos_value[count+color*dim] << (add_index + 64*color)

                            #if color==0:
                            #    tmp_debug[math.floor(add_index/8)][add_index%8] = pos_value[count+color*dim]
                            #else:
                            #    tmp_debug[math.floor(add_index/8)][add_index%8] -= pos_value[count+color*dim]


                    self.main_flip_possible_flip_mask[move][d_count][res_possible] = self.resize_bit(res_flip,64)
                    self.main_flip_possible_pattern[move][d_count][res_possible] = True

        '''
        for move in range(64):
            for d,d_count in zip([1,8,9,7],range(4)):


                #各方角の端っこを取得
                n = -1
                if d_count==0:
                    n = math.floor(move/8)*8
                    small_move = move%8
                    dim = 8
                if d_count==1:
                    n = move%8
                    small_move = math.floor(move/8)
                    dim = 8
                if d_count==2:
                    n = self.move_to_leftup[move]
                    small_move = self.move_to_base_leftup[move]
                    dim = self.stones_num_leftup[move]
                if d_count==3:
                    n = self.move_to_rightup[move]
                    small_move = self.move_to_base_rightup[move]
                    dim = self.stones_num_right[move]

                dim_index = dim - 3
                if dim<3 or len(self.base_flip_possible_pattern[dim_index][small_move])==0:
                    continue

                for key,value in self.base_flip_possible_pattern[dim_index][small_move].items():
                    res_possible = 0
                    
                    tmp_debug = [[0] * 8 for i in range(8)]

                    #1盤面の64bitを生成
                    for color in [0,1]:
                        for count in range(dim):
                            add_index = n + d * count
                            #if 63<add_index:
                                #break

                            res_possible |= value[count+color*dim] << (add_index + 64*color)

                            if color==0:
                                tmp_debug[math.floor(add_index/8)][add_index%8] = value[count+color*dim]
                            else:
                                tmp_debug[math.floor(add_index/8)][add_index%8] -= value[count+color*dim]



                    self.main_flip_possible_pattern[move][d_count][res_possible] = tmp_debug
        
         #最終的なひっくり返す場所を示すマスクの作成
        self.main_flip_possible_flip_mask =  [[{} for _ in range(4)] for _ in range(64)]
        for move in range(64):
            for d,d_count in zip([1,8,9,7],range(4)):


                #各方角の端っこを取得
                n = -1
                if d_count==0:
                    n = math.floor(move/8)*8
                    small_move = move%8
                    dim = 8
                if d_count==1:
                    n = move%8
                    small_move = math.floor(move/8)
                    dim = 8
                if d_count==2:
                    n = self.move_to_leftup[move]
                    small_move = self.move_to_base_leftup[move]
                    dim = self.stones_num_leftup[move]
                if d_count==3:
                    n = self.move_to_rightup[move]
                    small_move = self.move_to_base_rightup[move]
                    dim = self.stones_num_right[move]

                dim_index = dim - 3
                if dim<3 or len(self.base_flip_possible_pattern[dim_index][small_move])==0:
                    continue

                for key,value in self.base_flip_possible_flip_mask[dim_index][small_move].items():
                    res_flip = 0
                    
                    tmp_debug = [[0] * 8 for i in range(8)]

                    #1盤面の64bitを生成

                    for count in range(dim):
                        add_index = n + d * count
                        #if 63<add_index:
                            #break

                        res_flip |= value[count] << (add_index)

                        tmp_debug[math.floor(add_index/8)][add_index%8] = value[count]




                    self.main_flip_possible_flip_mask[move][d_count][key] = self.resize_bit(res_flip,128)
        '''

        print('高速な盤面生成の準備完了')
                            

        
    def int_to_bit_list(self, n: int, bit_length: int) -> list:
        # 整数を2進数に変換し、指定されたビット数になるように左側にゼロパディング
        bit_str = f"{n:0{bit_length}b}"
        # 文字列を1文字ずつリストに変換し、各要素を整数にする
        return [int(bit) for bit in bit_str]

    def resize_bit(self,value,size:int):
        all_1 = 1<<(size+1)
        all_1 -=1


        return value & all_1

            

        

    
    def generate_mask(self):
        for move in range(64):
            #既にデータを作成済みなので何もしない
            #if isinstance(self.maskdata[0][move],list):
            #    return

            result_list = []
            directions = [1, 8, 9, 7] # 8方向
            
            count = 0

            for d,d_count in zip(directions,range(4)):
                res = [0]*64
                mask = 0
                if d==1:
                    n = math.floor(move/8)*8
                elif d == 8:
                    n = (move%8)
                elif d==9:
                    n = self.move_to_leftup[move]
                else:
                    n = self.move_to_rightup[move]
                start_n = n

                for count in range(8):
                    res[n] = 1
                    mask |= (1<<n)

                    if move==0 and d==7 : break
                    if count!=0 and  (d == 1 or d == 7) and n % 8 == 0: break
                    if count!=0 and d == 9 and n % 8 == 7: break
                    n += d
                    if not (0 <= n < 64): break  # 盤面外に出たかのチェック
                    


                mask = mask | (mask<<64)
                self.maskdata[d_count][move] = FlipPossibleSplitBoardMask(res,start_n,d,mask)#ディープコピーされるかあやしいので監視する
                count+=1





       


    def get_possible(self,move,plyer_board,oppenet_board):

        target = plyer_board | (oppenet_board<<64)
        

        for i in range(4):
            search = target & self.maskdata[i][move].bit_maskdata
            if search in self.main_flip_possible_pattern[move][i]:
                return True

        return False
    
    def get_flip_mask(self,move,plyer_board,oppenet_board):

        target = plyer_board | (oppenet_board<<64)
        res_mask = 0

        for i in range(4):
            search = target & self.maskdata[i][move].bit_maskdata
            value = self.main_flip_possible_flip_mask[move][i].get(search)
            if value is not None:
                res_mask |= value

                
                        

        return res_mask
    
    def get_possible_direction(self,move,plyer_board,oppenet_board):
        target = plyer_board | (oppenet_board<<64)
        
        res = [False] * 4
        for i in range(4):
            search = target & self.maskdata[i][move].bit_maskdata
            res[i] = search in self.main_flip_possible_pattern[move][i]
            

        return res




#test = FlipBuffer()

pass