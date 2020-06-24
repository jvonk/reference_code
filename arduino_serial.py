import serial
import datetime
import time
import serial.tools.list_ports
import os.path
import math
coms = [serial.Serial(x[0], 9600, timeout=1) for x in serial.tools.list_ports.comports()]
print('Reading from '+', '.join([x.port for x in coms]))
uuids=['e66fae5f-cc87-4803-9f87-8e1eedf3cb34',
       '3bc2afc8-d924-472a-b617-8430d43f8aa3',
       'fdf89eab-93b1-4655-882c-540ec651a1c8',
       'c5cd5566-8cf2-4279-bc8e-d6a6b4285474',
       'd8020ffa-6fb9-4478-97ed-61537a947f58',
       '89b6d740-b228-47d7-af3d-19ba4e499957',
       '5e89115a-ea5b-4178-afbf-72413b17feb9',
       '879be7b7-439a-4f88-8d88-106b1f6d0f10',
       'aeb2919c-5d50-4cf0-b854-4e8184748239',
       '2f941f84-f759-4516-8635-565facd34049']
pos = {'COM3': (2, 2),
       'COM9': (3, 0),
       'COM7': (1, 0),
       'COM8': (2, 0),
       'COM5': (0, 2),
       'COM6': (0, 0),
       'COM10': (3, 2)}
for i in range(len(coms)):
    coms[i].write(bytes.fromhex(uuids[i].replace('-','')))
    coms[i].write(('arduino'+str(i)).encode('ascii'))
    time.sleep(0.15/len(coms))
with open('pi_pact_scan.csv','a+') as file:
    print('Writing to '+file.name)
    if (file.tell()<50):
        file.write('TIMESTAMP,SCANNER,ADVERTISER,TX POWER,RSSI,DISTANCE\n')
    while True:
        for i in range(len(coms)):
            ser=coms[i]
            data = ser.readline()
            data = data.decode('ascii').rstrip().split(',')
            if (len(data)>2):
                try:
                    j=uuids.index(data[3])
                except:
                    print('UUID ('+data[3]+') not recognized')
                else:
                    a=pos[coms[i].name]
                    b=pos[coms[j].name]
                    new=[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), str(i), str(j), data[6], data[7], "{:.1f}".format(math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)*24)]
                    file.write(','.join(new)+'\n')
        file.flush()