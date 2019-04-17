import pyb
import upcd8544
from machine import SPI,Pin
from pyb import UART
 
#lcd5110��ʼ��
SPI = pyb.SPI(1) #DIN=>X8-MOSI/CLK=>X6-SCK
#DIN =>SPI(1).MOSI 'X8' data flow (Master out, Slave in)
#CLK =>SPI(1).SCK  'X6' SPI clock
RST    = pyb.Pin('X20')
CE     = pyb.Pin('X19')
DC     = pyb.Pin('X18')
LIGHT  = pyb.Pin('X17')
lcd_5110 = upcd8544.PCD8544(SPI, RST, CE, DC, LIGHT)
lcd_5110.clear()
lcd_5110.lcd_write_string('Getting Ready',0,1)
#GU620ģ���ʼ��
N1 = Pin('Y6', Pin.OUT_PP)#����ͨ��ϵͳ��������
N1.low()
pyb.delay(2000)
N1.high()
pyb.delay(10000)#�����������ţ�����ͨ��ϵͳ
u2 = UART(4,115200,timeout = 100)#���崮��4������ ������Ϊ115200
#������ϸ��ʽ˵�������ܲ����ӷ���ƽ̨ʾ�����ĸ�ʽ��
#www.turnipsmart.com:8080
message = 'TPGPS,1234567890abcde,36.67191670,119.17200000,201701120825,25,50,END'
if __name__ == '__main__':
    #����TCP������
    u2.write('AT+CIPSTART="TCP","139.196.110.155",30000\r\n')
    while True:
        if u2.any() > 0:
            _dataRead = u2.read()
            print('_dataRead:',_dataRead)
            if _dataRead.find(b'CONNECT OK') > -1:
                #˵���Ѿ��ͷ������ɹ���������
                lcd_5110.lcd_write_string('CONNECT OK',0,2)
                print('CONNECT OK')
                pyb.LED(2).on()
                #����ָ�����͸��ģʽ
                u2.write('ATO0\r\n')
            if _dataRead.find(b'ATO0\r\n\r\nOK\r\n') > -1:
                #�ɹ�����͸��ģʽ,�˳�͸��ģʽ����+++,ע��ǰ��1���ڲ��������κ��ַ�
                #�������ݸ�������
                u2.write(message)
            if _dataRead.find(b'TPGPSOK') > -1:
                #������Ϊ����������
                #������������������ݺ󣬷�����������ݽ����жϣ�������Ӧ�ı���
                pyb.LED(3).on()
                lcd_5110.lcd_write_string('SEND OK',0,3)
                break