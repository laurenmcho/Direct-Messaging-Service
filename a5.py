# Lauren Cho
# lcho6@uci.edu
# 91059503
# a5.py with GUI

"""
Contains the code necessary to run the GUI.
"""

import os
import json
import socket
import tkinter.simpledialog
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import ds_protocol
from Profile import Profile
from Profile import DsuFileError
from ds_messenger import DirectMessenger


class Body(tk.Frame):
    """
    Contains attributes for the main body of the GUI.
    """
    def __init__(self, root, recipient_selected_callback=None):
        """
        Initializes instances for body frame of GUI.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """
        Handle the selection of a node in the contacts treeview.
        """
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """
        Inserts a new contact into the contacts treeview.
        """
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """
        Used to insert an id and contact in the contacts treeview.
        """
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        """
        Inserts a user's message into the body on the right side.
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """
        Inserts a contact's message into the body on the left side.
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """
        Gets the text in the text entry box to be used for the
        send function.
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """
        Empties the text entry box.
        """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """
        Contains the actual frames that build the program's body.
        """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5,
                                      background="#95D0EC")
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    Contains the attributes for the footer part of the GUI.
    """
    def __init__(self, root, send_callback=None):
        """
        Initializes the objects for the footer.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """
        Used as the command for the save button.
        """
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """
        Contains the actual frames for the footer part of the GUI.
        """
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """
    Used to configure new information if the user wants.
    """
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """
        Initializes objects for the new information.
        """
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """
        Contains the actual frame for the body.
        """
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        """
        Allows the information that the user put in
        to actually be stored and used.
        """
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """
    Contains the main application for the GUI."""
    def __init__(self, root):
        """
        Initializes the objects needed throughout the program so that
        they can be used.
        """
        tk.Frame.__init__(self, root, username=None,
                          password=None, server=None)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.login_frame = tk.Frame
        self.profile = Profile()
        self.path = None

        # Initializes the login window
        self.login_tk = ThemedTk(theme="breeze")
        self.login_tk.title("Log In")
        self.login(self.login_tk)

        # Initializes the DirectMessenger class
        self.direct_messenger = DirectMessenger()
        self.direct_messenger.dsuserver = None
        self.direct_messenger.username = None
        self.direct_messenger.password = None

        self._draw()

    def initialize_contact(self):
        """
        Used to initialize contacts into
        the contact treeview.
        """
        for i in self.profile.contacts:
            self.body.insert_contact(i)

    def login_get(self):
        """
        Gets the information from the login pop up. The information
        is then tested to see if the profile already exists, if the
        password matches, if any fields are left blank, or if the server
        address is valid.
        """
        self.server = self.dsuserver_entry.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        # Makes sure no fieds are left blank
        if self.server == '' or self.username == '' or self.password == '':
            messagebox.showerror("Error", 'Error. Fill all fields.')

        self.path = f'./{self.username}.dsu'
        file_name = f'{self.username}.dsu'

        # Checks the connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            try:
                connection.connect((self.server, ds_protocol.PORT))

            except ConnectionError:
                messagebox.showerror("Error", 'Error. The connection failed')
            except socket.gaierror:
                messagebox.showerror("Error", 'Error. The connection failed')
            except OSError:
                messagebox.showerror("Error", 'Error. The connection failed. Please make sure you are connected to the Internet.')  # pylint: disable=line-too-long 

        # The profile exists
        if os.path.exists(self.path):
            with open(file_name, 'r', encoding="utf-8") as dsu_file:
                read = dsu_file.read()
                data = json.loads(read)
                if data["password"] == self.password:
                    self.login_tk.destroy()
                elif data["password"] != self.password:
                    messagebox.showerror("Error",
                                         "Incorrect password! Try again.")
            self.direct_messenger = DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
            self.profile = Profile()
            self.profile.load_profile(self.path)

            self.initialize_contact()
            main.after(2000, app.check_new)

        # The profile doesn't exist and a file needs to be created
        else:
            Path.touch(self.path)
            self.direct_messenger = DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
            self.profile = Profile(self.server, self.username, self.password)
            self.profile.save_profile(self.path)
            self.login_tk.destroy()
            main.after(2000, app.check_new)

    def login(self, login_root):
        """
        Contains the frames for the login GUI.
        """
        dsuserver_label = tk.Label(login_root, text="DSU Server:")
        self.dsuserver_entry = tk.Entry(login_root, background="#95D0EC")
        dsuserver_label.grid(row=0, column=0)
        self.dsuserver_entry.grid(row=0, column=1)

        username_label = tk.Label(login_root, text="Username:")
        self.username_entry = tk.Entry(login_root, background="#95D0EC")
        username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)

        password_label = tk.Label(login_root, text="Password:")
        self.password_entry = tk.Entry(login_root, show="*",
                                       background="#95D0EC")
        password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)

        login_button = tk.Button(login_root, text="Login",
                                 command=self.login_get)
        login_button.grid(row=3, column=1)

    def get_msg(self, contact_name):
        """
        Gets messages from the contacts nested dictionary from profile.
        """
        for contact, msg_dict in self.profile.contacts.items():
            if contact_name == contact:
                for each_message in msg_dict:
                    for message in each_message.values():
                        if 'True' in message[:6]:
                            user_message = message[7:]
                            self.body.insert_user_message(user_message)
                        else:
                            contact_message = message[8:]
                            self.body.insert_contact_message(contact_message)

    def send_message(self):
        """
        Allows the user to send a message and store the same message so that
        it shows up in the message entry editor.
        """
        message = self.body.get_text_entry()
        self.body.insert_user_message(message)

        # Makes sure that the user has chosen a recipient to send a message to
        try:
            self.profile.add_message(self.path, self.recipient, message, True)
            self.direct_messenger.send(message, self.recipient)
            self.body.set_text_entry('')
        except KeyError:
            messagebox.showerror("Error", "Please select a user to send a message to.")  # pylint: disable=line-too-long 
            self.body.set_text_entry('')
        except DsuFileError:
            messagebox.showerror("Error", "Invalid DSU file path or type.")  # pylint: disable=line-too-long 
            self.body.set_text_entry('')

    def add_contact_main(self):
        """
        Allows a user to add a contact to the contact treeview.
        """
        new_contact = tkinter.simpledialog.askstring("Contact",
                                                     "New Contact Name")

        # Checks if the user already exists in the contact treeview
        for key in self.profile.contacts.keys():
            if new_contact in key:
                self.same_recipient_selected(new_contact)
                return

        self.body.insert_contact(new_contact)
        self.profile.add_contact(new_contact, self.profile.path)
        print(f'add contact path: {self.profile.path}')

        self.profile.save_profile(self.profile.path)

    def recipient_selected(self, recipient):
        """
        Used when user clicks different profiles to see
        different conversations. Also ensures that the
        entry editor is cleared before loading a new chat.
        """
        self.recipient = recipient
        self.body.entry_editor.delete("1.0", "end")
        self.get_msg(self.recipient)

    def same_recipient_selected(self, recipient):
        """
        Used when user adds a contact that already exists,
        so previous messages are loaded instead of creating
        a new chat.
        """
        self.recipient = recipient
        self.get_msg(self.recipient)

    def configure_server(self):
        """
        Contains variable assignments and connection testing to ensure
        that the configured server entered by the user is valid.
        """
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        old_username = self.username
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        os.rename(old_username + '.dsu', self.username + '.dsu')

        self.profile = Profile(self.server, self.username, self.password)
        self.profile.username = ud.user
        self.profile.password = ud.pwd
        self.profile.dsuserver = ud.server
        the_path = './' + self.profile.username + '.dsu'
        self.profile.path = the_path

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            try:
                connection.connect((self.server, ds_protocol.PORT))

            except ConnectionError:
                messagebox.showerror("Error", 'Error. The connection failed')
            except socket.gaierror:
                messagebox.showerror("Error", 'Error. The connection failed')
            except OSError:
                messagebox.showerror("Error", 'Error. The connection failed')

        dm = DirectMessenger(self.server, self.username, self.password)
        dm.dsuserver = self.server
        dm.username = self.username
        dm.password = self.password

        self.profile.save_profile(the_path)

    def check_new(self):
        """
        Method used to check if a user receieved new messages
        every two seconds.
        """

        new_msg = self.direct_messenger.retrieve_new()
        # If there is a new message:
        if new_msg is not None:
            for contact, message in new_msg.items():
                # If the contact already exists then the message
                # will be displayed in that conversation
                if contact in self.profile.contacts.keys():
                    self.profile.add_message(self.path, contact, message,
                                             False)
                    self.body.insert_contact_message(message)
                # If the contact doesn't exist then the contact
                # will be added to the treeview and the message will
                # be added to the conversation
                else:
                    self.profile.add_contact(contact, self.path)
                    self.body.insert_contact(contact)
                    self.profile.add_message(self.path, contact,
                                             message, False)
                    self.body.insert_contact_message(message)
        # Calls the function in itself so the program is constantly
        # searching for new messages while it's running
        main.after(2000, self.check_new)

    def _quit(self) -> None:
        """
        Destroys the window when the user decides to quit.
        """
        if messagebox.askokcancel(
                                title="Quit",
                                message="Are you sure you want to quit?"):
            self.destroy()
            exit()

    def _draw(self):
        """
        Builds the frame itself needed for the GUI.
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        # menu_file.add_command(label='New')
        # menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close', command=self._quit)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact_main)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = ThemedTk(theme="breeze")

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
