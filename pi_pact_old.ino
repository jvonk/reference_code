#include <CurieBLE.h> // #include <ArduinoBLE.h>

char* name;
char uuid[37];
byte iBeaconData[] = {
  0x4C, 0x00, 0x02, 0x15, //Apple iBeacon
  0xB9, 0x40, 0x7F, 0x30, 0xF5, 0xF8, 0x46, 0x6E, 0xAF, 0xF9, 0x25, 0x55, 0x6B, 0x57, 0xFE, 0x6D, //Example UUD
  0x01, 0x00, // major
  0x01, 0x00, // minor
  0xF6 // meaured power at 1 meter: 0xF6 = -75.15 dBm
};


void getUUID(unsigned char* data, char* buf_ptr) {
  for (int i = 4; i < 20; i++) {
      if (i==8||i==10||i==12||i==14) {
        *buf_ptr++ = '-';
      }
      buf_ptr += sprintf(buf_ptr, "%02x", (unsigned char)data[i]);
  }
  *(buf_ptr + 1) = '\0';
}

int scan = 0;
void setup() {
  Serial.begin(9600);
  while (!Serial.available()){}
  for (int i = 4; i < 20; i++) {
    iBeaconData[i]=Serial.read();
  }
  getUUID(iBeaconData, uuid);
  Serial.println(uuid);
  name=(char*)Serial.readString().c_str();
  BLE.setLocalName(name);
  BLE.setDeviceName(name);
  BLE.begin();
  BLE.setManufacturerData(iBeaconData, sizeof(iBeaconData));
  BLE.setEventHandler(BLEDiscovered, bleCentralDiscoverHandler);
  BLE.scan(true);
  BLE.advertise();
}

void loop() {
  BLE.poll();
}

void bleCentralDiscoverHandler(BLEDevice peripheral) {
  if (peripheral.hasManufacturerData()) {
    unsigned char manu_data[255];
    unsigned char manu_data_length;
    bool success = peripheral.getManufacturerData(manu_data, manu_data_length);
    if (success && memcmp(manu_data, "\x4c\x00\x02", 3) == 0) {
      Serial.print(uuid);
      Serial.print(',');
      Serial.print(scan);
      Serial.print(',');
      char buf_str[37];
      getUUID(manu_data, buf_str);
      Serial.print(buf_str);   
      Serial.print(',');
      Serial.print((manu_data[20]<<8)+ manu_data[21]);
      Serial.print(',');
      Serial.print((manu_data[22]<<8) + manu_data[23]);
      Serial.print(',');
      Serial.print(manu_data[24]);
      Serial.print(',');
      Serial.print(peripheral.rssi());
      Serial.print(',');
      Serial.println('0.0');
      scan++;
    }
  }
}
