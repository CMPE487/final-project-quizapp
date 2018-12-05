import threading
import os
import json
from _thread import *
from config import *
from utils import *

class QuizServer:

    def __init__(self, quiz):
        self.quiz = quiz
        self.participants = {}

    def start(self):
        self.listen_discovery_request()
        self.broadcast_quiz()

    def handle_discovery_request(self, message):
        type, source, *tmp = message.split('|')

        if int(type) == MESSAGE_TYPES["request"]:
            start_new_thread(self.send_discovery_packet, (source,))

    def receive_discovery_request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SELF_IP, DISCOVERY_PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    message = ""
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            # print(message)
                            self.handle_discovery_request(message)
                            # conn.send(b"OK")
                            conn.close()
                            break
                        message = message + data.decode('utf_8')

    def listen_discovery_request(self):
        discovery_thread = threading.Thread(target=self.receive_discovery_request)
        discovery_thread.setDaemon(True)
        discovery_thread.start()

    def broadcast_quiz(self):
        for i in range(1, 255):
            target_ip = SUBNET + "." + str(i)
            if target_ip != SELF_IP:
                self.send_discovery_packet(target_ip)

    def send_discovery_packet(self, target_ip):
        message = "{}|{}|{}".format(MESSAGE_TYPES["response"], SELF_IP, self.quiz.name)
        send_packet(target_ip, DISCOVERY_PORT, message)
