# 🎬 Movie Recommendation System (Full Stack)

A full-stack Movie Recommendation System that suggests similar movies using machine learning and real-time movie data from the TMDB API.

---

## 📌 Overview

This project is a production-ready full-stack application that:
- Uses TMDB API for movie data
- Implements content-based / collaborative filtering
- Provides real-time recommendations
- Includes a robust backend with retry mechanisms, SSL fixes, and fallbacks
- Features a modern frontend built with React and Tailwind CSS

---

## 🧠 Tech Stack

### 🔹 Backend
- Python
- FastAPI
- Uvicorn
- Scikit-learn
- Pickle (Model Storage)

### 🔹 Frontend
- React (Vite)
- Tailwind CSS
- Axios

### 🔹 Machine Learning
- Content-Based Filtering
- Cosine Similarity
- Pre-trained similarity matrix

---
### kaggle datasets
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata   

## 🚀 Features

- 🔍 Search for any movie
- 🎯 Get top 5–10 similar recommendations
- ⚡ Fast API response using pre-trained model
- 🔁 Retry & fallback support in backend
- 🎨 Modern UI with responsive design

---

🤖 ML Models

Pre-trained files:

movies.pkl
similarity.pkl
-----
frontend:cd frontend ;npm run dev
backend:cd backend;python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
