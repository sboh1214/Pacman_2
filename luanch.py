import os

red = input("Red Team : ")
blue = input("Blue Team : ")
os.system("cd src")
os.system("capture.py -r "+str(red)+" -b "+str(blue))
os.system("cd ..")