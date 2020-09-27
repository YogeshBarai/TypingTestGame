try:
    from TypingTestGame import TypingTestAppV2
except:
    import TypingTestAppV2
def main():
    print("Inside main")
    OBJ = TypingTestAppV2.TypingTestAppV2()
    OBJ.run()

if __name__ == "__main__":
    main()