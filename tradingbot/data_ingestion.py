from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.docstore.document import Document
from tradingbot.helper import load_file
from tqdm import tqdm
import os
import pandas as pd

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASTRADB_API_ENDPOINT = os.getenv("ASTRADB_API_ENDPOINT")
ASTRADB_APPLICATION_TOKEN = os.getenv("ASTRADB_APPLICATION_TOKEN")
ASTRADB_KEYSPACE = os.getenv("ASTRADB_KEYSPACE")
ASTRADB_COLLECTION_NAME = os.getenv("ASTRADB_COLLECTION_NAME")

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def ingestdata(status):
    vstore = AstraDBVectorStore(
            embedding=embedding,
            collection_name=ASTRADB_COLLECTION_NAME,
            api_endpoint=ASTRADB_API_ENDPOINT,
            token=ASTRADB_APPLICATION_TOKEN,
            namespace=ASTRADB_KEYSPACE,
        )
    
    storage=status
    
    if storage==None:
        docs=load_file()
        try:
            docs = [Document(text) for text in tqdm(docs)]
            inserted_ids = vstore.add_documents(docs)
        except Exception as e:
             pass
    else:
        return vstore
    
    return vstore, inserted_ids

if __name__=='__main__':
    vstore,inserted_ids=ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")
            