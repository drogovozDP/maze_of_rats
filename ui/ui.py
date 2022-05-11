from tkinter import Tk
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter.constants import CENTER


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
               text="connect",
               font="Helvetica 14 bold",
               command=lambda: self.start_waiting_room('server')).place(relx=0.4,
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
               command=lambda: self.start_waiting_room('client')).place(relx=0.4,
                                                                        rely=0.45)

    def start_waiting_room(self, loader):
        if loader == 'client':
            print('client')
        elif loader == 'server':
            pass


if __name__ == '__main__':
    ui = UI()