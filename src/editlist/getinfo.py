from bs4 import BeautifulSoup as Html
from tkinter.ttk import Combobox
from winnotify import PlaySound
from urllib3 import PoolManager
from bs4.element import Tag

from tkinter import (
    StringVar,
    IntVar,
    Text
)
from re import (
    findall as re_findall,
    search as re_search,
    sub as re_sub
)

try:
    from ..constants import _SELECTORS as Sel
    from ..constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit


class GetF95Info(Html):
    catToggles: dict[str, IntVar] = dict
    catSelects: dict[str, Combobox] = dict
    tagToggles: dict[str, IntVar] = dict
    tagSelects: dict[str, Combobox] = dict
    infoEnts: dict[str, StringVar] = dict
    infoDesc: Text

    def __init__(self, cTogs: catToggles, cSel: catSelects, tTogs: tagToggles, tSel: tagSelects, iEnts: infoEnts, iDesc: Text, url: str):
        self.catToggles = cTogs
        self.catSelects = cSel
        self.tagToggles = tTogs
        self.tagSelects = tSel
        self.infoEnts = iEnts
        self.infoDesc = iDesc
        pool = PoolManager()
        raw: bytes = pool.request(method='GET', url=url).data
        decoded = raw.decode(encoding='utf-8', errors='ignore')
        Html.__init__(self, markup=decoded, features='html.parser')
        self.getInfo()

    def getInfo(self) -> None:
        # header
        rawHeader = self.select(selector=Sel.title, limit=1)
        if rawHeader:
            self.fillHeader(rawHeader[0])
        # tags
        rawTags = {t.get_text() for t in self.select(selector=Sel.tags)}
        if rawTags:
            self.fillTags(rawTags)
        # description
        if not self.infoDesc.get(1.0, 'end-1c').strip():
            rawContent = self.select(selector=Sel.desc, limit=1)
            if rawContent:
                self.fillDescription(rawContent[0])
        # version
        self.fillVersion()
        PlaySound('Beep')

    def fillHeader(self, rawHeader: Tag) -> None:
        header = rawHeader.get_text().lower()
        headerTtl = re_search(r'\]\s*([^\[\]]{3,}?)\s*(?:\[|$)',
                              formatStr(header))
        if headerTtl:
            self.infoEnts['Title'].set(headerTtl.group(1))
        headerInfo: list[str] = re_findall(r'(?<=\[).+?(?=\])',
                                           formatStr(header))
        for item in headerInfo:
            for status in ['Completed', 'Abandoned']:
                if status.lower() in item:
                    self.catToggles[status].set(1)
            for c in CAT_SEL['Engine']:
                if c.lower() in item:
                    self.catSelects['Engine'].set(c)

    def fillTags(self, rawTags: set[str]) -> None:
        subbedTags = {v for k, v in (TAG_EQU | CAT_EQU).items()
                      if k in rawTags}
        allTags = rawTags - {*TAG_EQU, *CAT_EQU} | subbedTags
        if not allTags:
            return
        # set toggle tags
        for tag in [t for t in TAG_TOG if t.lower() in allTags]:
            self.tagToggles[tag].set(1)
        # set toggle categories
        for tag in [t for t in CAT_TOG if t.lower() in allTags]:
            self.catToggles[tag].set(1)
        # set art category
        for tag in CAT_SEL['Art']:
            if tag.lower() in allTags:
                self.catSelects['Art'].set(tag)
                break
        # set protagonist
        if 'character creation' in allTags:
            protag = 'Created'
        else:
            protag = getProtagonist(allTags)
        self.catSelects['Protagonist'].set(protag)

    def fillDescription(self, rawContent: Tag) -> None:
        rawDesc = rawContent.find_parent().get_text()
        desc = re_sub(r'(?s)\s*(Overview:?|Spoiler.+?register now\.)\s*',
                      r'',
                      formatStr(rawDesc))
        self.infoDesc.insert(1.0, desc.strip())

    def fillVersion(self) -> None:
        el: Tag
        for el in self.select(Sel.ver):
            if 'version' in el.get_text().lower():
                ver = el.next_sibling.strip(' :')
                self.infoEnts['Version'].set(ver)
                break


def formatStr(s: str) -> str:
    string = re_sub(r'\s*(\r+|\n+)\s*',
                    r'\n',
                    ''.join(s))
    encoded = string.encode('ascii', 'ignore')
    return encoded.decode().strip()


def getProtagonist(allTags: str) -> str:
    rawProtag = {t.split(' ')[0] for t in allTags
                 if 'protagonist' in t}
    protagCt = len(rawProtag)
    if protagCt == 0:
        return 'Unknown'
    elif protagCt == 1:
        for protag in CAT_SEL['Protagonist']:
            if protag.lower() in rawProtag:
                return protag
    elif 'multiple' in rawProtag or protagCt > 1:
        return 'Multiple'
    return 'Unknown'
