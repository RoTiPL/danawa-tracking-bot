import requests
from bs4 import BeautifulSoup

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Server': 'Apache',
    'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0',
    'Vary': 'Accept-Encoding, User-Agent',
    'Content-Encoding': 'gzip',
    'Keep-Alive': 'timeout=15, max=100',
    'Content-Type': 'text/html; charset=UTF-8'
}

def danawa_crawler(url):
    html = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(html.text, 'html.parser')
    lowest = soup.select_one('#lowPriceCash > span.lwst_prc > a')
    
    if lowest is None:
        lowest = soup.select_one('#blog_content > div.summary_info > div.detail_summary > div.summary_left > div.lowest_area > div.lowest_top > div.row.lowest_price > span.lwst_prc > a')
    
    result = {
        'link': lowest.get('href'),
        'price': lowest.text
    }
    return result
    