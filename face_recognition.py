import csv
from tkinter import*
from tkinter import ttk
import pandas as pd
from PIL import Image,ImageTk
from tkinter import messagebox
#from train import Train
from time import strftime
from datetime import datetime
import mysql.connector
import cv2
import os
import dlib
import numpy as np
class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="Face Recognition", font=("times new roman", 35, "bold"), bg="blue", fg="black")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\face_rec.jpg")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl_left = Label(self.root, image=self.photoimg_top)
        f_lbl_left.place(x=0, y=55, width=650, height=700)

        img_bottom = Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\face_rec3.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl_right = Label(self.root, image=self.photoimg_bottom)
        f_lbl_right.place(x=650, y=55, width=950, height=700)

                #button
        b1_1=Button(f_lbl_right,text="Click Here",cursor="hand2",command=self.face_Recog,font=("time new roman",32,"bold"),bg="cyan",fg="black")
        b1_1.place(x=1,y=300,width=250,height=90)
        # self.marked_attendance_today = set()

        
        # =================================================ATTENDANCE==============================================================

    
    def mark_attendance(self, i, r, n, d):
        now = datetime.now()
        current_date = now.strftime("%d/%m/%Y")
        current_hour = now.hour
        current_minute = now.minute

        
        # Check for valid student data before proceeding
        if i == "Unknown" or r == "Unknown" or n == "Unknown" or d == "Unknown":
            print("Invalid student data. Attendance not recorded.")
            return

        # Determine which CSV file to use based on the time
        if (current_hour == 10 and current_minute >= 0) or (current_hour < 12):  # 10:00 AM to 12:00 PM
            file_name = "morning.csv"
        elif (current_hour == 13 and current_minute >= 0) or (current_hour > 13 and current_hour < 15) or (current_hour == 15 and current_minute <= 15):  # 1:00 PM to 3:15 PM
            file_name = "afternoon.csv"
        elif (current_hour == 15 and current_minute >= 16) or (current_hour > 15 and current_hour < 17) or (current_hour == 17 and current_minute <= 15):  # 3:16 PM to 5:15 PM
            file_name = "evening.csv"
        else:
            with open("temp21_invalid.csv", "a", newline="\n") as f:
                dl = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Invalid Time")
            print("Attendance marking is not available at this time.")
            return

        # Check if student is already marked present today
        attendance_marked = False
        for attendance_file in ["morning.csv", "afternoon.csv", "evening.csv", "temp21_invalid.csv"]:
            if os.path.exists(attendance_file):
                with open(attendance_file, "r") as f:
                    myDataList = f.readlines()
                    for line in myDataList:
                        entry = line.split(",")
                        if entry[0] == str(i) and entry[5] == current_date:
                            attendance_marked = True
                            break
                if attendance_marked:
                    break

        if attendance_marked:
            print("Attendance already marked for today.")
            # Face_Recognition.calculate_attendance_summary()

            return  # Exit if already marked present today

        # Mark attendance in the corresponding file
        with open(file_name, "a", newline="\n") as f:
            dl = now.strftime("%d/%m/%Y")
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Present")
            print("Attendance marked successfully.")
            # Face_Recognition.calculate_attendance_summary()

            


 
    def face_Recog(self):
        marked_attendance_today = set()
        def draw_boundary(img, detector, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces using Dlib
            faces = detector(gray_image)
            coord = []
            
            for face in faces:
                x, y, w, h = (face.left(), face.top(), face.width(), face.height())
                
                # Ensure the face region is valid (non-zero size)
                if w > 0 and h > 0:
                    img_face = gray_image[y:y + h, x:x + w]
                    img_face = cv2.resize(img_face, (200, 200))  # Resize for consistency
                    img_face = img_face / 255.0  # Normalize pixel values

                    id, predict = clf.predict(img_face)
                    confidence = int((100 * (1 - predict / 300)))

                    conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
                    my_cursor = conn.cursor()

                    # Fetch student details from the database
                    my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
                    n = my_cursor.fetchone()
                    n = n[0] if n else "Unknown"

                    my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
                    r = my_cursor.fetchone()
                    r = str(r[0]) if r else "Unknown"

                    my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
                    d = my_cursor.fetchone()
                    d = d[0] if d else "Unknown"
                    
                    my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
                    i = my_cursor.fetchone()
                    i = i[0] if i else "Unknown"

                    if confidence > 77:  # Set confidence threshold
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
                        cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
                        cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
                        cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)

                        # Mark attendance only once
                        if i not in marked_attendance_today:
                            self.mark_attendance(i, r, n, d)
                            marked_attendance_today.add(i)  # Prevent re-marking attendance for the same student
                    else:
                    
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        cv2.putText(img, "Unknown", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)

                        
                else:
                    
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)

                
                coord = [x, y, w, h]
            
            return coord

        def recognize(img, clf, detector):
            coord = draw_boundary(img, detector, (255, 25, 255), "Face", clf)
            return img

        # Initialize Dlib's face detector
        detector = dlib.get_frontal_face_detector()

        # Load pre-trained LBPH face recognizer
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read(r"C:\Users\hp\Desktop\Face_Recognition_Proj\Trained_data.xml")

        video_cap = cv2.VideoCapture(0)

        if not video_cap.isOpened():
            messagebox.showerror("Error", "Could not open video device")
            return

        while True:
            ret, img = video_cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image")
                break

            img = recognize(img, clf, detector)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) & 0xFF == 13:  # 13 is the Enter key
                break

        video_cap.release()
        # self.calculate_attendance_summary()
        cv2.destroyAllWindows()

    
    
    
    
    
    
    
    



           
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    # obj.start_recognition()  # Call to start recognition
    root.mainloop()



