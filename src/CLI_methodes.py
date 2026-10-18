from .indexing import Index

class CLIMethods:
    def index(self, directory: str = "vllm-0.10.1", max_chunck_size=2000):
        if max_chunck_size < 100:
            raise ValueError("the Min chunck size  is 100!!!")
        Index(directory, max_chunck_size)

    def search():
        pass

    def search_dataset():
        pass

    def answer():
        pass

    def answer_dataset():
        pass