
import re
import sys
from collections import Counter
import datetime

# extract the twitter text from a csv line. by using the regular expression
# return a list - matchObj, and the text is matchObj(2).
def extractText( csvLine ):
   reFlags = re.M|re.I|re.U
   pattern = "\d+,\d+,\d+,\d+,(.*)text\"\":\"\"(.*)\"\",\"\"in_reply_to_status_id\"\":(.*)"
   matchObj = re.match(pattern, csvLine, reFlags)
   return matchObj

# count the frequence of target word in each line
# and return number.
def countTargetPerLine(target,twit):
    i = 0
    words = ''.join(c if c.isalnum() else ' ' for c in twit.lower()).split()

    for word in words:
        if(word == target):
            i = i+1
    return i

# find the @username in each line and return them as a list
def findUserPerLine(twit):
   users = re.findall(r"(?<=@)\w+",twit.lower())
   return users

# find the #topic in each line and return them as a list
def findTopicPerLine(twit):
   topics = re.findall(r"(?<=#)\w+",twit.lower())
   return topics

# add a list of terms to the Counter()
def appendTermsToDict(term_dict,terms):
   line_count = Counter(terms)
   term_dict = term_dict + line_count
   return term_dict

# aggrate the functions above.
def countAll(query, twit_list):
   query_count = 0
   user_dict = Counter()
   topic_dict = Counter()

   for twit in twit_list:

      query_count += countTargetPerLine(query,twit)

      users = findUserPerLine(twit)
      user_dict = appendTermsToDict(user_dict,users)

      topics = findTopicPerLine(twit)
      topic_dict = appendTermsToDict(topic_dict,topics)

   return [query_count, user_dict, topic_dict]

#--- main code start here --------
#-----------------------------
# if there is an command argument, take it as query word
# and the default query word is ash
query_word = "ash"
if(len(sys.argv)>=2):
    if(sys.argv[1]):
        query_word = sys.argv[1]

print("Will count the word: %s" % query_word)
print()

query_count = 0
user_count = Counter()
topic_count = Counter()

# ------------------------
start_time = datetime.datetime.now().timestamp()

# open the csv file.
with open('/Users/hayden/Desktop/miniTwitter.csv','r') as twitters:
    for line in twitters:
        twit_group = extractText(line)
        if(twit_group):
            twit = twit_group.group(2)
            query_count += countTargetPerLine(query_word,twit)

            users = findUserPerLine(twit)
            user_count = appendTermsToDict(user_count,users)
            topics = findTopicPerLine(twit)
            topic_count = appendTermsToDict(topic_count,topics)

# 32 位

count = 0
print('=========== Word Frequency ===========')
print(query_word + ' ', end = '')
count = 30 - len(str(query_count)) - len(query_word)
while(count > 0):
    print('.', end = '')
    count -= 1
print(' %s times\n' % query_count)

print('============ Top10 Users =============')
for (name, times) in user_count.most_common(10):
    print('@' + name + ' ', end = '')
    count = 29 - len(str(times)) - len(name)
    while(count > 0):
        print('.', end = '')
        count -= 1
    print(' %s times' % times)
print()

print('============ Top10 Topics ============')
for (name, times) in user_count.most_common(10):
    print('#' + name + ' ', end = '')
    count = 29 - len(str(times)) - len(name)
    while(count > 0):
        print('.', end = '')
        count -= 1
    print(' %s times' % times)
print()

end_time = datetime.datetime.now().timestamp()
total_time = end_time - start_time
duration = str("%.2f" %total_time)
print('Duration: %s seconds' % duration)
