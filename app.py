import streamlit as st
import json
from difflib import get_close_matches

# Loading knowledge base from JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Saving knowledge base to JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Finding the best match for the question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)  # 60% accurate
    return matches[0] if matches else None

# Getting the answer for the question
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# Streamlit app
def chat_bot():
    st.title("Mental Health Therapist Chat Bot")

    knowledge_base_path = 'knowledge_base.json'
    knowledge_base:dict = load_knowledge_base(knowledge_base_path)

    
    user_input = st.text_input("You:", "")
    if user_input.lower() == 'quit':
        st.stop()

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        st.text(f'Bot: {answer}')
    else:
        st.text('Bot: I don\'t know the answer. Can you teach me?')
        new_answer = st.text_input('Type the answer or "skip" to skip:', "")
        if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer":new_answer})
                save_knowledge_base(knowledge_base_path, knowledge_base)
                st.text('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
