import numpy as np

class MemoryData:
    pass

class Memory:

    def __init__(self,gamma):

        self.multilist = []
        multi = 1.0
        for m in range(100):
            self.multilist.append(multi)
            multi *= gamma

        self.multilist = list(reversed(self.multilist))
        #self.multilist = np.array(self.multilist)

        self.reset()

    

    def reset(self):
        self.main_memory = []
        self.onegame_state = []
        self.onegame_rewards = []


    def add(self,state, reward,before_reward):
        if len(self.onegame_rewards)!=0:
            self.onegame_rewards[-1] += before_reward

        self.onegame_state.append(state)
        self.onegame_rewards.append(reward)


    def compile_onegame(self,gamma,other_gamma):
        last = self.onegame_rewards[len(self.onegame_rewards)-1]

        #a = list(reversed(self.onegame_rewards)) 

        '''
        #最後の値のみを伝達する
        game_end_reward = [last] * len(self.onegame_rewards)
        gamma_multi = self.multilist[len(self.multilist)-len(self.onegame_rewards):]
        self.onegame_rewards[len(self.onegame_rewards)-1] = 0.0

        tmp = list(zip(self.onegame_state, np.array(game_end_reward) * gamma_multi + self.onegame_rewards))

        '''
        #報酬ごとに伝達する
        
        multi = other_gamma
        res = [0]
        new = 0.0

        #勝ち負け以外の報酬を計算する
        for reward in reversed(self.onegame_rewards[:-1]):
            if not reward==0.0:
                multi = 1.0
                new = reward

            res.append(new * multi)

            
            multi *= other_gamma



        #勝ち負けの報酬を加える
        game_end_reward = [last] * len(self.onegame_rewards)
        gamma_multi = self.multilist[len(self.multilist)-len(self.onegame_rewards):]
        self.onegame_rewards[len(self.onegame_rewards)-1] = 0.0

        #tmp = list(zip(self.onegame_state, np.array(game_end_reward) * gamma_multi))
        tmp = np.array(game_end_reward) * gamma_multi

        #self.main_memory += tmp
        self.main_memory += list(zip(self.onegame_state,list(reversed(res)) + tmp))

        self.onegame_state = []
        self.onegame_rewards = []
        pass

    def insert_last_reward(self,value):
        last = len(self.onegame_rewards) -1
        self.onegame_rewards[last] = value

        


