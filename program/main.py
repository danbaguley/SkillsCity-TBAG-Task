from room import Room
from character import Enemy, Friend
from item import Item

# Create rooms
kitchen = Room("Kitchen")
ballroom = Room("Ballroom")
dining_hall = Room("Dining Hall")

# Set descriptions
kitchen.set_description("A dank and dirty room buzzing with flies.")
ballroom.set_description("A vast room with a shiny wooden floor.")
dining_hall.set_description("A large room with ornate golden decorations.")

# Link rooms
kitchen.link_room(dining_hall, "south")
dining_hall.link_room(kitchen, "north")
dining_hall.link_room(ballroom, "west")
ballroom.link_room(dining_hall, "east")

# Create an enemy
dave = Enemy("Dave", "A smelly zombie")
dave.set_conversation("Brrlgrh... rgrhl... brains...")
dave.set_weakness("cheese")

# Create a friend
alice = Friend("Alice", "A friendly ghost")
alice.set_conversation("Hello there! I can help you on your journey.")

# Add a key item to the dining hall
key = Item("key")
dining_hall.set_item(key)

# Place characters in rooms
dining_hall.set_character(dave)
ballroom.set_character(alice)

# Inventory system
inventory = []

# Game loop
current_room = kitchen
while True:
    print("\n")
    current_room.get_details()

    # Check for characters in the room
    inhabitant = current_room.get_character()
    if inhabitant:
        inhabitant.describe()

    # Ask for user input
    command = input("> ").strip().lower()

    if command in ["north", "south", "east", "west"]:
        current_room = current_room.move(command)
    elif command == "talk":
        if inhabitant:
            inhabitant.talk()
        else:
            print("There's no one here to talk to.")
    elif command == "fight":
        if isinstance(inhabitant, Enemy):
            weapon = input("What will you fight with? ").strip().lower()
            if weapon in inventory:
                if inhabitant.fight(weapon):
                    print("You defeated the enemy!")
                    current_room.set_character(None)  # Remove defeated enemy
                else:
                    print("You were defeated... Game Over!")
                    break
            else:
                print("You don't have that weapon!")
        else:
            print("There's no enemy to fight here.")
    elif command == "hug":
        if isinstance(inhabitant, Friend):
            inhabitant.hug()
        else:
            print("That wouldn't be a good idea.")
    elif command.startswith("take"):
        if current_room.item and command.split(" ")[1] == current_room.item.name.lower():
            inventory.append(current_room.item.name.lower())
            print(f"You picked up the {current_room.item.name}.")
            current_room.set_item(None)
        else:
            print("There's nothing to take here.")
    elif command == "unlock":
        if "key" in inventory and current_room == dining_hall:
            print("You unlocked the door! You win!")
            break
        else:
            print("You need a key to unlock the door.")
    else:
        print("Invalid command.")
