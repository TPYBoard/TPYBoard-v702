import pyb
import upcd8544
from machine import SPI,Pin
from pyb import UART
 
SPI = pyb.SPI(1) #DIN=>X8-MOSI/CLK=>X6-SCK
#DIN =>SPI(1).MOSI 'X8' data flow (Master out, Slave in)
#CLK =>SPI(1).SCK  'X6' SPI clock
RST    = pyb.Pin('X20')
CE     = pyb.Pin('X19')
DC     = pyb.Pin('X18')
LIGHT  = pyb.Pin('X17')
lcd_5110 = upcd8544.PCD8544(SPI, RST, CE, DC, LIGHT)
N1 = Pin('Y6', Pin.OUT_PP)
N1.low()
lcd_5110.lcd_write_string('Getting Ready',0,1)
pyb.delay(2000)
N1.high()
pyb.delay(10000)
u2 = UART(4, 115200,timeout = 100)
Message = 'Hello,I am TPYBoard v702'#��������Ҫ���͵Ķ��ŵ����ݣ�
number = '1800000000'#������Ҫ���͵��ֻ���
 
lcd_5110.lcd_write_string('Send Message',0,1)
lcd_5110.lcd_write_string(str(Message),0,2)
u2.write('AT+CMGF=1\r\n')#�������ı���ʽ���Ͷ���
while True:
    if u2.any() > 0:
        _dataRead = u2.read()
        print('dataRead:',_dataRead)
        if _dataRead.find(b'AT+CMGF=1\r\n\r\nOK\r\n') > -1:
            u2.write('AT+CSCS="GB2312"\r\n')#�����ı�����
            lcd_5110.lcd_write_string('..',0,4)
        elif _dataRead.find(b'AT+CSCS="GB2312"\r\n\r\nOK\r\n') > -1:
            u2.write('AT+CNMI=2,2\r\n')#�յ�����ֱ�Ӹ�����ʾ
            lcd_5110.lcd_write_string('...',0,4)
        elif _dataRead.find(b'AT+CNMI=2,2\r\n\r\nOK\r\n') > -1:
            u2.write('AT+CMGS="'+number+'"\r\n')#����Է��ֻ���
            lcd_5110.lcd_write_string('....',0,4)
        elif _dataRead.find(b'AT+CMGS="'+number+'"\r\n\r\n> ') > -1:
            u2.write(Message+'\r\n')#�����������
            lcd_5110.lcd_write_string('.....',0,4)
        elif _dataRead.find(b'\r\n+CMGS') > -1 and _dataRead.find(b'OK') > -1:
            print('Send success')
            lcd_5110.lcd_write_string('Send success!',0,4)
        elif _dataRead.find(b''+Message+'') > -1:
            lcd_5110.lcd_write_string('......',0,4)
        else:
            print('error')