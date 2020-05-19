# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     666666666
   Description :
   date：          2020/5/18
-------------------------------------------------
   Change Activity:
                   2020/5/18:
-------------------------------------------------
"""
import logging
from datetime import datetime
from PIL import Image
import os
from selenium import  webdriver
import  time
import  pytesseract
import  sqlite3
from  selenium.webdriver.support.select import  Select
from  aip import AipOcr
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import  xlrd
def login_xzmu(xue_id, pwd,email):
    driver = webdriver.Chrome("C:\Program Files\Python\Python37\chromedriver.exe")
    driver.get("")
    driver.maximize_window()
    xuehao= driver.find_element_by_id("account")

    #xue_id,pwd,email = query_sql(xue_id,pwd, email)
    xuehao.send_keys(xue_id)
    mima= driver.find_element_by_id("pwd")
    mima.send_keys(pwd)

    yanzhengma=driver.find_element_by_id("checkcode")
    driver.save_screenshot(r"D:\Github-fork\beba-ctrl\ryu\app\beba\ddos\img\screen.png")
    imgelement=  driver.find_element_by_id("checkcodeimg")
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x'])*1.25, int(location['y'])*1.25, int(location['x']*1.27+ size['width']),
              int(location['y']*1.27+ size['height']))  # 写成我们需要截取的位置坐标

    # 通过Image处理图像
    im=Image.open(r"D:\Github-fork\beba-ctrl\ryu\app\beba\ddos\img\screen.png")
    frame=im.crop(rangle)
    frame.save(r"D:\Github-fork\beba-ctrl\ryu\app\beba\ddos\img\code.png")
    x= Image.open(r"D:\Github-fork\beba-ctrl\ryu\app\beba\ddos\img\code.png")
    # pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # number=pytesseract.image_to_string(x)
    number= baidu_ocr()
    #print(number)
    try:
        if len(number) ==4:
            if number.isdigit():
                yanzhengma.send_keys(number)
                logging.Logger(">>>>>>> reading send....",number)

                driver.find_element_by_xpath("/html/body/div/div/div/div[3]/div/div[1]/a").click()
                time.sleep(1)
                alert=driver.switch_to.alert
                alert.accept()
                #print("00000000000")
                se=driver.find_element_by_xpath("/html/body/header/div/a[3]").click()

                jiankanglable= driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/ul/li[4]/div/div[2]/div[2]/select")
                #print('11111')

                Select(jiankanglable).select_by_index(1)
                time.sleep(3)

                driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[3]/div/div/a").click()
                #print('33333333')
                #time.sleep(3)
                driver.close()

        else:
            driver.refresh()

    except Exception as e:
        print e
        # 如果用户有电话号 直接发短信 否则 发邮件
        # 发送邮件给该用户
        #id_to_email=query_sql(id)
        send_email(email=email)
        #print('发送邮件成功！！！！')
        # 报告master
def baidu_ocr():
    APP_ID = '18692900'
    API_KEY = ''
    SECRET_KEY =' '

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    """ 读取图片 """
    filePath=r"D:\Github-fork\beba-ctrl\ryu\app\beba\ddos\img\code.png"
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(filePath)

    """ 调用通用文字识别（高精度版） """
    client.basicAccurate(image)

    """ 如果有可选参数 """
    options = {}
    options["detect_direction"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别（高精度版） """
    # get json
    x=client.basicAccurate(image, options)
    #print(x)
    code= x['words_result'][0]['words']

    return code
# 发邮件
def send_email(email):
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '            @qq.com'
    # pwd为qq邮箱的授权码
    pwd = '                      '  ##
    # 发件人的邮箱
    sender_qq_mail = '           @qq.com'
    # 收件人邮箱
    receiver = '                  @gmail.com'
    #receiver = email

    # 邮件的正文内容
    mail_content = "你好，打卡失败了请重新手动打卡！！！！！"
    # 邮件标题
    mail_title = '打卡失败-请勿回复'

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = Header("接收者测试", 'utf-8')  ## 接收者的别名

    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
# 发短信
def send_msg(telenumber):
    from twilio.rest import Client

    # Your Account SID from twilio.com/console
    account_sid = "你的sid"
    # Your Auth Token from twilio.com/console
    auth_token = "你的token"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+86验证过的号码",
        from_="+twilio给你的号码 ",
        body="你好!")

    #print(message.sid)
# 创建数据库
# def insert_sql(filepath):
#
#     connect,course= creat_sql()
#
#     # 第一行 为 表头信息不能加入计算
#     table,all_row,all_col= read_excel(read_excel(excel_name=filepath))
#
#     for i in range(1,all_row+1):
#         id = table.row_values(i)
#         # 插入表格 语句
#         #insert_sql='INSERT INTO USER (ID,PASSWD,EMAIL) VALUES (%d, %s,%s)' %(id,passwd,email)
#         course.execute(insert_sql)
#
#     #course.execute("insert into user (id, telenumber,emaile) values ('1','15518183831','zhousodo@gmail.com')")
#     connect.commit()
#     course.close()
#     connect.close()


# 从excel 的数据中导入数据库
def excel_to_sql(excel_name):

    workbook= xlrd.open_workbook(filename=excel_name)
    sheet= workbook.sheet_by_name("Sheet1")

    connect,course= creat_sql()
    for i in range(0,sheet.nrows):
        temp=[]
        for j in range(0,sheet.ncols):
            temp.append(sheet.cell(i,j).value)
        #insert_sql = 'INSERT INTO USER (ID,PASSWD,EMAIL) VALUES (\"%s\", \"%s\",\"%s\")' % '(temp[0], temp[1], temp[2])'
        temp[0]=str(temp[0])[:-2]
        temp[1]=str(temp[1])[:-2]
        temp[2]=str(temp[2])
        insert_sql= "insert into USER (ID, PASSWD, EMAIL) values('%s','%s','%s')" % (temp[0], temp[1], temp[2])
        connect.execute(insert_sql)
        connect.commit()
    connect.close()
    #print('导入成功！！！')
    # 返回行 /列
    return sheet.nrows, sheet.ncols

def creat_sql():
    connect = sqlite3.connect('students.db')
    course = connect.cursor()
    sql = "CREATE TABLE IF NOT EXISTS  USER (ID,PASSWD,EMAIL) "
    course.execute(sql)
    return connect, course

def query_sql():
    connect,cursor= creat_sql()
    cursor = connect.execute('SELECT * FROM USER ')
    # 获取查询结构
    while  True:
        result = cursor.fetchone()  # 获取查询结果的语句块  返回的是一个元组
        if result != None:
            id = result[0]
            passwd = result[1]
            email = result[2]
            print(result[0], result[1], result[2])
        else:
            break
    return id,passwd,email

if __name__ == '__main__':

    pass
    # filepath=r"D:\Github-fork\beba-ctrl\ryu\app\beba\ddos\5.xlsx"
    # row, col = excel_to_sql(filepath)
    #
    # for row in range(0,3):
    #     xue_id, passwd, email = query_sql()
    #     login_xzmu(xue_id,passwd,email)
    #     time.sleep(10)
    
    # id=''
    # passwd=""
    # email=''
    # login_xzmu(id,passwd,email)