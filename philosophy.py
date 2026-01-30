import httpx
from selectolax.parser import HTMLParser

url = 'https://www.bookxcess.com/search?q=philosophy&options%5Bprefix%5D=last&type=product'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15'}

resp = httpx.get(url, headers=headers)
html = HTMLParser(resp.text)

def extract_text(html, sel):
    try:
        return html.css_first(sel).text(strip=True)
    except AttributeError:
        return None

products = html.css('div.pro_grid_btm')

for product in products:
    item = {
        'name': extract_text(product, '.pro_gridmeta a'),
        'price': extract_text(product, '.bp_regular')
    }

    print(item)