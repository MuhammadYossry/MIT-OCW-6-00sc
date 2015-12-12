# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

def print_line_sep():
    print '----------'

def get_placeholder(word,right_guessed_chars):
    place_holder = ''
    for char in word:
        if char in right_guessed_chars:
            place_holder += char
        else:
            place_holder += '-'
    return place_holder

def guess_word(word):
    """
    word(string): the word you want the use to guess

    Returns a Bool represents if the the user succeeded to guess the word or not
    """
    n_tries = 8
    right_guessed_chars = []
    avail_letters = string.lowercase
    place_holder = get_placeholder(word, right_guessed_chars)

    for n in range(n_tries):
        print_line_sep()
        print "You have %i guesses left." %((n_tries - n),)
        print "Available letters: %s" % (avail_letters,)
        in_char = raw_input("Please guess a letter:")
        in_char = in_char.lower()
        if in_char in word:
            right_guessed_chars.append(in_char)
            place_holder = get_placeholder(word, right_guessed_chars)
            avail_letters.replace(in_char, '')
            print "Good guess: %s" % (place_holder,)
            if place_holder == word:
                return True # You won!
        else:
            print "Oops! That letter is not in my word: %s" % (place_holder,)
    return False


wordlist = load_words()

print 'Welcome to the game, Hangman!'
word = choose_word(wordlist)
print "I am thinking of a word that is %i letters long." % (len(word),)

won = guess_word(word)

print_line_sep()
if won:
    print 'Congratulations, you won!'
else:
    print "Hard luck, the word was %s" % (word,)