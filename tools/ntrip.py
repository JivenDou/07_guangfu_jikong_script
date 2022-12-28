import platform, socket, base64, serial, serial.tools.list_ports

# userid = 'qxwpcc001'
# password = '12345678'
userid = 'qxxtbq001'
password = '1edeed6'

# Connect Serial Port
defaultbaudrate = 115200

while True:
        try:
                print ('Available serial ports: [ ', end='')
                devices = [port.device for port in serial.tools.list_ports.comports()]
                devices.sort()
                for device in devices:
                        print (device, end=' ')
                print (']')
                
                print ('Please input serial port:')
                print ('Default: [ ', end='')
                defaultdevice = None
                if len(devices) > 0:
                        defaultdevice = devices[0]
                        if defaultdevice == 'COM1':
                                if len(devices) > 1:
                                        defaultdevice = devices[1]
                        print (defaultdevice, end=' ')
                print (']')
                
                serialnum = input()
                if serialnum == '':
                        if defaultdevice != None:
                                serialnum = defaultdevice
                else:
                        serialnum = serialnum.replace(' ', '')
                        if platform.system() == 'Windows':
                                serialnum = serialnum.upper()
                                if serialnum.find('COM') == -1:
                                        serialnum = 'COM'+serialnum
                
                print ('Please input baudrate:')
                print ('Default: [ '+str(defaultbaudrate)+' ]')
                
                baudratestr = input()
                if baudratestr == '':
                        baudrate = defaultbaudrate
                else:
                        baudrate = int(baudratestr)
                sc = serial.Serial (serialnum, baudrate, timeout=0.01)
                print ('=== Serial Connected ===')
                break
        except:
                pass

# Connect TCP
while True:
        try:
                s = socket.socket()
                s.connect(('ntrip.qxwz.com', 8002))
                s.settimeout(0)
                print('=== TCP Connected ===')
                break
        except:
                pass

# Regester
s.send(b'GET /RTCM32_GGB HTTP/1.0\r\n')
s.send(b'User-Agent: NTRIP GNSSInternetRadio/1.4.10\r\n')
s.send(b'Authorization: Basic '+base64.encodebytes((userid+':'+password).encode())+b'\r\n\r\n')
while True:
        try:
                print(s.recv(1024))
                break
        except:
                pass

sc.flush()
uartdata = b''
while True:
        uartdata += sc.read()
        i = uartdata.find(b'\r\n')
        if i != -1:
                frame = uartdata[:i+2]
                uartdata = uartdata[i+2:]
                s.send(frame)
                print('>>>', frame)
        
        try:
                tcpdata = s.recv(1024)
                sc.write(tcpdata)
                print('<<<', tcpdata)
        except:
                pass
