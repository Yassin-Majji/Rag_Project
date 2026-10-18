from pathlib import Path

directory = Path("test.py")
print(directory.is_file())
for file in directory.rglob("*.txt"):
    print(type(file))
