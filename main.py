import os
import time
import random


def generateItems(x):
    items = ["Metal detector",'2X damage', "Extra life",'Inverter','Burner phone']
    SelectedItems = []

    for i in range(x):
        pickedItem = random.choice(items)
        SelectedItems.append(pickedItem)
    return SelectedItems


def generateChamber(ammo):
    chamber = ['live', 'blank']
    while len(chamber) < ammo:
        chamber.append( random.choice(["live", 'blank', 'blank']))
    random.shuffle(chamber)
    return chamber

def playerAction(player, bot):
    if not chamber:
        print("The chamber is empty! Reloading...")
        chamber.extend(generateChamber(5))
        print("BEWARE!!!  current chamber has ",sorted(chamber))
        sleepy(3)
        if len(player1.inventory) < 5:
            newItems = generateItems(2)
            player1.inventory.extend(newItems)
        clear()

    displayHealth(player, bot)
    print(f"Your current items: {player1.inventory}")
    choice = input("Do you want to shoot yourself, the dealer or use an item ? (self/dealer): ").lower()

    if choice == "item":
        useItem = input("To select an item enter the first letter of the item: ")
        match useItem.upper():
            case "M":
                if "Metal detector" in player1.inventory:
                     print("Metal detector")
                     player1.inventory.remove("Metal detector")
                else:
                    print("You don't have that item")
    
            case "B":
                if "Burner phone" in player1.inventory:
                    print("Burner phone")
                    player1.inventory.remove("Burner phone")
                else:
                    print("You don't have that item")

            case "2":
                if "2X damage" in player1.inventory:
                    print("Double damage")
                    player1.inventory.remove("2X damage")
                else:
                    print("You don't have that item")

            case "E":
                if "Extra life" in player1.inventory:
                    print("Extra life")
                    player1.inventory.remove("Extra life")
                else:
                    print("You don't have that item")
                
            case "I":     
                if "Inverter" in player1.inventory:
                    print("Inverter")
                    player1.inventory.remove("Inverter")
                else:
                    print("You don't have that item")
        sleepy(3)
        playerAction(player, bot)
    


    current_shell = chamber[0]
    switch_turn = True    

    if choice == "self":
        if current_shell == "live":
            player.life -= 1
            print(f"\nBang! The shell was {current_shell.upper()}!")
            print(f"\n💀 You got hit!")
            chamber.pop(0)
            sleepy(1)
        else:
            bot.life -= 1
            print(f"\n💀 {bot.name} got hit!")
    elif choice == "dealer":
        print("\nClick... blank shell.")
        if choice == 'self':
            switch_turn = False
    else:
        print("Wrong input")
        sleepy(2)
        playerAction(player, bot)

    # Update alive status
    if player.life <= 0:
        player.isAlive = False
    if bot.life <= 0:
        bot.isAlive = False
    return switch_turn

def botAction(bot, player):
    if not chamber:
        print("The chamber is empty! Reloading...")
        chamber.extend(generateChamber(5))
        print("BEWARE!!!  current chamber has ",sorted(chamber))
        sleepy(3)
        clear()

    displayHealth(bot, player)

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


# MAIN GAME LOGIC

clear()
print("Welcome to Buckshot roulette")
play = input("Play again bot Y for yes and any other button to quit: ")
if play.lower() == 'y':
    sleepy(0.5)
    print("Let's play some buckshot roulette") 
    name = input("Please enter Name: ")
    while name == ''.strip():
        clear()
        print("Invalid input")
        sleepy(1.2)

        print("Please enter a valid input")
        name = input("Please enter Name: ")

    player1 = participant(name)
    bot = participant()
    player1.inventory = generateItems(1)
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
    
    if  player1.isAlive:
        print("-------YOU WIN!!!!!!----------")
    else:
        print("------YOU LOSE!!!------")


            
        


