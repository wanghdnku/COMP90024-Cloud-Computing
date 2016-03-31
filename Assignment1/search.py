import re
import sys
from datetime import datetime
from collections import Counter

# 获取查询单词
query = 'melbourne'
if len(sys.argv) >= 2 and sys.argv[1]:
    query = sys.argv[1]

# 初始化计数器
query_count = Counter()
users_count = Counter()
topic_count = Counter()

path = '/Users/hayden/Desktop/miniTwitter.csv'

# 开始时间
beginning = datetime.now().timestamp()

twitters = open(path, 'r')

# 把文件读取成为数组,并删除文件头
single_twitter = twitters.readlines()
del single_twitter[0]

# 逐行搜索,并新计数器
for item in single_twitter:
    queryPerItem = re.findall(query, item.lower())
    usersPerItem = re.findall(r'(?<=@)\w+', item.lower())
    topicPerItem = re.findall(r'(?<=#)\w+', item.lower())
    query_count.update(queryPerItem)
    users_count.update(usersPerItem)
    topic_count.update(topicPerItem)

# print(query_count.most_common(), end='\n')
# print(users_count.most_common(10), end='\n')
# print(topic_count.most_common(10), end='\n')

# 结束时间
ending = datetime.now().timestamp()
# 计算所用时间
duration = str("%.2f" % (ending - beginning))
print('\n\nDuration: %s s' % duration)

# 打印结果
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
