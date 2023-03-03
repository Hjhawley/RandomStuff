import random

def main():
    print("Can't decide what to listen to?")
    albumDict = {}
    try:
        with open("albums.txt", "r", encoding="UTF-8") as file:
            albumNumber = 1
            for line in file:
                line = line.strip()
                if line: # Ignore empty lines
                    artist, albumTitleYear = line.split(" – ")
                    albumTitle, year = albumTitleYear.rsplit("(", 1)
                    year = int(year.strip(")"))
                    albumDict[albumNumber] = {"artist": artist, "title": albumTitle.strip(), "year": year}
                    albumNumber += 1

            if albumDict:
                userInput = input("Press ENTER for a random album, Q to quit. ")
                while userInput.upper() != "Q":
                    randomIndex = random.randint(1, len(albumDict))
                    album = albumDict[randomIndex]
                    print(f"{randomIndex}. {album['artist']} - {album['title']} ({album['year']})")
                    userInput = input()
            else:
                print("Error: File is empty.")
    except FileNotFoundError:
        print("Error: File not found.")

if __name__ == "__main__":
    main()