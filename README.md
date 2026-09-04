# 🥗 AI Nutritionist

An AI-powered nutrition analysis platform that combines **Machine Learning**, **Google Gemini**, and **Retrieval-Augmented Generation (RAG)** to help users understand food products, analyze ingredients, predict nutrition grades, and receive evidence-based nutrition guidance.

🌐 **Live Demo:** https://ai-nutritionist-frontend.onrender.com

---

## 🚀 Features

### 🧠 Nutrition Grade Prediction
Analyze food products using nutritional values and predict a health grade from **A to E** using a trained XGBoost model.

### 🔍 Ingredient Analysis
Uses Google Gemini to identify potentially harmful ingredients, explain their purpose, and highlight possible health concerns.

### 💬 AI Nutrition Chatbot
Ask nutrition-related questions and receive context-aware responses generated using RAG and Google Gemini.

### 📚 Retrieval-Augmented Generation (RAG)
Retrieves information from trusted nutrition documents before generating answers, reducing hallucinations and improving response quality.

### 📄 Source Attribution
Displays the documents and knowledge sources used to generate chatbot responses.

---

## 🏗️ System Architecture

```text
                    User
                      │
                      ▼
              React Frontend
                      │
                      ▼
              FastAPI Backend
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
  ML Model        RAG Engine       Gemini AI
      │               │               │
      │               ▼               │
      │            FAISS              │
      │               │               │
      │               ▼               │
      │      WHO / FSSAI Documents    │
      └───────────────┴───────────────┘
                      │
                      ▼
                   Response
```

---

## 🛠️ Tech Stack

### Frontend
- React.js
- JavaScript
- CSS
- Fetch API

### Backend
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning
- XGBoost
- Scikit-Learn
- NumPy
- Pandas

### AI & RAG
- Google Gemini
- Google Embeddings
- FAISS Vector Store
- Prompt Engineering
- Retrieval-Augmented Generation

### Deployment
- Render

---

## 📂 Project Structure

```text
AI_Nutritionist_Project
│
├── frontend
│   ├── src
│   ├── components
│   ├── pages
│   └── services
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── routes
│   │   ├── services
│   │   ├── schemas
│   │   ├── core
│   │   └── main.py
│   │
│   ├── rag
│   │   ├── chain.py
│   │   ├── prompt.py
│   │   ├── llm.py
│   │   └── question_classifier.py
│   │
│   ├── knowledge_base
│   │   ├── retriever.py
│   │   ├── service.py
│   │   └── vector_store
│   │
│   └── ml
│       ├── preprocessing
│       ├── training
│       └── models
│
└── requirements.txt
```

---

## 🤖 Nutrition Analysis Workflow

```text
User Input
     │
     ▼
Data Validation
     │
     ▼
XGBoost Model
     │
     ▼
Nutrition Grade
     │
     ▼
Gemini Ingredient Analysis
     │
     ▼
AI Summary Generation
     │
     ▼
Final Response
```

---

## 💬 Chatbot Workflow

```text
User Question
      │
      ▼
Question Classification
      │
      ▼
Knowledge Base Lookup
      │
      ▼
FAISS Retrieval
      │
      ▼
Context Building
      │
      ▼
Prompt Engineering
      │
      ▼
Google Gemini
      │
      ▼
Answer + Sources
```

---

## 🧠 Machine Learning Pipeline

The nutrition prediction system is built using **XGBoost Classifier** and trained on food nutrition data.

### Input Features

- Energy
- Fat
- Saturated Fat
- Carbohydrates
- Sugar
- Fiber
- Protein
- Salt

### Output

```text
A → Very Healthy
B → Healthy
C → Moderate
D → Less Healthy
E → Unhealthy
```

---

## 📚 RAG Pipeline

### Document Sources

- WHO Nutrition Guidelines
- FSSAI Resources
- Nutrition Research Documents

### RAG Flow

```text
Documents
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
FAISS Index
    │
    ▼
Semantic Search
    │
    ▼
Retrieved Context
    │
    ▼
Gemini Response
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

### Nutrition Prediction

```http
POST /api/v1/predict
```

### AI Nutrition Chat

```http
POST /chat/
```

---

## ⚙️ Environment Variables

Create a `.env` file inside the backend directory:

```env
GEMINI_API_KEY=your_api_key
```

---

## 🖥️ Local Setup

### Clone Repository

```bash
git clone <repository_url>
cd AI_Nutritionist_Project
```

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend will run on:

```text
http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

## 🚀 Deployment

### Frontend
Deployed on Render

### Backend
Deployed on Render

### Live Application

https://ai-nutritionist-frontend.onrender.com

---

## 🎯 Key Learning Outcomes

- Machine Learning Model Deployment
- FastAPI Backend Development
- Retrieval-Augmented Generation (RAG)
- Vector Databases with FAISS
- Prompt Engineering
- Google Gemini Integration
- REST API Development
- Full Stack AI Application Development
- Production Deployment on Render

---

## 🔮 Future Enhancements

- Personalized Diet Recommendations
- User Authentication
- Meal Planning System
- Nutrition Recommendation Engine
- Docker Support
- AWS Deployment
- Advanced Analytics Dashboard
- Scalable Vector Database Integration

---

## 👨‍💻 Author

**Prity kumari and Nishant Kumar**

B.Tech Student  
National Institute of Technology (NIT)

Passionate about AI, Machine Learning, Full-Stack Development, and Generative AI Applications.
