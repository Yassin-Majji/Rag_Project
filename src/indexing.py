from pathlib import Path

class TxtParser:
    pass

class MarkdownParser:
    pass

class PythonParser:
    pass

class Index:
    def __init__(self, directory: str, max_chunck_size: int):
        self.directory = Path(directory)
        self.max_chunck_size = max_chunck_size
        self.txt_files: list[str] = []
        self.markdown_files: list[str] = []
        self.python_files: list[str] = []

        self.parse_files()

    def find_files_paths(self, extension: str, file_type: list) -> list[str]:
        for file in self.directory.rglob(extension):
            if file.is_file():
                file_type.append(str(file))
                
        
    def parse_files(self):
        if not self.directory.is_dir():
            raise ValueError(f"{self.directory}: is not a directory")
        self.find_files_paths('*.txt', self.txt_files)
        self.find_files_paths('*.md', self.markdown_files)
        self.find_files_paths('*.py', self.python_files)
        TxtParser(self.max_chunck_size, self.txt_files)
        print("hh")

        MarkdownParser()
        PythonParser()



        