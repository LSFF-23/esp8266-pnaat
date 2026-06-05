#tbi
# mpu6050.py - MicroPython driver for MPU-6050
class mpu6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00') # Wake up MPU-6050

    def get_raw_values(self):
        res = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        return res

    def bytes_to_int(self, first_byte, second_byte):
        if not first_byte & 0x80:
            return (first_byte << 8) | second_byte
        return -(((first_byte ^ 255) << 8) | (second_byte ^ 255) + 1)

    def get_values(self):
        raw = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_to_int(raw[0], raw[1])
        vals["AcY"] = self.bytes_to_int(raw[2], raw[3])
        vals["AcZ"] = self.bytes_to_int(raw[4], raw[5])
        vals["Tmp"] = self.bytes_to_int(raw[6], raw[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_to_int(raw[8], raw[9])
        vals["GyY"] = self.bytes_to_int(raw[10], raw[11])
        vals["GyZ"] = self.bytes_to_int(raw[12], raw[13])
        return vals

#tbi
if __name__ == "__main__":
    from machine import Pin, I2C
    import time

    scl = Pin(5, Pin.OUT)
    sda = Pin(4, Pin.OUT)
    i2c = I2C(scl=scl, sda=sda)
    sensor = mpu6050(i2c)

    while True:
        data = sensor.get_values()
        
        ax = data["AcX"]
        ay = data["AcY"]
        az = data["AcZ"]
        gx = data["GyX"]
        gy = data["GyY"]
        gz = data["GyZ"]
        tmp = data["Tmp"]
        
        print(f"ACCEL -> X: {ax:6d} | Y: {ay:6d} | Z: {az:6d}")
        print(f"GYRO  -> X: {gx:6d} | Y: {gy:6d} | Z: {gz:6d}")
        print(f"TEMP  -> {tmp:.1f} °C\n")
        
        time.sleep(0.5)