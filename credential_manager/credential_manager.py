import os
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

credentials = [
    "SECRET_KEY",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWD",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWD"
]

def printCredentialsName():
    for i in range(len(credentials)):
        print(i, credentials[i])
    print(len(credentials), "QUIT\n")

def changeCredential(idx, value):
    with open(os.path.join(BASE_DIR, os.environ["CRED_PATH"]), 'r') as fp:
        data = fp.read()
    cred = json.loads(data)
    cred[credentials[idx]] = value
    with open(os.path.join(BASE_DIR, os.environ["CRED_PATH"]), 'w') as fp:
        json.dump(cred, fp)

def main():
    print("\nSelect an option:")
    try_count = 0
    while True:
        try_count += 1
        printCredentialsName()
        try:
            opt = int(input())
        except Exception as e:
            opt = len(credentials) + 1
        print("")
        if opt < 0 or opt >= len(credentials):
            if opt == len(credentials):
                print("Exiting...")
                return
            if try_count >= 3:
                print("You have exhausted me")
                print("Exiting...")
                return
            print("Wrong option. Please choose again")
            print("Attempt(s) remaining %d/3\n" % (3 - try_count))
        else:
            break

    value = input("Enter new %s: " % credentials[opt])
    changeCredential(opt, value)
    print("%s changed" % credentials[opt])
    print("Starting encryption of credentials...")
    subprocess.call("python " + "encrypt.py", shell=True)


if __name__ == "__main__":
    main()
