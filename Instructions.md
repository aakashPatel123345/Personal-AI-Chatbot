# Personal AI Chatbot

A step-by-step guide to building a personal AI chatbot with React and Python, starting with a simple proxy chatbot and upgrading to a RAG-powered smart chatbot.

---

## Phase 1: The Simple "Proxy" Chatbot

Your first goal is to have a React app that sends a message to your Python backend, which then forwards it to a free LLM API and streams the response back.

### Step 1: Set up the Python Backend (with FastAPI)

Your Node.js/Express knowledge will make this feel very familiar. FastAPI is the modern Python standard for this.

#### 1.1 Create a Project Folder

Make a new folder for your entire project (e.g., `personal-chatbot`).

#### 1.2 Set up the Backend

Inside that folder, create a `backend` directory.

#### 1.3 Install FastAPI

```bash
pip install fastapi "uvicorn[standard]"
```

#### 1.4 Create Your Server

Make a file named `main.py`. This file will have one job: create one API endpoint (e.g., `/chat`).

#### 1.5 Handle API Keys

Load your LLM API key safely using an environment variable (don't hard-code it).

#### 1.6 Implement the `/chat` Endpoint

This endpoint will:

- Receive a JSON object with a message from your React app.
- Use an LLM client library (like `google-generativeai` for Google's Gemini, or `anthropic` for Claude) to send that message to the free-tier API.
- Return the LLM's response as JSON.

#### 1.7 Enable CORS

This is a crucial step! Your React app (on `localhost:5173`) will be blocked from talking to your Python backend (on `localhost:8000`) unless you allow it. FastAPI has a "CORS middleware" that is very easy to add.

---

### Step 2: Set up the React Frontend (with Vite)

A quick note: The React team no longer recommends `create-react-app`. The new standard is Vite (pronounced "Veet"). It's 10-100x faster and simpler.

#### 2.1 Create the Frontend

In your main project folder, run:

```bash
npm create vite@latest frontend -- --template react
```

This creates a new React project in a `frontend` folder.

```bash
cd frontend
npm install
```

#### 2.2 Build the UI

Open `src/App.jsx`. You only need two core things:

- A list to display messages (an array in your component's state).
- An input form (with a text box and submit button).

#### 2.3 Manage State

Use `useState` to store:

```javascript
const [message, setMessage] = useState(""); // for the input box
const [chatHistory, setChatHistory] = useState([]); // for the list of messages
```

#### 2.4 Handle Form Submit

Create a `handleSubmit` function that:

- Prevents the page from reloading.
- Adds the user's message to the `chatHistory`.
- Uses `fetch` to POST the message to your Python backend's `/chat` endpoint.
- Takes the JSON response from the backend and adds that to the `chatHistory` as well.

**At this point, you have a fully working, extensible chatbot!**

---

## Phase 2: Upgrading to a "Smart" RAG Chatbot

Now you'll add your personal data. The best part? You won't have to touch your React frontend at all. All the changes happen in your Python backend.

### Step 3: Prepare Your Personal Data

1. In your `backend` folder, create a new folder named `data`.
2. Inside `data`, create simple `.md` (Markdown) or `.txt` files:
   - `about_me.md` ("I am a software developer with 5 years of experience...")
   - `projects.md` ("Project A: I built an e-commerce site using React...")
   - `experience.md` ("At Company X, I worked on...")

### Step 4: Install RAG Tools

In your Python environment, you'll install the "glue" that makes RAG work.

```bash
# Install LangChain
pip install langchain

# Install an Embedding Model
# Option 1: OpenAI (excellent and has a generous free tier)
pip install langchain-openai

# Option 2: Free local models
pip install langchain-huggingface

# Install a Vector Database
pip install chromadb
```

**Note:** ChromaDB is perfect because it's free and can run locally in a folder. No separate server needed.

### Step 5: Create a One-Time "Ingestion" Script

Create a new Python file called `ingest.py`.

This script will use LangChain to:

1. **Load:** Read all the `.md` files from your `data` folder.
2. **Split:** Break the text into small, overlapping chunks (e.g., 500 characters each).
3. **Embed:** Use the embedding model to convert each chunk into a vector (a list of numbers).
4. **Store:** Save these vectors inside a ChromaDB database (it will just be a new folder in your backend, e.g., `chroma_db`).

You only need to run this script once (or anytime you update your personal files).

### Step 6: Modify Your Backend `/chat` Endpoint

This is the final, most important step. You'll change your `/chat` endpoint's logic.

#### OLD Logic:
```
(User Message) → LLM API → (Response)
```

#### NEW Logic:

1. **Receive** the message from React.
2. **Embed:** Convert the user's message into a vector (using the same embedding model from Step 5).
3. **Retrieve:** Search your ChromaDB database for the most similar text chunks from your personal data.
4. **Augment:** Create a new, detailed prompt for the LLM:
   ```
   "You are a helpful assistant for [Your Name]. Answer the user's question based only on the following context: [Paste the retrieved text chunks here] Question: [Paste the user's original message here]"
   ```
5. **Generate:** Send this new, augmented prompt to the LLM API.
6. **Return** the final response to your React app.

**Note:** LangChain has tools (like `RetrievalChain`) that can do all of this new logic in just a few lines of code.
