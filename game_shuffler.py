import os
import random

def random_game_selector(directory):
    # Read the file extensions from the text file
    with open('filetypes.txt', 'r') as f:
        filetypes = tuple(line.strip() for line in f if line.strip())
    
    # Get all ROM files in the directory and subdirectories
    rom_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(filetypes):
                rom_files.append(os.path.join(dirpath, filename))
    
    if not rom_files:
        return None

    # Randomly select a ROM
    selected_rom = random.choice(rom_files)
    
    return selected_rom

def get_game_and_system_from_path(path, system_mapping):
    # Extract the game name by splitting the path and taking the last part without the extension
    game_name = os.path.splitext(os.path.basename(path))[0]
    
    # If the file is a .cue (or any other special case), navigate two directories up
    if path.lower().endswith(('.cue', '.zip')):
        system = os.path.basename(os.path.dirname(os.path.dirname(path)))
    else:
        # For regular cases, just take the parent directory name
        system = os.path.basename(os.path.dirname(path))
    
    # Get the full platform name from the system_mapping dictionary
    full_system_name = system_mapping.get(system, system)  # Default to the abbreviation if not found
    
    return game_name, full_system_name

def main():
    # Possible directories
    possible_directories = ["H:/Emulation/Games", "D:/Emulation/Games"]
    
    # Find the first existing directory from the list
    directory = next((dir for dir in possible_directories if os.path.exists(dir)), None)
    
    if not directory:
        print("No valid game directories found!")
        return
    
    # Define the system abbreviation to full name mapping
    system_mapping = {
        "3DS": "Nintendo 3DS",
        "DS": "Nintendo DS",
        "GB": "Game Boy",
        "GBA": "Game Boy Advance",
        "GCN": "GameCube",
        "N64": "Nintendo 64",
        "PS1": "PlayStation",
        "PS2": "PlayStation 2",
        "TG-16": "TurboGrafx-16",
        "TG-CD": "TurboGrafx-CD",
        # ... Add other mappings as needed ...
    }

    while True:
        selected_game = random_game_selector(directory)

        if selected_game is None:
            print("No ROMs found.")
        else:
            game_name, system = get_game_and_system_from_path(selected_game, system_mapping)
            print(f"You should play '{game_name}' for the {system}")
        
        response = input("Hit ENTER to roll again or type 'q' to quit: ")
        print()
        if response.upper() == 'Q':
            print("Goodbye!")
            break

main()
