"""
ChatMate
ChatMate Version 1.0 BETA 1
Copyrigth © Muhammad Abdullah Elahi, ElahiNexusTech. All rights Reserved
Date Started June 9, 2023
Date Ended June _, 2023
"""



# Importing Required Files
from os import system, path, makedirs
from customtkinter import CTk, CTkScrollableFrame, CTkFrame, CTkEntry, CTkButton, CTkLabel
from tkinter import TOP, LEFT, BOTTOM, X, END, messagebox, Menu, filedialog
import openai
from json import dump, load
from datetime import datetime, date

# home directory of the user
home = path.expanduser('~')
CHATMATE_DATA_FILE_PATH:str = f"{home}/Documents/ChatMate/chats"

if not path.exists(CHATMATE_DATA_FILE_PATH):
    makedirs(CHATMATE_DATA_FILE_PATH)

# Application Dimensions
app_width = 1000
app_height = 850

# Font, & Colours
text_font = ("Arial", 16)
query_font = ("Arial", 18, "bold")
datetime_font = ("Arial", 20, "bold")
highlighted_text_font = ("Arial", 20)
placeholder_color = ("#F5F5F5", "#2A2A2A")
text_frame_bg = ("#F5F5F5", "#2A2A2A")
chat_box_bg = ("#DEDEDE", "#3A3A3A")

# Getting Date Time
time = datetime.now()
dates = date.today()
hour = time.hour
minute = time.minute
year = dates.year
month = dates.month
day = dates.day

# Access the api key
openai.api_key = "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"  

# Creating Scrollable Frames for chatbox
class ScrollFrames(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

# Creating Main Application
class App(CTk):
    
    # Constructor: Main UI Elements
    def __init__(self):
        super().__init__()

        # Window Properties
        self.geometry(f'{app_width}x{app_height}')
        self.title('ChatMate')
        self.resizable(False, False)

        # Create a chatbox frame to store chats
        self.chatBoxFrame = ScrollFrames(self, width=app_width, corner_radius=8, height=app_height - 150, fg_color=chat_box_bg)
        self.chatBoxFrame.pack(padx=10, pady=10)

        #  Create a inputing and submiting frame, Frame/input & submit btn
        self.frame = CTkFrame(self, corner_radius=0)

        self.input = CTkEntry(self.frame, font=text_font, corner_radius=10, width=app_width - 150, placeholder_text="Type your query (Press Return Key to submit it)")
        self.input.pack(side=LEFT, padx=20, pady=20, ipady=10)

        self.sbumit_btn = CTkButton(self.frame, text="➤", fg_color="#fcc203", font=highlighted_text_font, width=50,  height=50, hover=None, command=lambda: self.generate(input.get()))

        self.sbumit_btn.pack(side=LEFT, padx=20, pady=20)

        self.frame.pack(side=BOTTOM, fill=X)

        # Load the saved chats
        self.load_chat()

        # Key bindings and Menu Creation
        self.bind("<Meta_L><e>", self.export_chat)
        self.bind("<Meta_R><e>", self.export_chat)
        self.bind("<Meta_L><d>", self.delete_chat)
        self.bind("<Meta_R><d>", self.delete_chat)
        self.bind("<Meta_L><o>", self.open_docs)
        self.bind("<Meta_R><o>", self.open_docs)
        self.bind("<Return>", lambda event: self.key_shortcuts(event, self.input.get()))
        self.bind("<KP_Enter>", lambda event: self.key_shortcuts(event, self.input.get()))

        menu = Menu(self)

        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label="Export Chat", accelerator="Command+e", command=self.export_chat)
        fileMenu.add_command(label="Delete Chat", accelerator="Command+d", command=self.delete_chat)
        fileMenu.add_command(label="Open Documentation", accelerator="Command+o", command=self.open_docs)
        fileMenu.add_separator()
        fileMenu.add_command(label="Submit Query", accelerator="Return", command=lambda event="Return": self.key_shortcuts(event))

        helpMenu = Menu(menu)
        helpMenu.add_command(label="Help", accelerator="Command+h", command=self.help)

        menu.add_cascade(label="File", menu=fileMenu)
        menu.add_cascade(label="Help", menu=helpMenu)
        self.configure(menu=menu)

    
    # Methods: Generate AI Responses,
    def generate(self, query):
        try:
            if len(query) != 0:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=query,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )['choices'][0]['text']

                date_time = f"{hour}:{minute}, {month}/{day}/{year}\n"

                self.chat_frame(dt=date_time, query=query, resp=response)

                self.input.delete(0, END)  # Clear the text field

                self.save_chat(date_time, query, response)

        except Exception as e:
            messagebox.showerror("Error", f"{e}\n")

 
    # Methods: Create Chat Frame,
    def chat_frame(self, dt, query, resp):
        self.childFrame = CTkFrame(self.chatBoxFrame, fg_color=text_frame_bg, width=app_width, corner_radius=8)
        self.datetime_label = CTkLabel(self.childFrame, text=dt, font=datetime_font)
        self.datetime_label.pack(anchor="w", padx=20, pady=10)
        self.query_text = CTkLabel(self.childFrame, text=f"Query: {query}", font=query_font, wraplength=900,
                                   justify=LEFT)
        self.query_text.pack(anchor="w", padx=10, pady=10)
        self.query_text = CTkLabel(self.childFrame, text=f"Answer: {resp}", font=text_font, wraplength=900,
                                   justify=LEFT)
        self.query_text.pack(anchor="w", padx=10, pady=10)
        self.childFrame.pack(fill=X, pady=10, padx=10)  # Pack frame

 
    # Methods: KeyBoard Events,
    def key_shortcuts(self, event, input: str = ""):
        if event.keysym == "Return" or event.keysym == "KP_Enter":
            self.generate(input)


    # Methods: Save Chats,
    def save_chat(self, dt, query, response):
        try:
            chat_file = path.join(CHATMATE_DATA_FILE_PATH, "chat.json")
            with open(chat_file, "r", encoding='utf-8') as f:
                data = load(f)
        except FileNotFoundError:
            open("data.json", "w")
            data = []
        except:
            data = []

        # Add new chat data
        chat_data = {
            "Date-Time": dt,
            "Query": query + "\n",
            "Response": response
        }
        data.append(chat_data)

        # Save updated data to the file
        with open(f"{home}/Documents/ChatMate/chats/chat.json", "w") as f:
            dump(data, f)


    # Methods: Load Chat,
    def load_chat(self):
        try:
            chat_file = path.join(CHATMATE_DATA_FILE_PATH, "chat.json")
            with open(chat_file, "r", encoding='utf-8') as f:
                data = load(f)
            for item in data:
                self.childFrame = CTkFrame(self.chatBoxFrame, fg_color=text_frame_bg, width=app_width, corner_radius=16)

                self.datetime_label = CTkLabel(self.childFrame, text=item["Date-Time"], font=datetime_font)
                self.datetime_label.pack(anchor="w", padx=20, pady=10)

                self.query_text = CTkLabel(self.childFrame, text=f'Query: {item["Query"]}', font=query_font, wraplength=900, justify=LEFT)
                self.query_text.pack(anchor="w", padx=10, pady=10)

                self.query_text = CTkLabel(self.childFrame, text=f'Answer: {item["Response"]}', font=text_font, wraplength=900, justify=LEFT)
                self.query_text.pack(anchor="w", padx=10, pady=10)

                self.childFrame.pack(fill=X, pady=10, padx=10)  # Pack frame
        except:
            data = []


    # Methods: Export Chat if required,
    def export_chat(self, event=None):
        try:
            chat_file = path.join(CHATMATE_DATA_FILE_PATH, "chat.json")
            with open(chat_file, "r", encoding='utf-8') as f:
                data = load(f)

            date_time = f"{hour}:{minute}-{month}/{day}/{year}"
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile=f"ChatMate-Chats-{date_time}")

            if len(data) != 0:
                if file_path:
                    directory = path.dirname(file_path)

                    makedirs(directory, exist_ok=True)

                    with open(file_path, "w") as f:
                        for item in data:
                            f.write(f'Date-Time: {item["Date-Time"]}')
                            f.write(f'Query: {item["Query"]}')
                            f.write(f'Reponse: {item["Response"]}')
                            f.write("\n\n------------------------------------------------------------------\n\n")
        except:
            messagebox.showinfo("Export Chat Info", "There is no DATA provided in the JSON file to be exported")

    # Methods: Delete Chat if required,
    def delete_chat(self, event=None):

        permit = messagebox.askyesno("Warning!", "Are you sure you want to delete all the chat data! All the data/chats stored are going to be DELETED PERMENANTLY from your device!")

        if permit:
            chat_file = path.join(CHATMATE_DATA_FILE_PATH, "chat.json")
            with open(chat_file, "w") as f:
                f.truncate(0)

            self.destroy()
            self.__init__()

            messagebox.showinfo("Information!", "All chats are cleared!")

    # Methods: Open Documents,
    def open_docs(self, event=None):
        print("Hello world, Opening Docs!")

    # Methods: Help Functions,
    def help(self, event=None):
        pass