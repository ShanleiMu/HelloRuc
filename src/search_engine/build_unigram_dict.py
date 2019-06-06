import json
import math
import re
import jieba
from pypinyin import lazy_pinyin

# 对单字纠错
# unig = dict()
# pinyin = dict()
# corpus = open('../data/processed_data/ruc_content.txt','r',encoding='utf-8')
# wf = open('../data/unig_dict.json','w',encoding='utf-8')
# wf2 = open('../data/pinyin_dict.json','w',encoding='utf-8')
# n = 0
# for line in corpus.readlines():
# 	cut = line.strip().split('|||')[-1]
# 	line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）\{\};；”“:：a-zA-Z]+", "",cut)
# 	for i in range(len(line)-1):
# 		if line[i] not in unig.keys():
# 			unig[line[i]] = dict()
# 			unig[line[i]]['count'] = 0
# 		if line[i+1] not in unig[line[i]].keys():
# 			unig[line[i]][line[i+1]]=0
# 		unig[line[i]][line[i+1]] += 1
# 		unig[line[i]]['count'] += 1

# 		py = lazy_pinyin(line[i+1])[0]
# 		if py not in pinyin.keys():
# 			pinyin[py] = [line[i+1]]
# 		elif line[i+1] not in pinyin[py]:
# 			pinyin[py].append(line[i+1])
# 	n += 1
# 	if n % 500 == 0:
# 		print(n)

# for key1 in list(unig.keys()):
# 	count = unig[key1]['count']
# 	for key2 in list(unig[key1].keys()):
# 		if key2 == 'count':
# 			continue
# 		unig[key1][key2] = math.log(1.0 * unig[key1][key2] / count + 1e-9)

# jsonObj = json.dumps(unig, ensure_ascii=False)
# wf.write(jsonObj)
# jsonObj = json.dumps(pinyin, ensure_ascii=False)
# wf2.write(jsonObj)


# 对词纠错
unig = dict()
pinyin = dict()
corpus = open('../data/processed_data/ruc_content.txt','r',encoding='utf-8')
wf = open('../data/unig_term_dict.json','w',encoding='utf-8')
wf2 = open('../data/pinyin_term_dict.json','w',encoding='utf-8')
n = 0
for line in corpus.readlines():
	cut = line.strip().split('|||')[-1]
	line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）\{\};；”“:：a-zA-Z]+", "",cut)
	line = list(jieba.cut(line))
	for i in range(len(line)-1):
		if line[i] not in unig.keys():
			unig[line[i]] = dict()
			unig[line[i]]['count'] = 0
		if line[i+1] not in unig[line[i]].keys():
			unig[line[i]][line[i+1]]=0
		unig[line[i]][line[i+1]] += 1
		unig[line[i]]['count'] += 1

		py = "".join(lazy_pinyin(line[i+1]))
		if py not in pinyin.keys():
			pinyin[py] = [line[i+1]]
		elif line[i+1] not in pinyin[py]:
			pinyin[py].append(line[i+1])
	n += 1
	if n % 500 == 0:
		print(n)

for key1 in list(unig.keys()):
	count = unig[key1]['count']
	for key2 in list(unig[key1].keys()):
		if key2 == 'count':
			continue
		unig[key1][key2] = math.log(1.0 * unig[key1][key2] / count + 1e-9)

jsonObj = json.dumps(unig, ensure_ascii=False)
wf.write(jsonObj)
jsonObj = json.dumps(pinyin, ensure_ascii=False)
wf2.write(jsonObj)