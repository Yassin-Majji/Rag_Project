from pathlib import Path
import re
import sys
from time import sleep


class BaseParser:
    @classmethod
    def read_file_content(cls, file_path: str) -> str:
        with open(file_path, 'r') as f:
            content = f.read().strip()
        return content

    @classmethod
    def chunk_content(cls, content: str, split_by) -> list:
        if split_by == '.':
            return re.split(r"(?<!\d)\.(?!\d)", content)
        return (content.split(split_by))

    @classmethod
    def merge_small_chunks(cls, max_size_chunck, chuncks):
        result = []
        i = 0
        while i < len(chuncks):
            small_chuncks = ""
            large_chuck = ""
            j = 0
            while i + j < len(chuncks):
                if len(small_chuncks + chuncks[i + j]) <= max_size_chunck:
                    small_chuncks += chuncks[i + j]
                    j += 1
                else:
                    large_chuck = chuncks[i + j]
                    j += 1
                    break
            i += j
            if small_chuncks:
                result.append(small_chuncks)
            if  large_chuck:
                    result.append(large_chuck)
        return result

    @classmethod
    def chunk(cls, chunck: str, chuncking_by, max_chunck_size):
        if chuncking_by == ',':
            print("\n\n_______________________________________________________")
            print("chunck is:   ",chunck)
        chuncks = cls.chunk_content(chunck, chuncking_by)
        print("chunks result is:      ",chuncks)
        chuncks = cls.merge_small_chunks(max_chunck_size, chuncks)
        print("chunks result after is:      ",chuncks)
        print("________________________________________________________________________")
        return chuncks

    @classmethod
    def save_chunckings_in_file(cls, chunks):
        with open('result.txt', 'a') as f:
            for ch in chunks:
                f.write(ch)
                f.write('\n\n\n\n')


class TxtParser:
    def __init__(self, max_chunck_size, paths):
        self.paths = paths
        self.max_chunck_size = max_chunck_size
        self.content: str = ""
        self.valid_chunks: list = []
        self.chunks = []
        self.chunck_files()

    def chunck_files(self):
        for p in self.paths:
            self.chunck_file_step(p)
            self.merge_chuks_step()
            self.handle_the_large_chunks_step()
            BaseParser.save_chunckings_in_file(self.valid_chunks)
            print("every things is good~~")

    def chunck_file_step(self, p) -> None:
        self.content = BaseParser.read_file_content(p)
        self.chunks = BaseParser.chunk_content(self.content, '\n\n')

    def merge_chuks_step(self):
        self.chunks = BaseParser.merge_small_chunks(self.max_chunck_size, self.chunks)

    def handle_the_large_chunks_step(self):
        chuncking_by = ['.', ',', ';', '\n', ' ']
        while len(self.chunks):
            chunck = self.chunks.pop(0)
            if len(chunck) <= self.max_chunck_size:
                self.valid_chunks.append(chunck)
                continue
            chuncks = BaseParser.chunk(chunck, chuncking_by[0], self.max_chunck_size)
            for chunck_by in chuncking_by[1:]:
                print(f"chuncks: {chuncks}")
                new_chunks = []
                finished = True
                for ch in chuncks:
                    print(f"ch chosen:     {ch}")
                    print(f"it will spit by:  {chunck_by} {ord(chunck_by)}")
                    if len(ch) > self.max_chunck_size:
                        finished = False
                        return_chunks = BaseParser.chunk(ch, chunck_by, self.max_chunck_size)
                        print(f"the return chunks {return_chunks}")
                        new_chunks += return_chunks
                    else:
                        new_chunks += ch
                print(f"result: {new_chunks}")
                if finished:
                    self.valid_chunks += chuncks
                    break
                chuncks = new_chunks
        print(self.valid_chunks)






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
        # PythonParser(self.max_chunck_size, self.python_files)
        # MarkdownParser(self.max_chunck_size, self.markdown_files)
