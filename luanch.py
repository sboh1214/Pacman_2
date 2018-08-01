import os

print("====================")
print("Auto Launch\n")
print("ex) Path : ")
print("====================")

path = input("Path : ")
red = input("Red Team : ")
blue = input("Blue Team : ")
os.system("cd "+path)
os.system("capture.py -r "+str(red)+" -b "+str(blue))
os.system("cd ..")