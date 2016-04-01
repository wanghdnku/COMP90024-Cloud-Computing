#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import some module used in this program.
import re
import sys
from mpi4py import MPI
from datetime import datetime
from collections import Counter

# Record the begining time.
beginning = datetime.now().timestamp()

# Set the query word, if users input words from console, then replace it.
query = 'melbourne'
if len(sys.argv) >= 2 and sys.argv[1]:
    query = sys.argv[1]

# Initialize MPI variables.
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
mode = MPI.MODE_RDONLY

# Set the path of twitter file, then open it.
path = 'twitter.csv'
twitter_file = open(path, 'r', encoding='utf-8')

# Do different tasks in different rank.
if rank == 0:
    # Read twitter file as a list of twitters, each element of this list is a
    # twitter. The header of twitter file is also been moved.
    twitter_list = twitter_file.readlines()
    del twitter_list[0]
    # Create a now twitter_chunks which is a list of list.
    twitter_chunks = [[] for _ in range(size)]
    for i, chunk in enumerate(twitter_list):
        twitter_chunks[i % size].append(chunk)
else:
    # Do nothing is the rank isn't the root
    twitter_list = None
    twitter_chunks = None
# Each rank get their data from satter.
local_chunk = comm.scatter(twitter_chunks, root=0)

# Create 3 counters to record statistical data.
query_per_chunk = Counter()
users_per_chunk = Counter()
topic_per_chunk = Counter()

# Search each line of chunk, update counters.
for item in local_chunk:
    queryPerItem = re.findall(query, item.lower())
    usersPerItem = re.findall(r'(?<=@)\w+', item.lower())
    topicPerItem = re.findall(r'(?<=#)\w+', item.lower())
    query_per_chunk.update(queryPerItem)
    users_per_chunk.update(usersPerItem)
    topic_per_chunk.update(topicPerItem)

# Gathering data as a tuple.
local_data = (query_per_chunk, users_per_chunk, topic_per_chunk)
combine_data = comm.gather(local_data,root=0)

# Add counters from each chunk together at the root.
if rank == 0:
    query_count = Counter()
    users_count = Counter()
    topic_count = Counter()
    for data_tuple in combine_data:
        query_count.update(data_tuple[0])
        users_count.update(data_tuple[1])
        topic_count.update(data_tuple[2])

# Record the end time.
ending = datetime.now().timestamp()


# Printing the data and formatting.
if rank == 0:
    # Printing the result.
    dotFormat = 0
    print('\n================= Word Frequency ==================')
    for (query, times) in query_count.most_common():
        print(' ' + query + ' ', end='')
        dotFormat = 41 - len(str(times)) - len(query)
        while dotFormat > 0:
            print('.', end='')
            dotFormat -= 1
        print(' %s times' % times)

    print('\n================== Top10 Users ====================')
    for (names, times) in users_count.most_common(10):
        print(' @' + names + ' ', end='')
        dotFormat = 40 - len(str(times)) - len(names)
        while dotFormat > 0:
            print('.', end='')
            dotFormat -= 1
        print(' %s times' % times)

    print('\n================== Top10 Topics ===================')
    for (topic, times) in topic_count.most_common(10):
        print(' #' + topic + ' ', end='')
        dotFormat = 40 - len(str(times)) - len(topic)
        while dotFormat > 0:
            print('.', end='')
            dotFormat -= 1
        print(' %s times' % times)

    # Calculating the duration time.
    duration = str("%.2f" % (ending - beginning))
    print('\nDuration of work: %s s' % duration)
