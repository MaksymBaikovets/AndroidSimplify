from os import system
import time
#import subprocess

#subprocess.run("ll", capture_output = True)
#cmd = subprocess.run(["C:\\src\\platform-tools\\adb", "devices"], capture_output = False)
#print(cmd)

program_owner = "* This program was written by Maksym Baikovets."
disclimer = "* All you done here are under your responsibility."
final_words = "* So, don't blame me if something went wrong. Thanks for using!"

def clear():
    system("cls")

def decore(func):
    def run():
        try:
            clear()
            print("".join("-" for i in range(80)))
            print(program_owner, "".join("-" for i in range(79-len(program_owner))))
            print(disclimer, "".join("-" for i in range(79-len(disclimer))))
            print(final_words, "".join("-" for i in range(79-len(final_words))))
            print("".join("-" for i in range(80)))
            func()
        except Exception:
            pass
    return run

def exit():
    print(input("See you next time! Bye... (Press any key to close the window)"))
    raise SystemExit

def zero():
    return "zero"
 
def one():
    return "one"

switcher = {
        0: exit,
        1: zero,
        2: one
    }

def operation_select(argument):
    # Get the command from switcher dictionary
    func = switcher.get(argument)
    return func()

@decore
def main_loop():
    while True:
        try:
            user_input = int(input("Please, choose the command to execute (number): "))
            output = operation_select(user_input)
            print(output, " ", "(Press enter to continue)")
            input()
        except ValueError:
            print("Not integer received! Please, try again!")
            time.sleep(2)
        except TypeError:
            print("Out of available options! Please, try again!")
            time.sleep(2)
        break

def main():
    while True:
        main_loop()

if __name__ == "__main__":
    main()