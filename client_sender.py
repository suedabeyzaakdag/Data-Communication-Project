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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    text = input("Gönderilecek metni girin: ")
    print("\nLütfen Kontrol Yöntemi Seçin:")
    print("1: CRC16\n2: Parity\n3: Checksum\n4: 2D-Parity")
    secim = input("Seçiminiz (1-4): ")

    if secim == "1":
        method, control = "CRC16", crc16(text)
    elif secim == "2":
        method, control = "PARITY", calculate_parity(text)
    elif secim == "3":
        method, control = "CHECKSUM", internet_checksum(text)
    elif secim == "4":
        method, control = "2DPARITY", calculate_2d_parity(text)
    else:
        print("Geçersiz seçim, CRC16 varsayılan seçildi.")
        method, control = "CRC16", crc16(text)

    packet = f"{text}|{method}|{control}"
    client.send(packet.encode())
    print("\nGönderilen Paket:", packet)
    client.close()


if __name__ == "__main__":
    main()