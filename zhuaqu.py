import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import os
import schedule
import datetime

def fetch_article_content(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(article_url, headers=headers)
    response.encoding = 'utf-8'
    
    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')
    dom = etree.HTML(str(soup))
    
    # 获取标题
    title = dom.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/h1/text()')
    if title:
        title = title[0]
    else:
        return None, None
    
    # 获取正文内容
    content_elements = dom.xpath('/html/body/div[4]/div[1]/div[2]/div[2]//text()')
    content = '\n'.join(content_elements).strip()
    
    return title, content

def fetch_and_save_articles():
    base_url = 'https://www.qm120.com/zt/baike/{}.html'
    start_id = 607340
    end_id = 607341
    all_articles = []

    for article_id in range(start_id, end_id + 1):
        article_url = base_url.format(article_id)
        try:
            title, content = fetch_article_content(article_url)
            if title and content:
                all_articles.append({'title': title, 'url': article_url, 'content': content})
                print(f'Successfully fetched: {title}')
            else:
                print(f'No content found for {article_url}')
            time.sleep(1)  # 适当的延迟，避免被封禁
        except Exception as e:
            print(f'Error fetching {article_url}: {e}')
            continue

    # 保存结果
    output_dir = "C:\Users\zhuaqu"
    os.makedirs(output_dir, exist_ok=True)  # 创建目录，如果不存在则创建
    output_file = os.path.join(output_dir, 'articles.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for article in all_articles:
            f.write(f"Title: {article['title']}\nURL: {article['url']}\nContent:\n{article['content']}\n\n{'='*80}\n\n")

def run_job():
    now = datetime.datetime.now()
    if now.hour == 8 and now.minute == 0:
        fetch_and_save_articles()

# 设置定时任务，每分钟检查一次是否到了执行时间
schedule.every().minute.do(run_job)

while True:
    schedule.run_pending()
    time.sleep(1)
