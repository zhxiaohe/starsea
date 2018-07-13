#!/usr/bin/env python

class pages(object):
    def __init__(self):
        self.previous = ''
        self.next = ''
        page_size = 10
    def pageinit(self,current_page,total_count,url,page_size,search):
        self.page_size = int(page_size)
        self.url = url
        self.current_page = int(current_page)
        self.total_count = total_count
        self._pagecount()
        if self.page_count < (self.current_page + 1): # or (self.page_count == self.current_page):
            self.next = 'null'
        if self.current_page == 1 :
            self.previous = 'null'

        if self.page_count == 1:
            self.next = 'null'
            self.previous = 'null'
        
        if self.next != 'null':
            self.next = '{url}?page={page}&page_size={page_size}&search={search}'.format(url=url,
                                                                                         page=self.current_page + 1,
                                                                                         page_size=self.page_size ,
                                                                                         search=search)

        if self.previous != 'null':
            self.previous = '{url}?page={page}&page_size={page_size}&search={search}'.format(url=url,
                                                                                         page=self.current_page - 1,
                                                                                         page_size=self.page_size ,
                                                                                         search=search)

        return {
            'current_page': self.current_page,
            'next': self.next,
            'page_count': self.page_count,
            'page_size': self.page_size,
            'previous': self.previous,
            'results': '',
            'total_count': self.total_count,
        }

    def _pagecount(self):
        page_count = self.total_count // self.page_size
        page_remainder = self.total_count % self.page_size
        if page_remainder != 0:
            page_count += 1
        self.page_count = page_count

        if self.current_page > page_count:
            self.current_page = page_count

    def ssp(self):
        return (self.current_page * self.page_size - self.page_size),(self.current_page * self.page_size)

if __name__ == '__main__':
    current_page = 2
    total_count = 1000
    url = 'http://127.0.0.1/vip/bb/'
    page_size = 10
    search ='all'
    pp=pages()
    bp = pp.pageinit(current_page,total_count,url,page_size,search)
    print(bp)
