import re
import sys
from mpi4py import MPI
from datetime import datetime
from collections import Counter

# 获取查询单词
query = 'melbourne'
if len(sys.argv) >= 2 and sys.argv[1]:
    query = sys.argv[1]

path = '/Users/hayden/Desktop/miniTwitter.csv'

# 初始化MPI变量
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
mode = MPI.MODE_RDONLY

# 开始时间
beginning = datetime.now().timestamp()

# 读取文件
twitters = open(path, 'r')

# 按结点不同分别处理数据
if rank == 0:
    # 当结点为跟结点,把文件读取成为数组,并删除文件头
    single_twitter = twitters.readlines()
    del single_twitter[0]
    # 将twitter列表按结点数拆分
    twitter_chunks = [[] for _ in range(size)]
    for i, chunk in enumerate(single_twitter):
        twitter_chunks[i % size].append(chunk)
else:
    # 当结点不是根结点
    data = None
    chunks = None
# 将分割好的twitter列表分发给各个结点
data = comm.scatter(twitter_chunks, root=0)

# 每个结点,包括根结点,都要处理的数据
# 用来存储每个结点统计的信息
query_per_process = Counter()
users_per_process = Counter()
topic_per_process = Counter()

# 逐行搜索,并新计数器
for item in twitter_chunks:
    queryPerItem = re.findall(query, item.lower())
    usersPerItem = re.findall(r'(?<=@)\w+', item.lower())
    topicPerItem = re.findall(r'(?<=#)\w+', item.lower())
    query_per_process.update(queryPerItem)
    users_per_process.update(usersPerItem)
    topic_per_process.update(topicPerItem)

# Gathering Data
local_data = (query_per_process, users_per_process, topic_per_process)
combine_data = comm.gather(local_data,root=0)

if rank == 0:
     # 初始化计数器
     query_count = Counter()
     users_count = Counter()
     topic_count = Counter()
     for data_tuple in combine_data:
         query_count.update(data_tuple[0])
         users_count.update(data_tuple[1])
         topic_count.update(data_tuple[2])







# print(query_count.most_common(), end='\n')
# print(users_count.most_common(10), end='\n')
# print(topic_count.most_common(10), end='\n')

# 结束时间
ending = datetime.now().timestamp()


# 只在根结点打印信息
if rank == 0:
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
