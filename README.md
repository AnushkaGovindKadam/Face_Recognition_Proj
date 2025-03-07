# Face_Recognition_System_for_Attendance_using_Python
 Hello Everyone , this Repository will contain every information and every code related to this project called as Face Recognition System for Student Attendance using Python. 
 In this project I have used only and only one language i.e Python.
 Even the Frontend is also made by using Python library called as "tkinter".

There are also many libraries used in this projects such as : numpy , opencv , pandas , etc 


In the modern educational environment, traditional methods of marking attendance, such as paper-based or manual logging, are becoming increasingly inefficient and prone to errors. With advancements in artificial intelligence (AI) and computer vision, face recognition technology has emerged as a reliable solution to automate attendance systems. This paper presents a Face Recognition-based Attendance System built entirely using Python, which leverages the power of machine learning and image processing to provide an accurate and real-time method of tracking attendance.

The proposed system is designed to identify and verify individuals based on facial features, ensuring that the attendance process is seamless, fast, and accurate. The backend of the system is developed using Python, with crucial libraries like OpenCV, Face_recognition, and NumPy for image processing, facial recognition, and handling the face data. For data storage, the system utilizes Pandas to manage attendance logs and saves them in a CSV file to maintain a record of the students or employees attending the sessions.


The system operates through a webcam or external camera connected to a computer, capturing real-time images of individuals in front of it. These images are then processed by the face-recognition library to detect faces and match them with the pre-stored face data. Each face is encoded using a unique numerical representation, allowing the system to compare the live frame against the previously stored images for accurate identification.

The system initially requires the registration of participants (students, employees, or members) by uploading images to the system. These images are then processed, and facial encodings are stored in the backend. During each subsequent session, the system scans the captured video frames, extracts facial encodings, and matches them against the stored encodings. If a match is found, the system records the person's name along with the timestamp of their attendance.

The attendance records are saved in a CSV file, where each entry consists of the recognized individual’s name and the time of their attendance. The system is designed to efficiently handle large datasets and provides an easy-to-use interface for users.
