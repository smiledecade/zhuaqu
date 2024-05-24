import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import schedule
import datetime
import time

def send_email():
    # 邮件发送方的邮箱地址和密码
    sender_email = "zhuaqu2024@163.com"
    sender_password = "AGAKBGYUENUCQNCP"

    # 收件人邮箱地址
    receiver_email = "1292407020@qq.com"

    # 创建一个 MIMEMultipart 对象
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Daily Report"  # 邮件主题

    # 邮件正文
    body = "请查收附件，这是今天的日报。"
    message.attach(MIMEText(body, 'plain'))

    # 添加附件
    filename = "report.txt"  # 你要发送的文件名
    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    message.attach(part)

    # 连接到 Foxmail 邮箱 SMTP 服务器
    server = smtplib.SMTP_SSL('smtp.yourfoxmail.com', 465)
    server.login(sender_email, sender_password)

    # 发送邮件
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("邮件发送成功！")

    # 退出 SMTP 服务器连接
    server.quit()

def run_job():
    now = datetime.datetime.now()
    if now.hour == 8 and now.minute == 0:
        send_email()

# 设置定时任务，每天的早上 8 点发送邮件
schedule.every().day.at("08:00").do(run_job)

while True:
    schedule.run_pending()
    time.sleep(1)
