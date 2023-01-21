# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import binascii

if __name__ == '__main__':
    filename = 'cs352_lecture.mp4'
    with open(filename, 'rb') as f:
        content = f.read()
    print(binascii.hexlify(content))


# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
