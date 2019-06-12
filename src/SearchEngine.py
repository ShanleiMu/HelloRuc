import math
import re
from flask import Markup, url_for
import pickle
import redis
from src.search_engine.main import se, rs, rel, co, qe


class Link:
    pattern_prefix = re.compile(r'.*://')
    pattern_suffix = re.compile(r'/.*')

    def __init__(self, docid, url, title, date, caption):
        self.docid = docid
        self.url = url
        self.title = title
        self.date = date
        self.caption = caption

    @property
    def cite(self):
        cite = re.sub(self.pattern_prefix, "", self.url)
        return re.sub(self.pattern_suffix, "", cite)


class SearchEngine:
    def __init__(self, query="", page=1, per_page=10, inst_filter="", time_filter="", requery=True, ext_query=False):
        """
        url_per_page: the amount of urls to be displayed on a body
        query: string of the query
        page_list: the list of instance of page
        """
        self.url_per_page = 10
        self.query = query
        self.page = page
        self.per_page = per_page
        self.inst_filter = inst_filter
        self.time_filter = time_filter
        self.requery = requery
        self.ext_query = ext_query
        self.need_requery = False
        self.origin_query = query
        self.link_list = []
        self.rel_people = [] # list of ('person name', 'url')
        self.rel_inst = [] # list of ('org name', 'url')
        self.r = redis.Redis(host='localhost', port=6379)

    def make_redis_key(self):
        return self.query + "_" + self.inst_filter + \
               "_" + self.time_filter + \
               "_" + str(self.requery) + \
               "_" + str(self.ext_query)

    def search(self):
        if self.requery:
            origin_query = self.query
            self.query = co.detect(self.query, co.dict, co.pinyin)
            self.query = co.detect(self.query, co.dict_term, co.pinyin_term, True)
            self.need_requery = (origin_query != self.query)

        link_list_raw = self.r.get(self.make_redis_key())
        # link_list_raw = None

        if link_list_raw is None:
            link_list = []
            cleaned_dict = se.split_query(self.query)
            if self.ext_query:
                cleaned_dict = qe.expansion(cleaned_dict)
            flag, scores, cleaned_dict = se.result_by_hot(cleaned_dict, self.inst_filter, self.time_filter)
            flag, result_list, captions = rs.return_result(flag, scores, cleaned_dict)
            if flag:
                for r in result_list:
                    docid = r[0]
                    url = r[3]
                    title = r[1]
                    date = r[2]
                    title = Markup(rs.deal_title(title, cleaned_dict))
                    caption = Markup(captions[docid])
                    link_list.append(Link(docid, url, title, date, caption))
                self.r.set(self.make_redis_key(), pickle.dumps(link_list))
        else:
            link_list = pickle.loads(link_list_raw)
        self.link_list = link_list
        left_side = self.link_list[(self.page-1)*self.per_page : self.page*self.per_page]
        left_side_score = [(link.docid, pos) for link, pos in zip(left_side, range(1, self.per_page+1))]
        rel_people = rel.get_relevant_person_with_url(left_side_score)
        rel_inst = rel.get_relevant_org_with_url(left_side_score)
        self.rel_people = self.remove_qword(rel_people, rel.num_rightside_person)
        self.rel_inst = self.remove_qword(rel_inst, rel.num_rightside_org)

    @property
    def url_num(self):
        """
        get the amount of relevant documents
        """
        return len(self.link_list)

    @property
    def page_amount(self):
        """
        :return: the amount of pages to display all the urls
        """
        return math.ceil(self.url_num / self.url_per_page)

    def get_page_list(self, page):
        """
        :param page: the page number, begin with 1
        :return: the corresponding urls in that page
        """
        page_index = page - 1
        if 1 <= page <= self.page_amount:
            start_index = page_index * self.url_per_page
            if page == self.page_amount:
                end_index = self.url_num
            else:
                end_index = page * self.url_per_page
            return self.link_list[start_index: end_index]
        else:
            return []

    def get_result(self, page):
        return self.url_num, self.need_requery, self.origin_query, self.query, self.get_page_list(page), self.rel_people, self.rel_inst

    def remove_qword(self, rel_list, length):
        """
        remove relevant things that contain query itself
        (can contain part of the query)
        args:
            rel_list: a list of ('relevant thing', 'url') pair
            length: int, length of return list
        return:
            rel_list: a list of ('relevant thing', 'url') pair, len(rel_list)==length
        """
        for i, thing in enumerate(rel_list):
            if thing[0] == self.query:
                del rel_list[i]
        return rel_list[:length]