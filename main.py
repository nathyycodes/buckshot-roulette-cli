import os
import time
import random


def generateChamber(ammo):
    chamber = ['live', 'blank']
    while len(chamber) < ammo:
        chamber.append( random.choice(["live", 'blank', 'blank']))
    random.shuffle(chamber)
    return chamber

class participant:
    def __init__(self, name ="B.O.T."):
        self.name = name 
        self.life = 4
        self.inventory = []
        self.record = 0 

def PlayRound():
    playerTurn = True
    while playerTurn:
        print(f"It's {player1.name} turn")
        print("My health : ",'❤️ '*player1.life )
        print(f"{bot.name} : ",'❤️ '*bot.life )
        playerTurn = False
        
        




def clear():
    os.system("cls")

def sleepy(x):
    time.sleep(x)

def Game():
    name = input("Please enter Name: ")
    player1 = participant(name)
    print(f'{player1.name} has {player1.life}lives left')
    round()


clear()
print("Welcome to Buckshot roulette")
play = input("Play again bot Y for yes and any other button to quit: ")
if play.lower() == 'y':
    sleepy(0.3)
    print("Let's play some buckshot roulette") 
    name = input("Please enter Name: ")
    player1 = participant(name)
    bot = participant()
    clear()
    chamber = generateChamber(5)
    print("BEWARE!!!  current chamber has ",sorted(chamber))
    sleepy(3.4)
    clear()
    PlayRound()


print("I am going to build expert systems")

    

