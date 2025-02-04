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
# import csv
# from tkinter import *
# from tkinter import ttk
# import pandas as pd
# from PIL import Image, ImageTk
# from tkinter import messagebox
# import mysql.connector
# import cv2
# import os
# import dlib
# import numpy as np
# import threading
# from datetime import datetime

# class Face_Recognition:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("1530x790+0+0")
#         self.root.title("Face Recognition System")

#         title_lbl = Label(self.root, text="Face Recognition", font=("times new roman", 35, "bold"), bg="blue", fg="black")
#         title_lbl.place(x=0, y=0, width=1530, height=45)

#         img_top = Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\face_rec.jpg")
#         img_top = img_top.resize((650, 700), Image.LANCZOS)
#         self.photoimg_top = ImageTk.PhotoImage(img_top)

#         f_lbl_left = Label(self.root, image=self.photoimg_top)
#         f_lbl_left.place(x=0, y=55, width=650, height=700)

#         img_bottom = Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\face_rec3.jpg")
#         img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
#         self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

#         f_lbl_right = Label(self.root, image=self.photoimg_bottom)
#         f_lbl_right.place(x=650, y=55, width=950, height=700)

#         # Button for starting the face recognition
#         b1_1 = Button(f_lbl_right, text="Click Here", cursor="hand2", command=self.start_face_recognition, font=("times new roman", 32, "bold"), bg="cyan", fg="black")
#         b1_1.place(x=1, y=300, width=250, height=90)

#         self.marked_attendance_today = set()  # Set to track attendance for today
#         self.last_known_coords = None  # To hold last known face coordinates for stability

#     def mark_attendance(self, i, r, n, d):
#         now = datetime.now()
#         current_date = now.strftime("%d/%m/%Y")
#         current_hour = now.hour
#         current_minute = now.minute

#         # Check for valid student data before proceeding
#         if i == "Unknown" or r == "Unknown" or n == "Unknown" or d == "Unknown":
#             print("Invalid student data. Attendance not recorded.")
#             return

#         # Determine which CSV file to use based on the time
#         if (current_hour == 10 and current_minute >= 0) or (current_hour < 12) or (current_hour == 12 and current_minute <= 15):
#             file_name = "morning.csv"
#         elif (current_hour == 12 and current_minute > 15) or (current_hour < 15):
#             file_name = "afternoon.csv"
#         elif (current_hour == 15 and current_minute >= 0) or (current_hour < 17) or (current_hour == 17 and current_minute <= 15):
#             file_name = "evening.csv"
#         else:
#             with open("temp21_invalid.csv", "a", newline="\n") as f:
#                 dl = now.strftime("%d/%m/%Y")
#                 dtString = now.strftime("%H:%M:%S")
#                 f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Invalid Time")
#             print("Attendance marking is not available at this time.")
#             return

#         # Check if student is already marked present today
#         attendance_marked = False
#         for attendance_file in ["morning.csv", "afternoon.csv", "evening.csv", "temp21_invalid.csv"]:
#             if os.path.exists(attendance_file):
#                 with open(attendance_file, "r") as f:
#                     myDataList = f.readlines()
#                     for line in myDataList:
#                         entry = line.split(",")
#                         if entry[0] == str(i) and entry[5] == current_date:
#                             attendance_marked = True
#                             break
#                 if attendance_marked:
#                     break

#         if attendance_marked:
#             print("Attendance already marked for today.")
#             return  # Exit if already marked present today

#         # Mark attendance in the corresponding file
#         with open(file_name, "a", newline="\n") as f:
#             dl = now.strftime("%d/%m/%Y")
#             dtString = now.strftime("%H:%M:%S")
#             f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Present")
#             print("Attendance marked successfully.")

#     def start_face_recognition(self):
#         # Run face recognition in a separate thread to avoid blocking the main thread
#         capture_thread = threading.Thread(target=self.face_Recog)
#         capture_thread.start()

#     def face_Recog(self):
#         video_cap = cv2.VideoCapture(0)  # Start the video capture

#         # Check if the camera is opened
#         if not video_cap.isOpened():
#             messagebox.showerror("Error", "Could not open video device. Please check your camera connection.")
#             print("Error: Could not open camera.")
#             return

#         print("Camera opened successfully.")

#         # Initialize Dlib's face detector
#         detector = dlib.get_frontal_face_detector()

#         # Load pre-trained LBPH face recognizer
#         clf = cv2.face.LBPHFaceRecognizer_create()
#         clf.read(r"C:\Users\hp\Desktop\Face_Recognition_Proj\Trained_data.xml")

#         frame_skip = 1  # Process every 3rd frame to reduce CPU usage
#         frame_count = 0

#         while True:
#             ret, img = video_cap.read()
#             if not ret:
#                 messagebox.showerror("Error", "Failed to capture image")
#                 print("Failed to capture image.")
#                 break

#             if frame_count % frame_skip == 0:
#                 img = self.recognize_face(img, clf, detector)

#             frame_count += 1

#             cv2.imshow("Face Recognition", img)

#             if cv2.waitKey(1) & 0xFF == 13:  # 13 is the Enter key to break the loop
#                 break

#         video_cap.release()
#         cv2.destroyAllWindows()

#     def recognize_face(self, img, clf, detector):
#         gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Detect faces using Dlib
#         faces = detector(gray_image)
        
#         for face in faces:
#             x, y, w, h = (face.left(), face.top(), face.width(), face.height())

#             # If a valid face is detected (non-zero width/height)
#             if w > 0 and h > 0:
#                 img_face = gray_image[y:y + h, x:x + w]
#                 img_face = cv2.resize(img_face, (200, 200))  # Resize for consistency
#                 img_face = img_face / 255.0  # Normalize pixel values

#                 id, predict = clf.predict(img_face)
#                 confidence = int((100 * (1 - predict / 300)))

#                 conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
#                 my_cursor = conn.cursor()

#                 # Fetch student details from the database
#                 my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
#                 n = my_cursor.fetchone()
#                 n = n[0] if n else "Unknown"

#                 my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
#                 r = my_cursor.fetchone()
#                 r = str(r[0]) if r else "Unknown"

#                 my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
#                 d = my_cursor.fetchone()
#                 d = d[0] if d else "Unknown"
                
#                 my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
#                 i = my_cursor.fetchone()
#                 i = i[0] if i else "Unknown"

#                 # Check if face recognition confidence is high enough
#                 if confidence > 77:  # Confidence threshold
#                     # Mark attendance if not already marked today
#                     if i not in self.marked_attendance_today:
#                         self.mark_attendance(i, r, n, d)
#                         self.marked_attendance_today.add(i)  # Prevent re-marking attendance for the same student

#                     # Draw bounding box and student info over the face
#                     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
#                     cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
#                     cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
#                     cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
#                     cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
                
#                 else:
#                     # Handle unrecognized faces
#                     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
#                     cv2.putText(img, "Unknown", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)

#         return img

    
    
    
    
    # def mark_attendance(self, i, r, n, d):
    #     now = datetime.now()
    #     current_date = now.strftime("%d/%m/%Y")
    #     current_hour = now.hour
    #     current_minute = now.minute

    #     print(f"Current time: {now.strftime('%H:%M')}")  # Debug print

    #     # Check for valid student data before proceeding
    #     if i == "Unknown" or r == "Unknown" or n == "Unknown" or d == "Unknown":
    #         print("Invalid student data. Attendance not recorded.")
    #         return  # Exit if any student data is unknown

    #     # Determine which CSV file to use based on the time
    #     if (current_hour == 10 and current_minute >= 0) or (current_hour < 12) or (current_hour == 12 and current_minute <= 15):
    #         file_name = "morning.csv"
    #     elif (current_hour == 12 and current_minute > 15) or (current_hour < 15):
    #         file_name = "afternoon.csv"
    #     elif (current_hour == 15 and current_minute >= 0) or (current_hour < 17) or (current_hour == 17 and current_minute <= 15):
    #         file_name = "evening.csv"
    #     else:
    #         with open("temp21_invalid.csv", "a", newline="\n") as f:
    #             dl = now.strftime("%d/%m/%Y")
    #             dtString = now.strftime("%H:%M:%S")
    #             f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Invalid Time")
    #         print("Attendance marking is not available at this time.")
    #         return  # Exit if invalid time

    #     # Check if student is already marked present today in any of the attendance files
    #     attendance_marked = False
    #     for attendance_file in ["morning.csv", "afternoon.csv", "evening.csv","temp21_invalid.csv"]:
    #         if os.path.exists(attendance_file):
    #             with open(attendance_file, "r") as f:
    #                 myDataList = f.readlines()
    #                 for line in myDataList:
    #                     entry = line.split(",")
    #                     if entry[0] == str(i) and entry[5] == current_date:  # Check date and student ID
    #                         attendance_marked = True
    #                         break
    #         if attendance_marked:
    #             break

    #     if attendance_marked:
    #         print("Attendance already marked for today.")
    #         return  # Exit if already marked present today

    #     # Mark attendance in the corresponding file
    #     with open(file_name, "a", newline="\n") as f:
    #         dl = now.strftime("%d/%m/%Y")
    #         dtString = now.strftime("%H:%M:%S")
    #         f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Present")
    #         print("Attendance marked successfully.")


    # def face_Recog(self):
    #     marked_attendance_today = set()
    #     def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    #         gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
    #         coord = []

    #         for (x, y, w, h) in features:
    #             img_face = gray_image[y:y + h, x:x + w]
    #             img_face = cv2.resize(img_face, (200, 200))  # Resize for consistency
    #             img_face = img_face / 255.0  # Normalize pixel values

    #             id, predict = clf.predict(img_face)
    #             confidence = int((100 * (1 - predict / 300)))

    #             conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
    #             my_cursor = conn.cursor()

    #             my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
    #             n = my_cursor.fetchone()
    #             n = n[0] if n else "Unknown"  # Get the first element and handle None

    #             my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
    #             r = my_cursor.fetchone()
    #             r = str(r[0]) if r else "Unknown"  # Convert to string and handle None

    #             my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
    #             d = my_cursor.fetchone()
    #             d = d[0] if d else "Unknown"  # Get the first element and handle None
                
    #             my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
    #             i = my_cursor.fetchone()
    #             i = i[0] if i else "Unknown"  # Get the first element and handle None

    #             if confidence > 77:  # Set confidence threshold
    #                 cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 self.mark_attendance(i, r, n, d)
                    
    #                 if i not in marked_attendance_today:
    #                     self.mark_attendance(i, r, n, d)
    #                     marked_attendance_today.add(i)  # Add ID to set to prevent future marks

    #             else:
    #                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #                 cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

    #             coord = [x, y, w, h]
    #         return coord 

    #     def recognize(img, clf, faceCascade):
    #         coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
    #         return img

    #     faceCascade = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\Face_Recognition_Proj\haarcascade_frontalface_default.xml")
    #     clf = cv2.face.LBPHFaceRecognizer_create()
    #     clf.read(r"C:\Users\hp\Desktop\Face_Recognition_Proj\classifier.xml")

    #     video_cap = cv2.VideoCapture(0)

    #     if not video_cap.isOpened():
    #         messagebox.showerror("Error", "Could not open video device")
    #         return

    #     while True:
    #         ret, img = video_cap.read()
    #         if not ret:
    #             messagebox.showerror("Error", "Failed to capture image")
    #             break

    #         img = recognize(img, clf, faceCascade)
    #         cv2.imshow("Welcome to Face Recognition", img)

    #         if cv2.waitKey(1) & 0xFF == 13:  # 13 is the Enter key
    #             break

    #     video_cap.release()
    #     cv2.destroyAllWindows()
    
    # def mark_attendance(self, i, r, n, d):
    #     now = datetime.now()
    #     current_date = now.strftime("%d/%m/%Y")
    #     current_hour = now.hour
    #     current_minute = now.minute

    #     print(f"Current time: {now.strftime('%H:%M')}")  # Debug print

    #     # Check for valid student data before proceeding
    #     if i == "Unknown" or r == "Unknown" or n == "Unknown" or d == "Unknown":
    #         print("Invalid student data. Attendance not recorded.")
    #         return  # Exit if any student data is unknown

    #     # Determine which CSV file to use based on the time
    #     if (current_hour == 10 and current_minute >= 0) or (current_hour < 12) or (current_hour == 12 and current_minute <= 15):
    #         file_name = "morning.csv"
    #     elif (current_hour == 12 and current_minute > 15) or (current_hour < 15):
    #         file_name = "afternoon.csv"
    #     elif (current_hour == 15 and current_minute >= 0) or (current_hour < 17) or (current_hour == 17 and current_minute <= 15):
    #         file_name = "evening.csv"
    #     else:
    #         with open("temp21_invalid.csv", "a", newline="\n") as f:
    #             dl = now.strftime("%d/%m/%Y")
    #             dtString = now.strftime("%H:%M:%S")
    #             f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Invalid Time")
    #         print("Attendance marking is not available at this time.")
    #         return  # Exit if invalid time

    #     # Check if student is already marked present today in any of the attendance files
    #     attendance_marked = False
    #     for attendance_file in ["morning.csv", "afternoon.csv", "evening.csv","temp21_invalid.csv"]:
    #         if os.path.exists(attendance_file):
    #             with open(attendance_file, "r") as f:
    #                 myDataList = f.readlines()
    #                 for line in myDataList:
    #                     entry = line.split(",")
    #                     if entry[0] == str(i) and entry[5] == current_date:  # Check date and student ID
    #                         attendance_marked = True
    #                         break
    #         if attendance_marked:
    #             break

    #     if attendance_marked:
    #         print("Attendance already marked for today.")
    #         return  # Exit if already marked present today

    #     # Mark attendance in the corresponding file
    #     with open(file_name, "a", newline="\n") as f:
    #         dl = now.strftime("%d/%m/%Y")
    #         dtString = now.strftime("%H:%M:%S")
    #         f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Present")
    #         print("Attendance marked successfully.")
       # @staticmethod
    # def calculate_attendance_summary():
    #     attendance_files = ["morning.csv", "afternoon.csv", "evening.csv"]

    #     student_attendance = {}

    #     for file in attendance_files:
    #         if os.path.exists(file):
    #             with open(file, "r") as f:
    #                 reader = csv.reader(f)
    #                 for row in reader:
    #                     if len(row) < 6:  # Ensure enough columns exist
    #                         print(f"Skipping malformed row: {row}")
    #                         continue

    #                     student_id = row[0]
    #                     attendance_status = row[-1].strip()

    #                     if attendance_status == "Present":
    #                         if student_id not in student_attendance:
    #                             student_attendance[student_id] = 0
    #                         student_attendance[student_id] += 1

    #     summary_data = []

    #     total_lectures = len(attendance_files)

    #     for student_id, attended_lectures in student_attendance.items():
    #         attendance_percentage = (attended_lectures / total_lectures) * 100
    #         summary_data.append({
    #             "Student ID": student_id,
    #             "Total Attended Lectures": attended_lectures,
    #             "Attendance Percentage": f"{attendance_percentage:.2f}%"
    #         })

    #     # Create a DataFrame from the summary data
    #     df = pd.DataFrame(summary_data)

    #     # Specify the path where the file will be saved
    #     output_path = r"C:\Users\hp\Desktop\attendance_summary.xlsx"

    #     # Save the DataFrame to an Excel file, using openpyxl as the engine
    #     df.to_excel(output_path, index=False, engine='openpyxl')

    #     print("Attendance summary saved to 'attendance_summary.xlsx'")

            
            

    # def face_Recog(self):
    #     marked_attendance_today = set()
        
        # def draw_boundary(img, detector, color, text, clf):
        #     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #     # Detect faces using Dlib
        #     faces = detector(gray_image)

        #     coord = []
        #     for face in faces:
        #         x, y, w, h = (face.left(), face.top(), face.width(), face.height())

        #         img_face = gray_image[y:y + h, x:x + w]
        #         img_face = cv2.resize(img_face, (200, 200))  # Resize for consistency
        #         img_face = img_face / 255.0  # Normalize pixel values

        #         id, predict = clf.predict(img_face)
        #         confidence = int((100 * (1 - predict / 300)))

        #         conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
        #         my_cursor = conn.cursor()

        #         my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
        #         n = my_cursor.fetchone()
        #         n = n[0] if n else "Unknown"  # Get the first element and handle None

        #         my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
        #         r = my_cursor.fetchone()
        #         r = str(r[0]) if r else "Unknown"  # Convert to string and handle None

        #         my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
        #         d = my_cursor.fetchone()
        #         d = d[0] if d else "Unknown"  # Get the first element and handle None
                
        #         my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
        #         i = my_cursor.fetchone()
        #         i = i[0] if i else "Unknown"  # Get the first element and handle None

        #         if confidence > 77:  # Set confidence threshold
        #             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        #             cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
        #             cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
        #             cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
        #             cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
        #             self.mark_attendance(i, r, n, d)
                    
        #             if i not in marked_attendance_today:
        #                 self.mark_attendance(i, r, n, d)
        #                 marked_attendance_today.add(i)  # Add ID to set to prevent future marks

        #         else:
        #             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        #             cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

        #         coord = [x, y, w, h]
        #     return coord 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def mark_attendance(self, i, r, n, d):
    #     now = datetime.now()
    #     current_date = now.strftime("%d/%m/%Y")
    #     current_hour = now.hour
    #     current_minute = now.minute
    #     print(f"Current time: {now.strftime('%H:%M')}")  # Debug print

    #     # Check for valid student data before proceeding
    #     if i == "Unknown" or r == "Unknown" or n == "Unknown" or d == "Unknown":
    #         print("Invalid student data. Attendance not recorded.")
    #         return  # Exit if any student data is unknown

    #     # Determine which CSV file to use based on the time
    #     if (current_hour == 10 and current_minute >= 0) or (current_hour < 12) or (current_hour == 12 and current_minute <= 15):
    #         file_name = "morning.csv"
    #     elif (current_hour == 12 and current_minute > 15) or (current_hour < 15):
    #         file_name = "afternoon.csv"
    #     elif (current_hour == 15 and current_minute >= 0) or (current_hour < 17) or (current_hour == 17 and current_minute <= 15):
    #         file_name = "evening.csv"
    #     else:
    #         with open("temp21_invalid.csv", "a", newline="\n") as f:
    #             dl = now.strftime("%d/%m/%Y")
    #             dtString = now.strftime("%H:%M:%S")
    #             f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Invalid Time")
    #         print("Attendance marking is not available at this time.")
    #         return  # Exit if invalid time

    #     # Check if student is already marked present today in any of the attendance files
    #     attendance_marked = False
    #     for attendance_file in ["morning.csv", "afternoon.csv", "evening.csv"]:
    #         if os.path.exists(attendance_file):
    #             with open(attendance_file, "r") as f:
    #                 myDataList = f.readlines()
    #                 for line in myDataList:
    #                     entry = line.split(",")
    #                     if entry[0] == str(i) and entry[5] == current_date:  # Check date and student ID
    #                         attendance_marked = True
    #                         break
    #         if attendance_marked:
    #             break

    #     if attendance_marked:
    #         print("Attendance already marked for today.")
    #         return  # Exit if already marked present today

    #     # Mark attendance in the corresponding file
    #     with open(file_name, "a", newline="\n") as f:
    #         dl = now.strftime("%d/%m/%Y")
    #         dtString = now.strftime("%H:%M:%S")
    #         f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Present")
    #         print("Attendance marked successfully.")

    # def face_Recog(self):
    #     import cv2
    #     import dlib

    #     # Initialize dlib's face detector
    #     detector = dlib.get_frontal_face_detector()

    #     # Load the trained model
    #     clf = cv2.face.LBPHFaceRecognizer_create()
    #     clf.read(r"C:\Users\hp\Desktop\Face_Recognition_Proj\classifier.xml")

    #     # Open camera
    #     video_cap = cv2.VideoCapture(0)

    #     if not video_cap.isOpened():
    #         messagebox.showerror("Error", "Could not open video device")
    #         return

    #     # Set the camera resolution (Optional but useful to improve performance)
    #     video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Width of the frame
    #     video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Height of the frame

    #     # Set the window to fullscreen
    #     cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
    #     cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #     while True:
    #         ret, img = video_cap.read()
    #         if not ret:
    #             messagebox.showerror("Error", "Failed to capture image")
    #             break

    #         gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #         # Detect faces using dlib
    #         faces = detector(gray_image)
            
    #         for face in faces:
    #             x, y, w, h = (face.left(), face.top(), face.width(), face.height())  # Get coordinates from dlib
    #             img_face = gray_image[y:y + h, x:x + w]
    #             img_face = cv2.resize(img_face, (200, 200))  # Resize for consistency
    #             img_face = img_face / 255.0  # Normalize pixel values

    #             id, predict = clf.predict(img_face)
    #             confidence = int((100 * (1 - predict / 300)))

    #             # Query database for student info
    #             conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
    #             my_cursor = conn.cursor()

    #             # Query student data from the database
    #             my_cursor.execute("SELECT Name, Roll, Dep, Student_id FROM student WHERE Student_id = %s", (id,))
    #             student_data = my_cursor.fetchone()
    #             if student_data:
    #                 n, r, d, i = student_data
    #             else:
    #                 n = r = d = i = "Unknown"

    #             if confidence > 70:  # Lower confidence threshold to 60
    #                 cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
    #                 cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
    #                 cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
    #                 cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)
    #                 self.mark_attendance(i, r, n, d)
    #             else:
    #                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #                 cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 3)

    #         # Display the frame with the detected face and attendance info
    #         cv2.imshow("Face Recognition", img)

    #         # Exit on pressing Enter
    #         if cv2.waitKey(1) & 0xFF == 13:  # 13 is the Enter key
    #             break

    #     video_cap.release()
    #     cv2.destroyAllWindows()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def mark_attendance(self, i, r, n, d):
    #     now = datetime.now()
    #     current_date = now.strftime("%d/%m/%Y")
    #     current_hour = now.hour
    #     current_minute = now.minute

    #     print(f"Current time: {now.strftime('%H:%M')}")  # Debug print

    #     # Check for valid student data before proceeding
    #     if i == "Unknown" or r == "Unknown" or n == "Unknown" or d == "Unknown":
    #         print("Invalid student data. Attendance not recorded.")
    #         return  # Exit if any student data is unknown

    #     # Determine which CSV file to use based on the time
    #     if (current_hour == 10 and current_minute >= 0) or (current_hour < 12) or (current_hour == 12 and current_minute <= 15):
    #         file_name = "morning.csv"
    #     elif (current_hour == 12 and current_minute > 15) or (current_hour < 15):
    #         file_name = "afternoon.csv"
    #     elif (current_hour == 15 and current_minute >= 0) or (current_hour < 17) or (current_hour == 17 and current_minute <= 15):
    #         file_name = "evening.csv"
    #     else:
    #         with open("temp21_invalid.csv", "a", newline="\n") as f:
    #             dl = now.strftime("%d/%m/%Y")
    #             dtString = now.strftime("%H:%M:%S")
    #             f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Invalid Time")
    #         print("Attendance marking is not available at this time.")
    #         return  # Exit if invalid time

    #     # Check if student is already marked present today in any of the attendance files
    #     attendance_marked = False
    #     for attendance_file in ["morning.csv", "afternoon.csv", "evening.csv"]:
    #         if os.path.exists(attendance_file):
    #             with open(attendance_file, "r") as f:
    #                 myDataList = f.readlines()
    #                 for line in myDataList:
    #                     entry = line.split(",")
    #                     if entry[0] == str(i) and entry[5] == current_date:  # Check date and student ID
    #                         attendance_marked = True
    #                         break
    #         if attendance_marked:
    #             break

    #     if attendance_marked:
    #         print("Attendance already marked for today.")
    #         return  # Exit if already marked present today

    #     # Mark attendance in the corresponding file
    #     with open(file_name, "a", newline="\n") as f:
    #         dl = now.strftime("%d/%m/%Y")
    #         dtString = now.strftime("%H:%M:%S")
    #         f.writelines(f"\n{i},{r},{n},{d},{dtString},{dl},Present")
    #         print("Attendance marked successfully.")

    # def face_Recog(self):
    #     marked_attendance_today = set()

    #     import dlib

    #     # Use dlib's face detector instead of Haar cascade
    #     detector = dlib.get_frontal_face_detector()

    #     def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    #         gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         faces = detector(gray_image)  # Use dlib for face detection

    #         coord = []
    #         for face in faces:
    #             x, y, w, h = (face.left(), face.top(), face.width(), face.height())  # Get coordinates from dlib

    #             img_face = gray_image[y:y + h, x:x + w]
    #             img_face = cv2.resize(img_face, (200, 200))  # Resize for consistency
    #             img_face = img_face / 255.0  # Normalize pixel values

    #             id, predict = clf.predict(img_face)
    #             confidence = int((100 * (1 - predict / 300)))

    #             conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
    #             my_cursor = conn.cursor()

    #             # Query database for student info
    #             my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
    #             n = my_cursor.fetchone()
    #             n = n[0] if n else "Unknown"  # Get the first element and handle None

    #             my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
    #             r = my_cursor.fetchone()
    #             r = str(r[0]) if r else "Unknown"  # Convert to string and handle None

    #             my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
    #             d = my_cursor.fetchone()
    #             d = d[0] if d else "Unknown"  # Get the first element and handle None
                
    #             my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
    #             i = my_cursor.fetchone()
    #             i = i[0] if i else "Unknown"  # Get the first element and handle None

    #             if confidence > 77:  # Set confidence threshold
    #                 cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 self.mark_attendance(i, r, n, d)
    #             else:
    #                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #                 cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

    #             coord = [x, y, w, h]
    #         return coord

    #     def recognize(img, clf, faceCascade):
    #         coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
    #         return img

    #     faceCascade = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\Face_Recognition_Proj\haarcascade_frontalface_default.xml")
    #     clf = cv2.face.LBPHFaceRecognizer_create()
    #     clf.read(r"C:\Users\hp\Desktop\Face_Recognition_Proj\classifier.xml")

    #     # Open camera
    #     video_cap = cv2.VideoCapture(0)

    #     if not video_cap.isOpened():
    #         messagebox.showerror("Error", "Could not open video device")
    #         return

    #     # Set the camera resolution (Optional but useful to improve performance)
    #     video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Full HD width
    #     video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Full HD height

    #     # Set the window to fullscreen
    #     cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
    #     cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #     while True:
    #         ret, img = video_cap.read()
    #         if not ret:
    #             messagebox.showerror("Error", "Failed to capture image")
    #             break

    #         img = recognize(img, clf, faceCascade)
    #         cv2.imshow("Face Recognition", img)

    #         # Exit on pressing Enter
    #         if cv2.waitKey(1) & 0xFF == 13:  # 13 is the Enter key
    #             break

    #     video_cap.release()
    #     cv2.destroyAllWindows()


           
    # def face_Recog(self):
    #     marked_attendance_today = set()  # To track marked attendance for the day

    #     def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    #         gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

    #         coord = []

    #         for (x, y, w, h) in features:
    #             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #             id, predict = clf.predict(gray_image[y:y + h, x:x + w])
    #             confidence = int((100 * (1 - predict / 300)))

    #             conn = mysql.connector.connect(host="localhost", username="root", password="pass123", database="face_recognizer")
    #             my_cursor = conn.cursor()

    #             my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
    #             n = my_cursor.fetchone()
    #             n = n[0] if n else "Unknown"

    #             my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
    #             r = my_cursor.fetchone()
    #             r = str(r[0]) if r else "Unknown"

    #             my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
    #             d = my_cursor.fetchone()
    #             d = d[0] if d else "Unknown"
                
    #             my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
    #             i = my_cursor.fetchone()
    #             i = i[0] if i else "Unknown"

    #             if confidence > 77:
    #                 cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
    #                 cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

    #                 # Mark attendance if not already marked today
    #                 if i not in marked_attendance_today:
    #                     self.mark_attendance(i, r, n, d)
    #                     marked_attendance_today.add(i)  # Add ID to set to prevent future marks

    #             else:
    #                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #                 cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

    #             coord = [x, y, w, h]
    #         return coord

    #     def recognize(img, clf, faceCascade):
    #         coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
    #         return img

    #     faceCascade = cv2.CascadeClassifier(r"C:\Users\hp\Desktop\Face_Recognition_Proj\haarcascade_frontalface_default.xml")
    #     clf = cv2.face.LBPHFaceRecognizer_create()
    #     clf.read(r"C:\Users\hp\Desktop\Face_Recognition_Proj\classifier.xml")

    #     video_cap = cv2.VideoCapture(0)

    #     if not video_cap.isOpened():
    #         messagebox.showerror("Error", "Could not open video device")
    #         return

    #     while True:
    #         ret, img = video_cap.read()
    #         if not ret:
    #             messagebox.showerror("Error", "Failed to capture image")
    #             break

    #         img = recognize(img, clf, faceCascade)
    #         cv2.imshow("Welcome to Face Recognition", img)

    #         if cv2.waitKey(1) & 0xFF == 13:  # 13 is the Enter key
    #             break

    #     video_cap.release()
    #     cv2.destroyAllWindows()


           
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    # obj.start_recognition()  # Call to start recognition
    root.mainloop()




    
# if __name__=="__main__":

#     root=Tk()
#     obj=Face_Recognition(root)
#     root.mainloop()
