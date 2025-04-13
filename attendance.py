# importing important libraries ---------------------------------------......................................----------------------------------

from email import message  #..........this feature is yet to add............. here the attendance marked message is directly send to email address of that particlar person .
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox


#from train import Train
import csv
from tkinter import filedialog
import mysql.connector
import cv2
import os
import numpy as np

mydata=[]
class Attendence:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        # ==================variable=================
        self.var_atten_id=StringVar()
        self.var_atten_roll=StringVar()
        self.var_atten_name=StringVar()
        self.var_atten_dep=StringVar()
        self.var_atten_time=StringVar()
        self.var_atten_date=StringVar()
        self.var_atten_attendance=StringVar()
        
    
        img= Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\attendance1.jpg")
        img=img.resize((800,200),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=800,height=200)

        img1= Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\attendance2.jpg")
        img1=img1.resize((800,200),Image.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=800,y=0,width=800,height=200)
        #bg image
        img3= Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\attendance3.jpg")
        img3 = img3.resize((1530, 710), Image.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        title_lbl=Label(bg_img,text="ATTENDANCE MANAGEMENT SYSTEM",font=("times new roman",35,"bold"))
        title_lbl.place(x=0,y=0,width=1530,height=45)

        main_frame=Frame(bg_img,bd=2,bg="cyan")
        main_frame.place(x=20,y=50,width=1480,height=600)

        #left label frame
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Attendance Details", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=580)

        img_l = Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\attendance5.jpg")
        img_l = img_l.resize((700, 200), Image.LANCZOS)
        self.photoimg_l = ImageTk.PhotoImage(img_l)
        f_lbl = Label(Left_frame, image=self.photoimg_l)
        f_lbl.place(x=5, y=0, width=720, height=130)

        left_inside_frame = Frame(Left_frame, bd=2, relief=RIDGE, bg="white", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        left_inside_frame.place(x=0, y=135, width=720, height=300)

        #labels & entrys
        #student id
        attendenceId_label=Label(left_inside_frame,text="Attendence Id:",font=("times new roman",13,"bold"),bg="white")
        attendenceId_label.grid(row=0,column=0,padx=2,pady=10,sticky=W)

        attendenceId_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_id,font=("times new roman",13,"bold"))
        attendenceId_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)


        #roll no 
        rollLabel=Label(left_inside_frame,text="Roll No",font=("times in new roman",13,"bold"))
        rollLabel.grid(row=0,column=2,padx=4,pady=8,sticky=W)

        atten_roll=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_roll,font=("times new roman",13,"bold"))
        atten_roll.grid(row=0,column=3,pady=8)

        #name
        atten_name=Label(left_inside_frame,text="name",bg="white",font=("times in new roman",13,"bold"))
        atten_name.grid(row=1,column=0,padx=4,pady=8,sticky=W)

        atten_name=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_name,font=("times new roman",13,"bold"))
        atten_name.grid(row=1,column=1,pady=8)

        #department
        depLabel=Label(left_inside_frame,text="Department",bg="white",font=("times in new roman",13,"bold"))

        depLabel.grid(row=1,column=2)

        depLabel=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_dep,font=("times new roman",13,"bold"))
        depLabel.grid(row=1,column=3,pady=8)

        #Time
        timeLabel=Label(left_inside_frame,text="Time",bg="white",font=("times in new roman",13,"bold"))
        timeLabel.grid(row=2,column=0)

        atten_time=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_time,font=("times new roman",13,"bold"))
        atten_time.grid(row=2,column=1,pady=8)

        #Date box 
        dateLabel=Label(left_inside_frame,text="Date",bg="white",font=("times in new roman",13,"bold"))
        dateLabel.grid(row=2,column=2)

        atten_date=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_date,font=("times new roman",13,"bold"))
        atten_date.grid(row=2,column=3,pady=8)

        # ComboBox for Attendance Status

        attendanceLabel = Label(left_inside_frame, text="Attendance Status:", bg="white", font=("times new roman", 13, "bold"))
        attendanceLabel.grid(row=3, column=0, padx=10, pady=8, sticky=W)

        self.atten_status = ttk.Combobox(left_inside_frame, width=20,textvariable=self.var_atten_attendance, font=("comicsans", 13, "bold"), state="readonly")
        self.atten_status["values"] = ("status", "Present", "Absent")
        self.atten_status.grid(row=3, column=1, padx=10, pady=8)
        self.atten_status.current(0)  # Default to "status"

        #button Frame
        btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=715,height=35)

        save_btn=Button(btn_frame,text="Import csv",width=17,command=self.importCsv,font=("times in new roman",13,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0) 

# command=self.update_data
        update_btn=Button(btn_frame,text="Export csv",width=17,command=self.exportCsv,font=("times in new roman",13,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)


# command=self.delete_data
        delete_btn=Button(btn_frame,text="update",width=17,font=("times in new roman",13,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)


# command=self.reset_data
        reset_btn=Button(btn_frame,text="Reset",width=17,command=self.reset_data,font=("times in new roman",13,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)


                #right frame
        Right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Attendence Details",font=("times new roman",12,"bold"))


        Right_frame.place(x=750,y=10,width=720,height=580)


                #button Frame
        table_frame=Frame(Right_frame,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=5,width=700,height=455)


        #scroll bar

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        self.AttendenceReportTable=ttk.Treeview(table_frame,column=("id","roll","name","department","time","date","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.AttendenceReportTable.xview)
        scroll_y.config(command=self.AttendenceReportTable.yview)

        self.AttendenceReportTable.heading("id",text="Attendance ID")
        self.AttendenceReportTable.heading("roll",text=" Roll")
        self.AttendenceReportTable.heading("name",text=" Name")
        self.AttendenceReportTable.heading("department",text="Department")
        self.AttendenceReportTable.heading("time",text="Time")
        self.AttendenceReportTable.heading("date",text="Date")
        self.AttendenceReportTable.heading("attendance",text="Attendance ")

        self.AttendenceReportTable["show"]="headings"
        self.AttendenceReportTable.column("id",width=100)
        self.AttendenceReportTable.column("roll",width=100)
        self.AttendenceReportTable.column("name",width=100)
        self.AttendenceReportTable.column("department",width=100)
        self.AttendenceReportTable.column("time",width=100)
        self.AttendenceReportTable.column("date",width=100)
        self.AttendenceReportTable.column("attendance",width=100)

        self.AttendenceReportTable.pack(fill=BOTH,expand=1)
        
        self.AttendenceReportTable.bind("<ButtonRelease>",self.get_cursor)

# ===============================================fetch data ====================================================
    def fetchData(self,rows):
        self.AttendenceReportTable.delete(*self.AttendenceReportTable.get_children())
        for i in rows:
            self.AttendenceReportTable.insert("",END,values=i)


# ----------------for importing --------------------
    def importCsv(self):
        global mydata
        # from tkinter import filedialog
        mydata.clear()

        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            parent=self.root
        )
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")     #delimiter = to separate by comma
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)
           
           
    # ----------------------for exporting -------------------- 
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data Found to Export ",parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            parent=self.root
            )
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export","Your data exported to "+os.path.basename(fln)+"Successfully")
        except Exception as es:
            messagebox.showerror("Error",f"Due To :{str(es)}",parent=self.root)
    
    
    def get_cursor(self,event=""):
        cursor_row=self.AttendenceReportTable.focus()
        content=self.AttendenceReportTable.item(cursor_row)
        rows=content['values']
        self.var_atten_id.set(rows[0])
        self.var_atten_roll.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_dep.set(rows[3])
        self.var_atten_time.set(rows[4])
        self.var_atten_date.set(rows[5])
        self.var_atten_attendance.set(rows[6])
        
    def reset_data(self):
        # rows=content['values'] ............................................Syntax 
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("")
        
            


if __name__=="__main__":
    root=Tk()
    obj=Attendence(root)
    root.mainloop()

