# SeekhoSakhi  
A Voice-Enabled Chatbot for Women’s Safety and Empowerment  

Live Demo: https://seekosakhi.onrender.com  

## Overview  
SeekhoSakhi is a web-based chatbot designed to support women by providing crime predictions, safety information, and access to emergency resources. The application uses voice interaction to make it accessible to users with low literacy or limited reading ability.  

The system predicts crime levels in Indian states using historical data and answers general questions about women’s rights, health, and safety using an external AI service. It also displays key helplines and educational content through a simple interface.  

## Features  

### Crime Prediction  
- Predicts total crimes against women for a given state and year.  
- Uses a trained machine learning model based on NCRB data (2010–2018).  
- Two models implemented: Random Forest Regressor and Linear Regression.  
- Returns prediction result along with safety tips and helpline numbers.  

### Conversational AI  
- Handles general queries about women’s rights, legal protections, health, and government schemes.  
- Powered by OpenRouter API for dynamic, context-aware responses.  

### Voice Interaction  
- Users can speak their queries using the microphone button.  
- Speech-to-text converts voice input to text.  
- Bot responses are read aloud using text-to-speech (Web Speech API).  
- Designed for ease of use without requiring typing or reading.  

### Emergency Helplines  
- Key helpline numbers are always visible in the footer:  
  - Police: 100  
  - Women Helpline: 181  
  - Child Helpline: 1098  

### Educational Carousel  
- Rotating image carousel on the left panel.  
- Images link to resources on:  
  - Women’s safety at workplace  
  - Rural health and safety  
  - Safety measures for women  
  - Women and child helplines  

## Dataset and Model  

- Data source: National Crime Records Bureau (NCRB), 2010–2018.  
- Features include: State/UT, District, Year, Rape, Dowry Deaths, Domestic Violence, Assault, Kidnapping, Cruelty by Husband, and more.  
- Preprocessing steps:  
  - Missing values filled with 0  
  - Duplicates removed  
  - Categorical variables encoded using LabelEncoder  
- Cleaned dataset saved as: `data/womencrimes_cleaned.csv`  
- Aggregated averages for prediction: `data/year_state_crime_averages.csv`  
- Trained model saved as: `models/womencrimes_model.pkl`  
- Training script: `train_womencrimes.py`  

## Technology Stack  

- Frontend: HTML, CSS, JavaScript (ES6+)  
- Backend: Flask (Python)  
- Machine Learning: scikit-learn, pandas, joblib  
- AI Integration: OpenRouter API  
- Speech: Web Speech API (SpeechRecognition and speechSynthesis)  
- Data Storage: CSV files, Pickle (.pkl) for model serialization  

## Project Structure  
SeekhoSakhi/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── models/
│   ├── womencrimes_model.pkl
│   └── state_encoder.pkl
├── data/
│   ├── womencrimes_cleaned.csv
│   └── year_state_crime_averages.csv
├── services/
│   ├── predict_crimes.py
│   ├── openrouter_api.py
│   └── faq_service.py
└── train_womencrimes.py


## How to Run Locally  

1. Clone the repository:  
git clone https://github.com/rajashre-e/SeekhoSakhi.git
cd SeekhoSakhi

2. Install required packages:  
pip install flask pandas scikit-learn joblib python-dotenv requests

3. Set up environment variable:  
Create a `.env` file and add your OpenRouter API key:  
OPENROUTER_API_KEY=your_api_key_here

4. Start the server:  
python app.py

5. Open in browser: http://localhost:5000  

## Deployment  

The application is deployed on Render:  
https://seekosakhi.onrender.com  

## Security and Accessibility  

- No user data is stored.  
- Input validation is applied on all endpoints.  
- Voice-based interaction supports users with low literacy.  
- Interface is responsive and works on both mobile and desktop.  

## Impact  

SeekhoSakhi helps women access critical safety information quickly. By combining data-driven crime prediction with conversational AI and voice support, it serves as a practical tool for awareness and emergency guidance. It can be used by individuals, families, and community workers to promote women’s safety and empowerment.  

## Credits  

- Crime Data: National Crime Records Bureau (NCRB)  
- AI Backend: OpenRouter API  
 
