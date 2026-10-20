from pathlib import Path
import re

class BaseParser:
    @classmethod
    def read_file_content(file_path: str) -> str:
        with open(file_path, 'r') as f:
            content = f.read().strip()
        return content

    @classmethod
    def chunk_file_content(content: str, split_by) -> list:
        if split_by == '.':
            return re.split(r"(?<!\d)\.(?!\d)", content)
        return (content.split(split_by))
    
    @classmethod
    def merge_small_chunks(max_size_chunck, chuncks):
        result = []
        i = 0
        while i < len(chuncks) - 1:
            content = ""
            j = 0
            while i + j < len(chuncks):
                if len(content + chuncks[i + j]) <= max_size_chunck:
                    content += chuncks[i + j]
                    j += 1
                else:
                    break
            i += j
            result.append(content)
        return result
    

class TxtParser:
    def __init__(self, max_chunck_size):
        self.max_chunck_size = max_chunck_size
        self.content: str = ""
        self.valid_chunks: list = []
        self.chunks = []

    def chunk_file_step(self) -> None:
        self.content = BaseParser.read_file_content()
        self.chunks = BaseParser.chunk_file_content('\n\n')

    def merge_chuks_step(self):
        self.chunks = BaseParser.merge_small_chunks(self.max_chunck_size, self.chunks)
    
    def handle_the_large_chunks_step(self):




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
        MarkdownParser(self.max_chunck_size, self.markdown_files)
        PythonParser(self.max_chunck_size, self.python_files)
