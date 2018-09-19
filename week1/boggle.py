# Schrijf een programma voor een NxN bord, waarbij N kan variëren. Het kan in minder dan 50 regels.
# Je hoeft geen GUI te maken, het mag gewoon met een CLI en gebaseerd op tekst.
# De file words.txt bevat een lijst met woorden die je kan gebruiken om te 'matchen'.
# Het is handig om hiervan eerst een lijst te maken in het geheugen van alle mogelijk prefixen.
# Prefixen van "MAT” zijn bijvoorbeeld “M" en "MA".
# Een 'geldige' toestand is een reeks van letters die overeenkomt met een prefix.
# Op basis van DFS kun je alle mogelijkheden aflopen.
# Een pad stopt wanneer de reeks letters niet voorkomt in de lijst met prefixen.

# Vraag: wat is de tijdcomplexiteit van je oplossing?
# Antwoord: wc: O(n²) (?) voor elke startpositie (coordinaat) is het mogelijk dat alle nodes bezocht worden
# (mogelijkheid is niet gelijk aan waarschijnlijkheid)

# Deze code is deels geïnspireerd door https://github.com/railto/boggle-solver/blob/master/boggle.py ,
# https://gist.github.com/RyanBalfanz/6116053 , en de slides van AI college 2

import os.path
import urllib.request
import urllib.error
import random


def get_words() -> tuple:
    """Get the word list to search in, if not present make one and use that"""
    wordlist = set()
    indices = set()
    if os.path.isfile("words.txt"):
        with open("words.txt", 'r', encoding='utf-8') as fd:
            for word in fd:
                word = word.rstrip('\n').upper()
                wordlist.add(word)
                for i in range(len(word)):
                    indices.add(word[:i + 1])
    else:
        print("words.txt not found\ndownloading new words.txt")
        try:
            download_words()
            get_words()
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            print(err.args)
            print("Couldn't download words.txt\nexiting")
            exit(1)
    return wordlist, indices


def generate_field(width: int, height: int):
    """"Populate the field with the letters from the alphabet for the given height and width"""
    alphabet = "ABCDEFGHIJKLMNOPRSTUVWZ" # no Q
    field = [[random.choice(alphabet) for x in range(width)] for y in range(height)]
    return field


def show_field(field):
    """"Rough print function for the 2D array that is field"""
    for row in field:
        print(row)


def download_words():
    """Download a list of (English) words using urllib"""
    url = "https://gist.githubusercontent.com/deekayen/4148741/raw/01c6252ccc5b5fb307c1bb899c95989a8a284616/1-1000.txt"
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        words = response.read().decode('utf-8')
        with open("words.txt", 'w') as fd:
            fd.write(words)


def successors(coordinates: tuple):
    """Find the coordinates next to one being passed"""
    row = coordinates[0]
    col = coordinates[1]

    left = (make_fit(row), make_fit(col - 1))
    right = (make_fit(row), make_fit(col + 1))
    up = make_fit(row - 1), make_fit(col)
    down = make_fit(row + 1), make_fit(col)
    return left, right, up, down


def make_fit(x: int):
    """Prevent going out of bounds"""
    #not pretty, unnecessary?
    if x < 0:
        x = n + x
    if x >= n:
        x = 0
    return x


def cobble(path):
    """Cobble together the letters from the coordinates in the path"""
    word = ""
    for coordinate in path:
        word += getfieldvalue(coordinate)
    return word


def find_all_paths(coordinate, path=[]):
    """Recursively find correct letter combinations for the coordinate"""
    path = path + [coordinate]
    word = cobble(path)
    if word not in indices:
        return
    if word in words:
        paths.append(path)

    for child in successors(coordinate):
        if child not in path:
            find_all_paths(child, path)

def getfieldvalue(coordinates: tuple):
    """Find a letter in the field by coordinate"""
    row = coordinates[0]
    col = coordinates[1]
    value = field[row][col]
    return value


# Defining global values for universal usage by methods
n = 5
field = [[]]
words, indices = get_words()
paths = []

def main():
    """Run through all the actions to find the words"""
    global field
    field = generate_field(n, n)
    show_field(field)
    all_coordinates = [(x, y) for x in range(n) for y in range(n)]
    for coordinate in all_coordinates:
        find_all_paths(coordinate)
    for path in paths:
        word = cobble(path)
        print(word)


if __name__ == "__main__":
    main()