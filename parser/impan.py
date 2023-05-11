from os import listdir
from os.path import isfile, join
from parsel import Selector
import pandas as pd
import re

def parser(file):
    with open('C:/coursework/pars/pars/spiders/data/impan/full/'+file, 'r', encoding="utf8", errors='ignore') as fp:
        data = fp.read()

    result = {
        'journal': '',
        'title': '',
        'eISSN': '',
        'pISSN': '',
        'DOI': '',
        'affilations': [],
        'year': 0,
        'pages': '',
        'volume': 0,
        'raw_url': '',
        'keywords': []

    }

    selector = Selector(text=data)

    #DOI
    s = selector.xpath('//meta[@name="citation_doi" or @name="DOI"]')
    if (s):
        result['DOI'] = s.attrib['content']
    else:
        print(file + "doi")

    #title
    s = selector.xpath('//meta[@name="citation_title" or @name="dc.title"]')
    if (s):
        s = s.attrib['content']
        result['title'] = " ".join(s.split())
    else:
        print(file + 'title')

    #journal
    s = selector.xpath('//meta[@name="citation_journal_title" or @name="prism.publicationName"]')
    if (s):
        s = s.attrib['content']
        result['journal'] = " ".join(s.split())
    else:
        print(file + 'journal')

    #ISSN
    s = selector.xpath('//meta[@name="citation_issn"]')
    if (s):
        result['eISSN'] = s[0].attrib['content']
        result['pISSN'] = s[1].attrib['content']
    else:
        print(file + 'issn')

    #Authors
    s1 = selector.xpath('//meta[@name="citation_author"]')
    s2 = selector.xpath('//meta[@name="citation_author_institution"]')
    temp = {}
    if s1 or s2:
        if s1:
            ans1 = s1.attrib['content']
        if (s2):
            ans2 = s2.attrib['content']
        result['affilations'].append({'Author': ans1, 'affilation': ans2})
    else:
        print(file + 'authors')

    #year
    s = selector.xpath('//meta[@name="citation_publication_date"]')
    if (s):
        s = s.attrib['content']
        result['year'] = int(s)
    else:
        print(file + 'year')

    #pages
    s1 = selector.xpath('//meta[@name="citation_firstpage"]')
    s2 = selector.xpath('//meta[@name="citation_lastpage"]')
    if (s1 and s2):
        s1 = s1.attrib['content']
        s2 = s2.attrib['content']
        result['pages'] = s1+'-'+s2
    else:
        print(file + 'pages')

    #volume
    s = selector.xpath('//meta[@name="citation_volume"]')
    if (s):
        s = s.attrib['content']
        result['volume'] = int(s)
    else:
        print(file + 'volume')

    #url
    s = selector.xpath('//meta[@name="citation_public_url"]')
    if (s):
        s = s.attrib['content']
        result['raw_url'] = s
    else:
        print(file + 'url')

    #keywords
    s = selector.xpath('//meta[@name="keywords"]')
    if (s):
        s = s.attrib['content']
        result['keywords'] = s.split(' ')
    else:
        print(file + 'keywords')

    return (result)

answer = []
mypath = 'C:/coursework/pars/pars/spiders/data/impan/full'
all = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in all:
    answer.append(parser(i))

pd.DataFrame(answer).to_csv('C:/coursework/pars/parser/output.csv')