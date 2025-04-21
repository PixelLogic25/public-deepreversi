class MagicNumber:
    def __init__(self):

        self.win_reward = 0.0
        self.lose_reward = -1.0
        self.draw_reward = 0.0

        '''
        possible_num_best_reward：
        非推奨
        一番相手の置ける場所が少ない手を置いた時の報酬。
        どれだけ値を小さくしても毎手報酬として出てくるためものすごく影響する。
        勝ち負け考えず相手の打つ場所をなくそうことしか考えなくなる。要調整。
        '''
        self.possible_num_best_reward  = -1e-8 
        self.train_every_n_episodes = 100#エピソード回数がtrain_every_n_episodesごとに学習をする。
        return
    
