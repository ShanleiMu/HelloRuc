import math


class Pagination:
    per_page = 10
    window = 5

    def __init__(self, cur, total):
        self.total_url = total
        self.total_page = math.ceil(self.total_url / self.per_page)
        self.cur_page = max(cur, self.total_page)
        self.page_window = self.get_page_window()


    @property
    def is_first_page(self):
        return self.cur_page == 1

    @property
    def is_last_page(self):
        return self.cur_page == self.total_page

    def get_page_window(self):
        page_window = []
        left_distance = self.cur_page - 1
        right_distance = self.total_page - self.cur_page
        if left_distance < right_distance:
            step = min(left_distance, math.floor((self.window - 1) / 2))
            for i in range(step + 1):
                # will append the current page
                page_window.append(self.cur_page - i)
            left = min(self.window - step - 1, right_distance)
            for i in range(1, left + 1):
                page_window.append(self.cur_page + i)
        else:
            step = min(right_distance, math.floor((self.window - 1) / 2))
            for i in range(step + 1):
                page_window.append(self.cur_page + i)
            left = min(left_distance, self.window - step - 1)
            for i in range(1, left + 1):
                page_window.append(self.cur_page - i)
        page_window.sort()
        return page_window

    def __iter__(self):
        return self.page_window.__iter__()


if __name__ == '__main__':
    cur = int(input())
    total = int(input())
    pagination = Pagination(cur, total)
    for i in pagination:
        print(i)