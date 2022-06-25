from bs4 import BeautifulSoup as Html
from winnotify import PlaySound
from urllib3 import PoolManager
from bs4.element import Tag

from PyQt5.QtWidgets import (
    QPlainTextEdit,
    QCheckBox,
    QComboBox,
    QLineEdit
)
from re import (
    findall as re_findall,
    search as re_search,
    sub as re_sub
)

from ..constants import _SELECTORS as SEL
from ..constants import *


class GetF95Info(Html):
    pointer_categories_chkBox: dict[str, QCheckBox]
    pointer_categories_cmbBox: dict[str, QComboBox]
    pointer_tags_chkBox: dict[str, QCheckBox]
    pointer_tags_cmbBox: dict[str, QComboBox]
    pointer_info: dict[str, QLineEdit]
    pointer_description: QPlainTextEdit

    def __init__(self, pt_cats_chkBox: dict[str, QCheckBox], pt_cats_cmbBox: dict[str, QComboBox], pt_tags_chkBox: dict[str, QCheckBox], pt_tags_cmbBox: dict[str, QComboBox], pt_info: dict[str, QLineEdit], pt_desc: QPlainTextEdit, url: str):
        self.pointer_categories_chkBox = pt_cats_chkBox
        self.pointer_categories_cmbBox = pt_cats_cmbBox
        self.pointer_tags_chkBox = pt_tags_chkBox
        self.pointer_tags_cmbBox = pt_tags_cmbBox
        self.pointer_info = pt_info
        self.pointer_description = pt_desc
        pool = PoolManager()
        raw: bytes = pool.request(method='GET', url=url).data
        decoded = raw.decode(encoding='utf-8', errors='ignore')
        Html.__init__(self, markup=decoded, features='html.parser')
        self.getInfo()

    def getInfo(self) -> None:
        # header
        raw_header = self.select(selector=SEL.title, limit=1)
        if raw_header:
            self.fillHeader(raw_header[0])
        # tags
        raw_tags = {t.get_text() for t in self.select(selector=SEL.tags)}
        if raw_tags:
            self.fillTags(raw_tags)
        # description
        if not self.pointer_description.toPlainText():
            raw_content = self.select(selector=SEL.desc, limit=1)
            if raw_content:
                self.fillDescription(raw_content[0])
        # version
        self.fillVersion()
        PlaySound('Beep')

    def fillHeader(self, raw_header: Tag) -> None:
        header = raw_header.get_text()
        header_ttl = re_search(r'\]\s*([^\[\]]{3,}?)\s*(?:\[|$)',
                               formatStr(header))
        if header_ttl and not self.pointer_info['Title'].text():
            self.pointer_info['Title'].setText(header_ttl.group(1))
        header_info: list[str] = re_findall(r'(?<=\[).+?(?=\])',
                                            formatStr(header.lower()))
        for item in header_info:
            for status in ['Completed', 'Abandoned']:
                if status.lower() in item:
                    self.pointer_categories_chkBox[status].setChecked(True)
            for c in CAT_SEL['Engine']:
                if c.lower() in item:
                    self.pointer_categories_cmbBox['Engine'].setCurrentText(c)

    def fillTags(self, raw_tags: set[str]) -> None:
        subbed_tags = {v for k, v in TAG_EQU.items()
                       if k in raw_tags}
        all_tags = raw_tags - set(TAG_EQU) | subbed_tags
        if not all_tags:
            return
        # set toggle tags
        for tag in [t for t in TAG_TOG if t.lower() in all_tags]:
            self.pointer_tags_chkBox[tag].setChecked(1)
        # set toggle categories
        for tag in [t for t in CAT_TOG if t.lower() in all_tags]:
            self.pointer_categories_chkBox[tag].setChecked(1)
        # set art category
        for tag in CAT_SEL['Art']:
            if tag.lower() in all_tags:
                self.pointer_categories_cmbBox['Art'].setCurrentText(tag)
                break
        # set protagonist
        if 'character creation' in all_tags:
            protag = 'Created'
        else:
            protag = getProtagonist(all_tags)
        self.pointer_categories_cmbBox['Protagonist'].setCurrentText(protag)

    def fillDescription(self, raw_content: Tag) -> None:
        if not self.pointer_description.toPlainText():
            raw_desc = raw_content.find_parent().get_text()
            desc = re_sub(r'(?s)\s*(Overview:?|Spoiler.+?register now\.)\s*',
                          r'',
                          formatStr(raw_desc))
            self.pointer_description.setPlainText(desc)

    def fillVersion(self) -> None:
        el: Tag
        for el in self.select(SEL.ver):
            if 'version' in el.get_text().lower():
                ver = el.next_sibling.strip(' :')
                self.pointer_info['Version'].setText(ver)
                break


def formatStr(s: str) -> str:
    string = re_sub(r'\s*(\r+|\n+)\s*',
                    r'\n',
                    ''.join(s))
    encoded = string.encode('utf-8', 'ignore')
    return encoded.decode().strip()


def getProtagonist(all_tags: str) -> str:
    raw_protag = {t.split(' ')[0] for t in all_tags
                  if 'protagonist' in t}
    protag_ct = len(raw_protag)
    if protag_ct == 0:
        return 'Unknown'
    elif protag_ct == 1:
        for protag in CAT_SEL['Protagonist']:
            if protag.lower() in raw_protag:
                return protag
    elif 'multiple' in raw_protag or protag_ct > 1:
        return 'Multiple'
    else:
        return 'Unknown'
