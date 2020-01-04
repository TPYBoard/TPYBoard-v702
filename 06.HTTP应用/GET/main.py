import pyb
from machine import SPI,Pin
from pyb import UART
import json

#GU620模块初始化
N1 = Pin('Y6', Pin.OUT_PP)#定义通信系统启动引脚
N1.low()
pyb.delay(2000)
N1.high()
pyb.delay(10000)#拉高拉低引脚，启动通信系统
u2 = UART(4,115200,timeout = 50)#定义串口4，设置 波特率为115200
#初始化 HTTP 应用
u2.write('AT+HTTPINIT\r\n')
getURLCMD = 'AT+HTTPPARA=1,"http://old.tpyboard.com/v702/httptest.php?t=123456"\r\n'
#getURLCMD = 'AT+HTTPPARA=1,"https://www.baidu.com"\r\n'
while True:
    if u2.any() > 0:
        dataRead = u2.read()
        print('_dataRead:',dataRead)
        print('-'*30)
        if dataRead.find(b'OK') > -1:
            #AT命令执行成功
            #判断是执行的哪一步操作
            if dataRead.find(b'AT+HTTPINIT') > -1:
                #初始化HTTP成功
                #设置 HTTP 参数值 设置url
                u2.write(getURLCMD)
            elif dataRead.find(b'AT+HTTPPARA=1') > -1:
                #HTTP参数设置成功
                #发起GET请求获取数据
                u2.write('AT+HTTPACTION=0\r\n')
            elif dataRead.find(b'AT+HTTPREAD\r\n\r\n+HTTPREAD') > -1:
                #返回可用的数据信息，进行解析 获取到数据长度
                datalen = dataRead.decode().split(':')[1].split(',')[0]
                print('datalen:',datalen)
                #从第0位开始 读取指定长度的数据
                u2.write('AT+HTTPREAD=0,{}\r\n'.format(datalen))
            elif dataRead.find(b'HTTP/1.1 200 OK') > -1:
                #成功读取数据后 停止HTTP应用
                u2.write('AT+HTTPTERM')
                #进行数据解析 提取出我们需要的信息
                b = dataRead.decode()
                c = "{"+b.split('{')[-1].split('}')[0]+"}"
                #转成json对象 查看是否请求成功
                jsonobj = json.loads(c)
                print(jsonobj["status"])
                pyb.delay(100)
                break
        elif dataRead.find(b'ERROR') > -1:
            #AT命令执行失败
            if dataRead.find(b'AT+HTTPINIT') > -1:
                #初始化HTTP失败 有可能是之前的没有停止等原因
                #发送停止HTTP命令 再重新初始化
                u2.write('AT+HTTPTERM\r\n')
                pyb.delay(300)
                u2.write('AT+HTTPINIT\r\n')
        else:
            if dataRead.find(b'\r\n+HTTPACTION: 0, 200') > -1:
                #收到的数据提示 说明请求成功
                #查询当前可用数据
                u2.write('AT+HTTPREAD\r\n')
            