"""
ChatMate
ChatMate Version 1.0 BETA 1
Copyrigth © Muhammad Abdullah Elahi, ElahiNexusTech. All rights Reserved
Date Started June 9, 2023
Date Ended June _, 2023
"""



# Importing Required Files
from os import path, makedirs
from customtkinter import CTk, CTkScrollableFrame, CTkFrame, CTkEntry, CTkButton, CTkLabel, set_appearance_mode
from tkinter import LEFT, BOTTOM, X, BOTH, END, messagebox, Menu, filedialog
import openai
from json import dump, load
from datetime import datetime, date

# home directory of the user
home = path.expanduser('~')
CHATMATE_DATA_FILE_PATH:str = f"{home}/Documents/ChatMate/chats"

if not path.exists(CHATMATE_DATA_FILE_PATH):
    makedirs(CHATMATE_DATA_FILE_PATH)

# Font, & Colours
text_font = ("Arial", 16)
highlighted_text_font = ("Arial", 20)
placeholder_color = ("#F5F5F5", "#2A2A2A")
parent_frame_bg = ("#DEDEDE", "#3A3A3A")
user_chat_frame_bg = ("#fff4d1", "#b58b02")
response_chat_frame_bg = ("#c9c9c9", "#595858")


# Getting Date Time
time = datetime.now()
dates = date.today()
hour = time.hour
minute = time.minute
year = dates.year
month = dates.month
day = dates.day

# Access the api key
openai.api_key = ""  

# Apperance Mode Settings
set_appearance_mode("system")

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
        self.width = self.winfo_screenwidth() - 1300
        self.height = self.winfo_screenheight() - 200
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.title('ChatMate')

        

        # Create a chatbox frame to store chats
        self.chatBoxFrame = ScrollFrames(self, width=self.width, corner_radius=8, height=self.height - 150, fg_color=parent_frame_bg)
        self.chatBoxFrame.pack(padx=10, pady=10, fill=BOTH, expand=True, anchor="center")

        #  Create a inputing and submiting frame, Frame/input & submit btn
        self.frame = CTkFrame(self, corner_radius=8, fg_color=parent_frame_bg)

        self.input = CTkEntry(self.frame, font=text_font, corner_radius=10, width=self.width - 150, placeholder_text="Type your query (Press Return Key to submit it)")
        self.input.pack(side=LEFT, padx=20, pady=20, ipady=10, fill=X, expand=True)

        self.sbumit_btn = CTkButton(self.frame, text="➤", fg_color="#fcc203", font=highlighted_text_font, width=50,  height=50, hover=None, command=lambda: self.generate(input.get()))

        self.sbumit_btn.pack(side=LEFT, padx=20, pady=20, fill=X)

        self.frame.pack(side=BOTTOM, padx=10, pady=10, fill=X, expand=True, anchor="s")

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

                self.chat_frame(query=query, resp=response)

                self.input.delete(0, END)  # Clear the text field

                self.save_chat(query, response)

        except Exception as e:
            messagebox.showerror("Error", f"{e}\n")

 
    # Methods: Create Chat Frame,
    def chat_frame(self, query, resp):
        
        # User Chatting Messages
        self.user = CTkFrame(self.chatBoxFrame, fg_color=user_chat_frame_bg, width=self.width-150, corner_radius=8)

        self.query = CTkLabel(self.user, text=query, font=text_font, wraplength=self.width-200, justify=LEFT)
        self.query.pack(padx=5, pady=5, anchor="e")
        
        self.user.pack(anchor="e", padx=10, pady=10)  # Pack frame
        
        # AI Chatting Messages/Responses
        self.response = CTkFrame(self.chatBoxFrame, fg_color=response_chat_frame_bg, width=self.width-150, corner_radius=8)

        self.resp = CTkLabel(self.response, text=resp, font=text_font, wraplength=self.width-200, justify=LEFT)
        self.resp.pack(padx=5, pady=5, anchor="w")
        
        self.response.pack(anchor="w", padx=10, pady=10)  # Pack frame
 

    # Methods: KeyBoard Events,
    def key_shortcuts(self, event, input: str = ""):
        if event.keysym == "Return" or event.keysym == "KP_Enter":
            self.generate(input)


    # Methods: Save Chats,
    def save_chat(self, query, response):
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
                self.chat_frame(query=item["Query"], resp=item["Response"])
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
