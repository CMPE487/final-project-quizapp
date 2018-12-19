import sys
import time

from quizClient import *
from quizServer import *
from quizUtils import *
from utils import *


def select_option(commands, message="Please enter your command"):
    for i, command in enumerate(commands):
        print("\t", change_style(str(i + 1) + ")", 'bold'), " ", command)

    return input("\n" + change_style(message, 'underline') + ": ")


quizServer = None
quizClient = QuizClient()

clear()
while True:
    print_header("AVAILABLE COMMANDS")

    option = select_option([
        "Start new quiz",
        "Enter a quiz",
        "Broadcast quiz",
        "Quit"
    ])

    if option == "1":
        clear()
        print_header("Start New Quiz")
        quiz_name = input("\n" + change_style("Enter quiz name", 'underline') + ": ")
        quiz = Quiz(quiz_name)
        clear()
        print_header("Quiz Create Methods")
        quiz_option = select_option(["Import from file", "Enter questions manually"])
        if quiz_option == "1":
            clear()
            print_header("Import Quiz")
            filename = input("Enter file name: ")
            quiz.import_file(filename)
        else:
            clear()
            print_header("Create Quiz")
            question_count = input("How many questions your quiz has?  ")
            for i in range(int(question_count)):
                question = Question.from_input(i + 1)
                quiz.add_question(question)

        clear()
        quiz.print()
        enter_continue()
        quizServer = QuizServer(quiz)
        quizServer.listen()
        print_header("QUIZ: " + quiz.name)
        print(change_style("\n\nWAITING FOR NEW PARTICIPANTS\n\n", 'bold'))
        tmp = input("Enter for start quiz")

    elif option == "2":
        for i, quiz_name in enumerate(quizClient.available_quizzes.values()):
            print("\t", change_style(str(i + 1) + ")", 'bold'), " ", quiz_name)

        id = input("\nEnter quiz ID: ")
        if id is "":
            clear()
        else:
            username = input("\nEnter username: ")
            quiz_ip = list(quizClient.available_quizzes.keys())[int(id) - 1]
            quizClient.enter(quiz_ip, username)
            enter_continue()

    elif option == "3":
        print_header("Discover quizzes")
        quizClient.broadcast_quiz()
        enter_continue()
    elif option == "4":
        clear()
        print_notification("Good bye \n\n")
        os.system("pkill -9 \"python3 main.py\"")
        sys.exit(0)
    else:
        clear()
        print_error("Invalid option")
