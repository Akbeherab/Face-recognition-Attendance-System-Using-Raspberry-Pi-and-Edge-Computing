import serial
import time

lora = serial.Serial("/dev/ttyUSB0", baudrate=9600)

def send_lora_data():
    with open("attendance.txt", "r") as f:
        data = f.read()
    lora.write(data.encode())
    time.sleep(5)

if __name__ == "__main__":
    while True:
        if os.path.exists("attendance.txt"):
            send_lora_data()
            os.remove("attendance.txt")
        time.sleep(60)
