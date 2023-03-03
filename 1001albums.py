import random
import re
ALBUMS_FILE = "albums.txt"

def main():
    print("Can't decide what to listen to?")
    print("Hit ENTER for a random album.")
    print("Type Menu to see more options.")
    handle_input(load_album_dict())

def load_album_dict():
    albumDict = {}
    try:
        with open(ALBUMS_FILE, "r", encoding="UTF-8") as file:
            albumNumber = 1
            for line in file:
                line = line.strip()
                if line: # Ignore empty lines
                    match = re.match(r"^(.+) – (.+) \((\d+)\)$", line)
                    if match:
                        artist, albumTitle, year = match.groups()
                        year = int(year)
                        albumDict[albumNumber] = {"artist": artist, "title": albumTitle, "year": year}
                        albumNumber += 1
            if not albumDict:
                print("Error: File is empty.")
    except FileNotFoundError:
        print("Error: File not found.")
    return albumDict

def user_menu():
    print("Hit ENTER for a random album.")
    print("Type Next to see the next album in the list.")
    print("Type Last to see the previous album in the list.")
    print("Type a year to limit albums to that year.")
    print("Type Q to quit.")

def handle_input(albumDict):
    while True:
        userInput = input("Command? ")
        if not userInput: # empty input
            random_album(albumDict)
        elif userInput.isdigit():
            random_album_by_year(albumDict, int(userInput))
        elif userInput.upper() == "Q":
            break
        elif userInput.upper() == "MENU":
            user_menu()
        else:
            print("Invalid input. Type Menu to see options.")

def print_albums(albums, message):
    if not albums:
        print(f"No albums found.")
        return
    for i, album in enumerate(albums, start=1):
        print(f"{i}. {album['artist']} - {album['title']} ({album['year']})")
    if message:
        print(message)

def random_album(albumDict):
    randomIndex = random.randint(1, len(albumDict))
    album = albumDict[randomIndex]
    print(f"{randomIndex}. {album['artist']} - {album['title']} ({album['year']})")

def random_album_by_year(albumDict, year):
    year_albums = [album for album in albumDict.values() if album['year'] == year]
    if not year_albums:
        print(f"No albums found for the year {year}.")
        return
    album = random.choice(year_albums)
    album_number = list(albumDict.keys())[list(albumDict.values()).index(album)]
    print(f"{album_number}. {album['artist']} - {album['title']} ({album['year']})")

if __name__ == "__main__":
    main()