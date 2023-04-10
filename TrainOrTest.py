from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten, Reshape, Input
from tensorflow.keras.optimizers import Adam
Adam._name = 'hey'

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from tensorflow.keras.callbacks import LambdaCallback
from tensorflow.keras.models import Model

import datetime
import os

import numpy as np
import GameEnv
    

# 先初始化強化學習環境    
env = GameEnv.CustomEnv()

# 取得狀態空間和行動空間，用以輸入模型(狀態)和輸出結果(動作)
states = env.observation_space.shape
actions = env.action_space.n


# 建立模型架構，輸入的shape為 (None,2) ; 輸出的為 (None,3)
def build_model(states, actions):
    input_layer = Input(shape=(None,) + states)
    x = Dense(24, activation='relu')(input_layer)
    x = Dense(24, activation='relu')(x)
    x = Dense(actions, activation='linear')(x)
    output_layer = Reshape((actions,))(x)
    model = Model(inputs=input_layer, outputs=output_layer)
    return model


# 建立agent
# model: 指定用於進行 Q 學習的神經網路模型。
# memory: 指定用於存儲過去的狀態、動作、獎勵等資訊的記憶體。
# policy: 指定用於選擇動作的策略。在這個例子中，使用了 BoltzmannQPolicy，該策略基於 Q 值進行機率性的選擇。
# nb_actions: 指定可執行的動作數量。
# nb_steps_warmup: 指定在開始進行訓練之前隨機選擇動作的步數。目前設定為 100，表示前 100 步的動作會完全隨機選擇，之後才會開始根據策略選擇動作。
# target_model_update: 指定更新目標模型的頻率。目前設定為 1e-2，表示每次訓練更新時，目標模型的權重會以 0.01 的速率進行更新。
def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, 
                  nb_actions=actions, nb_steps_warmup=100, target_model_update=1e-2)
    return dqn





current_dir = os.path.dirname(os.path.abspath(__file__))

option = input('輸入1為訓練模型及測試，輸入2為載入最新模型以測試')
if option == '1':
    #del model

    model = build_model(states, actions)
    model.summary()
    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-2), metrics=['mae'])
    # 定義LambdaCallback
    custom_monitor_callback = LambdaCallback(on_epoch_end=lambda epoch, logs: env.custom_monitor_function(model))

    # 訓練模型並使用callbacks參數
    dqn.fit(env, nb_steps=60000, visualize=False, verbose=1, callbacks=[custom_monitor_callback])

    now = datetime.datetime.now()
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    model.save(os.path.join(current_dir, f'{current_time}_model.h5'))
    results = dqn.test(env, nb_episodes=150, visualize=False)
    print(np.mean(results.history['episode_reward']))
elif option == '2':
    files = os.listdir(current_dir)
    new = ''
    for file in files:
        if file.endswith(".h5"): 
            if file > new:
                new = file
    file_path = os.path.join(current_dir, new)
    # 載入模型權重
    #model.load_weights('model.h5')

    # 載入完整模型
    loaded_model = load_model(file_path)
    dqn = build_agent(loaded_model, actions)
    dqn.compile(Adam(lr=1e-2), metrics=['mae'])
    print('已載入模型: ',new)
    results = dqn.test(env, nb_episodes=150, visualize=False)
    print(np.mean(results.history['episode_reward']))