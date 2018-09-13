import socket

test_message = "Content: test\r\n\r\nThis is the payload."

if __name__ == "__main__":
    IP = "localhost"
    PORT = 1337

    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    s.sendto(test_message, (IP, PORT))
