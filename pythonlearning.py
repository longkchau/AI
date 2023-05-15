import json

# Function to load checklists from file
def load_checklists():
    try:
        with open("checklists.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save checklists to file
def save_checklists():
    with open("checklists.json", "w") as f:
        json.dump(checklists, f)

# Creating a dictionary to store multiple checklists
checklists = load_checklists()

# Function to create a new checklist
def create_checklist(name):
    checklist = []
    checklists[name] = checklist
    print(f"Checklist for {name} has been created!")
    save_checklists()

# Function to add items to a checklist
def add_item(name, item):
    if name not in checklists:
        print(f"No checklist found for {name}.")
    else:
        checklists[name].append({"item": item, "done": False})
        print(f"Item '{item}' has been added to {name}'s checklist.")
        save_checklists()

# Function to display a checklist
def display_checklist(name):
    if name not in checklists:
        print(f"No checklist found for {name}.")
    else:
        print(f"Checklist for {name}:")
        for i, item in enumerate(checklists[name]):
            status = "[ ]" if not item["done"] else "[X]"
            print(f"{i+1}. {status} {item['item']}")

# Function to mark an item as done
def mark_item_done(name, index):
    if name not in checklists:
        print(f"No checklist found for {name}.")
    elif index < 1 or index > len(checklists[name]):
        print("Invalid index.")
    else:
        checklists[name][index-1]["done"] = True
        print(f"Item '{checklists[name][index-1]['item']}' has been marked as done.")
        save_checklists()

# Main program loop
while True:
    print("Enter '1' to create a new checklist.")
    print("Enter '2' to add an item to a checklist.")
    print("Enter '3' to display a checklist.")
    print("Enter '4' to mark an item as done.")
    print("Enter '5' to exit.")

    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter a name for the new checklist: ")
        create_checklist(name)

    elif choice == '2':
        name = input("Enter the name of the checklist: ")
        item = input("Enter the item to add: ")
        add_item(name, item)

    elif choice == '3':
        name = input("Enter the name of the checklist: ")
        display_checklist(name)

    elif choice == '4':
        name = input("Enter the name of the checklist: ")
        index = int(input("Enter the index of the item to mark as done: "))
        mark_item_done(name, index)

    elif choice == '5':
        print("Exiting program.")
        break

    else:
        print("Invalid input. Please try again.")