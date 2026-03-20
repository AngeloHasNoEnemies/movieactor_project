# Movie-Actor Integration API

IT322 – Integrative Programming | Midterm Performance Task

**Group Members:**
- Luis John Tapdasan
- Levi Lumagbas
- Paul Angelo Burlat

---

## What This Project Does

This project integrates two public APIs — TMDB and TVmaze — and combines their data into a single unified JSON response. You send one request with a movie title and get back movie details and related actors all in one place.

The data is also transformed before being returned:
- Budget is formatted from a raw number to a readable string (e.g. `$160,000,000`)
- Runtime is converted from minutes to hours and minutes (e.g. `2h 28m`)
- Popularity score is converted to a label (e.g. `Blockbuster`)
- Only the necessary fields are returned — no clutter

---

## APIs Used

- **TMDB** – provides movie details like genre, budget, runtime, and ratings. Free API key required at [themoviedb.org](https://www.themoviedb.org/settings/api)
- **TVmaze** – provides actor/people search. No API key needed.

---

## Requirements

- Python 3.11+
- Django 4.2
- Django REST Framework
- drf-yasg
- requests

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/movieactor-api.git
cd movieactor-api
```

**2. Install dependencies**
```bash
python -m pip install -r requirements.txt
```

**3. Add your TMDB API key**

Open `api/views.py` and replace:
```python
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"
```
with your actual key from [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Start the server**
```bash
python manage.py runserver
```

**5. Visit**
```bash
http://127.0.0.1:8000/swagger/
```

---

## Endpoint

```
GET /api/v1/movie-summary/?title={movie_title}
```

**Example:**
```
http://localhost:8000/api/v1/movie-summary/?title=Inception
```

**Example Response:**
```json
{
  "meta": {
    "api_version": "v1",
    "sources": ["TMDB Movie API", "TVmaze People API"]
  },
  "movie": {
    "title": "Inception",
    "release_date": "2010-07-16",
    "genres": ["Action", "Science Fiction"],
    "runtime": "2h 28m",
    "budget": "$160,000,000",
    "vote_average": 8.4,
    "popularity_label": "Blockbuster"
  },
  "related_actors": [
    {
      "name": "Leonardo DiCaprio",
      "birthday": "1974-11-11",
      "country": "United States"
    }
  ],
  "quick_facts": "'Inception' is a Action, Science Fiction film released on 2010-07-16 with a rating of 8.4/10 and is classified as 'Blockbuster'."
}
```

---

## Error Responses

| Status | Reason |
|--------|--------|
| 400 | Missing or empty `title` parameter |
| 404 | No movie found matching the title |
| 502 | TMDB API could not be reached |
| 503 | TMDB API request timed out |

---

## Swagger Docs

Once the server is running, open:

```
http://localhost:8000/swagger/
```

---

## Running the Tests

```bash
python manage.py test api
```

Expected: 6 tests passing
