import gensim
# 阈值和词向量还可以进行修改


class QueryExpansion:
    def __init__(self, embedding_path='src/data/gensim_vectors.txt'):
        print('loading word embedding ...')
        self.model = gensim.models.KeyedVectors.load_word2vec_format(embedding_path, binary=False)

    def expansion(self, keyword_dict):
        expand_words = []
        for keyword in keyword_dict:
            similar_words = self.model.most_similar(keyword, topn=10)
            for word,  simialrity in similar_words:
                if simialrity <= 0.75: 
                     continue
                if word not in keyword_dict:
                    expand_words.append(word)
        for word in expand_words:
            keyword_dict[word] = 1
        return keyword_dict
