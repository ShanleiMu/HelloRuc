import json
import configparser
from pypinyin import lazy_pinyin
import jieba

class Corrector:
	"""docstring for Corrector"""
	def __init__(self, config_path, config_encoding):

		self.config_path = config_path
		self.config_encoding = config_encoding
		config = configparser.ConfigParser()
		config.read(config_path, config_encoding)
		
		self.dict = self.read_dict(config['DEFAULT']['ngram'])
		self.pinyin = self.read_dict(config['DEFAULT']['pinyin'])
		self.dict_term = self.read_dict(config['DEFAULT']['ngram_term'])
		self.pinyin_term = self.read_dict(config['DEFAULT']['pinyin_term'])
		self.threshold = float(config['DEFAULT']['threshold'])
		# print(self.dict)

	def read_dict(self, path):
		rf = open(path,'r',encoding='utf-8')
		return json.loads(rf.readline().strip())

	def replace(self, query, loc, ngdict, pydict, use_term = False):
		diff = 2
		if not use_term:
			query = list(query)
			diff = 5
		py = "".join(lazy_pinyin(query[loc]))
		max_value = -10000
		choice = query[loc]
		gt_value = -10.0
		if py not in pydict.keys():
			return False, "".join(query)
		for word in pydict[py]:
			p = -10000
			if loc-1>=0 and query[loc-1] in ngdict.keys() and word in ngdict[query[loc-1]].keys():
				p = ngdict[query[loc-1]][word]
			if loc+1<len(query) and word in ngdict.keys() and query[loc+1] in ngdict[word].keys():
				if p > -10000:
					p = max(p, ngdict[word][query[loc+1]]) / 2
				else:
					p = max(p, ngdict[word][query[loc+1]])
			if p > max_value:
				max_value = p
				choice = word
			if word == query[loc]:
				gt_value = p

		if max_value > -1.5 or (max_value > -5 and max_value - gt_value > diff):
			query[loc] = choice
			return True, query
		else:
			return False, query

	def detect(self, query, ngdict, pydict, use_term = False):
		update = False
		thd = self.threshold
		if use_term:
			query = list(jieba.cut(query))
			thd = self.threshold / 2
			# print(query)
		for i, word in enumerate(query):
			right, left = True, True
			if i != 0 and query[i-1] != " ":
				if query[i-1] in ngdict.keys() and (word not in ngdict[query[i-1]].keys() or ngdict[query[i-1]][word] < thd):
					left = False
			if i != len(query)-1 and query[i+1] != " ":
				if word in ngdict.keys() and (query[i+1] not in ngdict[word].keys() or ngdict[word][query[i+1]] < thd):
					right = False

			if (not right or not left) or (word not in ngdict.keys()):
				update, query = self.replace(query, i, ngdict, pydict, use_term)

		return update, "".join(query)


# corrector = Corrector('./config.ini', 'utf-8')
# # print(corrector.dict['北']['美'])
# while True:
# 	update1, query = corrector.detect(input('query: '), corrector.dict, corrector.pinyin)
# 	update2, query = corrector.detect(query, corrector.dict_term, corrector.pinyin_term, True)
# 	print(query)

# 中国人民大学室外场地使用申请表
# 刘伟校长走访慰问