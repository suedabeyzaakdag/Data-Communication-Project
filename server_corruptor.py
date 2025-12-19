import socket
import random

def inject_error(data):
    methods = [
        lambda d: bit_flip(d),
        lambda d: char_substitution(d),
        lambda d: char_deletion(d),
        lambda d: random_insert(d),
        lambda d: swap_adjacent(d),
        lambda d: burst_error(d)
    ]

    if random.random() < 0.5:
        print(">>> Hata EKLENDİ!")
        return random.choice(methods)(data)
    
    print(">>> Veri BOZULMADAN iletiliyor.")
    return data


def bit_flip(data):
    if len(data) == 0:
        return data
    idx = random.randrange(len(data))
    flipped = chr(ord(data[idx]) ^ 1)
    return data[:idx] + flipped + data[idx+1:]


def char_substitution(data):
    if len(data) == 0:
        return data
    idx = random.randrange(len(data))
    new_char = chr(random.randint(65, 90))
    return data[:idx] + new_char + data[idx+1:]


def char_deletion(data):
    if len(data) <= 1:
        return data
    idx = random.randrange(len(data))
    return data[:idx] + data[idx+1:]


def random_insert(data):
    idx = random.randrange(len(data)+1)
    new_char = chr(random.randint(97, 122))
    return data[:idx] + new_char + data[idx:]


def swap_adjacent(data):
    if len(data) < 2:
        return data
    idx = random.randrange(len(data)-1)
    return data[:idx] + data[idx+1] + data[idx] + data[idx+2:]


def burst_error(data):
    if len(data) < 3: return data
    # 3 karakteri birden rastgele değiştir
    start = random.randint(0, len(data)-3)
    return data[:start] + "!!!" + data[start+3:]

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen(5)

    print("Server çalışıyor...")

    while True:
        conn, addr = server.accept()
        print("Client1 bağlandı:", addr)

        packet = conn.recv(4096).decode()
        print("Alınan paket:", packet)

        data, method, control = packet.split("|")

        corrupted_data = inject_error(data)

        new_packet = f"{corrupted_data}|{method}|{control}"

        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.connect(("localhost", 9998))
        c2.send(new_packet.encode())
        c2.close()

        conn.close()


if __name__ == "__main__":
    main()