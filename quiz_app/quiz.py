import json
import os
import time
import random

class Question:
    def __init__(self , question , options , answer ):
        self.question = question
        self.answer = answer 
        self.option = options
        
    def display(self , number):
        print(f"/n Q{number} , {self.question}")
        for i , opt in enumerate(self.options):
            label = chr(65+i)
            print(f"  {label}.{opt}")
            
    def check(self , user_answer):
        return user_answer.upper() == self.answer.upper()
    

    
    
        
        
         