from pathlib import Path
from datetime import datetime

NOTES_DIR = Path("notes")

def setup():
    """Create the notes folder if it doesn't exist."""
    NOTES_DIR.mkdir(exist_ok=True)
    
def create_note(title , content):
    filename = title.strip().lower().replace(" ","_") + ".md"
    filepath = NOTES_DIR / filename
    
    if filepath.exists():
        print(f"  Note '{title}' already exists. Use a different title.")
        return
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    with open(filepath, "w") as f:
        f.write(f"# {title}\n")
        f.write(f"_Created: {timestamp}_\n\n")
        f.write(content)

    print(f"  ✓ Note saved: {filename}")
    
def list_notes():
    setup()
    files = sorted(NOTES_DIR.glob("*.md"))
    
    if not files:
        print("No notes yet")
        return[]
    
    print(f"\n  {'#':<4} {'TITLE':<30} {'LAST MODIFIED'}")
    print("  " + "-" * 55)
    
    for i, f in enumerate(files, 1):
        modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m/%Y %H:%M:%S")
        title = f.stem.replace("_", " ").title()
        print(f"  {i:<4} {title:<30} {modified}")

    print()
    return files

def view_note(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    print("\n" + "=" * 50)
    print(content)
    print("=" * 50)
    
def search_notes(keyword):
    setup()
    keyword = keyword.lower().strip()
    files = list(NOTES_DIR.glob("*.md"))
    found = []
    
    for f in files:
        content = f.read_text().lower()
        if keyword in content:
            found.append(f)
            
    if not found:
        print(f"  No notes found containing '{keyword}'.")
        return
    
    print(f"\n  Found {len(found)} note(s) containing '{keyword}':")
    for i, f in enumerate(found, 1):
        title = f.stem.replace("_", " ").title()
        print(f"    {i}. {title}")
        
def delete_note(filepath):
    title = filepath.stem.replace("_", " ").title()
    confirm = input(f"  Delete '{title}'? (yes/no): ").strip().lower()

    if confirm == "yes":
        filepath.unlink()
        print(f"  ✓ Deleted: {title}")
    else:
        print("  Cancelled.")
        
def get_multiline_input():
    print("  Enter note content (type 'DONE' on a new line to finish):")
    lines = []
    while True:
        line = input("  ")
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    return "\n".join(lines)

def pick_note(prompt):
    """Show note list and let user pick one by number."""
    files = list_notes()
    if not files:
        return None
    while True:
        try:
            choice = int(input(f"  {prompt}: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            print(f"  Enter a number between 1 and {len(files)}.")
        except ValueError:
            print("  Please enter a valid number.")


def menu():
    print("\n  📝 MARKDOWN NOTE-TAKER")
    print("  " + "=" * 25)
    print("  1. Create note")
    print("  2. List notes")
    print("  3. View note")
    print("  4. Search notes")
    print("  5. Delete note")
    print("  6. Exit")


def main():
    setup()
    while True:
        menu()
        choice = input("\n  Choose (1-6): ").strip()

        if choice == "1":
            title   = input("  Note title: ").strip()
            content = get_multiline_input()
            create_note(title, content)

        elif choice == "2":
            list_notes()

        elif choice == "3":
            filepath = pick_note("Pick a note number to view")
            if filepath:
                view_note(filepath)

        elif choice == "4":
            keyword = input("  Search keyword: ").strip()
            search_notes(keyword)

        elif choice == "5":
            filepath = pick_note("Pick a note number to delete")
            if filepath:
                delete_note(filepath)

        elif choice == "6":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  Invalid choice. Enter 1 to 6.")


if __name__ == "__main__":
    main()
    
