from tkinter import *
from tkinter import filedialog
import sys, textwrap
try:
    import cPickle as pickle
except ImportError:
    import pickle

version = "|DEV v1.8.1|"

saved_file="unnamed" #File name to display
true_path="None" #Actual file path; None means no file path selected yet

changed = False #Keep track of whether or not a change has been made since last save.

active = None #Store which widget is active

top = Tk() #Create a root

top.title("Digital Cornell Notes "+version+" - "+saved_file) #Set the window stuff
top.iconphoto(True, PhotoImage(file="./thingy.png")) #Temporary file path to icon
top.resizable(False, False)


###Create name, subject, and date entries for formatting
name = Entry(top, width=20)
subject = Entry(top, width=20)

name.insert(0,"Name")
subject.insert(0,"Subject")

date = Entry(top, width=20)
date.insert(0,"Date")

###Make the sections for keywords and notes

keywords = Text(top, width=20, height=25, wrap=WORD)
notes = Text(top, width=40, height=25, wrap=WORD)


###Function for synchronizing scroll between sections
def on_scroll(*args):
    #Sync the scroll between sections
    keywords.yview("moveto",args[0])
    notes.yview("moveto",args[0])
        
###Register which section is active

def on_click_n(*args):
    global active
    active = notes

def on_click_k(*args):
    global active
    active = keywords

###Bind the functions to the widget events
    
keywords['yscrollcommand'] = on_scroll
notes['yscrollcommand'] = on_scroll

keywords.bind("<Button-1>", on_click_k)
notes.bind("<Button-1>", on_click_n)

#Make a section for the summary

summary = Text(top, width=60, height=5, wrap=WORD)



#============================================
#Section for getting notes as a single string
#============================================

#This section is part of the unfinished exporting feature,
#and may or may not be functional

def get_notes_as_string(*args):

    def wrap(string, length):

        wrapped = []

        words = string.split(' ')

        new_line = ""
        for word in words:

            num_of_newlines = word.count('\n')

            #If there are no newlines
            
            if num_of_newlines == 0:
            
                if len(word)+len(new_line) < length:
                    
                    if new_line != "" and new_line[-1] != ' ':
                        new_line += " " + word
                    else:
                        new_line += word
                        
                else:
                    wrapped.append(new_line+' ')
                    new_line = word

            #If there ARE newlines

            else:

                line_words = word.split('\n')
                line_words.remove('')

                word1 = line_words[0]
                try:
                    word2 = line_words[1]
                except:
                    word2=""

                if len(word1)+len(new_line) < length:
                    
                    if new_line != "":
                        new_line += " " + word1
                    else:
                        new_line += word1

                else:
                    wrapped.append(new_line+' ')
                    new_line = word1

                wrapped.append(new_line)
                for i in range(num_of_newlines): wrapped.append('\n')
                new_line = word2

                    
                
        if wrapped[-1] != new_line:
            wrapped.append(new_line)
        return wrapped

    ####END OF WRAP FUNCTION####
                

    keyword_section = keywords.get("1.0","end-1c")
    note_section = notes.get("1.0","end-1c")

    final_string = ""

    keyword_lines = wrap(keyword_section,20)
    note_lines = wrap(note_section,40)

    if len(keyword_lines) >= len(note_lines):
        print("Using keyword length")
        total_lines = len(keyword_lines)
    else:
        print("Using note length")
        total_lines = len(note_lines)

    for i in range(len(keyword_lines)):
        k_line = keyword_lines[i]
        n_line = note_lines[i]
        if k_line != '\n' and n_line != '\n':
            while len(k_line) < 20: k_line += " "
            while len(n_line) < 40: n_line += " "
            final_string += f"{k_line}   {n_line}\n"
        else:
            print("Newline")
            final_string += '\n'
    print(final_string)
    print(keyword_lines)
    return final_string

#=====================#
#===END OF FUNCTION===#
#=====================#



#Function to save .note file using pickle

def save_to(file):
    data = [name.get(), subject.get(), date.get(),
            keywords.get("1.0",END), notes.get("1.0",END),
            summary.get("1.0",END)]
    f = open(file, 'wb')
    pickle.dump(data,f)
    f.close()

#Create event handler for ctrl-s event

def ctrl_s_save(event):
    global saved_file, true_path
    
    data = [name.get(), subject.get(), date.get(),
            keywords.get("1.0",END), notes.get("1.0",END),
            summary.get("1.0",END)]

    if true_path == "None":

        file = filedialog.asksaveasfilename()#Open system file dialog to get file path

        if file[-5:] != ".note": file += ".note" #add .note extension if not already added
        
        saved_file = file.split('/')[-1].split('.')[0]
        true_path = file
        top.title("Digital Cornell Notes "+version+" - "+saved_file)

        save_to(true_path)

    else:

        save_to(true_path)
        top.title("Digital Cornell Notes "+version+" - "+saved_file)

def ctrl_o_open(event):
    global true_path
    
    top.title("Digital Cornell Notes "+version+" - "+saved_file)
    f = open(true_path, 'rb')
    data = pickle.load(f)
    f.close()
    def load_to(obj, index):
        obj.delete(0,END)
        obj.insert(0,data[index])
    load_to(name,0)
    load_to(subject,1)
    load_to(date,2)
    keywords.delete("1.0",END)
    notes.delete("1.0",END)
    summary.delete("1.0",END)
    keywords.insert("1.0",data[3])
    notes.insert("1.0",data[4])
    summary.insert("1.0",data[5])

    

#Bind ctrl-s event to event handler
top.bind("<Control-s>", ctrl_s_save)
        


def file_manage(): #File managing window

    window = Toplevel(top)
    window.title("File")
    window.resizable(False,False)
    button_width = 15

    

    #Function for "save as" button

    def save_as():
        global saved_file, true_path
        file = filedialog.asksaveasfilename()

        if file[-5:] != ".note": file += ".note"
        
        saved_file = file.split('/')[-1].split('.')[0]
        true_path = file
        top.title("Digital Cornell Notes "+version+" - "+saved_file)

        save_to(true_path)
        window.destroy()

    #Function to open .note file

    def open_file():
        global saved_file, true_path
        file = filedialog.askopenfilename(filetypes=(('Note files','*.note'),
                                                     ('All files', '*.*')))
        saved_file = file.split('/')[-1].split('.')[0]
        true_path = file
        top.title("Digital Cornell Notes "+version+" - "+saved_file)
        f = open(true_path, 'rb')
        data = pickle.load(f)
        f.close()
        def load_to(obj, index):
            obj.delete(0,END)
            obj.insert(0,data[index])
        load_to(name,0)
        load_to(subject,1)
        load_to(date,2)
        keywords.delete("1.0",END)
        notes.delete("1.0",END)
        summary.delete("1.0",END)
        keywords.insert("1.0",data[3])
        notes.insert("1.0",data[4])
        summary.insert("1.0",data[5])
        window.destroy()

    #Function for "save" button

    def save():
        global saved_file, true_path
        if true_path != "None":
            save_to(true_path)
            window.destroy()
            top.title("Digital Cornell Notes "+version+" - "+saved_file)
        else:
            save_as()

    #Function for "new file" button

    def new():
        global saved_file, true_path
        saved_file = "unnamed"
        true_path = "None"
        name.delete(0,END)
        subject.delete(0,END)
        date.delete(0,END)
        name.insert(0,"Name")
        subject.insert(0,"Subject")
        date.insert(0,"Date")
        keywords.delete("1.0",END)
        notes.delete("1.0",END)
        summary.delete("1.0", END)
        top.title("Digital Cornell Notes "+version+" - "+saved_file)
        window.destroy()

    #Make all the buttons

    save_b = Button(window,text="Save As", command=save_as,width=button_width)
    save_as_b = Button(window, text="Save", command=save,width=button_width)
    open_b = Button(window, text="Open", command=open_file,width=button_width)
    new_b = Button(window, text="New", command=new,width=button_width)

    save_as_b.pack()
    save_b.pack()
    open_b.pack()
    new_b.pack()
    window.mainloop()

#Section to handle opening files directly and allow user to open .note file without
#opening the program first; executes every time program runs to se if it is being called
#from the command line; only serves a purpose after proper distribution

file_selection = sys.argv
if isinstance(file_selection, list) and len(file_selection)>=2:
    true_path = file_selection[1]
    saved_file = file.split('/')[-1].split('.')[0]

    top.title("Digital Cornell Notes "+version+" - "+saved_file)

    file = open(true_path,'rb')
    data = pickle.load(file)
    file.close()

    name.delete(0,END)
    subject.delete(0,END)
    date.delete(0,END)
    keywords.delete("1.0",END)
    notes.delete("1.0",END)
    summary.delete("1.0", END)
    
    name.insert(0,data[0])
    subject.insert(0,data[1])
    date.insert(0,data[2])
    keywords.insert("1.0",data[3])
    notes.insert("1.0",data[4])
    summary.insert("1.0",data[5])
    
#Make file managing button

file_manager = Button(top, text="File", command=file_manage,width=60)

#Place all buttons

name.grid(row=0, column=0)
subject.grid(row=1,column=0)
date.grid(row=0,column=1, sticky=NE)

keywords.grid(row=2,column=0)
notes.grid(row=2, column=1)

summary.grid(row=3, column=0,columnspan=2)

file_manager.grid(row=4,column=0,columnspan=2)

#Mainloop

top.mainloop()
