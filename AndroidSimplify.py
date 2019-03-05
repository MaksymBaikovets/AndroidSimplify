#import platform
import time
import subprocess
import sys
import msvcrt
import requests

from os import system
from os import getcwd

# -------------------- predefined program title --------------------

program_owner = "* This program was written by Maksym Baikovets."
disclimer = "* All you done here are under your responsibility."
final_words = "* So, don't blame me if something went wrong. Thanks for using!"

# -------------------- clear the screen --------------------

def clear():
    system("cls")

# -------------------- decorator (title and screen clear) --------------------

def decore(func):
    def run():
        try:
            clear()
            print("".join("-" for i in range(80)))
            print(program_owner, "".join \
                ("-" for i in range(79-len(program_owner))))
            print(disclimer, "".join \
                ("-" for i in range(79-len(disclimer))))
            print(final_words, "".join \
                ("-" for i in range(79-len(final_words))))
            print("".join("-" for i in range(80)))
            func()
        except Exception:
            pass
    return run

# -------------------- return to categories --------------------

# def go_back():
#     return "You'll be turned back to main menu."

# -------------------- quit the main loop --------------------

def exit_program():
    print(input("See you next time! Bye... (Press any key to exit)"))
    raise SystemExit

# -------------------- 1st block of cmds --------------------

def adb_devices():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "devices", \
        "-l"], capture_output = False)
    return "Completed!"
 
def reboot_bootloader():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "reboot", \
        "bootloader"], capture_output = False)
    return "Completed!"

def reboot_recovery():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "reboot", \
        "recovery"], capture_output = False)
    return "Completed!"

def soft_reboot():
    cmd = subprocess.run([".\\platform-tools-windows\\adb", "reboot"], \
        capture_output = False)
    return "Completed!"

cmd_switcher_1block = {
    # 0: go_back,
    1: adb_devices,
    2: reboot_bootloader,
    3: reboot_recovery,
    4: soft_reboot
}

def operation_select_1block(argument):
    # Get the command from switcher dictionary
    func = cmd_switcher_1block.get(argument)
    return func()

# -------------------- 2nd block of cmds --------------------

def fw_version():
    cmd = subprocess.run(["./platform-tools-windows/adb", "shell", \
        "getprop gsm.version.baseband"], capture_output = False)
    return "Completed!"

def flash_recovery():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    # user_choice = input()
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."
    
    elif keycode == 13:  
        
        subprocess.run([".\\platform-tools-windows\\adb", "reboot", \
            "bootloader"], capture_output = True)
        
        subprocess.run([".\\platform-tools-windows\\fastboot", "flash", \
            "recovery", ".\\files\\twrp\\twrp.img"], \
            capture_output = True)

        subprocess.run([".\\platform-tools-windows\\fastboot", "reboot"], \
            capture_output = True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."    


def flash_firmware():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    # user_choice = input()
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."
    
    elif keycode == 13:  
        
        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "mkdir /sdcard/temp"], capture_output = True)

        subprocess.run([".\\platform-tools-windows\\adb", "push", \
            getcwd()+"\\files\\fw\\firmware.zip", \
            "/sdcard/temp"], capture_output = True)

        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "twrp install /sdcard/temp/firmware.zip"], \
            capture_output = True)

        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "rm -f /sdcard/temp"], capture_output = True)

        return "OK!"
        
    else:
        print("Incorrect value!")
        return "Going back..."    

def flash_persist():
    pass 

cmd_switcher_2block = {
    # 0: go_back,
    1: fw_version,
    2: flash_recovery,
    3: flash_firmware,
    # 4: flash_persist
}

def operation_select_2block(argument):
    # Get the command from switcher dictionary
    func = cmd_switcher_2block.get(argument)
    return func()

# -------------------- 3rd block of cmds --------------------

def wipe_cache():
    pass

def wipe_system():
    pass  

def flash_system():
    pass  

def restore_system():
    pass 

def flash_gapps():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."
    
    elif keycode == 13:  

        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "mkdir /sdcard/temp"], capture_output = True)
        
        try:
            print("Choose the version of your ROM:")
            print("1 - Android 8.x")
            print("2 - Android 9.x")
            print("0 - Cancel operation")
            
            user_input = int(input())
            
            if user_input == 0:
                return "Going back..."

            elif user_input == 1:

                subprocess.run([".\\platform-tools-windows\\adb", "push", \
                    getcwd()+"\\files\\gapps\\arm64-8.1.zip", \
                    "/sdcard/temp"], capture_output = True)

                subprocess.run([".\\platform-tools-windows\\adb", "shell", \
                    "twrp install /sdcard/temp/arm64-8.1.zip"], \
                    capture_output = True)

                subprocess.run([".\\platform-tools-windows\\adb", "shell", \
                    "rm -f /sdcard/temp"], capture_output = True)
                
                return "OK!"

            elif user_input == 2:

                subprocess.run([".\\platform-tools-windows\\adb", "push", \
                    getcwd()+"\\files\\gapps\\arm64-9.0.zip", \
                    "/sdcard/temp"], capture_output = True)

                subprocess.run([".\\platform-tools-windows\\adb", "shell", \
                    "twrp install /sdcard/temp/arm64-9.0.zip"], \
                    capture_output = True)
                
                subprocess.run([".\\platform-tools-windows\\adb", "shell", \
                    "rm -f /sdcard/temp"], capture_output = True)
                
                return "OK!"
                         
        except ValueError:
            print("Not integer received!")
            time.sleep(2)
            return "Going back..."

        except TypeError:
            print("Out of available options!")
            time.sleep(2)
            return "Going back..."
        
    else:
        print("Incorrect value!")
        return "Going back..." 

cmd_switcher_3block = {
    # 0: go_back,
    # 1: wipe_cache,
    # 2: wipe_system,
    # 3: flash_system,
    # 4: restore_system,
    5: flash_gapps
}

def operation_select_3block(argument):
    # Get the command from switcher dictionary
    func = cmd_switcher_3block.get(argument)
    return func()

# -------------------- 4th block of cmds --------------------

def magisk_install():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."
    
    elif keycode == 13:  

        url = "https://github.com/topjohnwu/Magisk/releases/download/v18.1/Magisk-v18.1.zip"

        r = requests.get(url)
        file = requests.get(r.url)

        with open('./files/addons/magisk.zip', 'wb') as f:  
            f.write(file.content)

        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "mkdir /sdcard/temp"], capture_output = True)

        subprocess.run([".\\platform-tools-windows\\adb", "push", \
            getcwd()+"\\files\\addons\\magisk.zip", \
            "/sdcard/temp"], capture_output = True)

        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "twrp install /sdcard/temp/magisk.zip"], \
            capture_output = True)

        subprocess.run([".\\platform-tools-windows\\adb", "shell", \
            "rm -f /sdcard/temp"], capture_output = True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..." 
    
def launcher_install():
    pass  

def gcam_install():
    pass  

def bootanimation_install():
    pass 

cmd_switcher_4block = {
    # 0: go_back,
    1: magisk_install
    # 2: launcher_install,
    # 3: gcam_install,
    # 4: bootanimation_install
}

def operation_select_4block(argument):
    # Get the command from switcher dictionary
    func = cmd_switcher_4block.get(argument)
    return func()

# -------------------- cmds runners --------------------
# -------------------- 1st block runner --------------------

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

            if user_input == 0:
                break

            output = operation_select_1block(user_input)          
            print(output, " ", "(Press enter to continue)")
            input()
               
        except ValueError:
            print("Not integer received! Please, try again!")
            time.sleep(2)
        except TypeError:
            print("Out of available options! Please, try again!")
            time.sleep(2)
        break
    
# -------------------- 2nd block runner --------------------

@decore
def recovery_firmware():
    while True:
        try:
            print("Please, choose the command to execute (number): ")
            print("1 - Show FW version")
            print("2 - Flash recovery (TWRP)")
            print("3 - Flash FW")
            # print("4 - Restore Persist")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

            print("Type the command, please:", end = " ")
            user_input = int(input())

            if user_input == 0:
                break
            
            output = operation_select_2block(user_input)          
            print(output, " ", "(Press enter to continue)")
            input()
               
        except ValueError:
            print("Not integer received! Please, try again!")
            time.sleep(2)
        except TypeError:
            print("Out of available options! Please, try again!")
            time.sleep(2)
        break

# -------------------- 3rd block runner --------------------

@decore
def flashing_rom():
    while True:
        try:
            print("Please, choose the command to execute (number): ")
            # print("1 - Wipe Dalvik & Cache")
            # print("2 - Wipe current System")
            # print("3 - Flash new ROM")
            # print("4 - Restore ROM from the backup")
            print("5 - Flash GAPPs")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

            print("Type the command, please:", end = " ")
            user_input = int(input())

            if user_input == 0:
                break
            
            output = operation_select_3block(user_input)          
            print(output, " ", "(Press enter to continue)")
            input()
                
        except ValueError:
            print("Not integer received! Please, try again!")
            time.sleep(2)
        except TypeError:
            print("Out of available options! Please, try again!")
            time.sleep(2)
        break

# -------------------- 4th block runner --------------------

@decore
def modifications_install():
    while True:
        try:
            print("Please, choose the command to execute (number): ")
            print("1 - Install Magisk")
            # print("2 - Install Pixel Launcher")
            # print("3 - Install Google Camera")
            # print("4 - Flash Bootanimation from Pixel")
            # print("5 - Install Titanium Backup")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

            print("Type the command, please:", end = " ")
            user_input = int(input())

            if user_input == 0:
                break
            else:
                output = operation_select_4block(user_input)          
                print(output, " ", "(Press enter to continue)")
                input()
                
        except ValueError:
            print("Not integer received! Please, try again!")
            time.sleep(2)
        except TypeError:
            print("Out of available options! Please, try again!")
            time.sleep(2)
        break

# -------------------- select category --------------------

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


# -------------------- main loop of program --------------------

@decore
def main_loop():
    while True:
        try:
            # For the crossplatform support feature:
            # print("Targeted OS:", platform.system())

            print("Please, choose the category of CMDs (number): ")
            print("1 - Basics (adb devices, rebooting)")
            print("2 - Working with recovery & FW (fastboot, fw version,", \
                "update recovery / fw)")
            print("3 - Flashing ROM to device (flash ROM and GAPPs if needed)")
            print("4 - Install modifications (such as Magisk, launchers,", \
                "icons, etc.)")
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

# -------------------- launch main loop --------------------

def main():
    while True:
        main_loop()

# -------------------- program runner --------------------
if __name__ == "__main__":
    main()