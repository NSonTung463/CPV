import tkinter as tk
import cv2
from  tkinter import *
import os
from PIL import Image, ImageTk
from tkinter import filedialog  
from tkinter import Label, Scale,HORIZONTAL
from alig import drawKeypoints,drawMatch,convert_img
def get_ord(value):
    global ord_value
    ord_value = int(value)
def get_percentMatch(value):
    global pc_value
    pc_value = float(value)
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
    def start(self):
        self.update_frame() 
    def capture(self):
        if self.current_frame is not None:
            img = self.current_frame
            image_path = os.path.join(self.save_folder,  f"image_{self.count}.jpg")
            img.save(image_path)
            self.count +=1
def two21Image(image1, image2):
# Lấy kích thước của hai hình ảnh
    width1, height1 = image1.size
    width2, height2 = image2.size
    # Tính toán kích thước mới cho tấm ảnh kết quả
    new_width = width1 + width2
    new_height = max(height1, height2)
    # Tạo một tấm ảnh trống mới có kích thước mới
    new_image = Image.new('RGB', (new_width, new_height))
    # Vẽ hai hình ảnh gốc lên tấm ảnh mới
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (width1, 0))
    return new_image
def change_canvas():
    global current_canvas
    # Ẩn canvas hiện tại
    current_canvas.place_forget()

    # Thay đổi giữa canvas1 và canvas2
    if current_canvas == main_canvas:
        current_canvas = camera_canvas
    else:
        current_canvas = main_canvas
        
    current_canvas.place(relx=0.45, rely=0.5, anchor=tk.CENTER)
def open_image1():
    # Mở hộp thoại để chọn tệp hình ảnh
    global file_path1
    file_path1 = filedialog.askopenfilename(initialdir="./", title="Select Image", filetypes=(("Image Files", "*.jpg *.png"),))
    # Kiểm tra xem người dùng đã chọn một tệp hình ảnh hay chưa
    if file_path1:
        image_sourc = Image.open(file_path1)
        image = image_sourc.resize((220, 160))
        photo = ImageTk.PhotoImage(image)
        canvas_img1.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas_img1.image = photo 
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
def show_drawKeypoints():
    global file_path1 , file_path2,ord_value
    im1_display , im2_display = drawKeypoints(cv2.imread(file_path1),cv2.imread(file_path2),ord_value)    
    # Tạo đối tượng PhotoImage từ hình ảnh
    im1_display = Image.fromarray(im1_display)
    im2_display = Image.fromarray(im2_display)
    img = two21Image(im1_display,im2_display)
    img = img.resize((800,400))
    img = ImageTk.PhotoImage(img)
    # Hiển thị hình ảnh lên Canvas
    main_canvas.create_image(0, 0, anchor=tk.NW, image=img)
    main_canvas.image = img
def show_drawMatch():
    global file_path1 , file_path2
    im_matches = drawMatch(cv2.imread(file_path1),cv2.imread(file_path2),ord_value,pc_value)
    im_matches = Image.fromarray(im_matches)
    im_matches = im_matches.resize((800,400))
    im_matches = ImageTk.PhotoImage(im_matches)
    main_canvas.create_image(0, 0, anchor=tk.NW, image=im_matches)
    main_canvas.image = im_matches
def show_convert():
    global file_path1 , file_path2
    img_source , im2_reg = convert_img(cv2.imread(file_path1),cv2.imread(file_path2),ord_value,pc_value)
    # Tạo đối tượng PhotoImage từ hình ảnh
    img_source = Image.fromarray(img_source)
    im2_reg = Image.fromarray(im2_reg)
    img = two21Image(img_source,im2_reg)
    img = img.resize((800,400))
    img = ImageTk.PhotoImage(img)
    # Hiển thị hình ảnh lên Canvas
    main_canvas.create_image(0, 0, anchor=tk.NW, image=img)
    main_canvas.image = img
def combine_command():
    change_canvas()
    camera.toggle_camera()
# image_path = "background.jpg"
# image = Image.open(image_path)
# Chuyển đổi ảnh sang định dạng hỗ trợ bởi Tkinter
bg = '#1F6E8C'
bt = "#84A7A1"
window = tk.Tk()
window.geometry('1200x1000')
window['bg'] = bg

top_image = PhotoImage(file='image/topbar.png')
Label(window,image=top_image,bg=bg).pack()
# Tạo một Canvas trong Frame để hiển thị hình ảnh từ camera
main_canvas = tk.Canvas(window, width=800, height=400)
camera_canvas = tk.Canvas(window, width=630, height=475)
current_canvas = main_canvas
current_canvas.place(relx=0.45, rely=0.5, anchor=tk.CENTER)

camera = Camera(camera_canvas, width=630, height=475)
camera.start()
button_texts = ["Keypoints", "draw Match", "Convert", "Chup"]
button_commands = [show_drawKeypoints, show_drawMatch, show_convert, camera.capture]
# Tạo một Frame để chứa ba nút
frame_buttons = tk.Frame(window)
frame_buttons.pack(side=tk.LEFT, padx=20)

# Tạo ba nút trong Frame
button_change = tk.Button(window, text='Change', command=combine_command,
                        bg=bt, fg='#000', font=("Arial", 12), width=10, height=2, relief=tk.RAISED)
button_change.place(relx=0.5, rely=0.13, anchor=tk.CENTER)
for text, command in zip(button_texts, button_commands):
    button = tk.Button(frame_buttons, text=text, command=command, bg=bt, fg='#000', font=("Arial", 12), width=10, height=2, relief=tk.RAISED)
    button.pack()
window.bind('<space>', lambda event: camera.capture())
# Tạo một nút để mở hình ảnh
button_open_image1 = tk.Button(window, text="Open Image", command=open_image1,
                                bg=bt, fg='#000', font=("Arial", 12), width=10, height=2, relief=tk.RAISED)
button_open_image1.place(x=1020, y=150)

button_open_image2 = tk.Button(window, text="Open Image", command=open_image2,
                                bg=bt, fg='#000', font=("Arial", 12), width=10, height=2, relief=tk.RAISED)
button_open_image2.place(x=1020, y=470)

# Tạo một Canvas để hiển thị hình ảnh (canvas_img1)
canvas_img1 = tk.Canvas(window, width=220, height=160)
canvas_img1.place(x=950, y=200)

canvas_img2 = tk.Canvas(window, width=220, height=160)
canvas_img2.place(x=950, y=520)


posx_slide = 0.1
posy_slide = 0.23

#SLide 1
length_label1 = Label(window, text="ORB",bg=bg).place(relx=posx_slide, rely=posy_slide, anchor=tk.CENTER)
length_input1 = Scale(window, from_=0, to=1000, orient=HORIZONTAL, length= 300,command=get_ord
                    ,tickinterval= 250,resolution=10, bg="#D6D6D6",highlightthickness=-1)
length_input1.set(500)
length_input1.place(relx=posx_slide+0.14, rely=posy_slide, anchor=tk.CENTER)
#SLide 2
length_label2 = Label(window, text="Percent",bg=bg).place(relx=posx_slide-0.01, rely=posy_slide-0.1, anchor=tk.CENTER)
length_input2 = Scale(window, from_=0, to=1,orient=HORIZONTAL, length= 300,command=get_percentMatch
                    ,resolution=0.05,tickinterval=0.25, bg="#D6D6D6",highlightthickness=-1)
length_input2.set(0.2)
length_input2.place(relx=posx_slide+0.14, rely=posy_slide-0.1, anchor=tk.CENTER)

# Khởi chạy vòng lặp chính của ứng dụng
window.mainloop()

# Giải phóng tài nguyên
camera.cap.release()
cv2.destroyAllWindows()
