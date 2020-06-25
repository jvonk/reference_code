#include <CurieBLE.h> // #include <ArduinoBLE.h>

char* name;
byte* address;
byte iBeaconData[] = {
  0x4C, 0x00, 0x02, 0x15, //Apple iBeacon
  0xB9, 0x40, 0x7F, 0x30, 0xF5, 0xF8, 0x46, 0x6E, 0xAF, 0xF9, 0x25, 0x55, 0x6B, 0x57, 0xFE, 0x6D, //Example UUD
  0x01, 0x00, // major
  0x01, 0x00, // minor
  0xF6 // meaured power at 1 meter: 0xF6 = -75.15 dBm
};

byte* mac_bytes(char* str) {
  unsigned int iMac[6];
  static byte dest[6];
  sscanf(str, "%x:%x:%x:%x:%x:%x", &iMac[0], &iMac[1], &iMac[2], &iMac[3], &iMac[4], &iMac[5]);
  for(int i=0;i<6;i++) {
    dest[i] = (byte)iMac[i];
  }
  return dest;
}

void setup() {
  Serial.begin(9600);
  while (!Serial.available()){}
  for (int i = 4; i < 20; i++) {
    iBeaconData[i]=Serial.read();
  }
  name=(char*)Serial.readString().c_str();
  BLE.setLocalName(name);
  BLE.setDeviceName(name);
  BLE.begin();
  BLE.setManufacturerData(iBeaconData, sizeof(iBeaconData));
  BLE.setEventHandler(BLEDiscovered, bleCentralDiscoverHandler);
  BLE.scan(true);
  BLE.advertise();
  address=mac_bytes((char*)BLE.address().c_str());
}

void loop() {
  BLE.poll();
}

void bleCentralDiscoverHandler(BLEDevice peripheral) {
  if (peripheral.hasManufacturerData()) {
    unsigned char manu_data[255];
    unsigned char manu_data_length;
    bool success = peripheral.getManufacturerData(manu_data, manu_data_length);
    if (success && memcmp(manu_data, "\x4c\x00\x02\x15", 4) == 0) {
      Serial.write(address,6);
      Serial.write(mac_bytes((char*)peripheral.address().c_str()),6);
      Serial.write((byte)peripheral.rssi());
      Serial.println();
    }
  }
}
