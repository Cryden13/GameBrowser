from bs4 import BeautifulSoup as Html
from urllib3 import PoolManager
from bs4.element import Tag
from re import (
    findall as re_findall,
    search as re_search,
    sub as re_sub
)

url = "https://f95zone.to/threads/tales-of-androgyny-v0-3-20-0-majalis.1643/"


class SEL:
    title = 'div[uix_component="MainContent"] h1.p-title-value'
    tags = 'span.js-tagList > a'
    desc = 'article.message-body.js-selectToQuote > div.bbWrapper > div > b'
    ver = 'article.message-body.js-selectToQuote b'


def formatStr(s: str) -> str:
    string = re_sub(r'\s*(\r+|\n+)\s*',
                    r'\n',
                    ''.join(s))
    encoded = string.encode('ascii', 'ignore')
    return encoded.decode().strip()


pool = PoolManager()
raw: bytes = pool.request(method='GET', url=url).data
decoded = raw.decode(encoding='utf-8', errors='ignore')
html = Html(markup=decoded, features='html.parser')

# header
raw_header: Tag = html.select(selector=SEL.title, limit=1)[0]
header = raw_header.get_text()
header_ttl = re_search(r'\]\s*([^\[\]]{3,}?)\s*(?:\[|$)',
                       formatStr(header))
print(f'header_ttl: "{header_ttl.group(1)}"')
header_info: list[str] = re_findall(r'(?<=\[).+?(?=\])',
                                    formatStr(header.lower()))
print(f'header_info: "{header_info}"')

# tags
raw_tags = {t.get_text() for t in html.select(selector=SEL.tags)}
print(f'raw_tags: "{raw_tags}"')

# description
raw_content = html.select(selector=SEL.desc, limit=1)[0]
raw_desc = raw_content.find_parent().get_text()
desc = re_sub(r'(?s)\s*(Overview:?|Spoiler.+?register now\.)\s*',
              r'',
              formatStr(raw_desc))
print(f'desc: "{desc}"')

# version
ver = 'unknown'
el: Tag
for el in html.select(SEL.ver):
    if 'version' in el.get_text().lower():
        ver = el.next_sibling.strip(' :')
        break
print(f'ver: "{ver}"')
