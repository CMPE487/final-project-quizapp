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
