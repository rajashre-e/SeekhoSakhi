# SeekhoSakhi
Spoken app for teaching women

# 🗣️ Multilingual Spoken Educational App for Women  

## 📌 Project Overview  
This project is a **spoken, multilingual educational application** designed to help women learn about:  
- **Women’s rights**  
- **Maternity & childcare**  
- **General knowledge tips**  
- **Government schemes & health awareness**  

The app provides **FAQs, educational videos, and daily knowledge tips** in multiple Indian languages. It is designed to be **accessible to low-literacy users** through **speech-based interaction**.  

---

## 🚀 Key Functionalities  

### 🎙️ Multilingual Speech Interaction  
- **Speech-to-Text (STT):** Convert user queries in multiple languages into text.  
- **Text-to-Speech (TTS):** Provide spoken answers in natural voices.  
- **Language Detection:** Auto-detect the language of the user’s query.  

### ❓ FAQ Answering System  
- Searchable FAQ database covering women’s rights, maternity, and childcare.  
- **Semantic search** → understands meaning, not just exact keywords.  
- Example:  
  - “How long is maternity leave?”  
  - “Duration of leave after delivery?”  
  → Both map to the same answer.  

### 📹 Educational Content  
- Short videos, infographics, and guides on women’s health, childcare, and rights.  
- Personalized recommendations based on user interest.  

### 📢 General Knowledge Tips  
- Daily or weekly **spoken tips**:  
  - Legal rights  
  - Health & hygiene  
  - Financial literacy  
  - Childcare practices  

### ♿ Accessibility Features  
- Full **voice navigation** (hands-free, low-literacy friendly).  
- **Offline FAQ support** for areas with poor internet connectivity.  
- Simple UI with icons + audio labels.  

---

## ⚙️ Data Science & AI Requirements  

### 🧠 Natural Language Processing (NLP)  
- **Multilingual NLP models** (IndicNLP, HuggingFace Transformers).  
- Handle **transliteration & spelling variations**.  
- Use **embeddings (sentence-transformers / fastText)** for FAQ retrieval.  

### 🔊 Speech Technologies  
- **Speech-to-Text (ASR):** OpenAI Whisper, Vosk, or Google Speech API.  
- **Text-to-Speech (TTS):** CoquiTTS, Festival, or AWS Polly.  
- **Language Detection:** FastText or langdetect library.  

### 🎯 Recommendation System  
- Simple **content-based recommendation** (keywords & embeddings).  
- Later: **personalized suggestions** based on usage patterns.  

### 🔗 (Optional) Knowledge Graph  
- Connect related concepts like *Maternity → Leave Policy → Schemes → Hospitals*.  
- Helps answer related or follow-up questions.  

---

## 📋 Technical Requirements  

### 📂 Data Sources  
- Government portals (women’s rights, maternity leave policies, child schemes).  
- WHO / UNICEF data on women & child health.  
- NGO resources.  
- Curated FAQs from surveys/interviews.  

### 🛠️ Tools & Frameworks  
- **NLP:** HuggingFace, IndicNLP, spaCy  
- **Speech:** Whisper, Vosk, CoquiTTS  
- **Backend:** Flask / FastAPI  
- **Database:** SQLite / MongoDB  
- **Frontend:** Android (Java/Kotlin) or React Native  

### ☁️ Infrastructure  
- Phase 1: Use cloud APIs (Google/Azure/AWS) for quick prototyping.  
- Phase 2: Move to **open-source offline models** for rural deployments.  

---

## 🏗️ Roadmap  

### ✅ Phase 1: Prototype (MVP)  
- FAQ database (CSV/JSON).  
- Speech-to-Text → FAQ retrieval → Text-to-Speech in **1–2 languages**.  
- Basic Android app UI.  

### 🔜 Phase 2: Expansion  
- Add **multiple Indian languages**.  
- Add video & tip recommendations.  
- Daily knowledge updates.  

### 🎯 Phase 3: Smart Features  
- Personalized recommendations.  
- Knowledge graph for complex queries.  
- Offline mode support.  

---

## 📊 Example Workflow  

flowchart TD
    A[User Speaks] --> B[Speech-to-Text]
    B --> C[Language Detection]
    C --> D[NLP + FAQ Retrieval]
    D --> E[Answer Found]
    D --> F[Recommend Video/Tip]
    E --> G[Text-to-Speech]
    F --> G[Text-to-Speech]
    G --> H[User Hears Response]
