from tkinter import *
from tkinter import messagebox
from quiz_brain import QuizBrain
from PIL import Image, ImageTk

THEME_COLOR = "#0066cc"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain, create_quiz_func):
        self.quiz = quiz_brain
        self.create_quiz_func = create_quiz_func
        self.window = Tk()
        self.window.title("X-Quizz")
        self.window.geometry("800x600")
        self.window.config(bg=THEME_COLOR)

        # ✅ Load and resize logo image
        raw_image = Image.open("images/x-quiz.png")
        resized_image = raw_image.resize((600, 300), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(resized_image)

        # ✅ Start screen frame
        self.start_frame = Frame(self.window, bg=THEME_COLOR)
        self.start_frame.pack(expand=True)

        self.logo_label = Label(self.start_frame, image=self.logo_img, bg=THEME_COLOR)
        self.logo_label.pack(pady=(50, 20))

        # Nickname Entry
        self.name_label = Label(self.start_frame, text="Enter your nickname:", bg=THEME_COLOR, fg="white", font=("Arial", 12))
        self.name_label.pack(pady=(10, 5))

        self.name_entry = Entry(self.start_frame, font=("Arial", 12))
        self.name_entry.pack(pady=(0, 20))


        button_style = {
            "width": 15,
            "bg": "black",
            "fg": THEME_COLOR,
            "font": ("Arial", 12, "bold"),
            "relief": "raised",
            "bd": 2
        }

        self.start_button = Button(
            self.start_frame,
            text="Start Game",
            command=self.start_game,
            **button_style
        )
        self.start_button.pack(side=LEFT, padx=20, pady=10)


        self.scoreboard_button = Button(
            self.start_frame,
            text="Scoreboard",
            command=self.show_scoreboard,
            **button_style
        )
        self.scoreboard_button.pack(side=RIGHT, padx=20, pady=10)

        # ✅ Quiz UI frame (hidden initially)
        self.quiz_frame = Frame(self.window, bg=THEME_COLOR)

        # Inner frame to center content
        self.inner_frame = Frame(self.quiz_frame, bg=THEME_COLOR)
        self.inner_frame.pack(expand=True)

        self.score_label = Label(
            self.inner_frame,
            text="Score: 0",
            bg=THEME_COLOR,
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.score_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)


        # Play Again and View Scoreboard buttons (hidden initially)
        self.play_again_button = Button(
            self.inner_frame,
            text="Play Again",
            command=self.play_again,
            width=15,
            bg="black",
            fg=THEME_COLOR,
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2
        )

        self.view_scoreboard_button = Button(
            self.inner_frame,
            text="View Scoreboard",
            command=self.show_scoreboard,
            width=15,
            bg="black",
            fg=THEME_COLOR,
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2
        )


        # Question number label (right side)
        self.q_number_label = Label(
            self.inner_frame,
            text="Question 1/30",
            bg=THEME_COLOR,
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.q_number_label.grid(row=0, column=1, sticky="e", padx=20, pady=10)

        self.canvas = Canvas(
            self.inner_frame,
            width=560,
            height=300,
            bg="white",
            highlightthickness=0
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)

        self.question_text = self.canvas.create_text(
            280, 150,
            text="",
            fill=THEME_COLOR,
            font=("Arial", 18, "italic"),
            width=500
        )

        self.timer_canvas = Canvas(
            self.inner_frame,
            width=300,
            height=30,
            bg="white",
            highlightthickness=0
        )
        self.timer_canvas.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        self.timer_bar = self.timer_canvas.create_rectangle(0, 0, 300, 30, fill="#fffb00")
        self.timer_text = self.timer_canvas.create_text(150, 15, text="60", fill="black", font=("Arial", 14, "bold"))

        true_img = PhotoImage(file="images/true.png")
        self.true_button = Button(self.inner_frame, image=true_img, highlightthickness=0, command=self.true_pressed)
        self.true_button.image = true_img
        self.true_button.grid(row=3, column=0, pady=10, padx=20)

        false_img = PhotoImage(file="images/false.png")
        self.false_button = Button(self.inner_frame, image=false_img, highlightthickness=0, command=self.false_pressed)
        self.false_button.image = false_img
        self.false_button.grid(row=3, column=1, pady=10, padx=20)

        # ✅ Timer variables
        self.time_left = 60
        self.timer_job = None

        self.window.mainloop()



    def get_next_question(self):
        self.canvas.config(bg="white")

        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

        # Update score and question number labels
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.q_number_label.config(
            text=f"Question {self.quiz.question_number}/{len(self.quiz.question_list)}"
        )

        self.reset_timer()




    def true_pressed(self):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)
        
    

    def false_pressed(self):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)
        
    
    def give_feedback(self, is_right):

        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        
        self.window.after(1000, self.get_next_question)  # Wait for 1 second before showing the next question
        self.score_label.config(text=f"Score: {self.quiz.score}")
        if not self.quiz.still_has_questions():
            self.canvas.itemconfig(self.question_text, text="You've completed the quiz!")
            self.true_button.grid_forget()
            self.false_button.grid_forget()

            self.score_label.config(text=f"Final Score: {self.quiz.score}/{self.quiz.question_number}")

            self.play_again_button.grid(row=3, column=0, pady=10, padx=20)
            self.view_scoreboard_button.grid(row=3, column=1, pady=10, padx=20)


    def start_game(self):
        nickname = self.name_entry.get().strip()
        if not nickname:
            messagebox.showwarning("Missing Name", "Please enter your nickname before starting.")
            return

        self.player_name = nickname  
        self.start_frame.pack_forget()
        self.quiz_frame.pack(expand=True)
        self.get_next_question()






    def show_scoreboard(self):
        print("Scoreboard feature not yet implemented.")
        self.scoreboard_button = Button(
        text="Scoreboard", 
        command=self.show_scoreboard,
        width=15, 
        bg=THEME_COLOR,
        fg="black",
        font=("Arial", 12, "bold"),
        relief="raised",
        bd=2
)
    
    def play_again(self):
        # Create a new quiz with fresh questions
        self.quiz = self.create_quiz_func()

        self.score_label.config(text="Score: 0")
        self.q_number_label.config(text="Question 1/{}".format(len(self.quiz.question_list)))
        self.canvas.config(bg="white")

        self.play_again_button.grid_forget()
        self.view_scoreboard_button.grid_forget()
        self.true_button.grid(row=3, column=0, pady=10, padx=20)
        self.false_button.grid(row=3, column=1, pady=10, padx=20)

        self.get_next_question()



    def reset_timer(self):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
        self.time_left = 20
        self.update_timer()

    def update_timer(self):
        self.timer_canvas.itemconfig(self.timer_text, text=str(self.time_left))
        bar_width = int((self.time_left / 20) * 300)
        self.timer_canvas.coords(self.timer_bar, 0, 0, bar_width, 30)

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_job = self.window.after(1000, self.update_timer)
        else:
            self.time_ran_out()


    def time_ran_out(self):
        self.canvas.config(bg="red")
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)
