Reinforcement Learning - Q-Learning with Pacman
===

A simplified version of Pacman designed to implement a reinforcement learning 
technique known as Q-Learning. Pacman can be trained for n generations and 
then ran for an instance based on his trained experience.

Run
---

Run `./pacman` to begin the script. Originally developed on Python 2.7.11.

Usage
---

On run, a list of commands will be presented to use the script.

`t` or `train` without a specified quantity will train Pacman for a default 
number of generations (1000).

`l` or `load` without a specified file name will load a default save file
`"default_save.p"` from the the `saves/` directory. `s` or `save` without a 
specified file name will save to the default `"default_save.p"`.