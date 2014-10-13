#!/usr/bin/python2.7

# usage: vgs_pool.py [-h] [-a] [-r]
# optional arguments:
#   -h, --help       show this help message and exit
#   -a, --alternate  displays key combos and asks for the messages (default is
#                    the reverse)
#   -r, --rand       selects questions at random (default skews towards
#                    questions answered incorrectly in the past)

import argparse
import random 

# Set this value to control how many times more likely you are to see a given 
# card again if you answer it incorrectly (in the default "learning" mode)
multiplier = 4

# create and populate the master deck of questions
deck = {}

# Agressive
deck[('vaa', 'attack now!')] = 0
deck[('vad', 'dive!')] = 0
deck[('vaf', 'follow me')] = 0
deck[('vag', 'go!')] = 0
deck[('vas', 'stun now!')] = 0

# Enemy
deck[('ver', 'enemy has rune')] = 0
deck[('veh', 'invisible enemy nearby!')] = 0
deck[('vec', 'enemy incoming!')] = 0
deck[('ved', 'they have detection')] = 0

# Fluff
deck[('vfu', 'dont give up!')] = 0
deck[('vfg', 'game is hard')] = 0
deck[('vfl', 'good luck, have fun')] = 0
deck[('vfb', 'my bad')] = 0
deck[('vfm', 'new meta')] = 0
deck[('vfn', 'nice')] = 0
deck[('vfo', 'okay.')] = 0
deck[('vfe', 'i immediately regret my decision')] = 0
deck[('vfr', 'relax, youre doing fine')] = 0
deck[('vfs', 'sorry')] = 0
deck[('vft', 'thanks!')] = 0
deck[('vfh', 'that just happened')] = 0
deck[('vfw', 'well played!')] = 0

# Global Strategy
deck[('vgg', 'group up')] = 0
deck[('vgi', 'initiate!')] = 0
deck[('vgp', 'push now')] = 0
deck[('vgm', 'lets smoke gank')] = 0
deck[('vgf', 'split up and farm')] = 0
deck[('vgs', 'split push')] = 0

# Devices (items)
deck[('vdm', 'building mekansm')] = 0
deck[('vdp', 'building pipe')] = 0
deck[('vdc', 'buy a courier please')] = 0
deck[('vdt', 'buy a teleport scroll')] = 0
deck[('vdw', 'we need wards')] = 0
deck[('vdu', 'can anyone upgrade the courier?')] = 0
deck[('vdd', 'we need detection')] = 0

# Lane
deck[('vld', 'deny the tower!')] = 0
deck[('vlr', 'requesting a gank')] = 0
deck[('vlt', 'fight under the tower')] = 0

# Neutrals
deck[('vnj', 'jungling')] = 0
deck[('vnp', 'pull creeps please')] = 0
deck[('vnr', 'roshan')] = 0
deck[('vna', 'stack and pull please')] = 0
deck[('vns', 'stack neutrals')] = 0

# Quick
deck[('vqa', 'affirmative')] = 0
deck[('vqc', 'careful!')] = 0
deck[('vqq', 'current time')] = 0
deck[('vqb', 'get back!')] = 0
deck[('vqh', 'help!')] = 0
deck[('vqp', 'pause please!')] = 0
deck[('vqs', 'spread out')] = 0
deck[('vqw', 'wait')] = 0

# Self
deck[('vsb', 'be right back')] = 0
deck[('vsc', 'skills on cooldown')] = 0
deck[('vsh', 'heal')] = 0
deck[('vsm', 'mana')] = 0
deck[('vsw', 'on my way')] = 0
deck[('vsq', 'out of mana')] = 0
deck[('vsp', 'pulling creeps')] = 0
deck[('vsu', 'ultimate ready')] = 0

# Team
deck[('vtb', 'bait')] = 0
deck[('vtr', 'check runes please')] = 0
deck[('vtd', 'deward please')] = 0
deck[('vtg', 'get ready')] = 0
deck[('vtc', 're-use courier')] = 0

# Where did they go
deck[('vwa', 'all enemy heroes missing!')] = 0
deck[('vww', 'missing (lane)!')] = 0
deck[('vwb', 'missing bottom!')] = 0
deck[('vwg', 'missing mid!')] = 0
deck[('vwt',  'missing top!')] = 0
deck[('vwr', 'enemy returned')] = 0


# create and populate the dictionary of categories
cat = {}
cat['a'] = 'aggressive'
cat['e'] = 'enemy'
cat['f'] = 'fluff'
cat['g'] = 'global strategy'
cat['d'] = 'devices'
cat['l'] = 'lane'
cat['n'] = 'neutrals`'
cat['q'] = 'quick'
cat['s'] = 'self'
cat['t'] = 'team'
cat['w'] = 'where'


def percent(correct, total):
    '''
    Given a number of correct answers and a number of total answers, returns
    the percentage (an integer on [0,100]) of correct answers.
    '''
    assert (correct <= total)
    if total == 0: return 100
    correct = correct * 100.0
    return int(correct / total)


def group(code, categories):
    '''
    Given a three letter code string, returns as a string the category name 
    indicated by the middle letter of the code (as given in the category 
    dictionary)
    '''
    assert (len(code) == 3)
    middle = code[1]
    if middle in categories:
        return categories[middle]
    else:
        assert false

def get_key(tup):
    '''
    Given a tuple of at least length 2, returns element index 1
    '''
    assert(len(tup) > 1)
    return tup[1]


# populate the pool that questions are drawn from, and update the deck counts
# to reflect the fact that there is now one copy of every card in the pool
pool = [card for card in deck]
for card in deck: deck[card] = 1

# initialize score variables
ncorrect = 0
ntotal = 0

# parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a',
                    '--alternate',
                    help='displays key combos and asks for the messages (default is the reverse)',
                    action='store_true')
parser.add_argument('-r',
                    '--rand',
                    help='selects questions at random (default skews towards questions answered incorrectly in the past)',
                    action='store_true')
args = parser.parse_args()


# begin run-time loop
print 'Commands: [q]uit, [p]rint card info, [r]eset score.'
print 'Selection mode: Random' if args.rand else 'Selection mode: Learning'
print 'Write messages:' if args.alternate else 'Write abbreviations:'
while True:

    # select the question (command-line flag determines selection method)
    card = random.choice(deck.keys()) if args.rand else random.choice(pool)

    # select side of card to display (command-line flag determines side)
    if args.alternate:
        q = 0
        a = 1
    else:
        q = 1
        a = 0

    n = raw_input('\n' + card[q] + ' - ')

    # if input matches the answer
    if n == card[a]:
        ncorrect += 1
        ntotal += 1
        assert(deck[card] > 0)
        if deck[card] > 1:
            deck[card] -= 1
            pool.remove(card)
        print 'correct!   ' + \
              str(ncorrect) + '/' + str(ntotal) + '   ' + \
              str(percent(ncorrect, ntotal)) + '%'

    # if input is "quit"
    elif n == 'q':
        print '\nquitting...'
        break

    # if input is "reset"
    elif n == 'r':
        print '\nresetting...'
        ncorrect = 0
        ntotal = 0
        pool = [card for card in deck]
        for card in deck: deck[card] = 1

    # if input is "print"
    elif n == 'p':
        print '\nnumber\tcode\tmessage'
        print '--------------------------'
        for card in sorted(deck, key=get_key):
            print str(deck[card]) + '\t' + card[0] + '\t' + card[1]

    # if input doesn't match any expected patterns
    else:
        ntotal += 1
        assert(deck[card] > 0)
        old_count = deck[card]
        deck[card] *= multiplier
        for i in range(deck[card] - old_count):
            pool.append(card)
        print 'incorrect. ' + \
              str(ncorrect) + '/' + str(ntotal) + '   ' + \
              str(percent(ncorrect, ntotal)) + '%'
        if any(card for card in deck if card[0] == n):
            actual_card = next(card for card in deck if card[0] == n)
            print 'you typed "' + actual_card[q] + '"'
        print 'should be: "' + card[a] + '" (group "' + group(card[0], cat) + '")'