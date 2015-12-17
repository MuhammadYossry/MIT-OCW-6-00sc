from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    max_len = HAND_SIZE
    word_list_set = set(word_list)
    for n in range(HAND_SIZE, 0, -1):
        perms = get_perms(hand, n)
        match_set = word_list_set & set(perms)
        if len(match_set) > 0:
            return match_set.pop() # Return an element from the set
    return '.' # Method failed, '.' to end the tries
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    total_score = 0
    hand_ = copy.deepcopy(hand)
    done = False
    while not done:
        print "Current Hand:",
        display_hand(hand_)
        in_word = comp_choose_word(hand_, word_list)
        print "The computer entered: %s" % (in_word,)
        if in_word == '.':
            done = True
        elif is_valid_word(in_word, hand_, word_list):
            score = get_word_score(in_word, HAND_SIZE)
            total_score += score
            hand_ = update_hand(hand_, in_word)
            print '"%s" earned %i points. Total: %i points' % (in_word, score, total_score)
            if len(hand_) == 0:
                done = True
        else:
            print 'Invalid word, please try again.'

    print "Total score: %i points." % (total_score,)   
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # hand = deal_hand(HAND_SIZE)
    # comp_play_hand(hand, word_list)
    first_play = True
    player = ''
    while True:
        msg = 'Hi player. enter \'n\' to play a new random hand, '
        if not first_play:
            msg += "'r' to play the last hand, "
        msg += "'e' to exit the game: "
        ans = raw_input(msg)
        while True:
            player = raw_input("enter 'u' to play, enter 'c' to let the computer play: ")
            if player == 'u':
                play_hand_ = play_hand
            elif player == 'c':
                play_hand_ = comp_play_hand
            else:
                continue
            break
        if ans == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand_(hand,word_list)
            first_play = False
        elif ans == 'r' and not first_play:
            play_hand_(hand,word_list)
        elif ans == 'e':
            return
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
