from threading import Thread


class Quiz:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self):
        pass


class Question:
    def __init__(self, body, options, correct_answer):
        self.body = body
        self.options = options
        self.correct_answer = correct_answer


class Participant(Thread):
    def __init__(self, username, ip, score, connection):
        Thread.__init__(self)
        self.username = username
        self.ip = ip
        self.score = score
        self.connection = connection

    def run(self):
        self.connection.send("Welcome".encode())
        while True:
            data = self.connection.recv(1024)
            print(data)

    def close(self):
        self.connection.close()
