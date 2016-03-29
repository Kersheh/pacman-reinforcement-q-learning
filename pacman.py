# Q-learning - Simplified Pacman
# Source: http://modelai.gettysburg.edu/2016/pyconsole/ex5/index.html

import time, random, collections

## Game board with pellets and enemy ghost
class Environment:
    # environment constructor
    # var:      size - board size
    #           density - number of pellets
    def __init__(self, size, density):
        self.size = size
        self.density = density
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # left, down, right, up

    # initialize environment - randomize pacman, ghost, and pellets
    def initialize(self):
        locations = list()
        for r in range(1, self.size - 1):
            for c in range(1, self.size - 1):
                locations.append((r, c))
        
        random.shuffle(locations)
        self.pacman = locations.pop()
        
        self.pellets = set()
        for count in range(self.density):
            self.pellets.add(locations.pop())
            
        self.new_ghost()
        self.next_reward = 0
    
    # spawn ghost at one end of pacman's row or column randomly
    def new_ghost(self):
        (r, c) = self.pacman
        locations = [(r, 0), (0, c), (r, self.size - 1), (self.size - 1, c)]
        choice = random.choice(range(len(locations)))
        self.ghost = locations[choice]
        self.ghost_action = self.directions[choice]
    
    # print environment
    def display(self):
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) == self.ghost:
                    print "G",
                elif (r, c) == self.pacman:
                    print "O",
                elif (r, c) in self.pellets:
                    print ".",
                elif r == 0 or r == self.size - 1:
                    print "X",
                elif c == 0 or c == self.size - 1:
                    print "X",
                else:
                    print " ",
            print
        print
    
    # return actions pacman can make in the environment
    def actions(self):
        if self.is_over():
            return None
        else:
            return self.directions

    # return whether the episode is done
    def is_over(self):
        if self.next_reward == -100:
            return True
        elif len(self.pellets) == 0:
            return True
        else:
            return False
    
    # return reward earned at last environment update
    def reward(self):
        return self.next_reward
        
    # update the environment based on agent's action
    def update(self, action):
        pacman = self.pacman
        ghost = self.ghost
        
        # pacman moves as chosen
        (r, c) = self.pacman
        (dr, dc) = action
        self.pacman = (r + dr, c + dc)
        
        # ghost moves in its direction
        (r, c) = self.ghost
        (dr, dc) = self.ghost_action
        self.ghost = (r + dr, c + dc)
        
        # ghost is replaced when it leaves
        (r, c) = self.ghost
        if r == 0 or r == self.size - 1:
            self.new_ghost()
        elif c == 0 or c == self.size - 1:
            self.new_ghost()
        
        (r, c) = self.pacman
        (gr, gc) = self.ghost
        
        # negative reward for hitting the ghost
        if self.pacman == self.ghost:
            self.next_reward = -100
        elif (pacman, ghost) == (self.ghost, self.pacman):
            self.next_reward = -100
        
        # negative reward for hitting a wall
        elif r == 0 or r == self.size - 1:
            self.next_reward = -100
        elif c == 0 or c == self.size - 1:
            self.next_reward = -100
        
        # positive reward for consuming a pellet
        elif self.pacman in self.pellets:
            self.next_reward = 10
            self.pellets.remove(self.pacman)
        else:
            self.next_reward = 0

    # return a dict of state attributes of the environment
    def state(self):
        s = dict()
        s["pellets left"] = len(self.pellets) / float(self.density)
        
        # add more features
        
        return s

## Agent to learn actions within environment
class Agent:
    # agent constructor
    def __init__(self):
        self.w = collections.defaultdict(float) # each w((f,a)) starts at 0
        self.epsilon = 0.05 # exploration rate
        self.gamma = 0.99 # discount factor
        self.alpha = 0.01 # learning rate

    # return an action in a given state by the agent
    def choose(self, s, actions):
        p = random.random()
        if p < self.epsilon:
            return random.choice(actions)
        else:
            return self.policy(s, actions)

    # return the best action for a given state
    def policy(self, s, actions):
        max_value = max([self.Q(s, a) for a in actions])
        max_actions = [a for a in actions if self.Q(s, a) == max_value]
        return random.choice(max_actions)

    # return estimated Q-value of an action based on a given state
    def Q(self, s, a):
        return 0 # YOU CHANGE THIS
    
    # update weights based on observed step
    def update_weights(self, s, a, sp, r, actions):
        pass

# train an agent
def train_agent(env, agent, episodes=1000):
    for episode in range(episodes):
        environment.initialize()
        while not environment.is_over():
            
            s = env.state()
            actions = env.actions()
            a = agent.choose(s, actions)
            env.update(a)
            
            sp = env.state()
            r = env.reward()
            actions = env.actions()
            agent.update_weights(s, a, sp, r, actions)

# execute trained agent
def run_agent(env, agent):
    env.initialize()
    env.display()
    while not env.is_over():
        s = env.state()
        actions = env.actions()
        a = agent.policy(s, actions)
        
        env.update(a)
        time.sleep(0.1)
        env.display()

if __name__ == "__main__":
    environment = Environment(20, 10)
    agent = Agent()

    train_agent(environment, agent, episodes=1000)
    run_agent(environment, agent)