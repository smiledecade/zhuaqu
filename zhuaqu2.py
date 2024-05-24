import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import os
import subprocess  # 用于打开文件
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import schedule

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

def send_email_with_attachment(subject, body, attachment_path, sender_email, sender_password, receiver_email):
    # 创建一个 MIMEMultipart 对象
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 邮件正文
    message.attach(MIMEText(body, 'plain'))

    # 添加附件
    filename = os.path.basename(attachment_path)
    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    message.attach(part)

    # 连接到 SMTP 服务器
    server = smtplib.SMTP_SSL('smtp.163.com', 465)
    server.login(sender_email, sender_password)

    # 发送邮件
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("邮件发送成功！")

    # 退出 SMTP 服务器连接
    server.quit()

def main():
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
    output_dir = r"C:\Users\zhuaqu"
    os.makedirs(output_dir, exist_ok=True)  # 创建目录，如果不存在则创建
    output_file = os.path.join(output_dir, 'articles.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for article in all_articles:
            f.write(f"Title: {article['title']}\nURL: {article['url']}\nContent:\n{article['content']}\n\n{'='*80}\n\n")

    # 使用 Foxmail 发送邮件
    recipient = "1292407020@qq.com"  # 你的邮箱地址
    subject = "文章内容"  # 邮件主题
    body = "请查收附件，文章内容见附件。"  # 邮件正文
    sender_email = "zhuaqu2024@163.com"  # 你的 Foxmail 邮箱地址
    sender_password = "AGAKBGYUENUCQNCP"  # 你的 Foxmail 邮箱密码
    attachment_path = output_file  # 附件路径

    # 发送邮件
    send_email_with_attachment(subject, body, attachment_path, sender_email, sender_password, recipient)

if __name__ == '__main__':
    main()
