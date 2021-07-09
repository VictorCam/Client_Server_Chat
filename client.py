import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 1337))  # connected localhost to port 1337
print("CONNECTION SUCCESSFUL")

def send_data():
    text = input("CLIENT message: ")
    msg = f'{len(text)}' + " " + text
    sock.sendall(bytes(msg.encode('utf-8')))
    if(text == "/q"):  # case for quitting program
        time.sleep(0.5)  # sleeping to prevent error from occuring
        print("connection has been closed")
        # closing the following sockets and exiting program
        sock.close()
        sys.exit()

def get_data():
    # setting up default data
    result = ''
    msg = ''
    new_msg = 1
    while(1):
        if(new_msg):  # will enter once when getting the header_size
            result = sock.recv(8)  # send a message from 0-9999999!
            header_size = result.decode('utf-8')  # recv partial data w/ header
            sp = header_size.split(" ", 1)  # splitting the first space only
            if(sp[1] == "/q"):  # sp array contains partial message (quit case)
                sock.close()   # closes socket
                print("connection has been closed")
                sys.exit()  # exit the program
            if(int(sp[0]) <= 6):  # case for when input is too small
                print(sp[1])  # its a small msg so we can print it here instead
                break  # break since we got the msg
            msg_len = sp[0]  # get the length of the message
            msg += sp[1]  # get the partial msg that was taken
        result = sock.recv(4)  # get more data from server
        msg += result.decode('utf-8')  # concat message
        new_msg = 0  # prevent splitting from happening to rest of msg
        if(int(msg_len) == len(msg)):  # check if the msg = the header_size
            print(msg)  # if all message is recv then print
            new_msg = 1  # we now can do another split since msg is done
            break  # break since msg was recv


while(1):
    send_data()  # here we will get the data from the server
    get_data()  # here we will send the data to the server

# CITIED SOURCES
# https://www.youtube.com/watch?v=Lbfe3-v7yE0
# https://www.youtube.com/watch?v=8A4dqoGL62E
# https://www.geeksforgeeks.org/python-splitting-text-and-number-in-string/
# https://stackoverflow.com/questions/7899525/how-to-split-a-string-by-space/7899558
# https://realpython.com/python-sockets/
# https://docs.python.org/2/howto/sockets.html
# https://www.kite.com/python/answers/how-to-split-a-string-on-the-first-occurrence-in-python
# https://careerkarma.com/blog/python-string-to-int/
# https://docs.python.org/3/tutorial/errors.htm
