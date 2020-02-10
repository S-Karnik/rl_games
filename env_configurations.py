import networks 
import wrappers
import tr_helpers
import gym
import numpy as np

FLEX_PATH = '/home/viktor/Documents/rl/FlexRobotics'


class HCRewardEnv(gym.RewardWrapper):
    def __init__(self, env):
        gym.RewardWrapper.__init__(self, env)
        
        self.num_stops = 0
        self.stops_decay = 0
        self.max_stops = 30

    def reset(self, **kwargs):
        self.num_stops = 0
        self.stops_decay = 0
        return self.env.reset(**kwargs)

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        if self.num_stops > self.max_stops:
            print('too many stops!')
            reward = -100
            observation = self.reset()
            done = True
        return observation, self.reward(reward), done, info
    def reward(self, reward):
       # print('reward:', reward)
        '''
        if reward < 0.005:
            self.stops_decay = 0
            self.num_stops += 1
            #print('stops:', self.num_stops)
            return -0.1
        self.stops_decay += 1
        if self.stops_decay == self.max_stops:
            self.num_stops = 0
            self.stops_decay = 0
        '''
        return np.max([-10, reward])
class HCObsEnv(gym.ObservationWrapper):
    def __init__(self, env):
        gym.RewardWrapper.__init__(self, env)

    def observation(self, observation):
        obs = observation - [ 0.1193, -0.001 ,  0.0958, -0.0052, -0.629 , -0.01  ,  0.1604, -0.0205,
  0.7094,  0.6344,  0.0091,  0.1617, -0.0001,  0.7018,  0.4293,  0.3909,
  0.3776,  0.3662,  0.3722,  0.4043,  0.4497,  0.6033,  0.7825,  0.9575]

        obs = obs / [0.3528, 0.0501, 0.1561, 0.0531, 0.2936, 0.4599, 0.6598, 0.4978, 0.454 ,
 0.7168, 0.3419, 0.6492, 0.4548, 0.4575, 0.1024, 0.0716, 0.0918, 0.11  ,
 0.1289, 0.1501, 0.1649, 0.191 , 0.2036, 0.1095]
        obs = np.clip(obs, -5.0, 5.0)
        return obs

def create_super_mario_env(name='SuperMarioBros-v1'):
    import gym
    from nes_py.wrappers import JoypadSpace
    from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, COMPLEX_MOVEMENT
    import gym_super_mario_bros
    env = gym_super_mario_bros.make(name)
    env = JoypadSpace(env, SIMPLE_MOVEMENT)

    env = wrappers.MaxAndSkipEnv(env, skip=4)
    env = wrappers.wrap_deepmind(env, episode_life=False, clip_rewards=False, frame_stack=True, scale=True)
    return env

def create_super_mario_env_stage1(name='SuperMarioBrosRandomStage1-v1'):
    import gym
    from nes_py.wrappers import JoypadSpace
    from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, COMPLEX_MOVEMENT

    import gym_super_mario_bros
    stage_names = [
        'SuperMarioBros-1-1-v1',
        'SuperMarioBros-1-2-v1',
        'SuperMarioBros-1-3-v1',
        'SuperMarioBros-1-4-v1',
    ]

    env = gym_super_mario_bros.make(stage_names[1])
    env = JoypadSpace(env, SIMPLE_MOVEMENT)
    
    env = wrappers.MaxAndSkipEnv(env, skip=4)
    env = wrappers.wrap_deepmind(env, episode_life=False, clip_rewards=False, frame_stack=True, scale=True)
    #env = wrappers.AllowBacktracking(env)
    
    return env


def create_quadrupped_env():
    import gym
    import roboschool
    import quadruppedEnv
    return wrappers.FrameStack(wrappers.MaxAndSkipEnv(gym.make('QuadruppedWalk-v1'),4, False), 2, True)

def create_roboschool_env(name):
    import gym
    import roboschool
    return gym.make(name)


def create_multiflex(path, num_instances=1):
    from flex_gym.flex_vec_env import set_flex_bin_path, make_flex_vec_env_muli_env
    from autolab_core import YamlConfig
    import gym

    set_flex_bin_path(FLEX_PATH + '/bin')

    cfg_env = YamlConfig(path)
    env = make_flex_vec_env_muli_env([cfg_env] * num_instances)

    return env

def create_flex(path):
    from flex_gym.flex_vec_env import set_flex_bin_path, make_flex_vec_env
    from autolab_core import YamlConfig
    import gym

    set_flex_bin_path(FLEX_PATH + '/bin')

    cfg_env = YamlConfig(path)
    cfg_env['gym']['rank'] = 0
    env = make_flex_vec_env(cfg_env)

    return env

def create_smac(name, **kwargs):
    from smac_env import SMACEnv

    return SMACEnv(name, **kwargs)

def create_smac_cnn(name, **kwargs):
    from smac_env import SMACEnv
    env = SMACEnv(name, **kwargs)
    n_agents = env.get_number_of_agents()
    env = wrappers.BatchedFrameStack(env, 4, n_agents)
    return env

def __init__(self, env):
    gym.RewardWrapper.__init__(self, env)

def reward(self, reward):
    if reward == -100:
        return -5
    if reward == 0:
        return -0.1
    return reward

configurations = {
    'CartPole-v1' : {
        'vecenv_type' : 'RAY',
        'env_creator' : lambda : gym.make('CartPole-v1'),
    },
    'MountainCarContinuous-v0' : {
        'vecenv_type' : 'RAY',
        'env_creator' : lambda : gym.make('MountainCarContinuous-v0'),
    },
    'MountainCar-v0' : {
        'vecenv_type' : 'RAY',
        'env_creator' : lambda : gym.make('MountainCar-v0'),
    },
    'Acrobot-v1' : {
        'env_creator' : lambda : gym.make('Acrobot-v1'),
        'vecenv_type' : 'RAY'
    },
    'Pendulum-v0' : {
        'env_creator' : lambda : gym.make('Pendulum-v0'),
        'vecenv_type' : 'RAY'
    },
    'LunarLander-v2' : {
        'env_creator' : lambda : gym.make('LunarLander-v2'),
        'vecenv_type' : 'RAY'
    },
    'PongNoFrameskip-v4' : {
        'env_creator' : lambda :  wrappers.make_atari_deepmind('PongNoFrameskip-v4', skip=4),
        'vecenv_type' : 'RAY'
    },
    'BreakoutNoFrameskip-v4' : {
        'env_creator' : lambda :  wrappers.make_atari_deepmind('BreakoutNoFrameskip-v4', skip=4),
        'vecenv_type' : 'RAY'
    },
    'CarRacing-v0' : {
        'env_creator' : lambda :  wrappers.make_car_racing('CarRacing-v0', skip=4),
        'vecenv_type' : 'RAY'
    },
    'RoboschoolAnt-v1' : {
        'env_creator' : lambda : create_roboschool_env('RoboschoolAnt-v1'),
        'vecenv_type' : 'RAY'
    },
    'SuperMarioBros-v1' : {
        'env_creator' : lambda :  create_super_mario_env(),
        'vecenv_type' : 'RAY'
    },
    'SuperMarioBrosRandomStages-v1' : {
        'env_creator' : lambda :  create_super_mario_env('SuperMarioBrosRandomStages-v1'),
        'vecenv_type' : 'RAY'
    },
    'SuperMarioBrosRandomStage1-v1' : {
        'env_creator' : lambda :  create_super_mario_env_stage1('SuperMarioBrosRandomStage1-v1'),
        'vecenv_type' : 'RAY'
    },
    'RoboschoolHalfCheetah-v1' : {
        'env_creator' : lambda : create_roboschool_env('RoboschoolHalfCheetah-v1'),
        'vecenv_type' : 'RAY'
    },
    'RoboschoolHumanoid-v1' : {
        'env_creator' : lambda : wrappers.FrameStack(create_roboschool_env('RoboschoolHumanoid-v1'), 1, True),
        'vecenv_type' : 'RAY'
    },
    'LunarLanderContinuous-v2' : {
        'env_creator' : lambda : create_roboschool_env('LunarLanderContinuous-v2'),
        'vecenv_type' : 'RAY'
    },
    'RoboschoolHumanoidFlagrun-v1' : {
        'env_creator' : lambda : wrappers.FrameStack(create_roboschool_env('RoboschoolHumanoidFlagrun-v1'), 1, True),
        'vecenv_type' : 'RAY'
    },
    'BipedalWalker-v2' : {
        'env_creator' : lambda : wrappers.FrameStack(HCRewardEnv(gym.make('BipedalWalker-v2')), 1, True),
        'vecenv_type' : 'RAY'
    },
    'BipedalWalkerCnn-v2' : {
        'env_creator' : lambda : wrappers.FrameStack(HCRewardEnv(gym.make('BipedalWalker-v2')), 4, False),
        'vecenv_type' : 'RAY'
    },
    'BipedalWalkerHardcore-v2' : {
        'env_creator' : lambda : wrappers.FrameStack(HCRewardEnv(gym.make('BipedalWalkerHardcore-v2')), 1, True),
        'vecenv_type' : 'RAY'
    },
    'BipedalWalkerHardcoreCnn-v2' : {
        'env_creator' : lambda : wrappers.FrameStack(gym.make('BipedalWalkerHardcore-v2'), 4, False),
        'vecenv_type' : 'RAY'
    },
    'QuadruppedWalk-v1' : {
        'env_creator' : lambda : create_quadrupped_env(),
        'vecenv_type' : 'RAY'
    },
    'FlexAnt' : {
        'env_creator' : lambda : create_flex(FLEX_PATH + '/demo/gym/cfg/ant.yaml'),
        'vecenv_type' : 'ISAAC'
    },
    'FlexHumanoid' : {
        'env_creator' : lambda : create_flex(FLEX_PATH + '/demo/gym/cfg/humanoid.yaml'),
        'vecenv_type' : 'ISAAC'
    },
    'FlexHumanoidHard' : {
        'env_creator' : lambda : create_flex(FLEX_PATH + '/demo/gym/cfg/humanoid_hard.yaml'),
        'vecenv_type' : 'ISAAC'
    },
    'smac' : {
        'env_creator' : lambda **kwargs : create_smac('8m_vs_9m', **kwargs),
        'vecenv_type' : 'RAY_SMAC'
    },
    'smac_cnn' : {
        'env_creator' : lambda **kwargs : create_smac_cnn('8m_vs_9m', **kwargs),
        'vecenv_type' : 'RAY_SMAC'
    },
}


def get_obs_and_action_spaces(name):
    env = configurations[name]['env_creator']()
    observation_space = env.observation_space
    action_space = env.action_space
    env.close()
    return observation_space, action_space

def register(name, config):
    configurations[name] = config