import tkinter as tk
import cv2
import os
from  tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog  
from tkinter import Label, Scale,HORIZONTAL
from alig import function_2,haar
file_path2 = 'Messi.jpg'
class Camera:
    def __init__(self, canvas, width, height):
        self.save_folder = "captured_images"
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        self.count=1
        self.canvas = canvas
        self.width = width
        self.height = height
        self.is_camera_on = False
        self.current_frame = None
        self.cap = cv2.VideoCapture()
    def update_frame(self):
        ret, frame = self.cap.read()
        frame = haar(frame)
        if ret:
            self.current_frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame  = Image.fromarray(self.current_frame )
            self.current_frame  = self.current_frame .resize((self.width, self.height))
            photo = ImageTk.PhotoImage(self.current_frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
        self.canvas.after(10, self.update_frame)
    def toggle_camera(self):
        self.is_camera_on = not self.is_camera_on
        if self.is_camera_on == True:
            self.cap = cv2.VideoCapture(0)
        elif self.is_camera_on == False:
            self.cap.release()
        print(self.is_camera_on)
    def check(self):
        if self.is_camera_on == 0:
            return False
        return True 
    def start(self):
        self.update_frame() 
    def capture(self):
        if self.current_frame is not None:
            img = self.current_frame
            image_path = os.path.join(self.save_folder,  f"image_{self.count}.jpg")
            img.save(image_path)
            self.count +=1
    def restart_folder(self):
        os.makedirs(self.save_folder)
def change_canvas():
    global current_canvas
    # Ẩn canvas hiện tại
    current_canvas.place_forget()

    # Thay đổi giữa canvas1 và canvas2
    if current_canvas == main_canvas:
        current_canvas = camera_canvas
    else:
        current_canvas = main_canvas
        
    current_canvas.place(relx=0.45, rely=0.6, anchor=tk.CENTER)
def open_image2():
    global file_path2
    # Mở hộp thoại để chọn tệp hình ảnh
    file_path2 = filedialog.askopenfilename(initialdir="./", title="Select Image", filetypes=(("Image Files", "*.jpg *.png"),))
    # Kiểm tra xem người dùng đã chọn một tệp hình ảnh hay chưa
    if file_path2:
        image_sourc = Image.open(file_path2)
        image = image_sourc.resize((220, 160))
        photo = ImageTk.PhotoImage(image)
        canvas_img2.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas_img2.image = photo
def button_2():
    if camera.check() == 1:
        combine_command()

    global  file_path2
    img = cv2.imread(file_path2)
    img = function_2(img)
    img = Image.fromarray(img)
    img = img.resize((800,400))
    img = ImageTk.PhotoImage(img)
    # Hiển thị hình ảnh lên Canvas
    main_canvas.create_image(0, 0, anchor=tk.NW, image=img)
    main_canvas.image = img
def combine_command():
    change_canvas()
    camera.toggle_camera()


bg = '#326273'
bt = "#84A7A1"
window = tk.Tk()
window.geometry('1200x800')
window['bg'] = bg



top_image = PhotoImage(file='images/topbar.png')
Label(window,image=top_image,bg=bg).pack()
dock_image = PhotoImage(file='images/icon.png')
dock_image = dock_image.subsample(35, 35)
Label(window,image=dock_image,bg='#32405b').place(relx=0.37,y=10)
heading = Label(window,text='Face detection App',font='arial 18 bold',fg='white',bg='#32405b',)
heading.place(relx=0.42,rely=0.03)
# Tạo một Canvas trong Frame để hiển thị hình ảnh từ camera
main_canvas = tk.Canvas(window, width=800, height=400,border=2,highlightbackground="black")
camera_canvas = tk.Canvas(window, width=630, height=475,border=2,highlightbackground="black")

main_canvas.place(relx=0.45, rely=0.6, anchor=tk.CENTER)
current_canvas = main_canvas
current_canvas.place(relx=0.45, rely=0.6, anchor=tk.CENTER)

camera = Camera(camera_canvas, width=630, height=475)
camera.start()
button_texts = ["Detect",'Capture(space)']
button_commands = [button_2,camera.capture]
# Tạo một Frame để chứa ba nút
frame_buttons = tk.Frame(window,relief=GROOVE)
frame_buttons.place(relx=0.2, y=170, anchor=tk.CENTER)

# Tạo ba nút trong Frame

button_change = tk.Button(window, text='Camera', command=combine_command,
                        bg=bt, fg='#000', font=("Arial", 12), width=12, height=2, bd=5,relief=tk.RAISED)
button_change.place(relx=0.5, rely=0.18, anchor=tk.CENTER)
for text, command in zip(button_texts, button_commands):
    button = tk.Button(frame_buttons, text=text, command=command,bd=5, bg=bt, fg='#000', font=("Arial", 12), width=14, height=2, relief=tk.RAISED)
    button.pack() 
window.bind('<space>', lambda event: camera.capture())
# Tạo một nút để mở hình ảnh
button_open_image2 = tk.Button(window, text="Open Image", command=open_image2,bd=5,
                                bg=bt, fg='#000', font=("Arial", 12), width=10, height=2, relief=tk.RAISED)
button_open_image2.place(relx=0.86 ,  y=170)
background_image = tk.PhotoImage(file="images/user.png")
# Tạo một Canvas để hiển thị hình ảnh (canvas_img1)
canvas_img2 = tk.Canvas(window, width=220, height=160,border=2,highlightbackground="black")
canvas_img2.place(relx=0.8, y=240)
canvas_img2.create_image(0, 0, anchor=tk.NW, image=background_image)


posx_slide = 0.1
posy_slide = 0.18

window.mainloop()

# Giải phóng tài nguyên
camera.cap.release()
cv2.destroyAllWindows()
