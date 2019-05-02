# -------------------- import modules --------------------

import time
import subprocess
import sys
import msvcrt
import requests
import os
import zipfile


# -------------------- predefined program title --------------------

program_owner = "* This program was written by Maksym Baikovets."
disclaimer = "* All you done here are under your responsibility."
final_words = "* So, don't blame me if something went wrong. Thanks for using!"


# -------------------- clear the screen --------------------

def clear():
    os.system("cls")


# -------------------- decorator (title and screen clear) --------------------

def decore(func):
    def run():
        try:
            clear()
            print("".join("-" for i in range(80)))
            print(program_owner, "".join \
                ("-" for i in range(79 - len(program_owner))))
            print(disclaimer, "".join \
                ("-" for i in range(79 - len(disclaimer))))
            print(final_words, "".join \
                ("-" for i in range(79 - len(final_words))))
            print("".join("-" for i in range(80)))
            func()
        except Exception:
            pass

    return run


# -------------------- android tools pathes --------------------

adb_path = ".\\platform-tools\\adb"
fastboot_path = ".\\platform-tools\\fastboot"


# -------------------- quit the main loop --------------------

def exit_program():
    print(input("See you next time! Bye... (Press any key to exit)"))
    raise SystemExit


# -------------------- 1st block of cmds --------------------

def adb_devices():
    subprocess.run([adb_path, "devices", "-l"],
                   capture_output=False)
    return "Completed!"


def reboot_bootloader():
    subprocess.run([adb_path, "reboot", "bootloader"],
                   capture_output=False)
    return "Completed!"


def reboot_recovery():
    subprocess.run([adb_path, "reboot", "recovery"],
                   capture_output=False)
    return "Completed!"


def soft_reboot():
    subprocess.run([adb_path, "reboot"],
                   capture_output=False)
    return "Completed!"


cmd_switcher_1block = {
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
    subprocess.run([adb_path, "shell", "getprop", "gsm.version.baseband"],
                   capture_output=False)
    return "Completed!"


def flash_recovery():
    print("To perform this action you should be in the system!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        subprocess.run([adb_path, "reboot", "bootloader"],
                       capture_output=True)

        subprocess.run([fastboot_path, "flash", "recovery",
                        ".\\files\\twrp\\twrp.img"],
                       capture_output=True)

        subprocess.run([fastboot_path, "reboot"],
                       capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def flash_firmware():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        subprocess.run([adb_path, "shell", "mkdir", "/sdcard/temp"],
                       capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd() +
                        "\\files\\fw\\firmware.zip", "/sdcard/temp"],
                       capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "install",
                        "/sdcard/temp/firmware.zip"],
                       capture_output=True)

        subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                       capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def flash_persist():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:
        print("This operation restores persist partition.")
        print("Choose targeted device to start restore:")
        print("1 - Mi Pad 4 Plus (backup from LTE / 128 gB version)")
        # print("2 - Mi Pad 4 (backup from ... / ... gB version)")
        print("Choose targeted device to start restore:")
        keycode = ord(msvcrt.getch())
        # Need to perform backup from the regular Mi Pad 4 to add there
        # if keycode == 49 | 50:
        if keycode == 49:

            subprocess.run([adb_path, "reboot", "bootloader"],
                           capture_output=True)

            if keycode == 49:
                subprocess.run([fastboot_path, "flash", "persist",
                                ".\\files\\persist\\mipad4plus_persist.img"],
                               capture_output=True)

            elif keycode == 50:
                subprocess.run([fastboot_path, "flash", "persist",
                                ".\\files\\persist\\mipad4_persist.img"],
                               capture_output=True)

            subprocess.run([fastboot_path, "reboot"],
                           capture_output=True)

            return "OK!"

        else:
            print("Incorrect value!")
            return "Cancelled..."

    else:
        print("Incorrect value!")
        return "Going back..."


cmd_switcher_2block = {
    1: fw_version,
    2: flash_recovery,
    3: flash_firmware,
    4: flash_persist
}


def operation_select_2block(argument):
    # Get the command from switcher dictionary
    func = cmd_switcher_2block.get(argument)
    return func()


# -------------------- 3rd block of cmds --------------------

def wipe_cache():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:
        subprocess.run([adb_path, "shell", "twrp", "wipe", "cache"],
                       capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "wipe", "dalvik"],
                       capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def wipe_system():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:
        print("This operation wipes your current system. Are you sure: y/n (?)")

        keycode = ord(msvcrt.getch())
        if keycode == 110:
            return "Cancelled..."

        elif keycode == 121:

            subprocess.run([adb_path, "shell", "twrp", "wipe", "system"],
                           capture_output=True)

            return "OK!"

        else:
            print("Incorrect value!")
            return "Cancelled..."

    else:
        print("Incorrect value!")
        return "Going back..."


def flash_system():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        print(
            "This operation install/upgrade your current system. "
            "Are you sure: y/n (?)"
        )

        keycode = ord(msvcrt.getch())
        if keycode == 110:
            return "Cancelled..."

        elif keycode == 121:
            subprocess.run([adb_path, "shell", "mkdir", "/sdcard/temp"],
                           capture_output=True)

            subprocess.run([adb_path, "push",
                            os.getcwd() + "\\files\\fw\\rom.zip",
                            "/sdcard/temp"], capture_output=True)

            subprocess.run([adb_path, "shell", \
                            "twrp install /sdcard/temp/rom.zip"],
                           capture_output=True)

            subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                           capture_output=True)

            return "OK!"

        else:
            print("Incorrect value!")
            return "Going back..."

    else:
        print("Incorrect value!")
        return "Going back..."


def restore_system():
    # cmd = subprocess.run([adb_path, "shell", \
    #     r"ls -l /sdcard/TWRP/.BACKUPS/*/"], capture_output = True)

    # Need to define, in what the way user should select restore point folder
    # Investigate needs and possibilities

    # subprocess.run([adb_path, "shell", \
    #     "twrp restore <foldername> <switches>"], capture_output = True)

    pass


def flash_gapps():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        subprocess.run([adb_path, "shell", "mkdir", "/sdcard/temp"],
                       capture_output=True)

        try:
            print("Choose the version of your ROM:")
            print("1 - Android 8.x")
            print("2 - Android 9.x")
            print("0 - Cancel operation")

            user_input = int(input())

            if user_input == 0:
                return "Going back..."

            elif user_input == 1:

                subprocess.run([adb_path, "push",
                                os.getcwd() + "\\files\\gapps\\arm64-8.1.zip", "/sdcard/temp"],
                               capture_output=True)

                subprocess.run([adb_path, "shell",
                                "twrp", "install", "/sdcard/temp/arm64-8.1.zip"],
                               capture_output=True)

                subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                               capture_output=True)

                return "OK!"

            elif user_input == 2:

                subprocess.run([adb_path, "push",
                                os.getcwd() + "\\files\\gapps\\arm64-9.0.zip", "/sdcard/temp"],
                                capture_output=True)

                subprocess.run([adb_path, "shell",
                                "twrp", "install", "/sdcard/temp/arm64-9.0.zip"],
                               capture_output=True)

                subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                               capture_output=True)

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
    1: wipe_cache,
    2: wipe_system,
    3: flash_system,
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

        url = (
            "https://github.com/topjohnwu/Magisk/releases"
            "/download/v18.1/Magisk-v18.1.zip"
        )

        r = requests.get(url)
        file = requests.get(r.url)

        with open('./files/addons/magisk.zip', 'wb') as f:
            f.write(file.content)

        subprocess.run([adb_path, "shell", "mkdir", "/sdcard/temp"],
                       capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd()
                        + "\\files\\addons\\magisk.zip", "/sdcard/temp"],
                       capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "install",
                        "/sdcard/temp/magisk.zip"],
                       capture_output=True)

        subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                       capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def launcher_install():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        # Need to add dynamic load of archives

        # url = (
        #     "https://github.com/topjohnwu/Magisk/releases"
        #     "/download/v18.1/Magisk-v18.1.zip"""
        # )

        # r = requests.get(url)
        # file = requests.get(r.url)

        # with open('./files/addons/magisk.zip', 'wb') as f:  
        #     f.write(file.content)

        subprocess.run([adb_path, "shell", "mkdir", "/sdcard/temp"],
                        capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd()
                        + "\\files\\addons\\launcher.zip", "/sdcard/temp"],
                        capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd()
                        + "\\files\\addons\\matchmaker.zip", "/sdcard/temp"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "install",
                        "/sdcard/temp/matchmaker.zip"],
                       capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "install",
                        "/sdcard/temp/launcher.zip"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                        capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def gcam_install():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        subprocess.run([adb_path, "shell", "twrp", "mount", "system"],
                        capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd()
                        + "\\files\\addons\\camera.apk", "/system/app/"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "chmod", "644",
                        "/system/app/camera.apk"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "umount", "system"],
                        capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def titanium_install():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        subprocess.run([adb_path, "shell", "twrp", "mount", "system"],
                        capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd()
                        + "\\files\\addons\\titanium.apk", "/system/app/"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "chmod", "644",
                        "/system/app/titanium.apk"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "umount", "system"],
                        capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


def bootanimation_install():
    print("To perform this action you should be in the recovery!")
    print("Press 'Enter' to continue or press 'Esc' to abort operation.")
    keycode = ord(msvcrt.getch())

    if keycode == 27:
        return "Going back..."

    elif keycode == 13:

        # Need to add dynamic load of archive

        # url = (
        #     "https://github.com/topjohnwu/Magisk/releases"
        #     "/download/v18.1/Magisk-v18.1.zip"""
        # )

        # r = requests.get(url)
        # file = requests.get(r.url)

        # with open('./files/addons/magisk.zip', 'wb') as f:  
        #     f.write(file.content)

        subprocess.run([adb_path, "shell", "mkdir", "/sdcard/temp"],
                        capture_output=True)

        subprocess.run([adb_path, "push", os.getcwd()
                        + "\\files\\addons\\bootanimation.zip", "/sdcard/temp"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "twrp", "install",
                        "/sdcard/temp/bootanimation.zip"],
                        capture_output=True)

        subprocess.run([adb_path, "shell", "rm", "-rf", "/sdcard/temp"],
                        capture_output=True)

        return "OK!"

    else:
        print("Incorrect value!")
        return "Going back..."


cmd_switcher_4block = {
    1: magisk_install,
    2: launcher_install,
    3: gcam_install,
    4: titanium_install,
    5: bootanimation_install
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

            print("Type the command, please:", end=" ")
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
            print("4 - Restore Persist")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

            print("Type the command, please:", end=" ")
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
            print("1 - Wipe Dalvik & Cache")
            print("2 - Wipe System")
            print("3 - Flash new ROM")
            # print("4 - Restore ROM from the backup")
            print("5 - Flash GAPPs")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

            print("Type the command, please:", end=" ")
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
            print("2 - Install Pixel Launcher")
            print("3 - Install Google Camera")
            print("4 - Install Titanium Backup")
            print("5 - Flash Bootanimation from Pixel")
            print("0 - Go back to categories")
            print("".join("-" for i in range(80)))

            print("Type the command, please:", end=" ")
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
            print("2 - Working with recovery & FW (fastboot, fw version,",
                  "update recovery / fw)")
            print("3 - Flashing ROM to device (flash ROM and GAPPs if needed)")
            print("4 - Install modifications (such as Magisk, launchers,",
                  "icons, etc.)")
            print("0 - Exit program")
            print("".join("-" for i in range(80)))

            print("Choose the category, please:", end=" ")
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
    folders_names = ['addons', 'fw', 'gapps', 'persist']
    
    for folders in folders_names:
        if os.path.exists(os.getcwd() + '\\files\\' + folders) == False:
            os.makedirs(os.path.join(os.getcwd() + '\\files', folders))    

    try:
        if os.path.exists(os.getcwd() + '\\platform-tools') == True:
            pass
        elif os.path.exists(os.getcwd() + '\\platform-tools') == False:
            platform_tools_url = (
                "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
            )

            r = requests.get(platform_tools_url)
            file = requests.get(r.url)

            with open(os.getcwd() + '\\platform_tools.zip', 'wb') as cur_folder:
                cur_folder.write(file.content)

            zip_ref = zipfile.ZipFile(os.getcwd() + '\\platform_tools.zip', 'r')
            zip_ref.extractall(os.getcwd())
            zip_ref.close()

            os.remove('platform_tools.zip')

    except:
        print('Make sure you have platform_tools directory in current working directory.' + 
        '\n' + 'Press to continue...' + input())

    while True:
        main_loop()

# -------------------- program runner --------------------
if __name__ == "__main__":
    main()
