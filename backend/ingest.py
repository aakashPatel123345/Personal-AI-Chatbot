import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load all .md files from the data folder
data_dir = "./data"
all_docs = []

# Iterate through all .md files in the data directory
print("Loading documents from data folder...")
for filename in sorted(os.listdir(data_dir)):
    if filename.endswith(".md"):
        file_path = os.path.join(data_dir, filename)
        try:
            loader = TextLoader(file_path)
            docs = loader.load()
            all_docs.extend(docs)
            print(f"✅ Loaded: {filename} ({len(docs)} document(s))")
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")

if not all_docs:
    print("⚠️  No documents found! Make sure you have .md files in the ./data folder.")
    exit(1)

print(f"\n📄 Total documents loaded: {len(all_docs)}")

# Configure text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# Configure embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}  # Recommended for BGE
)

# Split documents into chunks
print("\n📝 Splitting documents into chunks...")
split_docs = text_splitter.split_documents(all_docs)
print(f"✅ Split into {len(split_docs)} chunks.")
print(f"\n📋 Example chunk (first 150 chars):\n{split_docs[0].page_content[:150]}...")

# Create embeddings and store in ChromaDB
print("\n🔢 Creating embeddings...")
persist_dir = "./chroma_db"

# If ChromaDB already exists, we'll overwrite it with new data
vector_store = Chroma.from_documents(
    split_docs,
    embeddings,
    persist_directory=persist_dir
)

# Persist the vector store
vector_store.persist()
print(f"\n✅ ChromaDB successfully stored locally at: {persist_dir}")
print(f"📊 Total chunks stored: {len(split_docs)}")