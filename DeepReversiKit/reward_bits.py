

class Reward_bits:
    def __init__(self) -> None:
        

        
        self.target_reward_bitboard =[]

        self.magic_number_2_65 = 2 ** 65

        
        #X打ち
        x_reward = -1.0/5
        c_reward = -0.4/5
        gomi_c_reward = -0.6/5

        hen6_reward = 0.1/5
        hen4_reward = 0.05/5

        o_reward = 0.1/5

        o_line_reward = 0.01/5

        x_turn_num = 48
        c_turn_num = 48
        hen_turn_num = 40
        kado_turn_num = 60
        o_line_turn_num = 64


        #self.generate_rewardmap(条件に該当する自分の石の位置,条件から除外する空きマス,条件から除外する自分の石,条件から除外する相手の石)
        #X打ちの設定0
        self.target_reward_bitboard.append(self.generate_rewardmap([9],[0],[],[],x_reward,x_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([14],[7],[],[],x_reward,x_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([49],[56],[],[],x_reward,x_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([54],[63],[],[],x_reward,x_turn_num))

        #C打ちの設定4
        self.target_reward_bitboard.append(self.generate_rewardmap([1],[0],[2,3,4,5,6],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([6],[7],[1,2,3,4,5],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([8],[0],[16,24,32,40,48],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([15],[7],[23,31,39,47,55],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([48],[56],[8,16,24,32,40],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([55],[63],[15,23,31,39,47],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([57],[56],[58,59,60,61,62],[],c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([62],[63],[57,58,59,60,61],[],c_reward,c_turn_num))

        #辺４の設定12
        self.target_reward_bitboard.append(self.generate_rewardmap([2,3,4,5],[0,1,6,7],[],[],hen4_reward,hen_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([16,24,32,40],[0,8,48,56],[],[],hen4_reward,hen_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([23,31,39,47],[7,15,55,63],[],[],hen4_reward,hen_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([58,59,60,61],[56,57,62,63],[],[],hen4_reward,hen_turn_num))

        #辺6の設定16
        self.target_reward_bitboard.append(self.generate_rewardmap([1,2,3,4,5,6],[0,7],[],[],hen6_reward,hen_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([8,16,24,32,40,48],[0,56],[],[],hen6_reward,hen_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([15,23,31,39,47,55],[7,63],[],[],hen6_reward,hen_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([57,58,59,60,61,62],[56,63],[],[],hen6_reward,hen_turn_num))

        #角ゲットの設定20
        self.target_reward_bitboard.append(self.generate_rewardmap([0],[],[],[],o_reward,kado_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([7],[],[],[],o_reward,kado_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([56],[],[],[],o_reward,kado_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([63],[],[],[],o_reward,kado_turn_num))


        #絶対打ってはいけないC打ちの設定24
        self.target_reward_bitboard.append(self.generate_rewardmap([1],[0],[2,3,4,5,6],[2],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([6],[7],[1,2,3,4,5],[5],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([8],[0],[16,24,32,40,48],[16],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([15],[7],[23,31,39,47,55],[23],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([48],[56],[8,16,24,32,40],[40],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([55],[63],[15,23,31,39,47],[47],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([57],[56],[58,59,60,61,62],[58],gomi_c_reward,c_turn_num))
        self.target_reward_bitboard.append(self.generate_rewardmap([62],[63],[57,58,59,60,61],[61],gomi_c_reward,c_turn_num))

        '''
        #辺の確定石の設定32

        '''
        '''
        #self.generate_rewardmap(条件に該当する自分の石の位置,条件から除外する空きマス,条件から除外する自分の石,条件から除外する相手の石)
        self.generate_rewardmap([0,1,2,3,4,5,6,7],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,1,2,3,4,5,6],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,1,2,3,4,5],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,1,2,3,4],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,1,2,3],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,1,2],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,1],[],[],[],o_line_reward,o_line_turn_num)

        #39
        self.generate_rewardmap([7,6,5,4,3,2,1],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,6,5,4,3,2],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,6,5,4,3],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,6,5,4],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,6,5],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,6],[],[],[],o_line_reward,o_line_turn_num)


        #45
        self.generate_rewardmap([7,15,23,31,39,47,55,63],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,15,23,31,39,47,55],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,15,23,31,39,47],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,15,23,31,39],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,15,23,31],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,15,23],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([7,15],[],[],[],o_line_reward,o_line_turn_num)
        
        #52
        self.generate_rewardmap([63,55,47,39,31,23,15],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,55,47,39,31,23],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,55,47,39,31],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,55,47,39],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,55,47],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,55],[],[],[],o_line_reward,o_line_turn_num)
        
        #58
        self.generate_rewardmap([0,8,16,24,32,40,48,56],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,8,16,24,32,40,48],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,8,16,24,32,40],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,8,16,24,32],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,8,16,24],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,8,16],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([0,8],[],[],[],o_line_reward,o_line_turn_num)
        
        #65
        self.generate_rewardmap([56,48,40,32,24,16,8],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,48,40,32,24,16],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,48,40,32,24],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,48,40,32],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,48,40],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,48],[],[],[],o_line_reward,o_line_turn_num)

        #71
        self.generate_rewardmap([56,57,58,59,60,61,62,63],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,57,58,59,60,61,62],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,57,58,59,60,61],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,57,58,59,60],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,57,58,59],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,57,58],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([56,57],[],[],[],o_line_reward,o_line_turn_num)
        
        #78
        self.generate_rewardmap([63,62,61,60,59,58,57],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,62,61,60,59,58],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,62,61,60,59],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,62,61,60],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,62,61],[],[],[],o_line_reward,o_line_turn_num)
        self.generate_rewardmap([63,62],[],[],[],o_line_reward,o_line_turn_num)
        '''
        



    def reset(self):
        self.reward_fire_flag = [True] * len(self.target_reward_bitboard)
        self.before_reward_fire_flag = [True] * len(self.target_reward_bitboard)

    #def registor(self,target:list,jyogai:list,reward,turn_num):
    def check_reward(self,game,ai_turn):

        #return 0.0,0.0#勝ち負け以外の報酬を0にする
    
    
        #turn:trueならplayer_boardを対象に調べる
        #falseなら opponent_boardを対象に調べる

        target_mystone_bit = 0
        target_oppstone_bit=0



        empty_point_bit = ~(game.player_board | game.opponent_board)
        if game.turn:
            black = game.player_board
            white = game.opponent_board
        else:
            black = game.opponent_board
            white = game.player_board

        if ai_turn:
            target_mystone_bit = black
            target_oppstone_bit = white
        else:
            target_mystone_bit = white
            target_oppstone_bit = black

        now_reward = 0.0
        before_reward = 0.0 #前の盤面に対する報酬 
        for i,(t,empty_point,jyogai_mystone,gaitou_oppstone,reward,turn_num) in enumerate(self.target_reward_bitboard):
            #t                  :自分の石がこの場所にある時に該当
            #empty_point        :場空きマスがこの場所にある時に該当
            #jyogai_mystone     : 自分の石がこの場所にある時は除外
            #gaitou_oppstone    :相手の石がこの場所にある時は除外
            if turn_num<=game.turn_num:
                continue
            
            #一度得た報酬は得たときからゲーム終了まで持続させる
            if not self.reward_fire_flag[i]:
                #除外条件に合うときは、たとえ以前にもらえていた報酬であっても報酬0で帰宅
                if (empty_point_bit & empty_point == empty_point and #target_mystone==tはここでは必ずTrue
                    (gaitou_oppstone==self.magic_number_2_65 or 
                     not(target_oppstone_bit & gaitou_oppstone == 0)) and 
                     not(target_mystone_bit & jyogai_mystone == jyogai_mystone)):
                    continue
                now_reward += reward
                continue


            #一度得た報酬は得たときからゲーム終了まで持続させる（相手の石の報酬）
            if not self.before_reward_fire_flag[i]:
                #除外条件に合うときは、たとえ以前にもらえていた報酬であっても報酬0で帰宅
                if (empty_point_bit & empty_point == empty_point and 
                        (gaitou_oppstone==self.magic_number_2_65 or 
                            not(target_mystone_bit & gaitou_oppstone == 0)) and 
                            not(target_oppstone_bit & jyogai_mystone == jyogai_mystone)):
                    
                    res=reward
                    if res<0:
                        res /=10 
                    
                    before_reward -= res
                    continue
            
            #現状の盤面に対する報酬を計算
            if (target_mystone_bit & t == t and 
                    empty_point_bit & empty_point == empty_point and 
                    (gaitou_oppstone==self.magic_number_2_65 or 
                     not(target_oppstone_bit & gaitou_oppstone == 0)) and 
                     not(target_mystone_bit & jyogai_mystone == jyogai_mystone)):
                #print('X uti.')
                
                #game.print_board()
                self.reward_fire_flag[i] = False
                now_reward += reward

            #前の手に対する報酬を与える（相手の石が報酬を得るようなときは、こちらは逆の報酬を得る）
            if (target_oppstone_bit & t == t and 
                    empty_point_bit & empty_point == empty_point and 
                    (gaitou_oppstone==self.magic_number_2_65 or 
                     not(target_mystone_bit & gaitou_oppstone == 0)) and 
                     not(target_oppstone_bit & jyogai_mystone == jyogai_mystone)):
                #print('X uti.')
                
                #game.print_board()
                self.before_reward_fire_flag[i] = False

                res=reward
                if res<0:
                    res /=10 

                before_reward -= res #逆の報酬を与える
            
        return now_reward,before_reward


    def generate_rewardmap(self,target:list,jyogai_empty:list,jyogai_mystone:list,jyogai_oppstone:list,reward,turn_num):
        t = self.generate_bitboard(target)
        j = self.generate_bitboard(jyogai_empty)
        j2 = self.generate_bitboard(jyogai_mystone)
        j3 = self.generate_bitboard(jyogai_oppstone)

        return [t,j,j2,j3,reward,turn_num]


    
    def generate_bitboard(self,target_points:list):
        res_bit1 = 0

        if len(target_points) == 0:
            target_points = [65]
        for i in target_points:
            k = i
            res_bit1 |= 1<<k
        
        return res_bit1

