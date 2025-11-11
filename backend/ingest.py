from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

file_path = "./data/about_me.md"
loader = TextLoader(file_path)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 10
)

embeddings = HuggingFaceEmbeddings (
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True} # Recommended for BGE
)

# This represents the entire document
docs = loader.load()
print(f"Loaded {len(docs)} document chunks.")
print(f"\nFirst 200 characters of the first chunk:\n{docs[0].page_content[:50]}")
print(f"\nMetadata of the first chunk:\n{docs[0].metadata}")
print(f"\nLength of page content is {len(docs[0].page_content)}")


# This is a bunch of document objects split from individual documents based on the chunk size we defined above.
split_docs = text_splitter.split_documents(docs)
print(f"\nSplit into {len(split_docs)} chunks.")
print(f"\nExample chunk:\n{split_docs[0].page_content[:100]}")

# Let's initialize an array to hold all the text from our documents
texts = [doc.page_content for doc in split_docs]
# Embed the text
embeddings_list = embeddings.embed_documents(texts)


# We can print out a few lines to show how the embeddings look like
print(f"Created {len(embeddings_list)} embeddings.")
print(f"Each embedding vector has length {len(embeddings_list[0])}.")

# Now let's store this in our local chroma db
persist_dir = "./chroma_db"
vector_store = Chroma.from_documents(
    split_docs,
    embeddings, 
    persist_directory = persist_dir
)
vector_store.persist()


print("\n✅ ChromaDB successfully stored locally.")