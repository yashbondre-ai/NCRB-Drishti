import os
import faiss

class FAISSStore():
    def __init__(self,dimesion=384):

        self.store_path = "apps/RAG/vectorstore_data"
        self.index_path = os.path.join(self.store_path, "index.faiss")
        
        self.dimension = dimesion
        self.index = None

        if self.index_exists():
            self.load_index()
        else:
            self.create_index()
        
        
    def create_index(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.save_index()

    def load_index(self):
        self.index = faiss.read_index(self.index_path)

    def save_index(self):
        folder_path = os.path.dirname(self.index_path)
        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            
        faiss.write_index(self.index, self.index_path)

    def get_index(self):
        return self.index

    def index_exists(self):
        return os.path.exists(self.index_path)