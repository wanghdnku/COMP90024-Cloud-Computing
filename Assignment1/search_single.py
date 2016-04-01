import re
import sys
from datetime import datetime
from collections import Counter

query = 'melbourne'
if len(sys.argv) >= 2 and sys.argv[1]:
    query = sys.argv[1]

query_count = Counter()
users_count = Counter()
topic_count = Counter()

path = '/Users/hayden/Desktop/miniTwitter.csv'

beginning = datetime.now().timestamp()

twitters = open(path, 'r', encoding='utf-8')

single_twitter = twitters.readlines()
del single_twitter[0]

for item in single_twitter:
    queryPerItem = re.findall(query, item.lower())
    usersPerItem = re.findall(r'(?<=@)\w+', item.lower())
    topicPerItem = re.findall(r'(?<=#)\w+', item.lower())
    query_count.update(queryPerItem)
    users_count.update(usersPerItem)
    topic_count.update(topicPerItem)


ending = datetime.now().timestamp()
duration = str("%.2f" % (ending - beginning))
print('\n\nDuration: %s s' % duration)

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
