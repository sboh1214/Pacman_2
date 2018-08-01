import os

print("====================")
print("Auto Launch\n")
print("ex) Drive : D:")
print("ex) Path : \dev\Pacman")
print("Enter team name without .py")
print("====================")

drive = input("Drive : ")
path = input("Path : ")

os.system(str(drive))
os.system("cd "+str(path))
os.system("cd src")

red = input("Red Team : ")
blue = input("Blue Team : ")

os.system("capture.py -r "+str(red)+".py -b "+str(blue)+".py")
os.system("cd ..")