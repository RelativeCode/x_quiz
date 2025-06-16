from question_model import Question
from data import fetch_new_questions  # updated import
from quiz_brain import QuizBrain
from ui import QuizInterface

# Factory function to create a fresh QuizBrain with new questions
def create_quiz():
    question_data = fetch_new_questions()  
    question_bank = []
    for question in question_data:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)
    return QuizBrain(question_bank)

# Create the initial quiz and start the UI
quiz = create_quiz()
quiz_ui = QuizInterface(quiz, create_quiz)  # pass factory function to UI