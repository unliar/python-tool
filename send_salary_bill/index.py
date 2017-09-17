import csv
from email.mime.text import MIMEText
import smtplib
import time
from random import choice


def send_mail(from_addr, from_pass, smtp_server, smtp_server_port, file_name):

    # from_addr = '你的发送邮箱地址'
    # from_pass = '你的发送邮箱密码或者校验码'
    # smtp_server = '你的发送邮箱smtp服务器--->自行查看各个邮箱配置项'
    # smtp_server_port = 你的发送邮箱smtp服务器端口
    # file_name = 你的csv数据文件名
    try:
        server = smtplib.SMTP(smtp_server, smtp_server_port)
        server.starttls()
        server.login(from_addr, from_pass)
    except Exception as e:
        print("登陆出错%s,login error" % e)
        raise Exception
    print('登陆成功...尝试打开文件发送邮件,login success!try to send mail with the csv file')
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for item in reader:
            html = ''
            for (k, v) in item.items():
                html = html + k + ":" + v + '</br>'

            msg = MIMEText(html, 'html', 'utf-8')
            # 发件人
            msg['From'] = from_addr
            # msg['To']  !包含你收件人邮箱的字段名 the csv header that have email account
            msg['To'] = item['邮箱']
            # 邮件主题
            msg['Subject'] = '你的账单到啦~请查收'
            try:
                server.sendmail(from_addr, [item['邮箱']], msg.as_string())
                print('发送成功,status:ok,%s' % item['邮箱'])
            except Exception as e:
                print('发送到%s出错,status:fail,' % item['邮箱'], 'error%s' % e)
            # 随机休眠
            time.sleep(choice([1, 2]))
        server.quit()
        print('邮件发送完毕,all done')


def main():
    send_mail('3707328x89@qq.com', 'youremailpass',
              'smtp.qq.com', 587, 'test.csv')


if __name__ == '__main__':
    main()
