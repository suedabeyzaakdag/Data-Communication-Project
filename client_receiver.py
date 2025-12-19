import socket

def calculate_parity(data):
    total_ones = sum(bin(ord(c)).count('1') for c in data)
    return "EVEN" if total_ones % 2 == 0 else "ODD"

def internet_checksum(data):
    total = sum(ord(c) for c in data)
    return format(total & 0xFFFF, "04X")

def calculate_2d_parity(data):
    rows = [data[i:i+4] for i in range(0, len(data), 4)]
    row_parities = ""
    for r in rows:
        row_parities += "0" if sum(bin(ord(c)).count('1') for c in r) % 2 == 0 else "1"
    return row_parities 
def crc16(data: str):
    crc = 0xFFFF
    poly = 0x1021

    for byte in data.encode("utf-8"):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF

    return format(crc, "04X")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9998))
    server.listen(5)

    print("Client2 (Receiver) çalışıyor...")

    while True:
        conn, addr = server.accept()
        print("Server bağlandı:", addr)

        packet = conn.recv(4096).decode()
        data, method, incoming_control = packet.split("|")

        if method == "CRC16":
            computed = crc16(data)
        elif method == "PARITY":
            computed = calculate_parity(data)
        elif method == "CHECKSUM":
            computed = internet_checksum(data)
        elif method == "2DPARITY":
            computed = calculate_2d_parity(data)
        else:
            computed = "UNKNOWN"

        print("\n===== SONUÇ =====")
        print("Alınan Veri         :", data)
        print("Yöntem              :", method)
        print("Gönderilen CRC      :", incoming_control)
        print("Hesaplanan CRC      :", computed)

        if incoming_control == computed:
            print("Durum: DATA CORRECT ✓")
        else:
            print("Durum: DATA CORRUPTED ✗")

        conn.close()


if __name__ == "__main__":
    main()