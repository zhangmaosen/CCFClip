
import chromadb
from langchain_ollama import OllamaEmbeddings

from langchain_chroma import Chroma
from tinydb import TinyDB, Query
import json

def list_workspace(db_name = "workspace"):
    db = TinyDB(f"./work_db/{db_name}.json")
    q = Query()
    return 
def load_workspace(worksapce_name, idx = -1, db_name = "ccfclip"):
    db = TinyDB(f"./work_db/{db_name}.json")
    wk = Query()
    if db.search(wk.wk_name == worksapce_name) == []:
        return {}
    else:
        #print("load workspace {}".format(db.search(wk.wk_name == worksapce_name)[-1]))
        return db.search(wk.wk_name == worksapce_name)[-1]
    
def insert_workspace(json_data, db_name="ccfclip"):
    db = TinyDB(f"./work_db/{db_name}.json")
    wk = Query()
    #print(json_data)
    db.insert(json_data)

def init_chroma_db(db_name):
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)    
    
    chroma_client.get_or_create_collection(db_name)
    chroma_client.delete_collection(db_name)   
def get_chroma_store(db_name, embeddings):
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)    
    
    chroma_client.get_or_create_collection(db_name)
    #collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

    vector_store_from_client = Chroma(
        client=chroma_client,
        collection_name=db_name,
        embedding_function=embeddings,
    )
    return vector_store_from_client
from langchain_experimental.text_splitter import SemanticChunker

def get_chunks(text, embeddings, threshold, sentence_split_regex='\n'):
    print(f"building chunks")
    text_splitter = SemanticChunker(embeddings,sentence_split_regex=sentence_split_regex, breakpoint_threshold_amount=threshold)
    chunks = text_splitter.create_documents([text])
    #print(f"chunks is {chunks}")
    idx = 0
    output_chunks = []
    for chunk in chunks:
        chunk.metadata = {"id": idx}
        idx += 1
        output_chunks.append(chunk)
    return output_chunks

def build_chunks(db_name,text, threshold=70, model="arkohut/gte-qwen2-1.5b-instruct:q8_0"):
    init_chroma_db(db_name)
    embeddings = OllamaEmbeddings(
    model=model,
    )
    #print(f"chunks is {chunks}")
    chunks = get_chunks(text, embeddings, threshold)
    insert_chunks(chunks, embeddings, db_name)
    return chunks
def insert_chunks(chunks, embeddings, db_name):
    
    store = get_chroma_store(db_name, embeddings)
    store.add_documents(chunks)

    return store

def query_chunks(db_name, query, top_k=1, model="arkohut/gte-qwen2-1.5b-instruct:q8_0", ):
    chunks = []
    embeddings = OllamaEmbeddings(
        model = model,
    )
    store = get_chroma_store(db_name, embeddings)
    for q in query.strip().split('\n'):
        print(q)
        chunk = store.similarity_search(q,k=top_k)
        chunk = sorted(chunk, key=lambda x: x.metadata["id"])
        for i in range(len(chunk)):
            print(chunk[i])
            #replace space in page_content to comma
            chunk[i].page_content = chunk[i].page_content.replace(" ",",")
            chunks.append(chunk[i].page_content)
        
        
        output = "\n\n".join(chunks)
        
        yield output