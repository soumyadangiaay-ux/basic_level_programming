# AI Vacuum Cleaner Agent

# Initial state of rooms
rooms = {
    "A": input("Enter status of Room A (Clean/Dirty): ").capitalize(),
    "B": input("Enter status of Room B (Clean/Dirty): ").capitalize()
}

# Starting location
current_room = input("Enter the starting room (A/B): ").upper()

print("\n--- Vacuum Cleaner Agent Started ---")

# Clean both rooms
for i in range(2):

    print("\nCurrent Room:", current_room)

    if rooms[current_room] == "Dirty":
        print("Room is Dirty.")
        print("Action: Cleaning the room...")
        rooms[current_room] = "Clean"
        print("Room is now Clean.")

    else:
        print("Room is already Clean.")

    # Move to next room
    if current_room == "A":
        current_room = "B"
    else:
        current_room = "A"

    print("Moving to Room", current_room)

print("\n--- Final Status of Rooms ---")
for room in rooms:
    print("Room", room, ":", rooms[room])

print("\nTask Completed!")
