import aiml
import os
import time
import random

from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import *

bot_name = "Nicole"
user_name = "Admin"
def_font_color = "#ffffff"
kernel = aiml.Kernel()


class ChatBot(Frame):
    def __init__(self, master, **kwargs):

        Frame.__init__(self, master)

        self.master = master
        # For the messages to be displayed
        self.chat_page_bot = Text(self, **kwargs)
        self.chat_page_bot.pack(side=LEFT, fill=BOTH, expand=True)

        self.chat_page_user = Text(self, **kwargs)
        self.chat_page_user.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.gui()

    def chat(self):
        kernel.verbose(0)
        kernel.setBotPredicate("name", bot_name)
        kernel.setPredicate('name', user_name)

        if os.path.isfile("bot_brain.brn"):
            kernel.bootstrap(brainFile="bot_brain.brn")
        else:
            kernel.bootstrap(learnFiles="startup.xml", commands="LOAD AIML B")
            kernel.saveBrain("bot_brain.brn")

        # kernel now ready for use

    def gui(self):
        # Calls the chat function which prepares the kernel and loads the Brain.
        self.chat()
        start = time.clock()

        # Info box to let the user know about the chat room.
        def info(event=None):
            messagebox.showinfo('Info', 'This is Nicole, the Tech Support ChatBot of your company. \n'
                                        'Entity made with the help of AIML and bit of Python.\n'
                                        '\n'
                                        'Your conversations are being logged for development purposes'
                                        '\n'
                                        'For queries contact: admin@company_name.co.in\n')

        # Function that is associated with the choosing of the font color
        def user_font_color_chooser(event=None):
            color = askcolor('#00B9E3', title='User Font Color')[1]
            self.chat_page_user.config(fg=color)

        def bot_font_color_chooser(event=None):
            color = askcolor('#00B9E3', title='Bot Font Color')[1]
            self.chat_page_bot.config(fg=color)

        def reset(event=None):
            self.chat_page_user.config(fg=def_font_color)
            self.chat_page_bot.config(fg=def_font_color)

        # GUI to change the name of the Bot.
        def name_bot(event=None):
            master_bot = Tk()
            master_bot.config(bg='#2e2e2e', bd=10)
            master_bot.title("Bot Name")
            master_bot.resizable(0, 0)
            master_bot.iconbitmap('icon (1).ico')

            label = Label(master_bot, text='Enter Preferred Bot Name', font=('Papyrus', 12, 'bold'),
                          bg='#1f1f1f', fg='#f0f0f0', height=2)
            label.grid(row=0, sticky=N + S + E + W)
            text = Text(master_bot, height=2, width=20, bg='#2e2e2e', fg='#f0f0f0', relief=FLAT)
            text.grid(row=1, column=0, sticky=N + S + E + W)

            def set_bot_name(event='<Return>'):
                global bot_name
                bot_name = text.get(1.0, END)
                bot_name = bot_name.rstrip()
                kernel.setBotPredicate("name", bot_name)
                master_bot.destroy()

            butt = Button(master_bot, text="Ok", font=('Papyrus bold', 10, 'bold'), command=set_bot_name,
                          width=17, height=1, pady=5, relief=GROOVE, overrelief=GROOVE, bg='#2e2e2e', fg='#f0f0f0')
            butt.grid(row=2, column=0, sticky=N + S + E + W)
            master_bot.mainloop()

        # GUI to set the name of the User.
        def name_user(event=None):
            master_user = Tk()
            master_user.config(bg='#2e2e2e', bd=10)
            master_user.title("User Name")
            master_user.resizable(0, 0)
            master_user.iconbitmap('icon (1).ico')

            label = Label(master_user, text='Enter Your Name', font=('Papyrus', 12, 'bold'),
                          bg='#1f1f1f', fg='#f0f0f0', height=2)
            label.grid(row=0, sticky=N + S + E + W)
            text = Text(master_user, height=2, width=20, bg='#2e2e2e', fg='#f0f0f0', relief=FLAT)
            text.grid(row=1, column=0, sticky=N + S + E + W)

            def set_user_name(event='<Return>'):
                global user_name
                user_name = text.get(1.0, END)
                user_name = user_name.rstrip()
                kernel.setPredicate("name", user_name)
                master_user.destroy()

            butt = Button(master_user, text="Ok", font=('Papyrus', 10, 'bold'), command=set_user_name,
                          width=17, height=1, pady=5, relief=GROOVE, overrelief=GROOVE, bg='#2e2e2e', fg='#f0f0f0')
            butt.grid(row=2, column=0, sticky=N + S + E + W)
            master_user.mainloop()

        # Function that handles the conversation.
        def messages(event='<Return>'):
            excitation = ''
            self.chat_page_user.config(state=NORMAL)
            self.chat_page_bot.config(state=NORMAL)

            def user():
                global excitation

                excitation = entry.get(1.0, END).strip()
                excite_msg = excitation
                self.chat_page_user.insert(END, excite_msg+"  ")
                self.chat_page_user.insert(END, '\n\n')
                self.chat_page_user.tag_configure("right", justify=RIGHT)
                self.chat_page_user.tag_add("right", 1.0, END)
                self.chat_page_user.yview(END)

                entry.delete('1.0', END)
                status_label.config(text=kernel.getBotPredicate('name') + ' is typing......')
                self.chat_page_bot.after(random.randint(1, 2) * 1000, bot)

            def bot():
                global excitation
                replies = ['Well, Tell Something', 'Speak up', 'Speak up please', 'Why did you go all shush on me?',
                           'What are you waiting for ?', 'What ? Are you writing me the 8th Harry Potter novel ?',
                           'Good chat !', 'Okay, Ask me anything when you are free.',
                           'Okay then, Ping me when you are free.', 'You there ?']
                status_label.config(text='')
                if excitation is '':
                    response = random.choice(replies)
                else:
                    response = kernel.respond(excitation)
                resp_msg = ">" + response + '\n'
                self.chat_page_bot.insert(END, '\n')
                self.chat_page_bot.insert(END, resp_msg)
                self.chat_page_bot.yview(END)

                self.chat_page_user.config(state=DISABLED)
                self.chat_page_bot.config(state=DISABLED)

            user()

        # Function that is associated with the clearing of the Text Widgets.
        def clear_chat():
            self.chat_page_user.config(state=NORMAL)
            self.chat_page_user.delete('1.0', END)

            self.chat_page_bot.config(state=NORMAL)
            self.chat_page_bot.delete('1.0', END)

        self.chat_page_bot.config(fg="#003057", bg='#efefef', height=15, width=35, relief=FLAT,
                                  font=('Segoe UI', 24,), wrap=WORD)
        self.chat_page_bot.config(state=DISABLED)

        self.chat_page_user.config(fg="#003057", bg='#efefef', height=15, width=35, relief=FLAT,
                                   font=('Segoe UI', 24,), wrap=WORD)
        self.chat_page_user.config(state=DISABLED)

        # Changing the settings to make the scrolling work.
        self.scrollbar.config(command=self.on_scrollbar)
        self.chat_page_bot.config(yscrollcommand=self.on_textscroll)
        self.chat_page_user.config(yscrollcommand=self.on_textscroll)

        # Making of the menu bar starts.
        menu_bar = Menu(root)
        menu_bar.add_command(label='About', command=info)

        settings = Menu(menu_bar, tearoff=1)
        # settings.add_command(label='Change Bot name', command=name_bot, accelerator='Ctrl+B')
        settings.add_command(label='Set User name', command=name_user, accelerator='Ctrl+U')
        settings.add_separator()
        # settings.add_command(label='Change User Font Color', command=user_font_color_chooser, accelerator='Ctrl+M')
        # settings.add_command(label='Change Bot Font Color',command=bot_font_color_chooser, accelerator='Ctrl+Shift+M')
        settings.add_command(label='Reset to Default', command=reset)

        menu_bar.add_cascade(label='Settings', menu=settings)
        menu_bar.add_command(label='Exit', command=quit)

        # Making of the message entry box and the send button

        frame = Frame(root, bg='#0063B1', relief=GROOVE)
        frame.pack(side=BOTTOM, fill=BOTH)

        clear_butt = Button(frame, text=u'\u274c', height=2, width=8, command=clear_chat,
                            bg='#0063B1', fg='#ffffff', relief=GROOVE, overrelief=GROOVE,
                            font=('Times New Roman', 12), activebackground='#003057',
                            activeforeground='#f0f0f0').pack(side=LEFT)

        def delete_text(event):
            entry.delete('1.0', END)

        entry = Text(frame, font=('Segoe UI', 18), relief=FLAT, bg='#0063B1', fg="#ffffff",
                     width=56, height=1, wrap=WORD, bd=3)
        entry.insert(END, '\nType a message...')
        entry.bind("<Button-1>", delete_text)
        entry.tag_configure("centre", justify=CENTER)
        entry.tag_add("centre", 1.0, END)
        entry.pack(side=LEFT, fill=X, expand=1, anchor=E)
        entry.bind("<Return>", messages)

        send_butt = Button(frame, text=u'\u2713', command=messages, height=2, width=8,
                           bg='#0063B1', fg='#ffffff', relief=GROOVE, overrelief=GROOVE,
                           font=('Times New Roman', 12), activebackground='#003057',
                           activeforeground='#f0f0f0').pack(side=LEFT)

        root.config(menu=menu_bar)
        kernel.saveBrain("bot_brain.brn")

        # Making of the Status Bar To print the current date in a label
        t = time.asctime(time.localtime(time.time()))
        date = t.split(" ")
        form = date[0] + ' | ' + date[1] + ' ' + date[2] + ' |  Session Started: ' + date[3]

        stat_frame = Frame(root, bg='#003057', relief=GROOVE, bd=3)
        stat_frame.pack(side=BOTTOM, fill=X)
        time_label = Label(stat_frame, bg="#003057", fg='#ffffff', font=('Segoe UI', 14), text=form)
        time_label.pack(side=RIGHT, anchor=E)
        status_label = Label(stat_frame, bg="#003057", fg='#ffffff', font=('Segoe UI', 14))
        status_label.config(text="")
        status_label.pack(side=LEFT, anchor=W)

        # Binding Events
        root.bind("<Control-m>", user_font_color_chooser)
        root.bind("<Control-M>", user_font_color_chooser)
        root.bind("<Control-Shift-M>", bot_font_color_chooser)
        root.bind("<Control-Shift-m>", bot_font_color_chooser)
        root.bind("<Control-B>", name_bot)
        root.bind("<Control-U>", name_user)
        root.bind("<Control-b>", name_bot)
        root.bind("<Control-u>", name_user)
        root.bind('<F1>', info)

    # Scrolls both text widgets when the scrollbar is moved
    def on_scrollbar(self, *args):
        self.chat_page_user.yview(*args)
        self.chat_page_bot.yview(*args)

    # Moves the scrollbar and scrolls text widgets when the mousewheel is moved on a text widget
    def on_textscroll(self, *args):
        self.scrollbar.set(*args)
        self.on_scrollbar('moveto', args[0])


if __name__ == '__main__':
    root = Tk()
    root.config(bg='#efefef', bd=7)
    root.resizable(1, 1)
    root.title("Nicole \t (Online)")

    ob = ChatBot(root, relief=GROOVE, bg='#0990E8')
    ob.pack(side=TOP, fill=BOTH, expand=True)
    root.iconbitmap('icon (1).ico')
    root.protocol("WM_DELETE_WINDOW", quit)
    root.mainloop()

