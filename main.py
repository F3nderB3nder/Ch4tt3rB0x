import tkinter as tk
import socket as sok
from threading import Thread


def receive():
    while True:
        msg = chatHole.recv(4096).decode("utf8")
        convo.insert(tk.END, "Them: " + msg)


def send(event=None):
    msg = message.get()
    message.set("")
    chatHole.send(bytes(msg, "utf8"))
    if msg != "":
        convo.insert(tk.END, ("Me: " + msg))


def closeChat():
    chatHole.close()
    window.destroy()


try:
    chatHole = sok.socket()
    chatHole.connect(('localhost', 22222))
except OSError:
    print("Just waiting for someone else to arrive...please hold")
    server = sok.socket(sok.AF_INET, sok.SOCK_STREAM)
    server.bind(('localhost', 22222))
    server.listen()
    (chatHole, clientAddress) = server.accept()
    print("There they are. Happy chatting!")

window = tk.Tk()
window.title("Ch4tt3rB0x")

messagesFrame = tk.Frame(window)
message = tk.StringVar()
scrollbar = tk.Scrollbar(messagesFrame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
convo = tk.Listbox(messagesFrame, height=25, width=50)
convo.pack(side=tk.LEFT, fill=tk.BOTH)
convo.pack()
messagesFrame.pack()

textField = tk.Entry(window, textvariable=message)
textField.bind("<Return>", send)
textField.pack()

sendBtn = tk.Button(window, text="Send", command=send)
sendBtn.pack()

receive_thread = Thread(target=receive)
receive_thread.start()
window.protocol('WM_DELETE_WINDOW', closeChat)
tk.mainloop()
