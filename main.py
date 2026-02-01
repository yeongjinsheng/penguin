import time
import httpx
from selectolax.parser import HTMLParser


def get_html(base_url, page_num):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15"
    }
    resp = httpx.get(base_url + str(page_num), headers=headers, follow_redirects=True)
    # to handle 404
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. Page Limit Exceeded"
        )
        return False
    html = HTMLParser(resp.text)
    return html


def parser(html):
    products = html.css(".BookCard_wrapper___AWCP")
    for product in products:
        item = {
            # "book name": product.css_first(".BookCard_title__4OQ1m").text(strip=True),
            "book name": extract_text(product, ".BookCard_title__4OQ1m"),
            "author": extract_text(product, ".BookCard_authors__SiuPz"),
        }
        yield item


def extract_text(html, sel):
    try:
        return html.css_first(sel).text(strip=True)
    except AttributeError:
        return None


def main():
    base_url = "https://www.penguin.co.uk/search-results?q=epictetus&tab=books&page="
    for page_num in range(1, 5):
        print(f"Page {page_num}")
        html = get_html(base_url, page_num)
        if html is False:
            break
        data = parser(html)
        for item in data:
            print(item)
        time.sleep(2)


if __name__ == "__main__":
    main()
