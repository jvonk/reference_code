import serial
import datetime
import serial.tools.list_ports
import os.path
coms = [serial.Serial(x[0], 9600, timeout=1) for x in serial.tools.list_ports.comports()]
print('Reading from '+', '.join([x.port for x in coms]))
setup=[(b'\xE6\x6F\xAE\x5F\xCC\x87\x48\x03\x9F\x87\x8E\x1E\xED\xF3\xCB\x34', 'arduino1'),
       (b'\x3B\xC2\xAF\xC8\xD9\x24\x47\x2A\xB6\x17\x84\x30\xD4\x3F\x8A\xA3', 'arduino2'),
       (b'\xFD\xF8\x9E\xAB\x93\xB1\x46\x55\x88\x2C\x54\x0E\xC6\x51\xA1\xC8', 'arduino3'),
       (b'\xC5\xCD\x55\x66\x8C\xF2\x42\x79\xBC\x8E\xD6\xA6\xB4\x28\x54\x74', 'arduino4'),
       (b'\xD8\x02\x0F\xFA\x6F\xB9\x44\x78\x97\xED\x61\x53\x7A\x94\x7F\x58', 'arduino5'),
       (b'\x89\xB6\xD7\x40\xB2\x28\x47\xD7\xAF\x3D\x19\xBA\x4E\x49\x99\x57', 'arduino6'),
       (b'\x5E\x89\x11\x5A\xEA\x5B\x41\x78\xAF\xBF\x72\x41\x3B\x17\xFE\xB9', 'arduino7'),
       (b'\x87\x9B\xE7\xB7\x43\x9A\x4F\x88\x8D\x88\x10\x6B\x1F\x6D\x0F\x10', 'arduino8'),
       (b'\xAE\xB2\x91\x9C\x5D\x50\x4C\xF0\xB8\x54\x4E\x81\x84\x74\x82\x39', 'arduino9'),
       (b'\x2F\x94\x1F\x84\xF7\x59\x45\x16\x86\x35\x56\x5F\xAC\xD3\x40\x49', 'arduino10')]
for i in range(len(coms)):
    coms[i].write(bytearray(setup[i][0]))
    coms[i].write(setup[i][1].encode('ascii'))
with open('pi_pact_scan.csv','a+') as file:
    print('Writing to '+file.name)
    if (file.tell()<50):
        file.write('RECEIVER,SCAN,ADDRESS,TIMESTAMP,UUID,MAJOR,MINOR,TX POWER,RSSI\n')
    while True:
        for ser in coms:
            data = ser.readline()
            data = data.decode('ascii').rstrip().split(',')
            if (len(data)>2):
                data.insert(3, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                file.write(','.join(data)+'\n')
        file.flush()