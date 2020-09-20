import argparse
import os
import random
import sys
from TypingTestGame import TypingTestDB

class TypingTestCmd:
    def __init__(self):
        self.db = TypingTestDB.TypingTestDB()
        
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Process Typing Test Command Line Arguments")
        parser.add_argument(
            "-v"
            ,"--version"
            ,default=False
            ,action="store_true"
            ,help="Show app version"
            )
        parser.add_argument(
            "-f"
            ,"--file"
            ,default=None
            ,help="New file for statements"
            ,metavar="FILENAME"
            ,type=str
            )
        parser.add_argument(
            "-i"
            ,"--id"
            ,default=None
            ,help="Display statement for particulat id from database"
            ,metavar="ID"
            ,type=int
            )
        parser.add_argument(
            "-d"
            ,"--difficulty"
            ,default=None
            ,help="Choose difficulty level (range 1 to 10)"
            ,metavar="DIFFICULTY"
            ,type=int
            )            
        args_opt = parser.parse_args()
        return args_opt
    
    def get_version(self):
        print("Typing Test App Version: ")
    
    def get_file(self, file_path):
        if not os.path.isfile(file_path):
            print("Cannot open file -", file_path)
            sys.exit(0)
        file_content = open(file_path).read()
        return file_content
    
    def get_db_text_by_id(self, searchID):
        db_text = self.db.search(searchID)
        return db_text

    def set_difficulty_level(self, difficulty_level=random.randint(1,10)):
        if difficulty_level > 10:
            print("Difficulty level should be betwen 1 and 10")
            sys.exit(0)
        
        upper_count = 500 * difficulty_level
        lower_count = upper_count - 500

        random_id = random.randrange(lower_count, upper_count)
        statement = self.db.search(random_id)
        return statement

    def get_text(self):
        args_opt = self.parse_arguments()
        file_content = ""
        if args_opt.version:
            self.get_version()
            sys.exit(0)
        elif args_opt.file:
            file_content = self.get_file(args_opt.file)
        elif args_opt.id:
            file_content = self.get_db_text_by_id(args_opt.id)
        elif args_opt.difficulty:
            file_content = self.set_difficulty_level(args_opt.difficulty)
        else:
            print("Incorrect Arguments. Displaying random text from system.")
            file_content = self.get_db_text_by_id(random.randint(1, 5000))

        return file_content