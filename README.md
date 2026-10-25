# Emotion Detector — IBM Watson NLP Final Project

An AI-powered web application that analyzes the emotion of any text using the
IBM Watson NLP **Emotion Prediction** model. It predicts the intensity of
five core emotions — **anger, disgust, fear, joy, and sadness** — identifies
the dominant emotion, and presents the results in a clean, responsive web
interface.

This is the final project for the IBM/Coursera course
*Developing AI Applications with Python and Flask* (worth 16 points).

---

## Features

- Text input area with example sentences for each of the five emotions
- One-click emotion analysis via the Watson NLP service
- Five emotion score cards with animated progress bars
- Clearly highlighted dominant emotion
- Blank-input and whitespace validation with friendly messages
- Backend error handling (service unreachable / unconfigured)
- Loading indicator and accessible keyboard navigation
- Fully responsive, modern blue-and-white theme
- Results are shown **only** after a real response from the backend — never
  fabricated

---

## Technology stack

| Layer       | Technology                                   |
|-------------|----------------------------------------------|
| Backend     | Python 3, Flask                              |
| AI service  | IBM Watson NLP (Emotion Prediction model)    |
| HTTP client | requests                                     |
| Frontend    | HTML5, CSS3, vanilla JavaScript              |
| Testing     | Python `unittest` (with mocks)               |
| Linting     | pylint (PEP 8)                               |

---

## Folder structure

```
oaqjp-final-project-emb-ai/
├── README.md
├── server.py                      # Flask application
├── test_emotion_detection.py      # Unit tests
├── requirements.txt               # Python dependencies
├── .gitignore
├── EmotionDetection/
│   ├── __init__.py                # Makes EmotionDetection a package
│   └── emotion_detection.py       # Watson NLP integration
├── templates/
│   └── index.html                 # Web UI
├── static/
│   ├── styles.css                 # Styling
│   └── script.js                  # Frontend logic (calls Flask backend)
└── evidence/
    └── README.md                  # 16-point grading evidence checklist
```

---

## Installation (Windows)

1. **Open the project folder** — open a terminal (PowerShell or Command
   Prompt) and navigate to the project directory:
   ```powershell
   cd path\to\oaqjp-final-project-emb-ai
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   You should see `(venv)` in your prompt. (On macOS/Linux use
   `source venv/bin/activate`.)

3. **Install requirements**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure the Watson NLP service** — in the course lab, open the
   Watson NLP service instance and copy its **service URL** (the Emotion
   Prediction endpoint). Set it as an environment variable in your terminal
   **before** starting Flask (PowerShell example):
   ```powershell
   set WATSON_NLP_URL=<the Watson NLP service URL from the course lab>
   set WATSON_NLP_API_KEY=<your-api-key>
   ```
   The URL is the one provided by the Skills Network Watson NLP lab (the
   Emotion Prediction model endpoint). If your lab instance does not require
   an API key, leave `WATSON_NLP_API_KEY` unset.
   (On macOS/Linux use `export` instead of `set`.)
   > Never put these values in a committed file. The `.gitignore` excludes
   > `.env` files for safety.

5. **Start Flask**:
   ```powershell
   python server.py
   ```

6. **Test the application in a browser** — open
   <http://localhost:5000>, type or paste text, and press **Analyze Emotion**.

7. **Run unit tests** (see the *Unit testing* section below).

8. **Run pylint** (see the *Static code analysis* section below).

9. **Capture screenshots** — see `evidence/README.md` for the exact
   filenames and what each screenshot must show.

10. **Push to a public GitHub repository** (see *GitHub publication*).

---

## Watson NLP configuration

This project expects **one required environment variable** and one optional
one:

| Variable              | Required | Description                                                |
|-----------------------|----------|------------------------------------------------------------|
| `WATSON_NLP_URL`      | Yes      | Watson NLP Emotion Prediction service URL (from the lab)  |
| `WATSON_NLP_API_KEY`  | No       | API key, only if your Watson NLP instance requires one     |

Both values come from the Watson NLP service instance you use in the course
lab. The module reads them from the environment so no secrets are stored in
the repository.

The function calls the Watson NLP **Emotion Prediction** model with the
`grpc-metadata-mm-model-id` header set to
`emotion_aggregated-workflow_lang_english` and the JSON body documented in the
course lab:

```json
{
  "raw_document": { "text": "<text to analyze>" }
}
```

It parses the real response at
`response["emotionPredictions"][0]["emotion"]` and extracts the five emotion
scores.

---

## Flask startup instructions

```powershell
python server.py
```

The server listens on `http://0.0.0.0:5000` by default. To use a different
port:

```powershell
set PORT=8080
python server.py
```

Routes:

| Route             | Method | Purpose                                  |
|-------------------|--------|------------------------------------------|
| `/`               | GET    | Serves the HTML interface                |
| `/emotionDetector`| GET/POST | Analyzes `textToAnalyze`, returns JSON |

---

## Unit testing instructions

From the project root:

```powershell
python -m unittest -v test_emotion_detection.py
```

The tests mock the outbound HTTP call (`requests.post`) so they run offline.
They cover:

- The five required emotion keys
- The dominant emotion (course example: joy)
- Correct output formatting (exact key set)
- HTTP 400 behavior (all values `None`)
- Request exceptions (network errors)
- Malformed response handling (non-JSON, missing `emotion` node)
- Blank / whitespace input
- Unconfigured service

---

## Pylint instructions

From the project root:

```powershell
pylint server.py
pylint EmotionDetection/emotion_detection.py
pylint test_emotion_detection.py
```

To automatically generate a report file (optional):

```powershell
pylint server.py > pylint_server.txt
```

> The course may require a specific pylint comment or score record in
> `server.py`. If your rubric asks you to paste pylint output into a
> comment block at the top of `server.py`, do so **after** you run pylint
> locally and copy the real output. Do not fabricate the score.

---

## GitHub publication instructions

These steps assume you have created an **empty, public** repository on
GitHub. Replace `<YOUR_GITHUB_USERNAME>` and `<YOUR_REPO_NAME>` with your
actual values.

1. Initialize git and add the remote:
   ```powershell
   git init
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git
   ```

2. Stage and commit the project files (`.gitignore` keeps secrets out):
   ```powershell
   git add .
   git commit -m "Add Emotion Detector final project"
   ```

3. Push to GitHub:
   ```powershell
   git branch -M main
   git push -u origin main
   ```

4. Verify the repository is **public** so graders can see the URLs required
   for evidence points 1 and 6:
   - README.md public URL:
     `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/blob/main/README.md`
   - `EmotionDetection/__init__.py` public URL:
     `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/blob/main/EmotionDetection/__init__.py`

> Replace the placeholder URLs above with your real repository URLs once
> you have published. Do **not** invent a GitHub username.

---

## Demonstration: import and print a result

From the project root:

```powershell
python -c "from EmotionDetection import emotion_detection; print(emotion_detection.emotion_detector('I am so happy and delighted today!'))"
```

This imports the package exactly as the course requires:

```python
from EmotionDetection import emotion_detection
```

> The scores shown will be the **real** Watson NLP scores only if your
> `WATSON_NLP_URL` and `WATSON_NLP_API_KEY` environment variables are set.
> Without them the function returns the blank result (`None` for every
> emotion) — do **not** treat placeholder output as a real analysis.

---

## Submission checklist

- [ ] All mandatory files exist (see folder structure)
- [ ] `emotion_detector()` returns the required dictionary format
- [ ] `EmotionDetection` package imports correctly
- [ ] `python -m unittest -v test_emotion_detection.py` passes
- [ ] Flask runs and serves `http://localhost:5000`
- [ ] Frontend calls the real backend and displays real results
- [ ] HTTP 400 handled (all values `None`)
- [ ] Blank / whitespace input handled in `server.py`
- [ ] pylint reaches the required score
- [ ] Repository is public on GitHub
- [ ] Both required screenshots captured from real execution
- [ ] All 16 grading activities have evidence in `evidence/README.md`
- [ ] No credentials, `.env` files, or personal info committed

See `evidence/README.md` for the full 16-point evidence checklist.