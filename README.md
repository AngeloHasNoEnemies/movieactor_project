# 🎬 Movie-Actor Integration API

**IT322 – Integrative Programming | Midterm Performance Task**

A unified REST API that integrates two public APIs — **TMDB (The Movie Database)** and **TVmaze** — to return enriched movie summaries in a single clean JSON response. Instead of calling two separate APIs yourself, you call one endpoint and get everything combined and transformed automatically.

---

## 👥 Group Members

| Name | Role |
|------|------|
| **Luis John Tapdasan** | Project setup, Django configuration, API fetch functions |
| **Levi Lumagbas** | URL routing, Swagger documentation, main view & error handling |
| **Paul Angelo Burlat** | Data transformation logic, automated testing, README |

---

## 📌 What This Project Does

This project demonstrates **API Integration and Data Transformation** by:

1. Accepting a movie title from the user via a query parameter
2. Calling the **TMDB API** to retrieve movie details (title, genres, budget, runtime, rating, popularity)
3. Calling the **TVmaze API** to retrieve related actor/people information
4. **Transforming and merging** the raw data from both APIs into one clean, structured response
5. Returning a single unified JSON response through a versioned REST endpoint

### Data Transformations Applied
- Raw popularity score (float) → human-readable label (`"Blockbuster"`, `"Highly Popular"`, etc.)
- Raw budget integer → formatted string (`160000000` → `"$160,000,000"`)
- Runtime in minutes → hours and minutes format (`148` → `"2h 28m"`)
- Genre objects → name strings only (`[{id: 28, name: "Action"}]` → `["Action"]`)
- Actor results → cleaned and limited to top 5
- Generates a new `quick_facts` summary sentence combining both API sources

---

## 🔗 APIs Used

| API | Purpose | Documentation | Auth |
|-----|---------|---------------|------|
| TMDB (The Movie Database) | Movie details, genres, budget, runtime, ratings | [themoviedb.org/documentation](https://developers.themoviedb.org/3) | Free API key required |
| TVmaze | Actor and people search | [tvmaze.com/api](https://www.tvmaze.com/api) | No key needed — completely free |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Django 4.2**
- **Django REST Framework** — for building the API
- **drf-yasg** — for Swagger / OpenAPI documentation
- **requests** — for calling external APIs

---

## 📁 Project Structure

```
movieactor_project/          ← root folder (GitHub repo)
│
├── manage.py                ← run server, migrations, and tests
├── requirements.txt         ← all required packages
├── README.md                ← this file
│
├── movieactor_project/      ← Django configuration folder
│   ├── __init__.py
│   ├── settings.py          ← installed apps, database, REST framework config
│   ├── urls.py              ← Swagger setup + links to api/urls.py
│   └── wsgi.py              ← server entry point
│
└── api/                     ← main application folder
    ├── __init__.py
    ├── apps.py              ← registers the app with Django
    ├── urls.py              ← defines /api/v1/movie-summary/ route
    ├── views.py             ← core logic: fetch, transform, and respond
    └── tests.py             ← 6 automated tests with mocked API responses
```

---

## ⚙️ Setup and Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/movieactor-api.git
cd movieactor-api
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Get a free TMDB API key

1. Go to [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
2. Create a free account and request an API key (takes about 2 minutes)
3. Open `api/views.py` and replace this line:

```python
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"
```

with your actual key:

```python
TMDB_API_KEY = "your_real_key_here"
```

### Step 4 — Run database migrations

```bash
python manage.py migrate
```

### Step 5 — Start the development server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

---

## 🚀 How to Use the API

### Main Endpoint

```
GET /api/v1/movie-summary/?title={movie_title}
```

### Example Requests

```
GET http://localhost:8000/api/v1/movie-summary/?title=Inception
GET http://localhost:8000/api/v1/movie-summary/?title=Avengers
GET http://localhost:8000/api/v1/movie-summary/?title=The Dark Knight
```

### Example Successful Response

```json
{
  "meta": {
    "api_version": "v1",
    "sources": ["TMDB Movie API", "TVmaze People API"]
  },
  "movie": {
    "title": "Inception",
    "tagline": "Your mind is the scene of the crime.",
    "release_date": "2010-07-16",
    "genres": ["Action", "Science Fiction", "Adventure"],
    "overview": "Cobb, a skilled thief who commits corporate espionage...",
    "runtime": "2h 28m",
    "budget": "$160,000,000",
    "vote_average": 8.4,
    "vote_count": 35000,
    "popularity_score": 125.5,
    "popularity_label": "Blockbuster",
    "original_language": "EN",
    "tmdb_id": 27205
  },
  "related_actors": [
    {
      "name": "Leonardo DiCaprio",
      "birthday": "1974-11-11",
      "country": "United States",
      "gender": "Male",
      "profile_image": "https://..."
    }
  ],
  "quick_facts": "'Inception' is a Action, Science Fiction, Adventure film released on 2010-07-16 with a rating of 8.4/10 and is classified as 'Blockbuster'."
}
```

---

## ❌ Error Handling

The API handles all error scenarios gracefully and returns consistent JSON error responses.

| Status Code | Meaning | When It Happens |
|-------------|---------|-----------------|
| `400 Bad Request` | Missing or invalid title | No `?title=` param, or title is empty |
| `404 Not Found` | Movie not found | No movie matches the search title |
| `502 Bad Gateway` | TMDB API failure | TMDB is down or API key is wrong |
| `503 Service Unavailable` | TMDB API timeout | TMDB took too long to respond |

### Example Error Response

```json
{
  "error": "Not Found",
  "message": "No movie found matching 'xyzabc999'. Try a different title."
}
```

---

## 📄 API Documentation (Swagger)

Once the server is running, visit:

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

These pages show all available endpoints, query parameters, and example responses interactively.

---

## 🧪 Running the Tests

```bash
python manage.py test api
```

The test suite includes 6 automated tests using mocked API responses (no internet connection or real API key needed to run tests):

| Test | What It Checks |
|------|---------------|
| `test_successful_response` | Valid request returns 200 with correct structure and transformed fields |
| `test_missing_title_returns_400` | Missing `?title=` returns 400 Bad Request |
| `test_empty_title_returns_400` | Empty `?title=` returns 400 Bad Request |
| `test_movie_not_found_returns_404` | Unknown movie title returns 404 Not Found |
| `test_external_api_failure_returns_502` | TMDB connection error returns 502 Bad Gateway |
| `test_popularity_label_transformation` | Low popularity score correctly maps to `"Niche / Classic"` |

Expected output:

```
✅ Test 1 passed: Successful response
✅ Test 2 passed: Missing title returns 400
✅ Test 3 passed: Empty title returns 400
✅ Test 4 passed: Non-existent movie returns 404
✅ Test 5 passed: External API failure returns 502
✅ Test 6 passed: Popularity label transformation correct

Ran 6 tests in 0.XXXs
OK
```

---

## 🔢 API Versioning

The endpoint uses **URI versioning** (`/api/v1/`). A new version (`/api/v2/`) would be introduced when a change would break existing clients, such as:

- Renaming or removing a response field
- Changing a field's data type
- Requiring authentication where v1 was public

Versioning ensures that existing clients continue to work while new improvements are rolled out.

---

*IT322 – Integrative Programming | Midterm Performance Task*
*Submitted by: Luis John Tapdasan, Levi Lumagbas, and Paul Angelo Burlat*
