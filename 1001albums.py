import random

print("Can't decide what to listen to?")
albumList = []
try:
    with open("albums.txt", "r", encoding="UTF-8") as file:
        for line in file:
            albumList.append(line.strip())
    if albumList:
        userInput = input("Press ENTER for a random album, Q to quit. ")
        while userInput.upper() != "Q":
            randomIndex = random.randint(0, len(albumList) - 1)
            userInput = input(str(randomIndex + 1) + ". " + albumList[randomIndex] + " ")
    else:
        print("Error: File is empty.")
except FileNotFoundError:
    print("Error: File not found.") 