#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================ #
#  File: search_mpi.py                                                         #
#  Author: Haidong Wang                                                        #
#  Student ID: 678725                                                          #
#  Input: This program can receive one string parameter in the console, this   #
#    parameter will be used to count it's frequency it appears in files.       #
#  Output: The search result will be print in the console, along with the wall #
#    time that the program costs.                                              #
#  Description: This is the program that search a csv file in parallel system. #
#    It can 1. find the frequency of given word, 2. find the top 10 popular    #
#    users, 3. find the top 10 popular topics.                                 #
# ============================================================================ #


# import some module used in this program.
import re
import sys
from datetime import datetime
from collections import Counter


# ---------------------------------------------------------------------------- #


# This function will divede a twitter file into a list of lines, the size of
# the list is appointed by the parameter: piece_size.
def divide_file(file, piece_size=1024 * 1024 * 50):
    # Divide file by lines. Each piece is default size.
    while True:
        file_lines = file.readlines(piece_size)
        if not file_lines:
            break
        yield file_lines


# ---------------------------------------------------------------------------- #


# Record the beginning time.
program_start_time = datetime.now().timestamp()

# Set the query word, if users input words from console, then replace it.
query = 'melbourne'
if len(sys.argv) >= 2 and sys.argv[1]:
    query = sys.argv[1]

# Set the path of twitter file, then open it.
path = 'twitter.csv'
# Open the file.
with open(path, 'r', encoding='utf-8') as twitter_file:
    sum_query = Counter()
    sum_users = Counter()
    sum_topic = Counter()

    parallel_time = 0

    # Divide large file into blocks
    for twitter_list in divide_file(twitter_file):
        # Do different tasks in different rank.

        # Start record the time that program start running in parallel
        parallel_start_time = datetime.now().timestamp()

        # Search each line of chunk, update counters.
        for item in twitter_list:
            # This regex will find all 'query word' in one twitter.
            queryPerItem = re.findall(query, item.lower())
            # This regex will find all 'user'(start with @) in one twitter.
            usersPerItem = re.findall(r'(?<=@)\w+', item.lower())
            # This regex will find all 'topic'(start with #) in one twitter.
            topicPerItem = re.findall(r'(?<=#)\w+', item.lower())
            # Store the results in counters.
            sum_query.update(queryPerItem)
            sum_users.update(usersPerItem)
            sum_topic.update(topicPerItem)

        # Start record the end time that program running in parallel
        parallel_end_time = datetime.now().timestamp()

        parallel_time += (parallel_end_time - parallel_start_time)

#### The file is now been closed.

# Record the end time.
program_end_time = datetime.now().timestamp()

# ---------------------------------------------------------------------------- #


# Printing the data and formatting.
# Printing the result.
dotFormat = 0
print('\n================= Word Frequency ==================')
for (query, times) in sum_query.most_common():
    print(' ' + query + ' ', end='')
    dotFormat = 41 - len(str(times)) - len(query)
    while dotFormat > 0:
        print('.', end='')
        dotFormat -= 1
    print(' %s times' % times)

print('\n================== Top10 Users ====================')
for (names, times) in sum_users.most_common(10):
    print(' @' + names + ' ', end='')
    dotFormat = 40 - len(str(times)) - len(names)
    while dotFormat > 0:
        print('.', end='')
        dotFormat -= 1
    print(' %s times' % times)

print('\n================== Top10 Topics ===================')
for (topic, times) in sum_topic.most_common(10):
    print(' #' + topic + ' ', end='')
    dotFormat = 40 - len(str(times)) - len(topic)
    while dotFormat > 0:
        print('.', end='')
        dotFormat -= 1
    print(' %s times' % times)

# Calculating the time of wall.
duration_time = str("%.2f" % (program_end_time - program_start_time))
# Calculating the time of program running in the parallel process.
parallel_time = str("%.2f" % (parallel_time))
print('\n[ Time of wall     : %s s ]' % duration_time)
print('\n[ Time of parallel : %s s ]' % parallel_time)
