import sys
import time

from quizClient import *
from quizServer import *
from quizUtils import *
from utils import *

quiz_server = None
quiz_client = QuizClient()

clear()
while True:
    option = select_option([
        "Start new quiz",
        "Enter a quiz",
        "Broadcast quiz",
        "Quit"
    ], header="AVAILABLE COMMANDS")

    if option == "1":
        clear()
        print_header("Start New Quiz")
        quiz_name = input("\n" + change_style("Enter quiz name", 'underline') + ": ")
        quiz = Quiz(quiz_name)
        clear()
        quiz_option = select_option(["Import from file", "Enter questions manually"], header="Quiz Create Methods")
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
        quiz_server = QuizServer(quiz)
        quiz_server.listen()
        print_header("QUIZ: " + quiz.name)
        print(change_style("\n\nWAITING FOR NEW PARTICIPANTS\n\n", 'bold'))
        tmp = input("Enter for start quiz")
        quiz_server.start()
    elif option == "2":
        quiz_client.broadcast_quiz(True)
        clear()
        id = select_option(quiz_client.available_quizzes.values(), prompt="Enter quiz ID", header="Enter a Quiz")

        if id is "":
            clear()
        else:
            username = input("\nEnter username: ")
            quiz_ip = list(quiz_client.available_quizzes.keys())[int(id) - 1]
            quiz_client.enter(quiz_ip, username)

    elif option == "3":
        clear()
        print_header("Discover quizzes")
        quiz_client.broadcast_quiz(False)
    elif option == "4":
        clear()
        print_notification("Good bye \n\n")
        os.system("pkill -9 \"python3 main.py\"")
        sys.exit(0)
    else:
        clear()
        print_error("Invalid option")
