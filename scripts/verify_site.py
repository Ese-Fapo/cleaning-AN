"""Check static routes, assets, labels, headings, and shared customer flows."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids, self.links, self.labels, self.controls = [], [], [], []
        self.headings = self.dialogs = 0
        self.description = False
        self.source = path.read_text(encoding='utf-8')
        self.feed(self.source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'h1': self.headings += 1
        if tag == 'dialog': self.dialogs += 1
        if tag == 'meta' and attrs.get('name') == 'description': self.description = True
        if tag == 'label' and 'for' in attrs: self.labels.append(attrs['for'])
        self.controls.extend(attrs.get('aria-controls', '').split())
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])
        if tag == 'a' and attrs.get('target') == '_blank':
            assert 'noopener' in attrs.get('rel', ''), (self.path.name, 'unsafe external link')

pages = {path.name: Page(path) for path in ROOT.glob('*.html')}
for name, page in pages.items():
    assert page.headings == 1, (name, 'main heading')
    assert all(count == 1 for count in Counter(page.ids).values()), (name, 'duplicate ID')
    assert all(target in page.ids for target in page.labels + page.controls), (name, 'label/control target')
    if name != '404.html':
        assert page.dialogs == 1 and page.description, (name, 'booking or metadata')
        assert 'class="skip_link"' in page.source and 'class="site_footer"' in page.source
        assert 'working_hours_table' in page.source
    for raw in page.links:
        url = urlsplit(raw)
        if url.scheme or url.netloc: continue
        target = unquote(url.path) or name
        assert (ROOT / target).is_file(), (name, 'missing file', raw)
        if url.fragment and target in pages:
            assert url.fragment in pages[target].ids, (name, 'missing anchor', raw)
home = pages['index.html'].source
assert 'ilustrativo' not in home and 'www.google.com/maps' not in home
assert 'id="perguntas-frequentes"' in home
for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', home, re.S):
    json.loads(raw)
print(f'PASS: {len(pages)} pages; local links/assets, headings, labels, controls, external links, booking, hours, metadata, and structured data.')
