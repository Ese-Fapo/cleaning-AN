"""Write crawler-readable sharing metadata; configure the real domain when available."""
import argparse
import html
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--site-url', help='Public HTTPS site URL, including any deployment subdirectory.')
args = parser.parse_args()
config_path = ROOT / 'sharing.json'
config = json.loads(config_path.read_text(encoding='utf-8'))
if args.site_url:
    url = urlsplit(args.site_url)
    if url.scheme != 'https' or not url.netloc or url.username or url.password:
        parser.error('Use the public HTTPS website URL without credentials.')
    path = url.path
    if path.endswith('.html'):
        path = path.rsplit('/', 1)[0] + '/'
    elif not path.endswith('/'):
        path += '/'
    config['site_url'] = urlunsplit((url.scheme, url.netloc, path, '', ''))
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
base = config.get('site_url')
assert (ROOT / config['image']).is_file(), 'Sharing image is missing.'
image_url = urljoin(base, config['image']) if base else config['image']
def meta(key, value, attribute='property'):
    return f'  <meta {attribute}="{key}" content="{html.escape(str(value), quote=True)}">'

count = 0
for page in ROOT.glob('*.html'):
    if page.name == '404.html':
        continue
    source = page.read_text(encoding='utf-8')
    source = re.sub(r'\s*<!-- Social preview -->.*?<!-- /Social preview -->', '', source, flags=re.S)
    # Remove prior image/card tags to avoid duplicate first-image behavior.
    source = re.sub(r'\s*<meta\s+(?:property="og:image(?::[^"]*)?"|name="twitter:[^"]*")[^>]*>', '', source)
    title = html.unescape(re.search(r'<title>(.*?)</title>', source, re.S).group(1))
    description = re.search(r'<meta name="description"\s+content="([^"]*)"', source, re.S)
    description = html.unescape(description.group(1)) if description else title
    tags = [meta('og:image', image_url), meta('og:image:type', config['type']),
            meta('og:image:width', config['width']), meta('og:image:height', config['height']),
            meta('og:image:alt', config['alt']), meta('twitter:card', 'summary_large_image', 'name'),
            meta('twitter:title', title, 'name'), meta('twitter:description', description, 'name'),
            meta('twitter:image', image_url, 'name'), meta('twitter:image:alt', config['alt'], 'name')]
    if base:
        canonical = urljoin(base, '' if page.name == 'index.html' else page.name)
        source = re.sub(r'\s*<meta property="og:url"[^>]*>', '', source)
        source = re.sub(r'\s*<link rel="canonical"[^>]*>', '', source)
        tags.extend([meta('og:image:secure_url', image_url), meta('og:url', canonical),
                     f'  <link rel="canonical" href="{html.escape(canonical, quote=True)}">'])
    source = source.replace('</head>', '  <!-- Social preview -->\n' + '\n'.join(tags) + '\n  <!-- /Social preview -->\n</head>')
    page.write_text(source, encoding='utf-8')
    count += 1
print(f'Updated sharing metadata on {count} pages.')
if not base:
    print('Public URL not configured: image paths are local. Run with --site-url after the domain is supplied.')
