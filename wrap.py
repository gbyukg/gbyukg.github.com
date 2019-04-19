# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from io import open
import itertools
import sys
from pathlib import Path

class NoMainSectionError(Exception):
    pass

wrapFolder = sys.argv[1]
# wrapFolder = ".tmp/cheatsheets"
# wrapFile = "./.tmp/cheatsheets/bash/index.html"

pathlist = Path(wrapFolder).glob('**/*.html')

def wrap(wrapFile):
    def wrapHeader(header, parentClass, childClass):
        for wrapEls in header:
            els = [i for i in itertools.takewhile(lambda x: x.name not in [wrapEls.name, 'script'], wrapEls.next_siblings)]

            parentSection = soup.new_tag('div', **{'class':parentClass})
            childSection = soup.new_tag('div', **{'class':childClass})
            #h3_section = soup.new_tag('div', **{'class':'h3-section'})
            #body_section = soup.new_tag('div', **{'class':'body'})

            wrapEls.wrap(parentSection)

            for tag in els:
                childSection.append(tag)

            parentSection.append(childSection)

    with open(wrapFile, 'r', encoding='utf-8') as source:
        soup = BeautifulSoup(source, "html.parser")

        main = soup.find('article', class_="article") # None
        if main == None:
            raise NoMainSectionError
        h2s = main.find_all('h2', recursive=False)
        h3s = main.find_all('h3', recursive=False)

        wrapHeader(h2s, 'h2-section', 'h3-section-list')
        wrapHeader(h3s, 'h3-section', 'body')

    with open(wrapFile, 'w', encoding='utf-8') as desc:
        desc.write(soup.prettify(formatter="None")) # 禁止转义 &it; 字符

for path in pathlist:
    try:
        wrap(str(path))
    except NoMainSectionError:
        pass
