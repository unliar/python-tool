import csv
import smtplib
import time
from random import choice
from email.mime.text import MIMEText


def create_mail_server(mail_server_host, mail_server_port, from_addr, from_pass):
    """
    @ mail_server_host 你的smtp服务器地址

    @ mail_server_port 你的smtp端口

    @ from_addr 你的发送邮件邮箱地址

    @ from_pass 你的发送邮件邮箱密码

    ### return  登录成功的服务器对象
    """
    try:
        server = smtplib.SMTP(mail_server_host, mail_server_port)
        server.starttls()
        server.login(from_addr, from_pass)
    except Exception as e:
        raise Exception(e)

    return server


def open_scv_data(file_name, mail_key):
    """
    @ file_name 文件名,the data file

    @ mail_key 邮箱键名,the key has email data.

    ### return  包含csv文件的data字典
    """
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data_dict = {}
        for item in reader:
            html = ''
            data_key = item[mail_key]
            for key, value in item.items():
                html = html + key + ':' + value + '</br>'
                data_dict[data_key] = html
        return data_dict


def send_email(server, mail_from, mail_to, mail_subject, mail_body):
    """
    @ server 邮件服务器对象

    @ mail_from 邮件发送人

    @ mail_to 邮件接受人

    @ mail_subjrct 邮件主题

    @ mail_body 邮件正文
    """
    msg = MIMEText(mail_body, 'html', 'utf-8')
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = mail_subject
    try:
        server.sendmail(mail_from, mail_to, msg.as_string())

    except Exception as e:
        print('发送邮件失败', mail_to)


# example qqmail
def main():
    server = create_mail_server(
        'smtp.qq.com', 587, '370732889@qq.com', 'xxx')
    data_dict = open_scv_data('test.csv', '邮箱')

    for key, value in data_dict.items():
        send_email(server, '370732889@qq.com', key, '你的账单到啦~', value)
        time.sleep(choice([1, 2, 3]))
    print('all done  似乎一切正常')


if __name__ == '__main__':
    main()
