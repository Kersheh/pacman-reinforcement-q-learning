import time
import random
import collections

class Environment(object):
    """A grid world with pellets to collect and an enemy to avoid."""

    def __init__(self, size, density):
        """Environments have fixed size and pellet counts."""
        self.size = size
        self.density = density
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # left, down, right, up

    def initialize(self):
        """Place pacman, pellets, and ghost at random locations."""
        
        locations = list()
        for r in range(1,self.size-1):
            for c in range(1,self.size-1):
                locations.append((r, c))
        
        random.shuffle(locations)
        self.pacman = locations.pop()
        
        self.pellets = set()
        for count in range(self.density):
            self.pellets.add(locations.pop())
            
        self.new_ghost()
        self.next_reward = 0
    
    def new_ghost(self):
        """Place a ghost at one end of pacman's row or column."""
        (r, c) = self.pacman
        locations = [(r, 0), (0, c), (r, self.size-1), (self.size-1, c)]
        choice = random.choice(range(len(locations)))
        self.ghost = locations[choice]
        self.ghost_action = self.directions[choice]
    
    def display(self):
        """Print the environment."""
        for r in range(self.size):
            for c in range(self.size):
                if (r,c) == self.ghost:
                    print 'G',
                elif (r,c) == self.pacman:
                    print 'O',
                elif (r,c) in self.pellets:
                    print '.',
                elif r == 0 or r == self.size-1:
                    print 'X',
                elif c == 0 or c == self.size-1:
                    print 'X',
                else:
                    print ' ',
            print
        print
    
    def actions(self):
        """Return the actions the agent may try to take."""
        if self.terminal():
            return None
        else:
            return self.directions

    def terminal(self):
        """Return whether the episode is over."""
        if self.next_reward == -100:
            return True
        elif len(self.pellets) == 0:
            return True
        else:
            return False
    
    def reward(self):
        """Return the reward earned at during the last update."""
        return self.next_reward
        
    def update(self, action):
        """Adjust the environment given the agent's choice of action."""
        
        pacman = self.pacman
        ghost = self.ghost
        
        # Pacman moves as chosen
        (r, c) = self.pacman
        (dr, dc) = action
        self.pacman = (r+dr, c+dc)
        
        # Ghost moves in its direction
        (r, c) = self.ghost
        (dr, dc) = self.ghost_action
        self.ghost = (r+dr, c+dc)
        
        # Ghost is replaced when it leaves
        (r, c) = self.ghost
        if r == 0 or r == self.size-1:
            self.new_ghost()
        elif c == 0 or c == self.size-1:
            self.new_ghost()
        
        (r,c) = self.pacman
        (gr,gc) = self.ghost
        
        # Negative reward for hitting the ghost
        if self.pacman == self.ghost:
            self.next_reward = -100
        elif (pacman, ghost) == (self.ghost, self.pacman):
            self.next_reward = -100
        
        # Negative reward for hitting a wall
        elif r == 0 or r == self.size-1:
            self.next_reward = -100
        elif c == 0 or c == self.size-1:
            self.next_reward = -100
        
        # Positive reward for consuming a pellet
        elif self.pacman in self.pellets:
            self.next_reward = 10
            self.pellets.remove(self.pacman)
        else:
            self.next_reward = 0

    def state(self):
        """Return a description of the state of the environment."""
        s = dict()
        
        # Baseline feature noting how many pellets are left
        s['pellets left'] = len(self.pellets) / float(self.density)
        
        # YOU ADD MORE FEATURES
        
        return s

class Agent(object):
    """Learns to act within the environment."""

    def __init__(self):
        """Establish initial weights and learning parameters."""
        self.w = collections.defaultdict(float) # Each w((f,a)) starts at 0
        self.epsilon = 0.05 # Exploration rate
        self.gamma = 0.99 # Discount factor
        self.alpha = 0.01 # Learning rate

    def choose(self, s, actions):
        """Return an action to try in this state."""
        p = random.random()
        if p < self.epsilon:
            return random.choice(actions)
        else:
            return self.policy(s, actions)

    def policy(self, s, actions):
        """Return the best action for this state."""
        max_value = max([self.Q(s,a) for a in actions])
        max_actions = [a for a in actions if self.Q(s,a) == max_value]
        return random.choice(max_actions)

    def Q(self, s, a):
        """Return the estimated Q-value of this action in this state."""
        return 0 # YOU CHANGE THIS
    
    def observe(self, s, a, sp, r, actions):
        """Update weights based on this observed step."""
        # YOU FILL THIS IN

def main():
    """Train an agent and then watch it act."""
    
    environment = Environment(20,10)
    agent = Agent()

    for episode in range(1000):
        environment.initialize()
        while not environment.terminal():
            
            s = environment.state()
            actions = environment.actions()
            a = agent.choose(s, actions)
            environment.update(a)
            
            sp = environment.state()
            r = environment.reward()
            actions = environment.actions()
            agent.observe(s, a, sp, r, actions)

    environment.initialize()
    environment.display()
    while not environment.terminal():
        
        s = environment.state()
        actions = environment.actions()
        a = agent.policy(s, actions)
        
        environment.update(a)
        time.sleep(0.25)
        environment.display()

if __name__ == '__main__':
    main()