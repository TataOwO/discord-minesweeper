import random
import numpy as np

pyperclipExists = True

try:
    import pyperclip
except ImportError:
    pyperclipExists = False

numberTable = {"0":"zero","1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight","-1":"boom"}

def randomPos(size):
    return (random.randint(0, size[0]-1), random.randint(0, size[1]-1))

def checkStatus(array, pos):
    return array[pos[0]][pos[1]] == -1

def addMine(array, size):
    array = array.copy()
    pos = randomPos(size)
    while checkStatus(array, pos): pos = randomPos(size)
    array[pos[0]][pos[1]] = -1
    array = setNearbyNumbers(array, size, pos)
    return array

def generateMines(array, size, num):
    if num == 0: return array
    return generateMines(addMine(array, size), size, num-1)

def getNearbyPos(size, pos):
    x, y = pos
    nearby = []
    if x != 0:
        nearby.append((x-1, y))
        if y != 0:
            nearby.append((x-1, y-1))
        if y != size[1] - 1:
            nearby.append((x-1, y+1))
    if x != size[0] - 1:
        nearby.append((x+1, y))
        if y != 0:
            nearby.append((x+1, y-1))
        if y != size[1] - 1:
            nearby.append((x+1, y+1))
    if y != 0:
        nearby.append((x, y-1))
    if y != size[1] - 1:
        nearby.append((x, y+1))
    return nearby

def setNearbyNumbers(array, size, pos):
    for each in getNearbyPos(size, pos):
        if array[each[0]][each[1]] == -1: continue
        array[each[0]][each[1]] += 1
    return array

def generateField(size, mineCount):
    emptyField = np.zeros(size, dtype=int)
    field = generateMines(emptyField, size, mineCount)
    return field

# turn the mine field into a playable minesweeper text on Discord
def generateText(array, size):
    text = "Minesweeper\n"
    for x in range(size[0]):
        for y in range(size[1]):
            text += f"||:{numberTable[str(array[x][y])]}:||"
        text += "\n"
    return text

if __name__ == "__main__":
    size = tuple([int(x) for x in input('enter the size of the field by this format "x y": ').split(" ")])
    if len(size) != 2: raise Exception(f"wrong length. length given: {len(size)}")
    
    mineCount = int(input("how many mines: "))
    if size[0] * size[1] < mineCount: raise Exception(f"too many mines. max count: {size[0] * size[1]}")
    
    field = generateField(size, mineCount)

    print()
    print(field)
    print()
    
    text = generateText(field, size)
    
    print(text)
    if pyperclipExists:
        pyperclip.copy(text)
        print("\ncopied to clipboard!")
    else:
        print("pyperclip was not found! run `pip install pyperclip` so that the program can copy the text to your clipboard!")
