import os
import time
import random


def generateChamber(ammo):
    chamber = ['live', 'blank']
    while len(chamber) < ammo:
        chamber.append( random.choice(["live", 'blank', 'blank']))
    random.shuffle(chamber)
    return chamber

def playerAction(player, bot):
    displayHealth(player, bot)
    choice = input("Do you want to shoot yourself or the dealer? (self/dealer): ").lower()
    if not chamber:
        print("The chamber is empty! Reloading...")
        chamber.extend(generateChamber(5))
        sleepy(2)

    switch_turn = True
    current_shell = chamber.pop(0)
    print(f"\nBang! The shell was {current_shell.upper()}!")
    sleepy(1)

    if current_shell == "live":
        if choice == "self":
            player.life -= 1
            print(f"\n💀 You got hit!")
        else:
            bot.life -= 1
            print(f"\n💀 {bot.name} got hit!")
    else:
        print("\nClick... blank shell.")
        if choice == 'self':
            switch_turn = False

    # Update alive status
    if player.life <= 0:
        player.isAlive = False
    if bot.life <= 0:
        bot.isAlive = False
    return switch_turn

def botAction(bot, player):
    displayHealth(bot, player)
    if not chamber:
        print("The chamber is empty! Reloading...")
        chamber.extend(generateChamber(5))
        sleepy(2)
    bot_choice = random.choice(["self", 'player'])
    current_shell = chamber.pop(0)
    if len(chamber) < 2 and current_shell == 'live':
        bot_choice = 'player'
    print(f"{bot.name} decides to shoot {bot_choice}!")
    print(f"\nBang! The shell was {current_shell.upper()}!")
    sleepy(1)
    switch = True

    if current_shell == "live":
        if bot_choice == "self":
            bot.life -= 1
            print(f"\n💀  Bot got hit!")
        else:
            player.life -= 1
            print(f"\n💀 {player.name} got hit!")
    else:
        print("\nClick... blank shell.")
        if bot_choice == "self":
            switch = False

    # Update alive status
    if player.life <= 0:
        player.isAlive = False
    if bot.life <= 0:
        bot.isAlive = False
    return switch



class participant:
    def __init__(self, name ="B.O.T."):
        self.name = name 
        self.life = 4
        self.inventory = []
        self.record = 0
        self.isAlive = True 
        self.turn_flag = True

def displayHealth(player, opp):
    clear()
    if player.turn_flag:
        print(f"It's {player.name}'s  turn")
    else:
        print(f"It's {bot.name}'s turn ")
    print("My health : ",'❤️ '*player.life )
    print(f"{opp.name} : ",'❤️ '*opp.life )




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
    sleepy(0.5)
    print("Let's play some buckshot roulette") 
    name = input("Please enter Name: ")
    player1 = participant(name)
    bot = participant()
    sleepy(2)
    clear()
    chamber = generateChamber(5)
    print("BEWARE!!!  current chamber has ",sorted(chamber))
    sleepy(3)


    while player1.isAlive and bot.isAlive:
        if player1.turn_flag:
            displayHealth(player1, bot)
            switch = playerAction(player1, bot)
            if switch:
                player1.turn_flag = not player1.turn_flag

            sleepy(1)
        else:
            displayHealth(bot, player1)
            switch = botAction(bot,player1)
            sleepy(3)
            if switch:
                player1.turn_flag = not player1.turn_flag

            
        


