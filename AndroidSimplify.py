from os import system
import time
import subprocess
#import platform

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

def go_back():
    print("You'll be turned back to main menu.")
    return 
    # print(input("See you next time! Bye... (Press any key to close the window)"))
    # raise SystemExit

def adb_devices():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "devices"], capture_output = False)
    return cmd
 
def reboot_bootloader():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "reboot", "bootloader"], capture_output = False)
    return cmd

def reboot_recovery():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "reboot", "recovery"], capture_output = False)
    return cmd

def soft_reboot():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "reboot"], capture_output = False)
    return cmd

cmd_switcher = {
        0: go_back,
        1: adb_devices,
        2: reboot_bootloader,
        3: reboot_recovery,
        4: soft_reboot
    }

def operation_select(argument):
    # Get the command from switcher dictionary
    func = cmd_switcher.get(argument)
    return func()

def exit_program():
    print(input("See you next time! Bye... (Press any key to close the window)"))
    raise SystemExit

@decore
def basic_functions():
    while True:
        try:
            print("Please, choose the command to execute (number): ")
            print("1 - Check connected devices")
            print("2 - Reboot to bootloader")
            print("3 - Reboot to recovery")
            print("4 - Soft reboot device")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

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
    
@decore
def recovery_firmware():
    pass

@decore
def flashing_rom():
    pass

@decore
def modifications_install():
    pass

category_switcher = {
    0: exit_program,
    1: basic_functions,
    2: recovery_firmware,
    3: flashing_rom,
    4: modifications_install
}

def category_select(argument):
    # Get the command from switcher dictionary
    func = category_switcher.get(argument)
    return func()

@decore
def main_loop():
    while True:
        try:
            # For the crossplatform support feature:
            # print("Targeted OS:", platform.system())
            print("Please, choose the category of CMDs (number): ")
            print("1 - Basics (adb devices, rebooting)")
            print("2 - Working with recovery & FW (fastboot, fw version, update recovery / fw)")
            print("3 - Flashing ROM to device (flash ROM and GAPPs if needed)")
            print("4 - Install modifications (such as Magisk, launchers, icons, etc.)")
            print("0 - Exit program")
            print("".join("-" for i in range(80)))
            
            print("Choose the category, please:", end = " ")
            selector = int(input())
            category_select(selector)

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