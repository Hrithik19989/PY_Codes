import json
import os
import time
import random 

# Quiz CLI in python
class Question:
    def __init__(self , question , options , answer ):
        self.question = question
        self.answer = answer 
        self.options = options
        
    def display(self , number):
        print(f"\n  Q{number}. {self.question}")
        for i , opt in enumerate(self.options):
            label = chr(65+i)
            print(f"  {label}.{opt}")
            
    def check(self , user_answer):
        mapping = {"1": "A", "2": "B", "3": "C", "4": "D"}
        return mapping.get(user_answer.strip()) == self.answer.upper()
    
QUESTIONS_FILE = 'questions.json'
SCORES_FILE = 'scores.json'

def load_questions(category):
    with open(QUESTIONS_FILE , 'r') as f:
        data = json.load(f)
    questions = data.get(category , [])
    random.shuffle(questions)
    return [Question(q["question"] , q["options"] , q["answer"]) for q in questions]

def load_score():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE , 'r') as f:
        content = f.read().strip()
        return json.loads(content) if content else {}
    
def save_score(category, score, total):
    scores = load_score()
    key = category
    best = scores.get(key , {}).get("score" , -1)
    if score > best:
        scores[key] = {"score":score , "total" : total}
        with open(SCORES_FILE , 'w') as f:
            json.dump(scores ,f , indent =2)
        print(f"  🏆 New best for {category}: {score}/{total}!")
    else:
        print(f"  Best for {category}: {best}/{total}")
        
def get_grade(score , total):
    percent = score/total * 100
    
    if percent == 100:
        return "A+ 🌟"
    elif percent >= 80:
        return "A  🎉"
    elif percent >= 60:
        return "B  👍"
    elif percent >= 50:
        return "C  😐"
    else:
        return "F  😢"
    
TIME_LIMIT = 10

def run_quiz(category):
    questions = load_questions(category)
    if not questions:
        print(f"No questions found for '{category}. ")
        return
    
    
    
    score = 0
    total = len(questions) 
    
    print(f"\n  {'='*45}")
    print(f"  Category: {category}  |  {total} questions  |  {TIME_LIMIT}s per question")
    print(f"  {'='*45}")
    input("\n  Press Enter to start...")
    
    for i, q in enumerate(questions, 1):
        q.display(i)
        print(f"\n  ⏱  You have {TIME_LIMIT} seconds!")

        start = time.time()
        while True:
          answer = input("  Your answer (1/2/3/4): ").strip()
          if answer in ("1", "2", "3", "4"):
              break
          print("  Please enter 1, 2, 3, or 4.")
        
        elapsed = time.time() - start
        
        if elapsed > TIME_LIMIT:
            print(f"  ⌛ Too slow! The answer was {q.answer}.")
        elif q.check(answer):
            print("  ✅ Correct!")
            score += 1
        else:
            print(f"  ❌ Wrong! The answer was {q.answer}.")
        
    grade = get_grade(score, total)
    print(f"\n  {'='*45}")
    print(f"  Score : {score}/{total}")
    print(f"  Grade : {grade}")
    print(f"  {'='*45}\n")
    save_score(category, score, total)
    
    
    
def choose_category():
    with open(QUESTIONS_FILE, "r") as f:
        data = json.load(f)
    categories = list(data.keys())

    print("\n  📚 Available categories:")
    for i, cat in enumerate(categories, 1):
        print(f"    {i}. {cat}")
        
    while True:
        try:
            choice = int(input("\n  Choose a category: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            print(f"  Enter a number between 1 and {len(categories)}.")
        except ValueError:
            print("  Please enter a valid number.")
            

def main():
    print("\n  🧠 QUIZ APP")
    print("  =" * 20)

    while True:
        print("\n  1. Start quiz")
        print("  2. View high scores")
        print("  3. Exit")

        choice = input("\n  Choose (1-3): ").strip()

        if choice == "1":
            category = choose_category()
            run_quiz(category)

        elif choice == "2":
            scores = load_score()
            if not scores:
                print("\n  No scores yet.")
            else:
                print("\n  🏆 High Scores:")
                for cat, data in scores.items():
                    print(f"    {cat}: {data['score']}/{data['total']}")

        elif choice == "3":
            print("\n  Thanks for playing! 👋\n")
            break

        else:
            print("  Invalid choice.")
            
if __name__ == "__main__":
    main()
    

    
    
        
        
         