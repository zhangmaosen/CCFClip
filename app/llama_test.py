from typing import List
from llama_index.core.node_parser import SentenceSplitter,SemanticSplitterNodeParser

from llama_index.embeddings.ollama import OllamaEmbedding

ollama_embedding = OllamaEmbedding(
    model_name="arkohut/gte-qwen2-1.5b-instruct:q8_0",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)



# also baseline splitter
base_splitter = SentenceSplitter(chunk_size=512)

from llama_index.core import SimpleDirectoryReader

from llama_index.core import Document

from llama_index.core import VectorStoreIndex

import gradio as gr
from utils.functions import *
from snownlp import SnowNLP
from llama_index.core.schema import (
    BaseNode,
    Document,
    MetadataMode,
    NodeRelationship,
    TextNode,
    TransformComponent,
)
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

llm = Ollama(model="qwen2:7b-instruct", request_timeout=320.0)
Settings.llm = llm
Settings.embed_model = ollama_embedding

g_nodes :List[BaseNode] = []
g_index :VectorStoreIndex = VectorStoreIndex.from_documents([])
g_engine :BaseQueryEngine = g_index.as_retriever
def srt_sentence_splitter(text: str) -> List[str]:
    # Use SnowNLP to split Chinese text into sentences
    # s = text.split('\n')
    # sentences = [x+' ' for x in s if x]
    s = SnowNLP(text)
    sentences = [x+' ' for x in s.sentences if x]
    return sentences
def split(file, threshold):

    splitter = SemanticSplitterNodeParser(
        buffer_size=1, breakpoint_percentile_threshold=threshold, embed_model=ollama_embedding,
        sentence_splitter=srt_sentence_splitter
    )
    
    [length, content, srt] = gen_full_text(file)
    doc = Document(text=content)
    #print(doc)
    g_nodes.extend(splitter.get_nodes_from_documents([doc]))
    #g_nodes.append(nodes)
    print(g_nodes)
    return [len(g_nodes), content, srt]

def index():

    g_index.insert_nodes(g_nodes)


    #srt_index = VectorStoreIndex(nodes)
    return 

def search( query):
    print(query)
    #global g_index
    #g_engine=g_index.as_retriever
    #query_engine = srt_index.as_query_engine()
    result = g_engine.retrieve(query)
    return result

with gr.Blocks() as demo:

    gr.Interface(split, [gr.File(file_types=['srt']), gr.Slider(value=95)],["text","text","text"]) 
    

    
    gr.Interface(index,inputs= None, outputs=["text"])
    gr.Interface(search, [ "text"], ["text"])
demo.launch()