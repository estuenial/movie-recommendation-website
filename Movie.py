import tkinter as tk
from tkinter import ttk
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import random
import itertools

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

TMDB_API_KEY = '18a5d54c15683b7bc03a7fb0f05007ab'  # Replace with your TMDb API key

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stop words and single-character tokens
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    # Lemmatize tokens
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def extract_nouns(text):
    # Tokenize and tag parts of speech
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    # Extract nouns and proper nouns
    nouns = [word for word, pos in tagged if pos.startswith('NN')]
    return nouns

def get_movie_recommendations(description):
    # Extract nouns from description
    nouns = extract_nouns(description)
    # Generate all possible combinations of nouns
    combinations = list(itertools.permutations(nouns))
    random.shuffle(combinations)  # Shuffle the combinations for variety
    for combo in combinations:
        # Construct search query
        query = '+'.join(combo)

        # Fetch movie recommendations from TMDb API
        url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": query
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Limit to 5 recommendations
                return [movie['title'] for movie in data['results'][:5]]
    return ["No recommendations found"]

def get_recommendations():
    description = entry.get()
    recommendations = get_movie_recommendations(description)
    random.shuffle(recommendations)  # Shuffle the recommendations list
    label_result.config(text='\n'.join(recommendations))

# GUI setup
root = tk.Tk()
root.title("Movie Recommendation")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position
window_width = int(screen_width * 0.6)
window_height = int(screen_height * 0.6)
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

# Set geometry
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
root.configure(bg="#f0f0f0")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f0f0f0")
style.configure("TButton", background="#007bff", foreground="white", font=("Arial", 10))
style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
style.map("TButton", background=[('active', '#0056b3')])

# Main Frame
main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Widgets
label_description = ttk.Label(main_frame, text="Enter movie description:", font=("Arial", 12))
label_description.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry = ttk.Entry(main_frame, width=50, font=("Arial", 12))
entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

button_recommend = ttk.Button(main_frame, text="Get Recommendations", command=get_recommendations)
button_recommend.grid(row=2, column=0, padx=10, pady=10, sticky="w")

label_result = ttk.Label(main_frame, text="", font=("Arial", 12), wraplength=window_width-40, justify="left")
label_result.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Adjust weights for resizing
main_frame.columnconfigure(0, weight=1)

root.mainloop()
