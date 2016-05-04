# a gui in python
from Tkinter import *
import tkFileDialog
import os
import tkMessageBox
import nbtest
import nbtestdirichlet
import nbtestjm
import nbtestngram
import nbtrain
import nbtraindirichlet
import nbtrainjm
import nbtrainngram

root = Tk()
root.title("Naive Bayes Classifier Interface")
root.geometry("600x300")
topframe = Frame(root)
middleframe = Frame(root)
bottomframe = Frame(root)
topframe.pack(side=TOP)
middleframe.pack(side=TOP)
bottomframe.pack(side=BOTTOM)
Label(topframe, text="Path for training dataset").grid(row=0,column=0)
entry1 = Entry(topframe).grid(row=0,column=1)
global v,value
v = IntVar()
v.set(1)
def write_data():
    tkMessageBox.showinfo("Message","Model File Generated Successfully!!!!!!!!!")

def browse_train_file():
    global tempdir
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    print tempdir

def train_system():
    global tempdir,value,v
    value = v.get()
    print "Choice selected is",value
    try:
        if value==1:
            nbtrain.getSubDir(tempdir)
        if value==2:
            nbtraindirichlet.getSubDir(tempdir)
        if value==3:
            nbtrainjm.getSubDir(tempdir)
        if value==4:
            global ngram
            nbtrainngram.getSubDir(tempdir,ngram)
        else:
            tkMessageBox.showinfo("Error","Error while training the system!!!!!!!!!!")
            root.destroy()
        write_data()
    except:
        tkMessageBox.showinfo("Error","Error while training the system!!!!!!!!!!")
        root.destroy()

def browse_classify_file():
    global classify_dir
    currdir=os.getcwd()
    classify_dir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    print classify_dir

def classify_system():
    global classify_dir,value,v
    value = v.get()
    try:
        try:
            with open('model.txt') as file:
                if value==1:
                    nbtest.readFile(classify_dir)
                if value==2:
                    nbtestdirichlet.readFile(classify_dir)
                if value==3:
                    nbtestjm.readFile(classify_dir)
                if value==4:
                    global ngram
                    print "value for ngram", ngram
                    nbtestngram.readFile(classify_dir,ngram)
                tkMessageBox.showinfo("Message","Classification done...Check output files generated")
        except IOError as e:
            print "Unable to open file"
    except:
        tkMessageBox.showinfo("Error","Error while classifying the system!!!!!!!!!!")


Button(topframe, text='Browse', command=browse_train_file).grid(row=0, column=6, sticky=W, pady=4)
Label(middleframe, text="""Choose a parameter from below::""",justify = LEFT,padx = 20).grid(row=2,column= 0)
parameters = [("Laplace Smoothing",1),("Dirichlet Smoothing",2),("JM Smoothing",3), ("Ngrams",4)]
def ShowChoice():
    global e,t1,v1,entry,value
    print "Choice" ,v.get()
    value = v.get()
    if value == 4:
        t1 = Tk()
        t1.title("N-Gram Option")
        t1.geometry("200x50")
        entry = Entry(t1)
        button = Button(t1,text="Get Value for N", command=on_button)
        button.pack()
        entry.pack()

def on_button():
    global t1,v1,entry,ngram
    ngram = int(entry.get())
    print entry.get()
    t1.destroy()

for txt, val in parameters:
    Radiobutton(middleframe, text=txt, indicatoron = 0, width = 20,padx = 20, variable=v,command=ShowChoice,value=val).grid()
Label(middleframe, text="Path for test dataset").grid(row=20)
l2 = Entry(middleframe).grid(row=20,column=1)
Button(middleframe, text='Browse', command=browse_classify_file).grid(row=20, column=6, sticky=W, pady=4)
def dono():
    print "Nothing"
b1=Button(bottomframe, text='TRAIN', command=train_system).pack(side=LEFT)
b2=Button(bottomframe, text='QUIT', command=root.quit).pack(side=LEFT)
b3=Button(bottomframe, text='CLASSIFY', command=classify_system).pack(side=LEFT)
root.mainloop()
