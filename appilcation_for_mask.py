#!/usr/bin/env python
# -*- coding:utf-8 -*-\
import datetime
import time
import sys
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import getpass


def send_mail(html):
    try:
        mail_password = getpass.getpass("Please input your email password:")
    except Exception as e:
        print(e)
        sys.exit()
    mail_info = {
        "from": "wei.wu@cienet.com.cn",
        "to": ["jiaqianchen@cienet.com.cn"],
        "cc": ["yinglei.jiang@cienet.com.cn", "wentao.qin@cienet.com.cn"],
        "hostname": "smtp.263xmail.com",
        "username": "wei.wu@cienet.com.cn",
        "password": mail_password,
        "mail_subject": "口罩申请",
        "mail_text": html,
        "mail_encoding": "utf-8"
    }

    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)

    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])
    msg = MIMEText(mail_info["mail_text"], _subtype="html", _charset=mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["From"] = mail_info["from"]
    msg["To"] = ",".join(mail_info["to"])
    msg["Cc"] = ",".join(mail_info["cc"])

    smtp.sendmail(mail_info["from"], mail_info["to"] + mail_info["cc"], msg.as_string())
    smtp.quit()


class MailTable(object):
    html = None
    table_head = None
    td_head = None

    def __init__(self):
        self.table_head = "<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=756 style='width:567.0pt;margin-left:-.65pt;border-collapse:collapse'>"
        self.td_head = """
                    <td width=96 valign=bottom style='width:1.0in;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>No<o:p></o:p></span></b></p></td>
                    <td width=119 nowrap valign=bottom style='width:89.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun, sans-serif;color:white'>姓名<o:p></o:p></span></b></p></td>
                    <td width=133 nowrap valign=bottom style='width:100.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>P CODE<o:p></o:p></span></b></p></td>
                    <td width=97 nowrap valign=bottom style='width:73.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun,sans-serif;color:white'>申请数量<o:p></o:p></span></b></p></td>
                    <td width=81 nowrap valign=bottom style='width:61.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun,sans-serif;color:white'>通勤方式<o:p></o:p></span></b></p></td>
        """
        curr_time = datetime.datetime.now()
        self.html = "<p>On {}/{}/{} {}:{}, Wu, Wei(wei)wrote:</p>".format(curr_time.day, curr_time.month,
                                                                          curr_time.year, curr_time.hour,
                                                                          curr_time.minute)
        self.html += self.table_head
        self.html += self.td_head

    def add_tr(self, no, name, pcode, count, transmisson_method):
        td = """
                    <td width=96 nowrap style='width:1.0in;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{}<o:p></o:p></span></p></td>
                    <td width=119 nowrap style='width:89.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun'>{}</span><span style='font-size:10.0pt;font-family:SimSun'><o:p></o:p></span></p></td>
                    <td width=133 nowrap valign=bottom style='width:100.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='color:black'>{}</span><span style='font-size:10.0pt;font-family:"Times New Roman",serif'><o:p></o:p></span></p></td>
                    <td width=133 nowrap valign=bottom style='width:100.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='color:black'>{}</span><span style='font-size:10.0pt;font-family:"Times New Roman",serif'><o:p></o:p></span></p></td>
                    <td width=85 nowrap valign=bottom style='width:64.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:#FCD5B4;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun'>{}</span></p></td>
        """.format(no, name, pcode, count, transmisson_method)
        tr = "<tr style='height:15.0pt'>" + td + "</tr>"
        self.html += tr

    def get_html(self):
        self.html += '</table>'
        self.html += '<p>BR/{0}</p>'.format("Wei")
        return self.html


mt = MailTable()
mt.add_tr(1, "吴威", "ERIC-Shanghai-HSS", 3, "公交")
mt.add_tr(2, "秦文涛", "ERIC-Shanghai-HSS", 3, "地铁")
send_mail(mt.get_html())
