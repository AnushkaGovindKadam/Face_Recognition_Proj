from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from attendance import Attendence
from student import Student 
import os
from train import Train
from face_recognition import Face_Recognition

class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        img2=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\bg3.jpg")
        img2=img2.resize((1530,710),Image.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        bg_img=Label(self.root,image=self.photoimg2)
        bg_img.place(x=0,y=0,width=1530,height=710)
        
        title_lbl=Label(bg_img,text="FACE RECOGNITION SYSTEM FOR ATTENDANCE",font =("times new roman",35,"bold"),bg="blue",fg="black")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        
        #Student Button 
        img4=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\Screenshot 2024-07-25 233948.png")
        img4=img4.resize((220,220),Image.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4) 
        
        b1=Button(bg_img,image=self.photoimg4,command=self.student_details,cursor="hand2")
        b1.place(x=200,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="Student Details",command=self.student_details,cursor="hand2",font =("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=280,width=220,height=40)
        
        #FACE DETECTION  Button 
        img5=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\WhatsApp Image 2024-11-08 at 16.47.19_13701cd1.jpg")
        img5=img5.resize((220,220),Image.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5) 
        
        b1=Button(bg_img,image=self.photoimg5,cursor="hand2",command=self.face_data)
        b1.place(x=500,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="Face Detector",cursor="hand2",command=self.face_data,font =("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=500,y=280,width=220,height=40)
        
        #Attendance Button 
        img6=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\attendance4.jpg")
        img6=img6.resize((220,220),Image.LANCZOS)
        self.photoimg6=ImageTk.PhotoImage(img6) 
        
        b1=Button(bg_img,image=self.photoimg6,cursor="hand2",command=self.attendance_data)
        b1.place(x=800,y=100,width=220,height=220)
        
        b1_1=Button(bg_img,text="Attendance",cursor="hand2",command=self.attendance_data,font =("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=280,width=220,height=40)
        
        #Train Face  Button 
        img7=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\train_faces2.jpg")
        img7=img7.resize((220,220),Image.LANCZOS)
        self.photoimg7=ImageTk.PhotoImage(img7) 
        
        b1=Button(bg_img,image=self.photoimg7,cursor="hand2",command=self.train_data)
        b1.place(x=200,y=400,width=220,height=220)
        
        b1_1=Button(bg_img,text="Train Faces ",cursor="hand2",command=self.train_data,font =("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=600,width=220,height=40)
        
        #Photos Button 
        img8=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\phots .jpg")
        img8=img8.resize((220,220),Image.LANCZOS)
        self.photoimg8=ImageTk.PhotoImage(img8) 
        
        b1=Button(bg_img,image=self.photoimg8,cursor="hand2",command=self.open_img)
        b1.place(x=500,y=400,width=220,height=220)
        
        b1_1=Button(bg_img,text="Photos ",cursor="hand2",command=self.open_img,font =("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=500,y=600,width=220,height=40)
        
        # exit  Button 
        img9=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\exit.jpg")
        img9=img9.resize((220,220),Image.LANCZOS)
        self.photoimg9=ImageTk.PhotoImage(img9) 
        
        b1=Button(bg_img,image=self.photoimg9,cursor="hand2",command=self.exit_application)
        b1.place(x=800,y=400,width=220,height=220)
        
        b1_1=Button(bg_img,text="Exit  ",cursor="hand2",command=self.exit_application,font =("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=600,width=220,height=40)
        
        
    def open_img(self):
        os.startfile("Data")
        # ============================================function button ==============================
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)
        
    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)
        
    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)\
                
            
    def attendance_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendence(self.new_window)
            
    def exit_application(self):
        self.root.destroy()  # Closes the main application window

        
if __name__ == "__main__":
    root=Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
    
    
    
