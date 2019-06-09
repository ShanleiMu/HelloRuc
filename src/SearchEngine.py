import math
import re
from flask import Markup, url_for
import pickle
import redis
from src.search_engine.main import se, rs


class Link:
    pattern_prefix = re.compile(r'.*://')
    pattern_suffix = re.compile(r'/.*')

    def __init__(self, url, title, date, caption):
        self.url = url
        self.title = title
        self.date = date
        self.caption = caption

    @property
    def cite(self):
        cite = re.sub(self.pattern_prefix, "", self.url)
        return re.sub(self.pattern_suffix, "", cite)


class SearchEngine:
    def __init__(self, query="", inst_filter="", requery=True):
        """
        url_per_page: the amount of urls to be displayed on a body
        query: string of the query
        page_list: the list of instance of page
        """
        self.url_per_page = 10
        self.query = query
        self.filter = inst_filter
        self.requery = requery
        self.need_requery = False
        self.origin_query = query
        self.link_list = []
        self.rel_people = []
        self.rel_inst = []
        self.r = redis.Redis(host='localhost', port=6379)

    def make_redis_key(self):
        return self.query + "_{" + self.filter + "}"

    def search(self):
        link_list_raw = self.r.get(self.make_redis_key())
        if link_list_raw is None:
            link_list = []
            flag, scores, cleaned_dict = se.result_by_hot(self.query)
            flag, result_list, captions = rs.return_result(flag, scores, cleaned_dict)
            if flag:
                for r in result_list:
                    docid = r[0]
                    url = r[3]
                    title = r[1]
                    date = r[2]
                    caption = captions[docid]
                    link_list.append(Link(url, title, date, caption))
                self.r.set(self.make_redis_key(), pickle.dumps(link_list))
        else:
            link_list = pickle.loads(link_list_raw)
        self.link_list = link_list

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