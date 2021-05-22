from bs4 import BeautifulSoup as Html
from winnotify import playSound
from urllib3 import PoolManager
from re import (
    findall as re_findall,
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

if TYPE_CHECKING:
    from tkinter import IntVar, StringVar, Text
    from tkinter.ttk import Combobox

T_CT: "dict[str, IntVar]" = dict
T_CS: "dict[str, Combobox]" = dict
T_TT: "dict[str, IntVar]" = dict
T_TS: "dict[str, Combobox]" = dict
T_IE: "dict[str, StringVar]" = dict


class GetF95Info(Html):
    catToggles: T_CT
    catSelects: T_CS
    tagToggles: T_TT
    tagSelects: T_TS
    infoEnts: T_IE
    infoDesc: "Text"

    def __init__(self, cTogs: T_CT, cSel: T_CS, tTogs: T_TT, tSel: T_TS, iEnts: T_IE, iDesc: "Text", url: str):
        self.catToggles = cTogs
        self.catSelects = cSel
        self.tagToggles = tTogs
        self.tagSelects = tSel
        self.infoEnts = iEnts
        self.infoDesc = iDesc
        pool = PoolManager()
        raw = pool.request('GET', url).data
        decoded = raw.decode('utf-8', errors='ignore')
        Html.__init__(self, decoded, 'html.parser')
        self.getInfo()

    def getInfo(self) -> None:
        # header
        rawHeader = self.select(Sel.title)
        self.fillHeader(rawHeader)
        # tags
        rawTags = {t.get_text() for t in self.select(Sel.tags)}
        self.fillTags(rawTags)
        # description
        rawContent = self.select(Sel.desc)
        self.fillDescription(rawContent)
        # version
        self.fillVersion()
        playSound('Beep')

    def fillHeader(self, rawHeader) -> None:
        if not rawHeader:
            return
        header = rawHeader[0].get_text().lower()
        headerInfo: list[str]
        headerInfo = re_findall(r'(?<=\[).+?(?=\])',
                                formatStr(header))
        for item in headerInfo:
            for status in ['Completed', 'Abandoned']:
                if status.lower() in item:
                    self.catToggles[status].set(1)
            for c in CAT_SEL['Engine']:
                if c.lower() in item:
                    self.catSelects['Engine'].set(c)

    def fillTags(self, rawTags: set[str]) -> None:
        if not rawTags:
            return
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

    def fillDescription(self, rawContent) -> None:
        if not rawContent or self.infoDesc.get(1.0, 'end-1c').strip():
            return
        rawDesc = rawContent[0].find_parent().get_text()
        desc = re_sub(r'(?s)\s*(Overview:?|Spoiler.+?register now\.)\s*',
                      r'',
                      formatStr(rawDesc))
        self.infoDesc.insert(1.0, desc.strip())

    def fillVersion(self) -> None:
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
