

import tensorflow as tf
import numpy as np

class DualNetworkAgent:
    def __init__(self, state_size, action_size,load_file_pass = None):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.85  # discount factor
        self.other_gamma = 0.8

        self.learning_rate = 1e-4
        if load_file_pass is None:
            self.model = self.build_model()
        else:
            self.model = tf.keras.models.load_model(load_file_pass)


            
        



    def build_model(self):
        '''
        input_layer = tf.keras.layers.Input(shape=(self.state_size,))
        common_dense = tf.keras.layers.Dense(128, activation='relu')(input_layer)
        common_dense = tf.keras.layers.Dense(128, activation='relu')(common_dense)

        # Value head
        value_head = tf.keras.layers.Dense(64, activation='relu')(common_dense)
        value_output = tf.keras.layers.Dense(1, activation='tanh', name='value_output')(value_head)  # 名前を追加

        
        # Policy head
        policy_head = tf.keras.layers.Dense(64, activation='relu')(common_dense)
        policy_output = tf.keras.layers.Dense(self.action_size, activation='softmax', name='policy_output')(policy_head)  # 名前を追加
       

        model = tf.keras.Model(inputs=input_layer, outputs=[value_output, policy_output])
        
        # カスタム損失関数を指定
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss={'value_output': 'mean_squared_error', 'policy_output': CustomMSE()},
            metrics={'policy_output': ['accuracy'], 'value_output': ['mean_squared_error']},
            loss_weights={'value_output': 0.5, 'policy_output': 0.5}
        )
        '''
        
        input_layer = tf.keras.layers.Input(self.state_size)
        common_dense = tf.keras.layers.Dense(1024, activation='relu')(input_layer)
        common_dense2 = tf.keras.layers.Dense(64, activation='relu')(common_dense)
        #common_dense3 = tf.keras.layers.Dense(512, activation='relu')(common_dense2)
        #common_dense4 = tf.keras.layers.Dense(256, activation='relu')(common_dense3)
        #common_dense5 = tf.keras.layers.Dense(128, activation='relu')(common_dense4)

        value_output = tf.keras.layers.Dense(1, activation='tanh', name='value_output')(common_dense2)  # 名前を追加
       

        model = tf.keras.Model(inputs=input_layer, outputs=value_output)


        # モデルのコンパイル
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                    loss='mean_squared_error',
                    metrics=['accuracy'])


        return model
    

    


class CustomMSE(tf.keras.losses.Loss):
    def __init__(self, regularization_factor=0.1, name="custom_mse"):
        super().__init__(name=name)
        self.regularization_factor = regularization_factor

    def call(self, y_true, y_pred):

        mask = y_pred / 100000000 + y_true
        #mask = y_true
        res = tf.square(y_true - mask)
        return tf.math.reduce_mean(res)





'''
class ReversiDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, states, policies, values, batch_size , moves):
        self.states = states
        self.policies = policies
        self.values = values
        self.batch_size = batch_size
        self.moves = moves

    def __len__(self):
        return (np.ceil(len(self.states) / float(self.batch_size))).astype(np.int64)
    
    def __getitem__(self, idx):
        
        #batch_x = self.states[idx * self.batch_size:(idx + 1) * self.batch_size]
        #batch_policies = self.policies[idx * self.batch_size:(idx + 1) * self.batch_size]
        #batch_values = self.values[idx * self.batch_size:(idx + 1) * self.batch_size]


        batch_x = self.states[idx]
        batch_policies = self.policies[idx]
        batch_values = self.values[idx]

        

        batch_start = idx * self.batch_size
        batch_end = min(batch_start + self.batch_size, len(self.states))
        batch_x = np.array(self.states[batch_start:batch_end])
        batch_policies = np.array(self.policies[batch_start:batch_end])
        batch_values = np.array(self.values[batch_start:batch_end])
        
        batch_mask = self.generate_masks()[batch_start:batch_end]


        # ここで各状態に対するマスクを生成
        #batch_mask = self.generate_masks()[idx]
       

        # モデルの出力が複数ある場合は、辞書形式で対応する出力にマッピング
        return {'value_output': batch_values, 'policy_output': batch_policies}

    def generate_masks(self):
        # ここで各状態に対するマスクを生成するロジックを実装
        # 例: 有効な着手可能位置に1, それ以外に0をセット

        # statesはバッチ内のゲームの状態を含むNumPy配列
        masks = np.zeros((len(self.moves), 64))  # 仮に64がアクションサイズ（盤面の位置数）
        for i, move in enumerate(self.moves):
            # ここで各stateに基づいて有効な着手位置を計算
            # 例としてランダムに有効な位置を選ぶ
            masks[i, move] = 1  # 有効な位置に対してマスクを1に設定
        return masks

'''