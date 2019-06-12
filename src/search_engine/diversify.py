import numpy as np


# 获取results列表中所有document的caption
# 为降低运算复杂度对document进行切分，切分尺寸为length
def GetCaption(docs, results, query_terms, length = 88):
	captions = dict()
	for item in results:
		docid = item[0]
		try:
			content = docs[docid][-1]
		except:
			print("error! " + docid + " not found")
			captions[docid] = "未找到该文档信息"

		num = int(len(content) / length) + 1
		count = list(np.zeros(num, dtype=int))
		for term in query_terms:
			last = 0
			while True:
				loc = content.find(term, last)
				if loc == -1:
					break
				else:
					count[int(loc / length)] += 1
					last = loc + 1
		idx = count.index(max(count))

		start = idx * length
		while content[start] not in ['，',',','。','.','!','！',';','；'] and start > -1:
			start -= 1
		start += 1
		end = min(start + length, len(content))
		content = content[start: end]
		for term in query_terms:
			last = 0
			while True:
				loc = content.find(term, last)
				if loc == -1:
					break
				else:
					content = content[:loc] + "<strong>" + content[loc:loc+len(term)] + "</strong>" + content[loc+len(term):]
					last = loc + 17 + len(term)
		captions[docid] = content + '...'
	return captions