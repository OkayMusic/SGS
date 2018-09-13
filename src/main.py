import socket
import thread
import threading
import time
import random


class SprongleGameServer(object):
    # good morning and welcome to my UDP server, have a nice morning
    ACK = "ACK: "

    def __init__(self, IP, port):
        """
        Initialize the socket on which the server will listen.
        """
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # bind socket to specified IP and PORT
        self.sock.bind((IP, port))

        # python ints are arbitrary precision, we can increment the ACK_ID
        # indefinitely. We need to lock the ACK_ID int with a mutex so that we
        # avoid multithreaded race conditions.
        self.lock_ACK = threading.Lock()
        self.ACK_ID = 0

        # the list of ACK's we're waiting to receieve, and a mutex for the list
        self.lock_ACK_pending = threading.Lock()
        self.ACK_pending = []

    def listen(self):
        """
        The server will listen for datagrams on port self.port.
        """
        while True:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            threading.Thread(target=self.parse_msg,
                             args=(data, addr)).start()

    def parse_msg(self, data, addr):
        """
        Parse the received message, and pass the payload to an appropriate
        handler.
        """
        def get_content_type(data):
            """
            Grab the content type. If the message was improperly formatted, it
            was probably a chinese ddoser. Here one could probably implement
            legitimate ddos protection.
            """
            for lines in data_list:
                if lines[0] == "content":
                    return lines[1]
            return "is_chinese"

        # no deps on whitespace, capitalization or carriage returns
        # keeping the data in this form is parse-friendly
        data_list = [x.replace(' ', '').lower().split(':')
                     for x in data.replace('\r', '').split("\n")]

        # get content type of the received message
        content_type = get_content_type(data_list)

        # if the message was from a rude chinese man, ask him to go away
        if content_type == "is_chinese":
            self.send(addr, "please go away mr chinaman")
            return

        # print address of client - DEBUG ONLY
        print "\nMessage received from ", addr

        # get the payload of the message
        payload = data_list[(data_list.index([""]) + 1):]

        # call appropriate handler method if it exists
        try:
            handler = getattr(self, "handle_" + content_type)
            handler(addr, payload)
        except:
            reply = "Invalid Content header"
            self.send(addr, reply)

    def send(self, addr, message):
        """
        Send a message to the client, without waiting for a response/ACK from
        the client. !This message may not reach the client!
        """
        pass

    def send_wait_ACK(self, addr, message):
        """
        Send a message to the client, waiting for an ACK. If no ACK is received,
        the message is resent until an ACK is received. 
        """
        pass


if __name__ == "__main__":
    IP = ''
    PORT = 1337

    MainServer = SprongleGameServer(IP=IP, port=PORT)
    MainServer.listen()
