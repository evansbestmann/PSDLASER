from tkinter import*
from tkinter import filedialog, messagebox,ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter.ttk import Notebook
from matplotlib.figure import Figure
from matplotlib.scale import LogScale
import scipy
import scipy.interpolate




root= Tk()
root.geometry("1200x600")
root.configure(bg='#e0e0e0')
root.iconbitmap(r'ICON.ico')
root.title("Particle Size Distribution")

root.resizable(0,0)


browsedata=Button(root,text="Browse data",padx=6,command=lambda :file_())
browsedata.place(x=20,y=560)

frame1=LabelFrame(root,relief="sunken",text="Graph",height=518,width=780)
frame1.place(x=370,y=30)

frame2=LabelFrame(root,relief="sunken",text="Data",height=518,width=300)
frame2.place(x=25,y=30)

loaddata=Button(root,text="Load data",padx=12,command=lambda :load_data())
loaddata.place(x=130,y=560)

coefcurvlabel1 = Label(root, text="Coefficient of curvature :")
coefcurvlabel1.place(x=400, y=560)

coefuniflabel1 = Label(root, text="Coefficient of uniformity :")
coefuniflabel1.place(x=690, y=560)
can1, axes1= plt.subplots(figsize=(6, 3.85), dpi=120)

plt.xscale('log')
plt.ylabel("Percentage Finer",fontsize="small")
plt.xlabel("Seive Size",fontsize="small")
plt.title("Seive size vs Percentage finer",fontsize="small")
plt.xlim([0.01,100])
plt.ylim([0,100])
plt.grid(True)


canvas1 = FigureCanvasTkAgg(can1,root)
canvas1.draw()
canvas1.get_tk_widget().place(x=400, y=50)
toolbar1=NavigationToolbar2Tk(canvas1,root)
toolbar1.update()
toolbar1.place(x=400,y=510)

def clear():
    can1, axes1= plt.subplots(figsize=(6, 3.85), dpi=120)
    plt.xscale('log')
    plt.ylabel("Percentage Finer",fontsize="small")
    plt.xlabel("Seive Size",fontsize="small")
    plt.title("Seive size vs Percentage finer",fontsize="small")
    plt.xlim([0.01,100])
    plt.ylim([0,100])
    plt.grid(True)


    canvas1 = FigureCanvasTkAgg(can1,root)
    canvas1.draw()
    canvas1.get_tk_widget().place(x=400, y=50)
    toolbar1=NavigationToolbar2Tk(canvas1,root)
    toolbar1.update()
    toolbar1.place(x=400,y=510)


tv1 = ttk.Treeview(root)
tv1.place(relheight=0.75, relwidth=0.23, x=40, y=50)
tvscrolly = Scrollbar(tv1, orient="vertical", command=tv1.yview)
tvscrollx = Scrollbar(tv1, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=tvscrollx.set, yscrollcommand=tvscrolly.set)
tvscrollx.pack(side="bottom", fill="x")
tvscrolly.pack(side="right", fill="y")
selectlabel = ttk.Label(root, text="No file selected ")
selectlabel.place(x=27, y=520, rely=0, relx=0)





def file_():
    filename = filedialog.askopenfilename(initialdir="This PC", title="file select",
                                          filetypes=(("xlsx", "*.xlsx"), ("All files", "*.*")))
    selectlabel["text"] = filename
    return None


def load_data():
    file_path = selectlabel["text"]
    try:
        excel_filename = r"{}".format(file_path, dtype=float)

        df = pd.read_excel(excel_filename)
    except ValueError:
        messagebox.showerror("Info", "Invalid file")
        return None
    except FileNotFoundError:
        messagebox.showerror("Info", f"No file as {file_path}")
        return None

    clear_data()

    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    data = np.array(df[0:], dtype=float)





    seive_size = (data[:, 0])
    mass_retained = (data[:, 1])
    cumm_mass_ret=np.cumsum(mass_retained)
    per_mass_ret=(cumm_mass_ret/cumm_mass_ret[-1])*100
    per_passing=per_mass_ret[-1]-per_mass_ret
    perpass=np.array(per_passing)
    seivesize=np.array(seive_size)





    interfunc=scipy.interpolate.interp1d(perpass,seivesize)
    nss10=interfunc(10)
    nss30=interfunc(30)
    nss60=interfunc(60)
    nsst=interfunc(76.9194536)


    coefcurv=(np.power(nss30,2))/(nss60*nss10)
    coefunif=nss60/nss10
    #print(nss10,coefcurv)



    plotbutn = Button(root, text="Plot",padx=28, command= lambda :plot())
    plotbutn.place(x=240, y=560)



    def plot():

        fig, axes = plt.subplots(figsize=(6, 3.85), dpi=120)
        axes.plot(seive_size, per_passing,"o-",color="black")
        plt.xscale('log')
        plt.ylabel("Percentage Finer", fontsize="small")
        plt.xlabel("Seive Size", fontsize="small")
        plt.title("Seive size vs Percentage finer", fontsize="small")
        plt.xlim([0.01,100])
        plt.yticks(np.arange(0,max(per_passing),10))




        plt.grid(True)



        canvas = FigureCanvasTkAgg(fig, root)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=50)

        coefcurvlabel0 = Label(root, text=coefcurv)
        coefcurvlabel0.place(x=540, y=560)

        coefuniflabel0 = Label(root, text=coefunif)
        coefuniflabel0.place(x=835, y=560)








        toolbar=NavigationToolbar2Tk(canvas,root)
        toolbar.update()
        toolbar.place(x=400,y=510)




        def on_key(event):
            print("Cliked {} ".format(event.key))
            key_press_handler(event,canvas,toolbar)

            canvas.mpl_connect("key_press_event",on_key)
def clear_data():
    tv1.delete(*tv1.get_children())

clearbutn = Button(root, text="Clear", padx=28, command=clear)
clearbutn.place(x=1040, y=560)

















root.mainloop()
