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
        self.broadcast_quiz()

    def broadcast_quiz(self):
        for i in range(1, 255):
            target_ip = SUBNET + "." + str(i)
            # if target_ip != SELF_IP:
            start_new_thread(self.send_discovery_packet, (target_ip,))

    def send_discovery_packet(self, target_ip):
        message = "{}|{}".format(MESSAGE_TYPES["request"], SELF_IP)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((target_ip, DISCOVERY_PORT))
                s.send(message.encode('utf-8'))
                print(target_ip)
                data = s.recv(1024)
                if data:
                    type, source, quiz_name = data.decode().split('|')
                    if int(type) == MESSAGE_TYPES["response"]:
                        self.available_quizzes[source] = quiz_name
                s.close()
        except Exception as ex:
            # print("Error while sending packet: " + message)
            # print(ex.__str__() + " " + str(port))
            pass

    def enter(self, quiz_ip, username):
        print("Entering: " + quiz_ip)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((quiz_ip, QUIZ_PORT))
            message = "{}|{}|{}".format(MESSAGE_TYPES["enter"], SELF_IP, username)
            s.send(message.encode('utf-8'))
            while True:
                data = s.recv(1024)
                if not data:
                    break
                print(data)
            s.close()

    # def listen_discovery(self):
    #     discovery_thread = threading.Thread(target=self.receive_discovery)
    #     discovery_thread.setDaemon(True)
    #     discovery_thread.start()
