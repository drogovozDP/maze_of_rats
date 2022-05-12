from tkinter import Tk
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter.constants import CENTER
from network.server import Server
from network.client import Client


class UI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.start_screen = Toplevel()
        self.start_screen.title("Maze of Rats: start menu")
        self.start_screen.resizable(width=False,
                                    height=False)
        self.start_screen.configure(width=400,
                                    height=300)

        Label(self.start_screen,
              text="Host or connect",
              justify=CENTER,
              font="Helvetica 14 bold").place(relheight=0.15,
                                              relx=0.3,
                                              rely=0.07)

        Button(self.start_screen,
               text="host",
               font="Helvetica 14 bold",
               command=lambda: self.start_server_screen()).place(relx=0.4,
                                                          rely=0.45)

        Button(self.start_screen,
               text="connect",
               font="Helvetica 14 bold",
               command=lambda: self.start_client_screen()).place(relx=0.4,
                                                          rely=0.55)


        self.window.mainloop()

    def start_server_screen(self):
        """
        creates screen for setup game
        """
        print('start server')
        self.start_screen.destroy()

        self.setup_screen = Toplevel()
        self.setup_screen.title("Maze of Rats: connection")
        self.setup_screen.resizable(width=False,
                                         height=False)
        self.setup_screen.configure(width=400,
                                         height=300)

        # Address section
        addr_entry = Entry(self.setup_screen,
                           font="Helvetica 14")
        addr_entry.place(relwidth=0.6,
                         relheight=0.12,
                         relx=0.35,
                         rely=0.2)
        addr_entry.focus()

        Label(self.setup_screen,
              text="Address:",
              justify=CENTER,
              font="Helvetica 14 bold").place(relheight=0.15,
                                              relx=0.08,
                                              rely=0.2)

        # Bots sections
        bots_count_entry = Entry(self.setup_screen,
                                 font="Helvetica 14")
        bots_count_entry.place(relwidth=0.6,
                               relheight=0.12,
                               relx=0.35,
                               rely=0.4)

        Label(self.setup_screen,
              text="Bot count:",
              justify=CENTER,
              font="Helvetica 14 bold").place(relheight=0.15,
                                              relx=0.08,
                                              rely=0.4)

        # Button to next screen
        Button(self.setup_screen,
               text="next",
               font="Helvetica 14 bold",
               command=lambda: self.start_waiting_room('server',
                                                       address=addr_entry.get(),
                                                       bots=bots_count_entry.get()
                                                       )).place(relx=0.4,
                                                                rely=0.65)

    def start_client_screen(self):
        """
        creates screen to connect to host
        """
        print('client screen')
        self.start_screen.destroy()

        self.connection_screen = Toplevel()
        self.connection_screen.title("Maze of Rats: connection")
        self.connection_screen.resizable(width=False,
                                         height=False)
        self.connection_screen.configure(width=400,
                                         height=300)

        addr_entry = Entry(self.connection_screen,
                           font="Helvetica 14")
        addr_entry.place(relwidth=0.6,
                         relheight=0.12,
                         relx=0.2,
                         rely=0.2)
        addr_entry.focus()

        Label(self.connection_screen,
              text="Write server address",
              justify=CENTER,
              font="Helvetica 14 bold").place(relheight=0.15,
                                              relx=0.25,
                                              rely=0.01)

        Button(self.connection_screen,
               text="connect",
               font="Helvetica 14 bold",
               command=lambda: self.start_waiting_room('client',
                                                       address=addr_entry.get()
                                                       )).place(relx=0.4,
                                                                rely=0.45)

    def start_waiting_room(self, loader, **kwargs):
        try:
            ip, port = kwargs['address'].split(':')
            port = int(port)
        except:
            ip, port = '127.0.0.1', 8000

        if loader == 'server':
            bots = kwargs['bots']
            self.server = Server(ip, int(port), self)
            print('server', ip, port, bots)
            self.setup_screen.destroy()

            # UI
            self.waiting_room = Toplevel()
            self.waiting_room.title("Maze of Rats: waiting for players")
            self.waiting_room.resizable(width=False,
                                        height=False)
            self.waiting_room.configure(width=400,
                                        height=300)

            self.players_count_label = Label(self.waiting_room,
                                             text="Players: 0",
                                             justify=CENTER,
                                             font="Helvetica 14 bold")
            self.players_count_label.place(relheight=0.15,
                                           relx=0.08,
                                           rely=0.4)

            Button(self.waiting_room,
                   text="start",
                   font="Helvetica 14 bold",
                   command=lambda: self.server.start_game()).place(relx=0.4, rely=0.4)
        else:
            # UI
            self.connection_screen.destroy()
            self.waiting_room = Toplevel()
            self.waiting_room.title("Maze of Rats: waiting for players")
            self.waiting_room.resizable(width=False,
                                        height=False)
            self.waiting_room.configure(width=400,
                                        height=300)

            self.cleint = Client(ip, port, self)
            self.players_count_label = Label(self.waiting_room,
                                             text=f"Waiting for host. Your id = {self.cleint.id} \n All players = {self.cleint.players_count}",
                                             justify=CENTER,
                                             font="Helvetica 14 bold")
            self.players_count_label.place(relheight=0.15,
                                           relx=0.08,
                                           rely=0.4)
            # self.cleint.sock.recv(1024)

    def update_player_count(self, count, which):
        if which == "server":
            text = f"Players: {count}"
        else:
            text = f"Waiting for host. Your id = {self.cleint.id} \n All players = {count}"
        self.players_count_label.config(text=text)
