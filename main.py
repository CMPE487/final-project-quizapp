import sys
import time

from quizClient import *
from quizServer import *
from quizUtils import *
from utils import *

quizServer = None
quizClient = QuizClient()

clear()
while True:
    print_header("AVAILABLE COMMANDS")

    commands = [
        "Start new quiz",
        "Enter a quiz",
        "Broadcast quiz",
        "Quit"
    ]

    for i, command in enumerate(commands):
        print("\t", change_style(str(i + 1) + ")", 'bold'), " ", command)

    option = input("\n" + change_style("Please enter your command", 'underline') + ": ")
    if option == "1":
        clear()
        print_header("Start new quiz")
        quiz_name = input("\n" + change_style("Enter quiz name", 'underline') + ": ")
        quizServer = QuizServer(Quiz(quiz_name))
        quizServer.start()
        while True:
            print(quizServer.participants)
            time.sleep(1)

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
