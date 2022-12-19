#importing libraries

from tkinter import ttk,messagebox
from tkinter import *
from pytube import YouTube,Stream
import threading
import sys
import os
# from tkinter.tix import *
from tkinter.filedialog import askdirectory

# print

#creating a main window with title and icon
root=Tk()
root.geometry("600x450+480+100")
root.resizable(0,0)
root.title("Youtube video downloader")

#adding icon to the window
icon = PhotoImage(file = '.\\resources\\icon.png')
root.iconphoto(False, icon)


#defalut variables
url_entry=StringVar()
All_list=[]
All_list2=[]
path=os.path.expanduser("~")+"\\Downloads\\"

#Downloading progress details
def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    download_per.config(text=f"{round(pct_completed, 2)} %")
    prog=f"{round(pct_completed, 2)}"
    progress_bar.config(value=prog)
    # print(f"Status: {round(pct_completed, 2)} %")

def search1():
    try:
        global All_list,All_list2,w,exit
        w["values"]=[]
        message.config(text="Please wait a while.......") 
        All_list=[]
        All_list2=[]
        youtube1=YouTube(url_entry.get(), on_progress_callback=on_progress)
        try:
            a=youtube1.streams.filter(mime_type="video/mp4",progressive= True )
        except:
            pass
        try:
            b=youtube1.streams.filter(mime_type="video/mp4",progressive= False )
        except:
            pass
        try:
            c=youtube1.streams.filter(only_audio=True).all()
        except:
            pass
        
        for i in a:
            root.update()
            All_list.append(i)
        for i in b:
            root.update()
            All_list.append(i)

        for i in c:
            root.update()
            All_list.append(i)
        try:
            for i in All_list:
                root.update()
                k=f"""{"%.2f" %float(((i.filesize)/1024)/1024)}"""  #size in mb
                if i.resolution==None:   #resolution
                    j=i.abr              #bitrate
                else:
                    j=i.resolution
                l=i.is_progressive
                root.update()
                m=i.subtype            #file type
                All_list2.append(str(m)+"     "+str(j)+"      "+str(k)+" MB"+"      "+str(l))
                root.update()
        except:
            pass
        w["values"]=All_list2
        exit=1
        message.config(text="Choose the resolution/format ......")
        return
    except:
        message.config(text="")
        messagebox.showerror("showerror", "1.Check Your internet connection... \n2.Or Fill the url properly.... ")


#process handling functions
def test():
    global s1,exit
    exit=0
    s1=threading.Thread(target=search1)
    s1.start()
    if exit==1:
        s1.join()
    return

def test1():
    global s1,exit1
    exit1=0
    s2=threading.Thread(target=download)
    s2.start()
    if exit1==1:
        s2.join()
    return

def download():
    global w
    print(variable.get)
    try:
        # print(w.current())
        if w.current()== -1:
            messagebox.showerror("Error","First select the option from the dropdown menu......")
        else:
            download_per.config(text="")
            progress_bar.config(value=0)
            messagebox.showinfo("Info","Don't close the app your file is downloading..")
            All_list[w.current()].download(path)
            messagebox.showinfo("Info",f"File downloaded successfully..\n Path : {path}")
            # print("Downloaded in "+path)      
        return
    except:
        messagebox.showerror("info","First select the option from the dropdown menu......")
    w.set('')


# #hover on directory
# tip=Balloon(root)

#select directory  function
def select_directory():
    global path
    a=path
    path=askdirectory()
    directory_name.config(text=path)
    if path=="":
        path=a
        directory_name.config(text=path)
        # print("Path is default...",path)
    else:
        pass


#youtube logo
yt=PhotoImage(file=".\\resources\\1.png")
yt_image=Label(root,image=yt)
yt_image.place(x=200,y=0)

#Please wait message label
message=Label(root,text="",font=("Helvetica",10,"bold"))
message.place(x=50,y=240)

#url label
url_label=Label(root,text="Paste URL :",font=("Helvetica",10,"bold"))
url_label.place(x=0,y=210)

#download percentage label
download_per=Label(root,text="",font=20)
download_per.place(x=110,y=405)

#Url entry 
url =Entry(root,textvariable = url_entry,border=1, width=50,font=('calibre',10,'normal'))
url.place(x=80,y=210)

#search button
img=PhotoImage(file=".\\resources\\search.png")
search_button=Button(root,image=img,command=test,border=0 )
search_button.place(x=440,y=208)

variable = StringVar()
variable.set("Type   bitrate/resol      size         progressive ") # default value
w = ttk.Combobox(root, textvariable=variable,width=50,font=("Helvetica",10,"bold"))
w.place(x=10,y=280)

#Progressbar of song
s = ttk.Style()
s.theme_use('default')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red',thickness=15)
progress_bar=ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient="horizontal",
                length=550, mode="determinate", maximum=100)
progress_bar.place(x=20,y=370)

#directory name label
directory_name=Label(root,text=path,width=40,font=("Helvetica",10,"bold"))
directory_name.place(x=40,y=330)

#directory arrow
img3=PhotoImage(file=".\\resources\\arrow.png")
directory_arrow=Label(root,image=img3)
directory_arrow.place(x=5,y=325)

#change directory button
img2=PhotoImage(file=".\\resources\\file.png")
ch_button=Button(root,image=img2,command=select_directory,border=0)
ch_button.place(x=370,y=322)

# #Bind the tooltip with button
# tip.bind_widget(ch_button,balloonmsg="Choose the directory where you want to save this file\nOr it will be downloaded in your download folder..")

#download button
download_image=PhotoImage(file=".\\resources\\download6.png")
Download_button=Button(root,image=download_image,command=test1,border=0)
Download_button.place(x=230,y=400)

#Exit function
def on_closing():
    os._exit(0)	
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()