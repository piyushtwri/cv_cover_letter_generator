import pandas as pd 
import chromadb
import uuid

class TechStacks:
    def __init__(self, file_path="resource/techstacks.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="techstacks")

    def load_techstacks(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["techstacks"],
                                    metadatas={"projects": row["projects"], "links":row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', ["links"])
    
    def query_projects(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', ["projects"])
