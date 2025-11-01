import os
from rich.console import Console
from rich.table import Table
from pathlib import Path
from src.streak import commands, __version__

console = Console()
DEFAULT_DATA = Path(__file__).parent.parent.parent / "data.json"
DATA_PATH = Path(os.environ.get("STREAK DATA", str(DEFAULT_DATA)))

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="streak", description="Simple habit tracker")
    parser.add_argument("--version", action="version", version=f"streak {__version__}")
    sub = parser.add_subparsers(dest="command")
    
    add_p = sub.add_parser("add", help="Add a new habit")
    add_p.add_argument("task", type=str)
    
    list_p = sub.add_parser("list", help="List habits.")
    
    done_p = sub.add_parser("done", help="Mark a habit done.")
    done_p.add_argument("id", type=int)
    
    args = parser.parse_args()
    
    if args.command == "add":
        commands.add_habit(args.task, DATA_PATH)
        console.print(f"[green] Added habit:[/] {args.task}")
        
    elif args.command == "list":
        table = Table(title="Your Habits", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Task", justify="left")
        table.add_column("Done", justify="center")
        table.add_column("Streak", justify="center")
        
        data = commands.get_habits(DATA_PATH)
        for item in data:
            id_ = str(item.get("id", ""))
            task = str(item.get("task", ""))
            done_mark = "x" if item.get("done") else " "
            streak = str(item.get("streak", 0))
            table.add_row(id_, task, done_mark, streak)
            
        console.print(table)
           
    elif args.command == "done":
        commands.mark_done(args.id, DATA_PATH)
        console.print("[cyan] Habit marked as done![/]")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()