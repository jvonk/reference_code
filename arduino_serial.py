import serial
import datetime
import time
import serial.tools.list_ports
import os.path
import math
coms = [serial.Serial('COM10',9600,timeout=1)]#[serial.Serial(x[0], 9600, timeout=1) for x in serial.tools.list_ports.comports()]
print('Reading from '+', '.join([x.port for x in coms]))
uuids=[b'\xe6\x6f\xae\x5f\xcc\x87\x48\x03\x9f\x87\x8e\x1e\xed\xf3\xcb\x34',
       b'\x3b\xc2\xaf\xc8\xd9\x24\x47\x2a\xb6\x17\x84\x30\xd4\x3f\x8a\xa3',
       b'\xfd\xf8\x9e\xab\x93\xb1\x46\x55\x88\x2c\x54\x0e\xc6\x51\xa1\xc8',
       b'\xc5\xcd\x55\x66\x8c\xf2\x42\x79\xbc\x8e\xd6\xa6\xb4\x28\x54\x74',
       b'\xd8\x02\x0f\xfa\x6f\xb9\x44\x78\x97\xed\x61\x53\x7a\x94\x7f\x58',
       b'\x89\xb6\xd7\x40\xb2\x28\x47\xd7\xaf\x3d\x19\xba\x4e\x49\x99\x57',
       b'\x5e\x89\x11\x5a\xea\x5b\x41\x78\xaf\xbf\x72\x41\x3b\x17\xfe\xb9',
       b'\x87\x9b\xe7\xb7\x43\x9a\x4f\x88\x8d\x88\x10\x6b\x1f\x6d\x0f\x10',
       b'\xae\xb2\x91\x9c\x5d\x50\x4c\xf0\xb8\x54\x4e\x81\x84\x74\x82\x39',
       b'\x2f\x94\x1f\x84\xf7\x59\x45\x16\x86\x35\x56\x5f\xac\xd3\x40\x49']
for i in range(len(coms)):
    coms[i].write(uuids[i])
    coms[i].write(('arduino'+str(i)).encode('ascii'))
    time.sleep(0.15/len(coms))
with open('pi_pact_scan2.csv','a+') as file:
    print('Writing to '+file.name)
    if (file.tell()<50):
        file.write('TIMESTAMP,SCANNER,ADVERTISER,TX POWER,RSSI,DIRECTION\n')
    while True:
        for i in range(len(coms)):
            data = coms[i].readline()
            print(data.hex())
            if len(data) is not 15:
                continue
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            scanner=data[:6].hex()
            advertiser=data[6:12].hex()
            tx_power='-75.15'
            rssi=str(data[12]-256)
            direction='0.0'
            file.write(','.join([timestamp, scanner, advertiser, tx_power, rssi, direction])+'\n')
        file.flush()