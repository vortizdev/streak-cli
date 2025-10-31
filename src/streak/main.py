import argparse
from pathlib import Path
from src.streak import commands

DATA_PATH = Path(__file__).parent.parent.parent / "data.json"

def main():
    parser = argparse.ArgumentParser(prog="streak", description="Simple habit tracker")
    sub = parser.add_subparsers(dest="command")
    
    add_p = sub.add_parser("add", help="Add a new habit")
    add_p.add_argument("task", type=str)
    
    list_p = sub.add_parser("list", help="List habits.")
    
    done_p = sub.add_parser("done", help="Mark a habit done.")
    done_p.add_argument("id", type=int)
    
    args = parser.parse_args()
    
    if args.command == "add":
        commands.add_habit(args.task, DATA_PATH)
        print("✅ Added habit:", args.task)
    elif args.command == "list":
        print(commands.list_habits(DATA_PATH))
    elif args.command == "done":
        commands.mark_done(args.id, DATA_PATH)
        print("🎯 Habit marked as done!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()