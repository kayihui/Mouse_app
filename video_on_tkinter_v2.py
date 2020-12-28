import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import pandas as pd

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Forced Swim Test scoring")
        self.choice = 0
        self.counter = 0
        self.time_dict = {}

        # create the video file name label
        self.video_file_name_label = tkinter.Label(text="Please enter the video filename:")
        self.video_file_name_label.grid(row=0, column=0)

        # create the video file name entry box
        self.video_file_input = tkinter.Entry(width=30)
        self.video_file_input.insert(0, "test.mp4")
        self.video_file_input.grid(row=0, column=1)

        # create a upload button
        self.upload_button = tkinter.Button(text="Upload & start", highlightthickness=0, command=self.upload_video)
        self.upload_button.grid(row=0, column=2)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=960, height=540)
        self.canvas.grid(row=1, column=0, columnspan=3)

        # create the swim button
        self.swim_button = tkinter.Button(text="Swim", highlightthickness=0, command=self.swim_clicked)
        self.swim_button.grid(row=2, column=0)

        # create the float button
        self.float_button = tkinter.Button(text="Float", highlightthickness=0, command=self.float_clicked)
        self.float_button.grid(row=2, column=1)

        # create the current choice label
        self.choice_label = tkinter.Label(text="Your current choice is:")
        self.choice_label.grid(row=3, column=0)

        # create the choice display label
        self.choice_display = tkinter.Label(text=f"{self.choice}")
        self.choice_display.grid(row=3, column=1)

        # create the file name label
        self.file_name_label = tkinter.Label(text="Output data filename:")
        self.file_name_label.grid(row=4, column=0)

        # create the file name entry box
        self.file_name_input = tkinter.Entry(width=30)
        self.file_name_input.insert(0, "animal1")
        self.file_name_input.grid(row=4, column=1)

        # create the stop/save button
        self.save_button = tkinter.Button(text="Save", highlightthickness=0, command=self.save_data)
        self.save_button.grid(row=4, column=2)

        self.window.mainloop()

    def upload_video(self):
        # get the video file
        self.video_source = self.video_file_input.get()
        # open video source, if not and message will be shown on the canvas
        self.vid = MyVideoCapture(self.video_source)
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 40
        self.update()


    def swim_clicked(self):
        self.choice = 1
        self.choice_display.config(text="Swim")
        return self.choice

    def float_clicked(self):
        self.choice = 0
        self.choice_display.config(text="Float")
        return self.choice

    def save_data(self):
        self.file_name = self.file_name_input.get()
        self.data = pd.DataFrame.from_dict(self.time_dict, orient="index", columns=["Swim/Float"])
        self.data.to_csv(f"{self.file_name}.csv", index=True)

    def update(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            self.counter += 1
            self.time_dict[self.counter] = self.choice

        self.window.after(self.delay, self.update)
        return self.time_dict

class MyVideoCapture:
    def __init__(self, video_source):
         # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 self.photo = cv2.resize(frame, (int(self.width/2), int(self.height/2)))
                 self.photo = cv2.cvtColor(self.photo, cv2.COLOR_BGR2RGB)
                 return (ret, self.photo)
            else:
                return ret, None

# Create a window and pass it to the Application object
App(tkinter.Tk())