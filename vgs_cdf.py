#!/usr/local/bin/python2.7

# usage: vgs_cdf.py [-h] [-a] [-r]
# optional arguments:
#   -h, --help       show this help message and exit
#   -a, --alternate  displays key combos and asks for the messages (default is
#                    the reverse)
#   -r, --rand       selects questions at random (default skews towards
#                    questions answered incorrectly in the past)

import argparse
import bisect
import collections
import pprint
import random


def percent(correct, total):
    '''
    Given a number of correct answers and a number of total answers, returns
    the percentage (an int on [0,100]) that "correct" is of "total".
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


def cdf(weights):
    '''
    Given a list of weights, returns a list containing the cumulative
    distribution function (values all on [0,1])
    '''
    # algorithm taken from
    # stackoverflow.com/questions/4113307/pythonic-way-to-select-list-elements-
    # with-different-probability

    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        if total == 0:
            result.append(0)
        else:
            result.append(cumsum / total)
    return result


def choice(population, weights):
    '''
    Given a list of choices and a list of corresponding weights, make a choice
    biased towards higher weighted choices.  Returns a member of "population".
    '''
    # algorithm taken from
    # stackoverflow.com/questions/4113307/pythonic-way-to-select-list-elements-
    # with-different-probability

    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)

    return population[idx]


def get_question(questions, scores, rand):
    '''
    Given a dictionary of questions, choose one and return it as a 2-tuple.
    If the random flag is set, choose the question completely at random.  
    Otherwise skew towards questions answered incorrectly in the past 
    (according to the dictionary of scores).
    '''
    if rand:
        # choose and return a question/answer pair from "questions"
        return random.sample(questions.items(), 1)[0]
    else:

        # make a list of question keys using "questions", and using that list
        # make a corresponding list of weights using "scores"
        lquestions = [key for key in questions]
        lweights = [scores[key][2] for key in lquestions]

        # choose a question and return question/answer 2-tuple
        chosen_key = choice(lquestions, lweights)
        return (chosen_key, questions[chosen_key])


# set up the command-line argument parser
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

# create the dictionary of categories
categories = {}
categories['a'] = 'aggressive'
categories['e'] = 'enemy'
categories['f'] = 'fluff'
categories['g'] = 'global strategy'
categories['d'] = 'devices'
categories['l'] = 'lane'
categories['n'] = 'neutrals`'
categories['q'] = 'quick'
categories['s'] = 'self'
categories['t'] = 'team'
categories['w'] = 'where'

by_key = {}         # dictionary of chats keyed on key combination
by_message = {}     # dictionary of chats keyed on displayed text

# populate the by_key dictionary

# Agressive
by_key['vaa'] = 'attack now!'
by_key['vad'] = 'dive!'
by_key['vaf'] = 'follow me'
by_key['vag'] = 'go!'
by_key['vas'] = 'stun now!'

# Enemy
by_key['ver'] = 'enemy has rune'
by_key['veh'] = 'invisible enemy nearby!'
by_key['vec'] = 'enemy incoming!'
by_key['ved'] = 'they have detection'

# Fluff
by_key['vfu'] = 'dont give up!'
by_key['vfg'] = 'game is hard'
by_key['vfl'] = 'good luck, have fun'
by_key['vfb'] = 'my bad'
by_key['vfm'] = 'new meta'
by_key['vfn'] = 'nice'
by_key['vfo'] = 'okay.'
by_key['vfe'] = 'i immediately regret my decision'
by_key['vfr'] = 'relax, youre doing fine'
by_key['vfs'] = 'sorry'
by_key['vft'] = 'thanks!'
by_key['vfh'] = 'that just happened'
by_key['vfw'] = 'well played!'

# Global Strategy
by_key['vgg'] = 'group up'
by_key['vgi'] = 'initiate!'
by_key['vgp'] = 'push now'
by_key['vgm'] = 'lets smoke gank'
by_key['vgf'] = 'split up and farm'
by_key['vgs'] = 'split push'

# Devices (items)
by_key['vdm'] = 'building mekansm'
by_key['vdp'] = 'building pipe'
by_key['vdc'] = 'buy a courier please'
by_key['vdt'] = 'buy a teleport scroll'
by_key['vdw'] = 'we need wards'
by_key['vdu'] = 'can anyone upgrade the courier?'
by_key['vdd'] = 'we need detection'

# Lane
by_key['vld'] = 'deny the tower!'
by_key['vlr'] = 'requesting a gank'
by_key['vlt'] = 'fight under the tower'

# Neutrals
by_key['vnj'] = 'jungling'
by_key['vnp'] = 'pull creeps please'
by_key['vnr'] = 'roshan'
by_key['vna'] = 'stack and pull please'
by_key['vns'] = 'stack neutrals'

# Quick
by_key['vqa'] = 'affirmative'
by_key['vqc'] = 'careful!'
by_key['vqq'] = 'current time'
by_key['vqb'] = 'get back!'
by_key['vqh'] = 'help!'
by_key['vqp'] = 'pause please!'
by_key['vqs'] = 'spread out'
by_key['vqw'] = 'wait'

# Self
by_key['vsb'] = 'be right back'
by_key['vsc'] = 'skills on cooldown'
by_key['vsh'] = 'heal'
by_key['vsm'] = 'mana'
by_key['vsw'] = 'on my way'
by_key['vsq'] = 'out of mana'
by_key['vsp'] = 'pulling creeps'
by_key['vsu'] = 'ultimate ready'

# Team
by_key['vtb'] = 'bait'
by_key['vtr'] = 'check runes please'
by_key['vtd'] = 'deward please'
by_key['vtg'] = 'get ready'
by_key['vtc'] = 're-use courier'

# Where did they go
by_key['vwa'] = 'all enemy heroes missing!'
by_key['vww'] = 'missing (lane)!'
by_key['vwb'] = 'missing bottom!'
by_key['vwg'] = 'missing mid!'
by_key['vwt'] = 'missing top!'
by_key['vwr'] = 'enemy returned'

# populate the by_message dictionary from the by_key dictionary
by_message = {contents: key for key, contents in by_key.iteritems()}

# initialize variables used in the runtime loop
live_dictionary = {}
introduction = ''
mode = ''
ntotal = 0
ncorrect = 0

# set question selection mode display message based on command-line flag
if args.rand:
    mode = 'Selection Mode: Random'
else:
    mode = 'Selection Mode: Learning'

# set quizzing mode display message based on command-line flag
if args.alternate:
    live_dictionary = by_key
    introduction = 'Write the corresponding messages.'
else:
    live_dictionary = by_message
    introduction = 'Write the corresponding key-codes.'

# initialize answers dictionary with starting values
answers = {key: [0, 0, 1.0] for key, contents in live_dictionary.iteritems()}

# enter runtime loop
print 'Commands: [q]uit, [p]rint per-question results, [r]eset score.'
print mode
print introduction
while True:
    # choose question, display it, and wait for user input
    pair = get_question(live_dictionary, answers, args.rand)
    n = raw_input('\n' + pair[0] + ' - ')

    # if input matches the answer
    if n == pair[1]:
        ncorrect += 1
        ntotal +=1
        answers[pair[0]][0] += 1
        answers[pair[0]][1] += 1
        answers[pair[0]][2] = answers[pair[0]][2] / 2
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
        answers = {key: [0, 0, 1.0] for key, contents in live_dictionary.iteritems()}

    # if input is "print"
    elif n == 'p':
        print "\n'question': [correct, total, weight]\n"
        pprint.pprint(answers)

    # if input doesn't match any expected patterns
    else:
        ntotal +=1
        answers[pair[0]][1] += 1
        print 'incorrect. ' + \
              str(ncorrect) + '/' + str(ntotal) + '   ' + \
              str(percent(ncorrect, ntotal)) + '%'
        if (not args.alternate) and n in by_key:
            print 'you typed "' + by_key[n] + '"'
        print 'should be: "' + pair[1] + '" (group "' + group(pair[1], categories) + '")'
