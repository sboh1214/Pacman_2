import os

print("====================")
print("Auto Launch\n")
print("ex) Drive : D:")
print("ex) Path : dev\Pacman")
print("Enter team name without .py")
print("====================")

Drive = input("Drive : ")

os.system(str(Drive))

Path=input("Path : ")
while (Path != ""):
    os.system("cd \"" + str(Path)+"\"")
    Path=input("Path : ")

os.system("cd src")

red = input("Red Team : ")
blue = input("Blue Team : ")

os.system("capture.py -r "+str(red)+".py -b "+str(blue)+".py")
os.system("cd ..")