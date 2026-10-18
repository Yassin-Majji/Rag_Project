from .CLI_methodes import CLIMethods
from fire import Fire

def main():
    Fire(CLIMethods)
        

if __name__ == '__main__':
    try:
        main()
    except:
        print("hello my freind there is error hhhhh")