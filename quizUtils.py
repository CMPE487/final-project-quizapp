from threading import Thread
from utils import change_style, print_header


class Quiz:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def import_file(self, filename):
        with open(filename) as file:
            for line in file:
                body, correct_answer, *options = line.split("|")
                self.new_question(body, options, correct_answer)

    def new_question(self, body, options, correct_answer):
        self.questions.append(Question(body, options, correct_answer))

    def add_question(self, question):
        self.questions.append(question)

    def print(self):
        print_header("QUIZ: " + self.name)
        for question in self.questions:
            print()
            print(change_style("Question: ", "question") + change_style(question.body, "bold"))
            for i, option in enumerate(question.options):
                print(change_style(str(i + 1) + ") ", "bold") + option)


class Question:
    def __init__(self, body, options, correct_answer):
        self.body = body
        self.options = options
        self.correct_answer = correct_answer

    @staticmethod
    def from_input(order):
        print(change_style("\n\nQuestion {}".format(order), "bold"))
        body = input(change_style("Question body", 'underline') + ": ")
        options = []
        for i in range(4):
            option = input(change_style("Option {}".format(i + 1), 'underline') + ": ")
            options.append(option)
        correct_answer = int(input(change_style("Correct answer", 'underline') + ": "))
        return Question(body, options, correct_answer)


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
