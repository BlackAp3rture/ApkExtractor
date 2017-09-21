import sys
import os
import csv
from optparse import OptionParser
import subprocess as sub
from subprocess import Popen, CalledProcessError
from adb import adb_commands
from adb import sign_m2crypto
import os.path as op

def d2j(apk):
    print("[*] Running dex2jar : " + apk)

    try:
        path = os.path.dirname(os.path.abspath(__file__))
        os.system("sh " + path + "/dex2jar-2.0/d2j-dex2jar.sh -f " + path + "/" + apk)

        print("[*] Finished!")

    except CalledProcessError as e:
        print(e)


def decompile(apk):
    print("[*] Running apktool : " + apk)

    try:
        path = os.path.dirname(os.path.abspath(__file__))
        os.system("java -jar " + path + "/apktool.jar d " + path + "/" + apk)


        print("[*] Finished!")

    except CalledProcessError as e:
        print(e)


def adb_package(apk):
    print("[*] Searching for app relative to: " + apk + "\n")
    try:
        # os.system("adb kill-server")
        signer = sign_m2crypto.M2CryptoSigner(op.expanduser('~/.android/adbkey'))
        # Connect to the device
        device = adb_commands.AdbCommands.ConnectDevice(rsa_keys=[signer])
        # Now we can use Shell, Pull, Push, etc!
        packages = device.Shell('pm list packages | grep ' + apk)

        print("[*] Packages found! \n\n" + packages)

        print("[*] Enter package name to extract: ")

        base = raw_input()
        extract(base,apk)

    except CalledProcessError as e:
        print(e)


def extract(base,apk):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        signer = sign_m2crypto.M2CryptoSigner(op.expanduser('~/.android/adbkey'))
        # Connect to the device
        device = adb_commands.AdbCommands.ConnectDevice(rsa_keys=[signer])
        # Now we can use Shell, Pull, Push, etc!
        apk_path = device.Shell('pm path ' + base)

        new_path = apk_path[apk_path.startswith("package:") and len("package:"):]
        real_path = new_path.rstrip("\n\r")

        print("\n[*] Pulling APK located at: " + real_path)

        device.Pull(real_path, path + "/" + apk + ".apk")

        print("[*] Do you want to decompile this new apk? (Y/N)")
        base = raw_input()
        if base.rstrip("\n\r") == "y" or base.rstrip("\n\r") == "Y":
            d2j(apk + ".apk")
            decompile(apk + ".apk")
        else:
            print("Thanks! Please report any issue you may have.")
            sys.exit(0)


    except CalledProcessError as e:
        print(e)


try:
    parser = OptionParser(usage="usage: %prog [options] <apk file name>",version="%prog 1.0")
    parser.add_option("-D", "--decompile", action="store_true", default=False,help="Decompiles APK to Jar file and pulls application contents.")
    parser.add_option("-A", "--adb", action="store_true", default=False,help="Finds application on device and pulls APK.")
    (options, args) = parser.parse_args()

    if (options.decompile):
        print ("[*] Working magic on: "+ str(args[0]))
        d2j(args[0])
        decompile(args[0])

    if (options.adb):
        print ("[*] Working magic on: "+ str(args[0]))
        adb_package(args[0])

    else:
	    print ("Error")
	    print ("[X] Option not selected. View --help option.")
	    sys.exit(0)
except Exception as e:
    print(e)
