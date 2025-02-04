from re import search
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
# from student import Student 
class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System") 
        
        # VARIABLE ==============
        self.var_dep=StringVar()
        self.var_course=StringVar()
        # self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=IntVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=IntVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=IntVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()
        
        
        #bg 
        img2=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\Screenshot 2024-07-25 233948.png")
        img2=img2.resize((1530,790),Image.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        bg_img=Label(self.root,image=self.photoimg2)
        bg_img.place(x=0,y=0,width=1530,height=710)
        
        title_lbl=Label(bg_img,text="STUDENT MANAGEMENT SYSTEM",font =("times new roman",35,"bold"),bg="white",fg="darkblue")
        title_lbl.place(x=0,y=0,width=1530,height=45) 
        
        main_frame=Frame(bg_img,bd=2)
        main_frame.place(x=20,y=55,width=1500,height=1000)
        
        # Left Label frame
        
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="STUDENT DETAILS",font=("times new roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=580)
        img_l=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\student.jpg")
        img_l=img_l.resize((700,130),Image.LANCZOS)
        self.photoimg_l=ImageTk.PhotoImage(img_l)
        f_lbl=Label(Left_frame,image=self.photoimg_l)
        f_lbl.place(x=5,y=0,width=700,height=130)
        
        #current course
        current_course_frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course Information",font=("times new roman",12,"bold"))
        current_course_frame.place(x=5,y=135,width=720,height=150)
        #Department
        dep_label=Label(current_course_frame,text="Department",font=("times new roman",13,"bold"),bg="white")
        dep_label.grid(row=0,column=0,padx=2,pady=10,sticky=W)
        
        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_dep,font=("times new roman",12,"bold"),state="readonly",width=17)
        dep_combo["values"]=("Select Department","Computer","Artificial Intelligence & Data Science","Civil","Mechanical","Electrical")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        
        #course
        course_label=Label(current_course_frame,text="Course",font=("times new roman",13,"bold"),bg="white")
        course_label.grid(row=0,column=2,padx=2,pady=10,sticky=W)

        course_combo=ttk.Combobox(current_course_frame,textvariable=self.var_course,font=("times new roman",12,"bold"),state="readonly",width=17)
        course_combo["values"]=("Select year","FY","SY","TY","BTech")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)
        #semester
        semester_label=Label(current_course_frame,text="semester",font=("times new roman",13,"bold"),bg="white")
        semester_label.grid(row=1,column=0,padx=2,pady=10,sticky=W)

        semester_combo=ttk.Combobox(current_course_frame,textvariable=self.var_semester,font=("times new roman",12,"bold"),state="readonly",width=17)
        semester_combo["values"]=("Select semester","Semester-1","Semester-2","Semester-3","Semester-4","Semester-5","Semester-6","Semester-7","Semester-8")
        semester_combo.current(0)
        semester_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)
        
        #Class student Information
        class_student_frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Class Student Information",font=("times new roman",12,"bold"))
        class_student_frame.place(x=5,y=250,width=720,height=600)

        #student id
        studentId_label=Label(class_student_frame,text="StudentId:",font=("times new roman",13,"bold"),bg="white")
        studentId_label.grid(row=0,column=0,padx=2,pady=5,sticky=W)

        studentID_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_std_id,font=("times new roman",13,"bold"))
        studentID_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)
        # Student Name
        studentName_label=Label(class_student_frame,text="Student Name:",font=("times new roman",13,"bold"),bg="white")
        studentName_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        studentName_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_std_name,font=("times new roman",13,"bold"))
        studentName_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)

        #class Division
        class_div_label=Label(class_student_frame,text="Class Division",font=("times in new roman",13,"bold"))
        class_div_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)

        class_div_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_div,font=("times new roman",13,"bold"))
        class_div_entry.grid(row=1,column=1,padx=10,pady=5,sticky=W)

        #roll number
        roll_no_label=Label(class_student_frame,text="Roll No",font=("times new roman",13,"bold"),bg="white")
        roll_no_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        roll_no_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_roll,font=("times new roman",13,"bold"))
        roll_no_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        #Gender
        gender_label=Label(class_student_frame,text="Gender:",font=("times new roman",13,"bold"),bg="white")
        gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)

        gender_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_gender,font=("times new roman",13,"bold"))
        gender_entry.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        #dob
        dob_label=Label(class_student_frame,text="DOB:",font=("times new roman",13,"bold"),bg="white")
        dob_label.grid(row=2,column=2,padx=2,pady=5,sticky=W)

        dob_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_dob,font=("times new roman",13,"bold"))
        dob_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        #email
        email_label=Label(class_student_frame,text="Email:",font=("times new roman",13,"bold"),bg="white")
        email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        email_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_email,font=("times new roman",13,"bold"))
        email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)

        #phone number
        phone_label=Label(class_student_frame,text="Phone No:",font=("times new roman",13,"bold"),bg="white")
        phone_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        phone_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_phone,font=("times new roman",13,"bold"))
        phone_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)

        #address
        address_label=Label(class_student_frame,text="Address:",font=("times new roman",13,"bold"),bg="white")
        address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        address_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_address,font=("times new roman",13,"bold"))
        address_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)

        #Teacher Name
        teacher_label=Label(class_student_frame,text="Teacher Name:",font=("times new roman",13,"bold"),bg="white")
        teacher_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        teacher_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_teacher,font=("times new roman",13,"bold"))
        teacher_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)
# =====================================================================================================================================================================================
        #radio buttons
        self.var_radio1=StringVar() 
        radionbtn1=ttk.Radiobutton(class_student_frame,variable=self.var_radio1,text="Take photo sample",value="Yes")
        radionbtn1.grid(row=6,column=0)
        radionbtn2=ttk.Radiobutton(class_student_frame,variable=self.var_radio1,text="No photo sample",value="No")
        radionbtn2.grid(row=6,column=1)
        #button Frame
        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=715,height=35)

        save_btn=Button(btn_frame,text="SAVE",command=self.add_data,width=17,font=("times new roman",13,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn=Button(btn_frame,text="UPDATE",width=17,command=self.update_data,font=("times new roman",13,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn=Button(btn_frame,text="DELETE",width=17,command=self.delete_data,font=("times new roman",13,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="RESET",width=17,command=self.reset_data,font=("times new roman",13,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)
        #button Frame
        btn_frame1=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=0,y=235,width=715,height=35)
        take_btn=Button(btn_frame1,command=self.generate_dataset,text="Take Photo Sample",width=34,font=("times in new roman",13,"bold"),bg="blue",fg="white")
        take_btn.grid(row=2,column=0)

        update_btn=Button(btn_frame1,text="Update Photo Sample",width=34,font=("times in new roman",13,"bold"),bg="blue",fg="white")
        update_btn.grid(row=2,column=1)
        # right Label frame
        
        Right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="STUDENT DETAILS",font=("times new roman",12,"bold"))
        Right_frame.place(x=700,y=10,width=720,height=580)
        img_r=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\student.jpg")
        
        img_r=img_r.resize((720,130),Image.LANCZOS)
        self.photoimg_r=ImageTk.PhotoImage(img_r)
        f_lbl=Label(Right_frame,image=self.photoimg_r)
        f_lbl.place(x=5,y=0,width=720,height=130)
         #Class student Information
        Search_frame=LabelFrame(Right_frame,bd=2,bg="white",relief=RIDGE,text="Search System",font=("times new roman",12,"bold"))
        Search_frame.place(x=5,y=135,width=720,height=70)
        
        search_label=Label(Search_frame,text="Search By :",font=("times new roman",13,"bold"),bg="red",fg="white")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        
        search_combo=ttk.Combobox(Search_frame,font=("times new roman",13,"bold"),state="readonly",width=12)
        search_combo["values"]=("Select ","Roll_No","Phone_No")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        
        search_entry=ttk.Entry(Search_frame,width=15,font=("times new roman",13,"bold"))
        search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)
        
        search_btn=Button(Search_frame,text="Search",width=12,font=("times new roman",13,"bold"),bg="blue",fg="white")
        search_btn.grid(row=0,column=3)

        showAll_btn=Button(Search_frame,text="Show All",width=12,font=("times new roman",13,"bold"),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)
        
        table_frame=Frame(Right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=210,width=710,height=250)
        
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        self.student_table=ttk.Treeview(table_frame,column=("dep","course","sem","id","name","roll","div","dob","email","gender","phone","address","teacher","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        # Configure scrollbars
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Pack scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Attach scrollbars to the Treeview
        self.student_table.pack(fill=BOTH, expand=True)
        self.student_table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        
        self.student_table.heading("dep",text="Department")
        self.student_table.heading("course",text="Course") 
        # self.student_table.heading("year",text="Year") 
        self.student_table.heading("sem",text="Semester") 
        self.student_table.heading("id",text="StudentId") 
        self.student_table.heading("name",text="Name") 
        self.student_table.heading("roll",text="Roll") 
        self.student_table.heading("div",text="Division") 
        self.student_table.heading("dob",text="DOB") 
        self.student_table.heading("email",text="Email") 
        self.student_table.heading("gender",text="Gender") 

        self.student_table.heading("phone",text="Phone") 
        self.student_table.heading("address",text="Address") 
        self.student_table.heading("teacher",text="Teacher") 
        self.student_table.heading("photo",text="PhotoSampleStatus")
        self.student_table["show"]="headings"
        
        self.student_table.pack(fill=BOTH,expand=1) 
        self.student_table.column("dep",width=100)
        self.student_table.column("course",width=100)
        # self.student_table.column("dep",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("roll",width=100)

        self.student_table.column("div",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("teacher",width=100)
        self.student_table.column("photo",width=150)
        
        self.student_table.pack(fill=BOTH,expand=1)
        # self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()
        
# =========================================================function declaration ========================
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            # messagebox.showeinfo("success","welcome")
            try:
                
                conn=mysql.connector.connect(host="localhost",username="root",password="pass123",database="face_recognizer")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                                        self.var_dep.get(),
                                                                                                        self.var_course.get(),
                                                                                                        #  self.var_year.get(),
                                                                                                        self.var_semester.get(),
                                                                                                        self.var_std_id.get(),
                                                                                                        self.var_std_name.get(),
                                                                                                        self.var_roll.get(),
                                                                                                        self.var_div.get(),
                                                                                                        self.var_dob.get(),
                                                                                                        self.var_email.get(),
                                                                                                        self.var_gender.get(),
                                                                                                        self.var_phone.get(),
                                                                                                        # self.var_phone.get(),
                                                                                                        self.var_address.get(),
                                                                                                        self.var_teacher.get(),
                                                                                                        self.var_radio1.get(),
                    
                    
                    
                    
                    
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("success","Student details has been added successfully ",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To :{str(es)}",parent=self.root)
    
    
    def fetch_data(Self):
        # Connect to the database
        conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM student")
        data = my_cursor.fetchall()
        
        # Check if data is not empty
        if len(data) != 0:
            # Clear existing data from the Treeview
            Self.student_table.delete(*Self.student_table.get_children())  # Use * to unpack the list of children
            
            # Insert new data into the Treeview
            for i in data:
                Self.student_table.insert("", "end", values=i)
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        
    #    ======================update=================
    def get_cursor(self, event):
        # Get the selected row
        selected_row = self.student_table.focus()
        # Get the values from the selected row
        values = self.student_table.item(selected_row)['values']
        
        # Check if values are retrieved correctly
        if values:
            # Assign each value to the corresponding variable/input field
            self.var_dep.set(values[0])         # Department
            self.var_course.set(values[1])      # Course
            self.var_semester.set(values[2])    # Semester
            self.var_std_id.set(values[3])      # Student ID
            self.var_std_name.set(values[4])     # Name
            self.var_roll.set(values[5])        # Roll No
            self.var_div.set(values[6])         # Division
            self.var_dob.set(values[7])         # DOB
            self.var_email.set(values[8])       # Email
            self.var_gender.set(values[9])      # Gender
            self.var_phone.set(values[10])      # Phone
            self.var_address.set(values[11])    # Address
            self.var_teacher.set(values[12])    # Teacher
            self.var_radio1.set(values[13])     # PhotoSampleStatus (ensure this is correct)

        # =========================================update function=================
    def update_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
                my_cursor = conn.cursor()
                my_cursor.execute("UPDATE student SET `dep` = %s, `course` = %s, `Semester` = %s, `name` = %s, `roll` = %s, `div` = %s, `gender` = %s, `dob` = %s, `email` = %s, `phone` = %s, `address` = %s, `teacher` = %s, `PhotoSample` = %s WHERE `Student_id` = %s", (
                self.var_dep.get(),
                self.var_course.get(),
                self.var_semester.get(),
                self.var_std_name.get(),
                self.var_roll.get(),
                self.var_div.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_radio1.get(),
                self.var_std_id.get()  # Ensure you're updating the right record
            ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details have been updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

        
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        # self.var_dep.set(data[0])
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_roll.set("")
        self.var_div.set("")
        
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")
        
    def delete_data(self):
        if self.var_dep.get()=="":
            messagebox.showerror("Error","Student id must be required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student delete page","Do you want to delete this student",parent=self.root)
                if delete>0:

                    conn=mysql.connector.connect(host="localhost",username="root",password="pass123",database="face_recognizer")
                    my_cursor=conn.cursor()
                    sql="delete from student where Student_id=%s"
                    val=(self.var_std_id.get(),)
                    my_cursor.execute(sql,val)
                else:

                    if not delete:
                        return
                    
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Successfully deleted student details",parent=self.root)
            
            except Exception as es:
                messagebox.showi("Error",f"Due to:{str(es)}",parent=self.root)
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return  # Exit the function if fields are missing

        # Prepare values for the database
        dep = self.var_dep.get()
        course = self.var_course.get()
        semester = self.var_semester.get()
        name = self.var_std_name.get()
        roll = self.var_roll.get() if self.var_roll.get() else None
        div = self.var_div.get() 
        gender = self.var_gender.get()
        dob = self.var_dob.get()
        email = self.var_email.get()
        phone = self.var_phone.get() if self.var_phone.get() else None
        address = self.var_address.get()
        teacher = self.var_teacher.get()
        photo_sample = self.var_radio1.get()
        student_id = self.var_std_id.get()

        # Log values for debugging
        print(f"Values: {dep}, {course}, {semester}, {name}, {roll}, {div}, {gender}, {dob}, {email}, {phone}, {address}, {teacher}, {photo_sample}, {student_id}")

        try:
            # Database connection
            conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
            my_cursor = conn.cursor()

            # Correct SQL update statement
            my_cursor.execute("""
                UPDATE student SET 
                    `Dep` = %s,
                    `Course` = %s,
                    `Semester` = %s,
                    `Name` = %s,
                    `Roll` = %s,
                    `Div` = %s,
                    `Gender` = %s,
                    `Dob` = %s,
                    `Email` = %s,
                    `Phone` = %s,
                    `Address` = %s,
                    `Teacher` = %s,
                    `PhotoSample` = %s
                WHERE `Student_id` = %s
            """, (
                dep,
                course,
                semester,
                name,
                roll,
                div,
                gender,
                dob,
                email,
                phone,
                address,
                teacher,
                photo_sample,
                student_id  # Ensure this is the correct ID
            ))

            conn.commit()
            self.fetch_data()
            self.reset_data()
            conn.close()

            # Initialize Face Detection and Image Capture Process
            face_classifier = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\Face_Recognition_Proj\haarcascade_frontalface_default.xml")
            if face_classifier.empty():
                raise Exception("Could not load Haar cascade classifier.")

            cap = cv2.VideoCapture(0)  # Open video capture

            img_id = 0  # Counter for number of images captured

            while True:
                ret, my_frame = cap.read()
                if not ret:
                    break  # If we failed to grab a frame, stop the process

                # Convert frame to grayscale and detect faces
                gray = cv2.cvtColor(my_frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # If no faces are detected, show a message
                if len(faces) == 0:
                    cv2.putText(my_frame, "No face detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                for (x, y, w, h) in faces:
                    img_id += 1
                    face = gray[y:y + h, x:x + w]  # Extract the face from the image
                    face_resized = cv2.resize(face, (200, 200))  # Resize for consistency

                    # Save the image of the face to a specific file path
                    file_name_path = f"Data/user.{student_id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face_resized)

                    # Display the image with ID and a message
                    cv2.putText(my_frame, f"Image ID: {img_id}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.rectangle(my_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw a rectangle around the face
                    cv2.imshow("Capturing Face", my_frame)

                # Stop after 300 images or when Enter key (13) is pressed
                if cv2.waitKey(1) == 13 or img_id >= 200:
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Show completion message
            messagebox.showinfo("RESULT", "Generating dataset completed!")
        
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)          
    # def generate_dataset(self):
    #     if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
    #         messagebox.showerror("Error", "All Fields are required", parent=self.root)
    #         return  # Exit the function if fields are missing

    #     # Prepare values for the database
    #     dep = self.var_dep.get()
    #     course = self.var_course.get()
    #     semester = self.var_semester.get()
    #     name = self.var_std_name.get()
    #     roll = self.var_roll.get() if self.var_roll.get() else None
    #     div = self.var_div.get() 
    #     gender = self.var_gender.get()
    #     dob = self.var_dob.get()
    #     email = self.var_email.get()
    #     phone = self.var_phone.get() if self.var_phone.get() else None
    #     address = self.var_address.get()
    #     teacher = self.var_teacher.get()
    #     photo_sample = self.var_radio1.get()
    #     student_id = self.var_std_id.get()

    #     # Log values for debugging
    #     print(f"Values: {dep}, {course}, {semester}, {name}, {roll}, {div}, {gender}, {dob}, {email}, {phone}, {address}, {teacher}, {photo_sample}, {student_id}")

    #     try:
    #         # Database connection
    #         conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
    #         my_cursor = conn.cursor()

    #         # Correct SQL update statement
    #         my_cursor.execute("""
    #             UPDATE student SET 
    #                 `Dep` = %s,
    #                 `Course` = %s,
    #                 `Semester` = %s,
    #                 `Name` = %s,
    #                 `Roll` = %s,
    #                 `Div` = %s,
    #                 `Gender` = %s,
    #                 `Dob` = %s,
    #                 `Email` = %s,
    #                 `Phone` = %s,
    #                 `Address` = %s,
    #                 `Teacher` = %s,
    #                 `PhotoSample` = %s
    #             WHERE `Student_id` = %s
    #         """, (
    #             dep,
    #             course,
    #             semester,
    #             name,
    #             roll,
    #             div,
    #             gender,
    #             dob,
    #             email,
    #             phone,
    #             address,
    #             teacher,
    #             photo_sample,
    #             student_id  # Ensure this is the correct ID
    #         ))

    #         conn.commit()
    #         self.fetch_data()
    #         self.reset_data()
    #         conn.close()
            
    #         face_classifier = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\Face_Recognition_Proj\haarcascade_frontalface_default.xml")
    #         if face_classifier.empty():
    #             raise Exception("Could not load Haar cascade classifier.")

    #         cap = cv2.VideoCapture(0)
    #         img_id = 0

    #         while True:
    #             ret, my_frame = cap.read()
    #             if not ret:
    #                 break

    #             # Convert frame to grayscale and detect faces
    #             gray = cv2.cvtColor(my_frame, cv2.COLOR_BGR2GRAY)
    #             faces = face_classifier.detectMultiScale(gray, 1.8, 5)

    #             for (x, y, w, h) in faces:
    #                 img_id += 1
    #                 face = gray[y:y + h, x:x + w]
    #                 face_resized = cv2.resize(face, (200, 200))  # Resize for consistency

    #                 file_name_path = f"Data/user.{student_id}.{img_id}.jpg"
    #                 cv2.imwrite(file_name_path, face_resized)
    #                 cv2.putText(face_resized, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
    #                 cv2.imshow("Cropped Face", face_resized)

    #             if cv2.waitKey(1) == 13 or img_id == 150:  # Stop after 300 images
    #                 break

    #         cap.release()
    #         cv2.destroyAllWindows()
    #         messagebox.showinfo("RESULT", "Generating data sets completed!")
    #     except Exception as es:
    #         messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
       
if __name__ == "__main__":
    root=Tk()
    obj = Student(root)
    root.mainloop() 
    
    
    
    
    
    
    
            
        
    # def generate_dataset(self):
    #     if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
    #         messagebox.showerror("Error", "All Fields are required", parent=self.root)
    #         return  # Exit the function if fields are missing

    #     # Prepare values for the database
    #     dep = self.var_dep.get()
    #     course = self.var_course.get()
    #     semester = self.var_semester.get()
    #     name = self.var_std_name.get()
    #     roll = self.var_roll.get() if self.var_roll.get() else None
    #     div = self.var_div.get() 
    #     gender = self.var_gender.get()
    #     dob = self.var_dob.get()
    #     email = self.var_email.get()
    #     phone = self.var_phone.get() if self.var_phone.get() else None
    #     address = self.var_address.get()
    #     teacher = self.var_teacher.get()
    #     photo_sample = self.var_radio1.get()
    #     student_id = self.var_std_id.get()

    #     # Log values for debugging
    #     print(f"Values: {dep}, {course}, {semester}, {name}, {roll}, {div}, {gender}, {dob}, {email}, {phone}, {address}, {teacher}, {photo_sample}, {student_id}")

    #     try:
    #         # Database connection
    #         conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
    #         my_cursor = conn.cursor()

    #         # Correct SQL update statement
    #         my_cursor.execute("""
    #             UPDATE student SET 
    #                 `Dep` = %s,
    #                 `Course` = %s,
    #                 `Semester` = %s,
    #                 `Name` = %s,
    #                 `Roll` = %s,
    #                 `Div` = %s,
    #                 `Gender` = %s,
    #                 `Dob` = %s,
    #                 `Email` = %s,
    #                 `Phone` = %s,
    #                 `Address` = %s,
    #                 `Teacher` = %s,
    #                 `PhotoSample` = %s
    #             WHERE `Student_id` = %s
    #         """, (
    #             dep,
    #             course,
    #             semester,
    #             name,
    #             roll,
    #             div,
    #             gender,
    #             dob,
    #             email,
    #             phone,
    #             address,
    #             teacher,
    #             photo_sample,
    #             student_id  # Ensure this is the correct ID
    #         ))

    #         conn.commit()
    #         self.fetch_data()
    #         self.reset_data()
    #         conn.close()
            
    #         face_classifier = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\Face_Recognition_Proj\haarcascade_frontalface_default.xml")
    #         if face_classifier.empty():
    #             raise Exception("Could not load Haar cascade classifier.")

    #         cap = cv2.VideoCapture(0)
    #         img_id = 0

    #         while True:
    #             ret, my_frame = cap.read()
    #             if not ret:
    #                 break

    #             # Convert frame to grayscale and detect faces
    #             gray = cv2.cvtColor(my_frame, cv2.COLOR_BGR2GRAY)
    #             faces = face_classifier.detectMultiScale(gray, 1.8, 5)

    #             for (x, y, w, h) in faces:
    #                 img_id += 1
    #                 face = gray[y:y + h, x:x + w]
    #                 face_resized = cv2.resize(face, (200, 200))  # Resize for consistency

    #                 file_name_path = f"Data/user.{student_id}.{img_id}.jpg"
    #                 cv2.imwrite(file_name_path, face_resized)
    #                 cv2.putText(face_resized, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
    #                 cv2.imshow("Cropped Face", face_resized)

    #             if cv2.waitKey(1) == 13 or img_id == 300:  # Stop after 300 images
    #                 break

    #         cap.release()
    #         cv2.destroyAllWindows()
    #         messagebox.showinfo("RESULT", "Generating data sets completed!")
    #     except Exception as es:
    #         messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)