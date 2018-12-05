import threading
import os
import json
from _thread import *
from config import *
from utils import *
from quizUtils import *


class QuizServer:

    def __init__(self, quiz):
        self.quiz = quiz
        self.participants = {}

    def start(self):
        self.listen_discovery_request()
        self.listen_quiz_request()

    def receive_discovery_request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SELF_IP, DISCOVERY_PORT))
            s.listen()
            while True:
                conn, addr = s.accept()

                data = conn.recv(1024)
                if not data:
                    break

                message = str(data.decode('utf-8'))
                type, source = message.split('|')
                if int(type) == MESSAGE_TYPES["request"]:
                    response = "{}|{}|{}".format(MESSAGE_TYPES["response"], SELF_IP, self.quiz.name)
                    conn.send(response.encode())
                conn.close()
            s.close()

    def receive_quiz_request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SELF_IP, QUIZ_PORT))
            s.listen()
            while True:
                # TODO: quiz başladıysa kabul etme, olumsuz dön
                conn, addr = s.accept()
                data = conn.recv(1024)
                if not data:
                    break

                message = str(data.decode('utf-8'))
                type, source, username = message.split('|')

                if int(type) == MESSAGE_TYPES['enter']:
                    participant = Participant(username, source, 0, conn)
                    participant.start()
                    self.participants[source] = participant
            s.close()

    def listen_discovery_request(self):
        discovery_thread = threading.Thread(target=self.receive_discovery_request)
        discovery_thread.setDaemon(True)
        discovery_thread.start()

    def listen_quiz_request(self):
        quiz_thread = threading.Thread(target=self.receive_quiz_request)
        quiz_thread.setDaemon(True)
        quiz_thread.start()
