# ---------------------Importing imporrtant libraries --------------------------------------------------------------------
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import os
import numpy as np
import cv2.face
import cv2

# ---------------------------------actual code--------------------------------------------------------------------- 

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="TRAIN DATASET", font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        #bg 
        img2=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\attendance3.jpg")
        # img2=Image.open(r"C:\Users\hp\Desktop\Face_Recognition_Proj\college_images\bg4.jpg")
        img2=img2.resize((1530,710),Image.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        bg_img=Label(self.root,image=self.photoimg2)
        bg_img.place(x=0,y=0,width=1530,height=710)
        
        title_lbl=Label(bg_img,text="FACE RECOGNITION SYSTEM FOR ATTENDANCE",font =("times new roman",35,"bold"),bg="blue",fg="black")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        # Button
        b1_1 = Button(self.root, text="TRAIN All DATA", command=self.train_classifier, cursor="hand2",font=("times new roman", 35, "bold"), bg="blue", fg="black")
        b1_1.place(x=350, y=480, width=600, height=60)
        
        b1_2 = Button(self.root, text="TRAIN DATA", command=self.train_classifier1, cursor="hand2",font=("times new roman", 35, "bold"), bg="blue", fg="black")
        b1_2.place(x=350, y=580, width=600, height=60)

      #..............training the model with photos ..........................
    def train_classifier(self):
        data_dir = "Data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        if not path:
            messagebox.showerror("Error", "No images found in the Data directory.", parent=self.root)
            return

        faces = []
        ids = []

        for image in path:
            try:
                # Open and convert image to grayscale
                img = Image.open(image).convert('L')
                img = img.resize((200, 200))  # Resize to a consistent size
                imageNp = np.array(img, 'uint8')

                # Extract ID from filename (assuming the format "user.<id>.<other_info>.jpg")
                id = int(os.path.split(image)[1].split('.')[1])  # Adjust based on your filename structure
                faces.append(imageNp)
                ids.append(id)

                # Augmentation: No normalization before augmentation
                faces.append(np.fliplr(imageNp))  # Horizontal flip
                faces.append(np.rot90(imageNp))    # 90-degree rotation
                faces.append(np.rot90(imageNp, 2)) # 180-degree rotation
                faces.append(np.rot90(imageNp, 3)) # 270-degree rotation
                ids.extend([id] * 4)  # Duplicate ID for augmented images

                cv2.imshow("Training", imageNp)
                cv2.waitKey(1)
            except Exception as e:
                print(f"Error processing image {image}: {e}")

        if not faces or not ids:
            messagebox.showerror("Error", "No valid faces found for training.", parent=self.root)
            return

        ids = np.array(ids)

        try:
            # Create the LBPH face recognizer
            clf = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
            clf.train(faces, ids)
            clf.write("Trained_data.xml")  # Save the trained classifier
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training dataset completed!!!")
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {e}", parent=self.root)

    def train_classifier1(self):
        data_dir = "Data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        if not path:
            messagebox.showerror("Error", "No images found in the Data directory.", parent=self.root)
            return

        # Load existing classifier (if it exists) and get existing IDs
        clf = cv2.face.LBPHFaceRecognizer_create()
        existing_ids = set()

        # Check if classifier.xml exists and try to load it
        if os.path.exists("Trained_data.xml"):
            try:
                clf.read("Trained_data.xml")
                
                # Extract existing IDs from the trained classifier
                existing_ids = set(clf.getLabels().flatten())
                print(f"Existing IDs: {existing_ids}")

            except cv2.error as e:
                # If reading the classifier failed, inform the user and handle the error
                print(f"Error loading classifier: {e}")
                messagebox.showerror("Error", f"Failed to load existing classifier: {e}", parent=self.root)
                return  # Exit the function if the classifier is corrupt or cannot be loaded

        # Group images by their ID
        images_by_id = {}
        for image in path:
            try:
                # Extract ID from filename
                file_name = os.path.split(image)[1]
                parts = file_name.split('.')
                
                # Check if the filename has the expected number of parts
                if len(parts) >= 2:
                    id = int(parts[1])  # Extract the ID part (second element of the filename)
                    
                    if id not in images_by_id:
                        images_by_id[id] = []
                    images_by_id[id].append(image)
                else:
                    print(f"Skipping image {file_name} due to unexpected filename format")
            except Exception as e:
                print(f"Error processing image {image}: {e}")
        
        faces = []
        ids = []

        # Process all users, skipping only already trained ones
        for id, images in images_by_id.items():
            if id in existing_ids:
                print(f"Skipping all images for ID {id}, already trained.")
                continue  # Skip this ID entirely if it's already trained
            
            for image in images:
                try:
                    # Open and convert image to grayscale
                    img = Image.open(image).convert('L')
                    img = img.resize((200, 200))  # Resize to a consistent size
                    imageNp = np.array(img, 'uint8')

                    faces.append(imageNp)
                    ids.append(id)

                    # Augmentation: No normalization before augmentation
                    faces.append(np.fliplr(imageNp))  # Horizontal flip
                    faces.append(np.rot90(imageNp))    # 90-degree rotation
                    faces.append(np.rot90(imageNp, 2)) # 180-degree rotation
                    faces.append(np.rot90(imageNp, 3)) # 270-degree rotation
                    ids.extend([id] * 4)  # Duplicate ID for augmented images

                except Exception as e:
                    print(f"Error processing image {image}: {e}")

        if not faces or not ids:
            messagebox.showerror("Error", "No valid faces found for training.", parent=self.root)
            return

        ids = np.array(ids)

        try:
            # Create the LBPH face recognizer
            clf = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)

            # Train on the new data (both original and augmented)
            clf.train(faces, ids)
            
            # Save the updated classifier
            clf.write("Trained_data.xml")

            # Clear the display window if it was used
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training dataset completed!!!")
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {e}", parent=self.root)
            
if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
