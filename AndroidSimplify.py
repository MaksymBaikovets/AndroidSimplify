from os import system
import time
import subprocess
import platform

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

def adb_devices():
    cmd = subprocess.run(["C:\\src\\platform-tools\\adb", "devices"], capture_output = False)
    return cmd
 
def reboot_bootloader():
    cmd = subprocess.run(["C:\\src\\platform-tools\\adb", "reboot", "bootloader"], capture_output = False)
    return cmd

def reboot_recovery():
    cmd = subprocess.run(["C:\\src\\platform-tools\\adb", "reboot", "recovery"], capture_output = False)
    return cmd

def soft_reboot():
    cmd = subprocess.run(["C:\\src\\platform-tools\\adb", "reboot"], capture_output = False)
    return cmd

switcher = {
        0: exit,
        1: adb_devices,
        2: reboot_bootloader,
        3: reboot_recovery,
        4: soft_reboot

    }

def operation_select(argument):
    # Get the command from switcher dictionary
    func = switcher.get(argument)
    return func()

@decore
def main_loop():
    while True:
        try:
            print("Targeted OS:", platform.system())
            print("Please, choose the command to execute (number): ")
            print("0 - exit program")
            print("1 - check connected devices")
            print("2 - reboot to bootloader")
            print("3 - reboot to recovery")
            print("4 - soft reboot device")
            print("Type the command, please:", end = " ")
            user_input = int(input())

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