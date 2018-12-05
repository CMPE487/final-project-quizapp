import queue
import socket
import json
from quizUtils import *
import threading
from time import sleep
from config import *
from _thread import *
from utils import *


class QuizClient():
    def __init__(self):
        self.available_quizzes = {}

    def start(self):
        self.listen_discovery()
        self.broadcast_quiz()

    def handle_discovery_response(self, message):
        type, source, quiz_name = message.split('|')

        if int(type) == MESSAGE_TYPES["response"]:
            self.available_quizzes[source] = quiz_name

    def receive_discovery(self):
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
                            self.handle_discovery_response(message)
                            conn.close()
                            break
                        message = message + data.decode('utf_8')

    def broadcast_quiz(self):
        for i in range(1, 255):
            target_ip = SUBNET + "." + str(i)
            if target_ip != SELF_IP:
                self.send_discovery_packet(target_ip)

    def send_discovery_packet(self, target_ip):
        message = "{}|{}".format(MESSAGE_TYPES["request"], SELF_IP)
        send_packet(target_ip, DISCOVERY_PORT, message)

    def listen_discovery(self):
        discovery_thread = threading.Thread(target=self.receive_discovery)
        discovery_thread.setDaemon(True)
        discovery_thread.start()
