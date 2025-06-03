from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface: 

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("x_quiz")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        
        self.canvas = Canvas(width=400, height=300, bg="white")
        
        self.question_text = self.canvas.create_text(
            200, 150,  # Center position
            text="Placeholder", 
            fill=THEME_COLOR, 
            font=("Arial", 18, "italic"), 
            width=360  
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.score_label = Label(text="Score: 0", bg=THEME_COLOR, fg="white", font=("Arial", 12, "bold"))
        self.score_label.grid(row=0, column=1)

        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.image = true_image  # Prevent image from being garbage collected
        self.true_button.grid(row=2, column=0)

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.image = false_image
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)


    def true_pressed(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)
        
    

    def false_pressed(self):
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
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.score_label.config(text=f"Final Score: {self.quiz.score}/{self.quiz.question_number}")