
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    
    try:
        user_answers = session.get("user_answers", {})
        user_answers[current_question_id] = answer
        session["user_answers"] = user_answers
        session.save()
        return True, None
    except Exception as e:
        error_message = f"An error occurred while recording the answer: {str(e)}"
        return False, error_message


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    try:
        questions = PYTHON_QUESTION_LIST[current_question_id]
        
        if current_question_id is None:
            next_question_id = 0
        else:
            next_question_id = current_question_id + 1
        
        if next_question_id < len(questions):
            next_question = questions[next_question_id]
            return next_question, next_question_id
        else:
            return None, None
    except Exception as e:
        error_message = f"An error occurred while getting the next question: {str(e)}"
        return None, None

# Example usage
current_question_id = 0  # Replace with the current question ID
next_question, next_question_id = get_next_question(current_question_id)

if next_question is not None:
    print("Next Question:", next_question)
else:
    print("Quiz Completed!")
def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    try:
        user_answers = session.get("user_answers", {})
        total_questions = len(PYTHON_QUESTION_LIST)
        
        # Calculate user's score based on their answers
        score = calculate_score(user_answers)
        
        # Generate a final response message
        final_response = f"Congratulations! You have completed the quiz. Your score is {score} out of {total_questions}."
        
        return final_response
    except Exception as e:
        error_message = f"An error occurred while generating the final response: {str(e)}"
        return error_message

def calculate_score(user_answers):
    # Assuming you have a list of correct answers and total number of questions
    correct_answers = ["option_a", "option_b", "option_c"]  # Example correct answers
    correct_count = 0
    for question_id, user_answer in user_answers.items():
        if user_answer == correct_answers[question_id]:
            correct_count += 1
    
    return correct_count
