from scripts.TypingTestDB import TypingTestDB

if __name__ == "__main__":
    db = TypingTestDB()
    print(db.search(entry_id=1))