import { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [movie, setMovie] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const searchMovie = async () => {
    if (!movie.trim()) {
      setError('Please enter a movie name');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const res = await axios.post('http://127.0.0.1:8000/recommend', {
        movie: movie.trim(),
      });
      setResults(res.data.recommendations || []);
    } catch (err) {
      setError('No recommendations found or server error. Make sure backend is running.');
      console.error('Recommendation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="netflix-bg min-h-screen text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold mb-12 bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent text-center">
          🎬 Movie Recommender
        </h1>

        <div className="flex gap-4 mb-12">
          <input
            type="text"
            placeholder="Enter a movie name (e.g., Inception)"
            value={movie}
            onChange={(e) => {
              setMovie(e.target.value);
              setError('');
            }}
            className="flex-1 px-6 py-4 bg-gray-800/50 border border-gray-600 rounded-xl text-xl focus:outline-none focus:border-red-500/50 backdrop-blur-sm"
            disabled={loading}
          />
          <button
            onClick={searchMovie}
            disabled={loading}
            className="px-8 py-4 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-xl font-bold rounded-xl transition-all duration-300 shadow-lg hover:shadow-2xl disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Searching...' : 'Recommend'}
          </button>
        </div>

        {error && (
          <div className="bg-red-600/20 border border-red-500/50 p-6 rounded-xl mb-8 backdrop-blur-sm text-red-200 text-center">
            {error}
          </div>
        )}

        {results.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
{results.map((m, index) => (
              <div key={index} className="movie-card text-center">
                {m.poster && (
                  <img 
                    src={m.poster} 
                    alt={m.title || m} 
                    className="poster" 
                  />
                )}
                <h3 className="text-xl font-semibold mb-2 truncate">{m.title || m}</h3>
                {m.trailer && (
                  <a 
                    href={m.trailer} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="trailer-link"
                  >
                    ▶ Watch Trailer
                  </a>
                )}
              </div>
            ))}
          </div>
        )}

        {results.length === 0 && !loading && movie && !error && (
          <p className="text-gray-400 text-center text-lg mt-8">No results yet. Try searching!</p>
        )}
      </div>
    </div>
  );
}

export default App;
