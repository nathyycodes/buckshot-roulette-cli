import os
import time
import random

#HELPER FUNCTIONS
def displayChamber(chamber):
    """Show bullets as visual icons: 🔫 = live, ⚪ = blank"""
    visual_chamber = ""
    for bullet in chamber:
        if bullet == 'live':
            visual_chamber += "🔫 "
        else:
            visual_chamber += "⚪ "
    live_count = chamber.count('live')
    blank_count = chamber.count('blank')
    print(f"BEWARE!!! Current chamber: {visual_chamber.strip()}")
    print(f"Live bullets: {live_count}, Blank bullets: {blank_count}")
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sleepy(x):
    time.sleep(x)

def reloadChamber():
    global chamber, player1
    if not chamber:
        print("The chamber is empty! Reloading...")
        chamber.extend(generateChamber(5))
        displayChamber(chamber)
        sleepy(2)
        
        # Give items to player if inventory < 5
        if len(player1.inventory) < 5:
            new_items = generateItems(2)
            player1.inventory.extend(new_items)
            print(f"You received new items: {new_items}")
            sleepy(2)
        if len(bot.inventory) < 5:
            new_items = generateItems(2)
            bot.inventory.extend(new_items)
            print(f"BOT received new items: {new_items}")
            sleepy(1)


# ITEM LOGIC
def useExtralife():
    player1.heal(1)

def useMetalDetector():
    currentRound = chamber[0]
    print(f"The Current Round is a {currentRound}")

def useInverter():
    currentRound = chamber[0]
    if currentRound == 'live':
        chamber[0] = "blank"
    else:
        chamber[0] = 'live'
    print("the type of the current shell in the chamber has been inverted.")
    sleepy(3)

def useBurnerPhone():
    if len(chamber) > 2:
        randomItem = random.randrange(0, len(chamber))
        print(f"The {randomItem+ 1} bullet is a {chamber[randomItem]}!!")
        sleepy(2)
    else:
        print("You just wasted a valuable item!!")
        sleepy(2)



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
    global chamber
   
    while True:
        displayHealth(player, bot)
        print(f"Your current items: {player.inventory}")
        choice = input("Do you want to shoot yourself, the dealer or use an item? (self/dealer/item): ").lower()

        if choice == "item":
            useItem = input("Select an item by first letter or number (M/E/I/B/2): ").upper()
            if useItem == "M" and "Metal detector" in player.inventory:
                player.inventory.remove("Metal detector")
                useMetalDetector()
            elif useItem == "B" and "Burner phone" in player.inventory:
                player.inventory.remove("Burner phone")
                useBurnerPhone()
            elif useItem == "2" and "2X damage" in player.inventory:
                player.inventory.remove("2X damage")
                print("Double damage activated!")
                player.useDoubleDamage()
                bot.useDoubleDamage()
            elif useItem == "E" and "Extra life" in player.inventory:
                player.inventory.remove("Extra life")
                useExtralife()
            elif useItem == "I" and "Inverter" in player.inventory:
                player.inventory.remove("Inverter")
                useInverter()
            else:
                print("You don't have that item or invalid choice.")
                sleepy(2)
                continue  # loop again for valid input
            sleepy(2)
            continue  # loop again for player action after using an item

        if choice not in ["self", "dealer"]:
            print("Invalid choice. Try again.")
            sleepy(2)
            continue

        # Shooting logic
        if not chamber:
            print("The chamber is empty! Reloading...")
            chamber.extend(generateChamber(5))
            displayChamber(chamber)
            sleepy(2)

        current_shell = chamber.pop(0)

        if choice == "self":
            if current_shell == "live":
                player.takeDamage()
                print(f"\nBang! The shell was {current_shell.upper()}! 💀 You got hit!")
                switch_turn = True
            else:
                print(f"\nBang! The shell was {current_shell.upper()}! Click.. Lucky you!")
                switch_turn = False
        elif choice == "dealer":
            if current_shell == "live":
                bot.takeDamage()
                print(f"\nBang! The shell was {current_shell.upper()}! 💀 {bot.name} got hit!")
            else:
                print(f"\nBang! The shell was {current_shell.upper()}! Click..")
            switch_turn = True

        # Update alive status
        player.isAlive = player.life > 0
        bot.isAlive = bot.life > 0
        sleepy(2)
        player.doubleDamage = False
        bot.doubleDamage = False
        return switch_turn


def botAction(bot, player):
    global chamber

    # === Reload if empty ===
    if not chamber:
        print("The chamber is empty! Reloading...")
        chamber.extend(generateChamber(5))
        print("New chamber loaded!")
        print("BEWARE!!!  current chamber has ",sorted(chamber))
        sleepy(2)
        clear()

    displayHealth(bot, player)

    # === Analyze chamber ===
    live_count = chamber.count("live")
    blank_count = chamber.count("blank")
    total = len(chamber)
    prob_live = live_count / total if total > 0 else 0

    # === Bot decision logic ===
    # Add small randomness for realism
    decision_roll = random.random()

    # Base choice
    # and decision_roll < 0.8
    if prob_live < 0.35 :
        bot_choice = "self"   # safer, likely blank
    elif player.life == 1 and decision_roll < 0.9:
        bot_choice = "player" # go for the kill
    else:
        bot_choice = "player" if prob_live > 0.5 else random.choice(["self", "player"])



    #------ ITEM LOGIC --------
    

    # === Pull the trigger ===
    current_shell = chamber.pop(0)
    print(f"{bot.name} decides to shoot {bot_choice}!")
    sleepy(1)
    print(f"\nBang! The shell was {current_shell.upper()}!")
    sleepy(1)

    switch = True

    # === Apply result ===
    if current_shell == "live":
        if bot_choice == "self":
            bot.takeDamage()
            print("\n💀  Bot got hit!")
        else:
            player.takeDamage()
            print(f"\n💀 {player.name} got hit!")
    else:
        print("\nClick... blank shell.")
        # If bot risks itself and gets a blank, it earns another turn
        if bot_choice == "self":
            switch = False

    # === Update life status ===
    player.isAlive = player.life > 0
    bot.isAlive = bot.life > 0

    return switch



class participant:
    def __init__(self, name ="B.O.T."):
        self.name = name 
        self.life = 4
        self.inventory = []
        self.record = 0
        self.isAlive = True 
        self.turn_flag = True
        self.doubleDamage = False
 
    def heal(self, amount):
        self.life += amount

    def takeDamage(self):
        if self.doubleDamage :
            self.life -= 2
        else:
            self.life -= 1
        self.doubleDamage = False
    
    def useDoubleDamage(self):
        self.doubleDamage = True



def displayHealth(player, opp):
    clear()
    if player.turn_flag:
        print(f"It's {player.name}'s  turn")
    else:
        print(f"It's {bot.name}'s turn ")
    print("My health : ",'❤️ '*player.life )
    print(f"{opp.name} : ",'❤️ '*opp.life )







# MAIN GAME LOGIC
player_turn = True  # True = player, False = bot


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
        reloadChamber()
        if player_turn:
            switch_turn = playerAction(player1, bot)
        else:
            switch_turn = botAction(bot, player1)

        # Only flip turn if switch_turn is True
        if switch_turn:
            player_turn = not player_turn

    
    
    if  player1.isAlive:
        print("-------YOU WIN!!!!!!----------")
    else:
        print("------YOU LOSE!!!------")


            
        


