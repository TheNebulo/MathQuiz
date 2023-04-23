import random
import json
import os

def generate_question(difficulty):
    difficulties = {
        "Easy": (1, 10),
        "Medium": (1, 20),
        "Hard": (1, 100)
    }
    lower, upper = difficulties[difficulty]
    num1 = random.randint(lower, upper)
    num2 = random.randint(lower, upper)
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '/':
        num1 *= num2
    question = f"{num1} {operation} {num2}"
    return question

def ask_question(question):
    print(f"What is {question}?")
    while True:
        try:
            answer = float(input())
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return answer

def check_answer(question, answer):
    if eval(question) == answer:
        return True
    else:
        return False

def save_results(class_name, student_name, score, difficulty):
    if not os.path.exists('results'):
        os.makedirs('results')
    file_name = os.path.join('results', f'{class_name}.json')
    data = {}
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
    if student_name not in data:
        data[student_name] = []
    data[student_name].append({"score": score, "difficulty": difficulty})
    data[student_name] = data[student_name][-3:]
    with open(file_name, 'w') as file:
        json.dump(data, file)

def print_results(class_name):
    file_name = os.path.join('results', f'{class_name}.json')
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        sorted_data = sorted(data.items(), key=lambda x: (-max([d["score"] for d in x[1]]), x[0]))
        print(f"\nHigh scores for class {class_name}:")
        for student, scores in sorted_data:
            highest_score = max(scores, key=lambda x: x['score'])
            print(f"{student}: {highest_score['score']} ({highest_score['difficulty']})")
    else:
        print(f"No data for class {class_name}.")

def take_test():
    valid_class_names = ['Class A', 'Class B', 'Class C']
    while True:
        class_name = input("Enter class name (Class A, Class B, or Class C): ")
        if class_name in valid_class_names:
            break
        else:
            print("Invalid input. Please enter a valid class name.")
            
    valid_difficulties = ['Easy', 'Medium', 'Hard']
    while True:
        difficulty = input("Enter difficulty (Easy, Medium, or Hard): ")
        if difficulty in valid_difficulties:
            break
        else:
            print("Invalid input. Please enter a valid difficulty.")

    student_name = input("Enter student's name: ")

    score = 0
    for _ in range(10):
        question = generate_question(difficulty)
        answer = ask_question(question)
        if check_answer(question, answer):
            print('Correct.')
            score += 1
        else:
            print('Incorrect.')

    print(f"\n{student_name} got {score} out of 10 on {difficulty} difficulty.")
    save_results(class_name, student_name, score, difficulty)
    print("Last 3 Scores (sorted by best score and difficulty level):")
    print_results(class_name)

def view_high_scores():
    for class_name in ['Class A', 'Class B', 'Class C']:
        print_results(class_name)

def teacher_menu():
    valid_class_names = ['Class A', 'Class B', 'Class C']
    while True:
        class_name = input("Enter class name (Class A, Class B, or Class C) or 'Q' to exit: ")
        if class_name in valid_class_names:
            print_results(class_name)
        elif class_name.lower() == 'q':
            break
        else:
            print("Invalid input. Please enter a valid class name or 'Q' to exit.")

def main():
    while True:
        print("\nMain Menu:")
        print("1. Take the Test")
        print("2. View High Scores")
        print("3. Teacher Menu")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            take_test()
        elif choice == '2':
            view_high_scores()
        elif choice == '3':
            teacher_menu()
        elif choice == '4':
            break
        else:
            print("Invalid input. Please choose a valid option from the main menu.")

if __name__ == '__main__':
    main()