from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import os
import requests
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_KEY = os.getenv('TMDB_API_KEY', '64f81a053777929877835340f5567929')  # TMDB API key, fallback to env var

app = FastAPI(title="Movie Recommendation API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data (absolute paths relative to backend/)
MODEL_PATH = os.path.dirname(__file__)
movies_path = os.path.join(MODEL_PATH, "../models/movies.pkl")
similarity_path = os.path.join(MODEL_PATH, "../models/similarity.pkl")

movies = pickle.load(open(movies_path, 'rb'))
similarity_cache = {}  # Cache for TMDB details
similarity = pickle.load(open(similarity_path, 'rb'))

# 🔁 Retry session (VERY IMPORTANT)
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

class MovieRequest(BaseModel):
    movie: str

def fallback(title):
    return {
        "title": title,
        "poster": None,
        "trailer": "",
        "overview": "No details available (offline mode)",
        "rating": "N/A"
    }

def fetch_movie_details(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

        response = session.get(
            url,
            timeout=10,
            verify=certifi.where()   # 🔒 SSL FIX
        )

        if response.status_code != 200:
            print(f"TMDB search error {response.status_code}")
            return fallback(movie_name)

        data = response.json()

        if not data.get('results'):
            return fallback(movie_name)

        movie = data['results'][0]

        poster_path = movie.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        movie_id = movie.get('id')

        trailer = ""

        if movie_id:
            try:
                video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

                video_response = session.get(
                    video_url,
                    timeout=10,
                    verify=certifi.where()
                )

                if video_response.status_code == 200:
                    video_data = video_response.json()

                    for v in video_data.get('results', []):
                        if v.get('type') == "Trailer" and v.get('site') == "YouTube":
                            trailer = f"https://www.youtube.com/watch?v={v['key']}"
                            break

            except Exception as e:
                print(f"Trailer fetch error for {movie_name}: {e}")

        return {
            "title": movie.get('title', movie_name),
            "poster": poster_url,
            "trailer": trailer,
            "overview": movie.get('overview'),
            "rating": movie.get('vote_average')
        }

    except Exception as e:
        print(f"TMDB request error for {movie_name}: {e}")
        return fallback(movie_name)

def recommend(movie: str):
    movie_lower = movie.lower()
    matches = movies[movies['title'].str.lower() == movie_lower]
    if len(matches) == 0:
        return []
    movie_index = matches.index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    results = []
    cache = similarity_cache  # Shared cache
    for i in movies_list:
        title = movies.iloc[i[0]].title
        if title not in cache:
            cache[title] = fetch_movie_details(title) or {"title": title}
        details = cache[title]
        results.append(details)
    return results

@app.post("/recommend")
def get_recommendations(req: MovieRequest):
    result = recommend(req.movie)
    return {"recommendations": result}

@app.get("/health")
def health_check():
    return {"status": "healthy", "movies_loaded": len(movies)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

