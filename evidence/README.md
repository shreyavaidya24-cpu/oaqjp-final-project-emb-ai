# Evidence Checklist — 16 Grading Points

This checklist maps each of the 16 grading points to the file, command, or
screenshot that provides the evidence. **Do not fabricate any evidence.**
Every item below must be produced from a real execution of the project on
your machine, then added to your repository or submission.

Status below reflects the code inspection and execution checks actually run
during this audit. Mocked unit tests do not verify live Watson NLP connectivity.
Any environment-dependent or live-service check must be run on your computer
and supported by real output.

---

## 1. Public GitHub URL of `README.md` — 1 point

- **Required:** Public GitHub URL of `README.md`.
- **Status:** NOT RUN (depends on your GitHub push).
- **What to do:** Push to a public repo, then paste:
  `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/blob/main/README.md`
- README.md is present, has the project title, description, features, stack,
  folder structure, install steps, Watson NLP config, Flask instructions,
  unit-test instructions, pylint instructions, and GitHub publishing steps.

## 2. Emotion detection function code — 1 point

- **Required:** `emotion_detector(text_to_analyze)` implementation.
- **File:** `EmotionDetection/emotion_detection.py`
- **Status:** PASS (inspected; uses the Watson NLP Emotion Prediction model
  with the `grpc-metadata-mm-model-id` header, `raw_document` payload, and
  `emotionPredictions[0].emotion` response path).
- **Remaining:** Run a real request against the live Watson NLP service to
  confirm real scores are returned (requires `WATSON_NLP_URL` from the lab).

## 3. Terminal output showing successful import and test — 1 point

- **Required:** Terminal output of importing and calling the function.
- **Command (run from project root):**
  ```powershell
  python -c "from EmotionDetection import emotion_detection; print(emotion_detection.emotion_detector('I am so happy and delighted today!'))"
  ```
- **Status:** PASS for package import with installed `requests`; live Watson analysis NOT RUN because no course service URL is configured.
- **Remaining:** Run with `WATSON_NLP_URL` set; paste the real output. Without
  the URL the function returns all `None` — label that clearly, do not present
  it as a real analysis.

## 4. Correct output formatting implementation — 1 point

- **Required:** The function returns the dict with `anger`, `disgust`,
  `fear`, `joy`, `sadness`, and `dominant_emotion`.
- **File:** `EmotionDetection/emotion_detection.py`
- **Status:** PASS (inspected; the success path builds exactly these six keys;
  HTTP 400 and error paths return all-`None`).

## 5. Terminal output validating output format — 1 point

- **Required:** Terminal output showing the key set.
- **Command:**
  ```powershell
  python -c "from EmotionDetection import emotion_detection; r = emotion_detection.emotion_detector('I am so happy and delighted today!'); print(sorted(r.keys()))"
  ```
- **Expected (with Watson URL set):**
  ```
  ['anger', 'disgust', 'dominant_emotion', 'fear', 'joy', 'sadness']
  ```
- **Status:** PASS for output-key structure in mocked unit tests; live output NOT RUN because no course service URL is configured.

## 6. Public GitHub URL of `EmotionDetection/__init__.py` — 1 point

- **Required:** Public GitHub URL.
- **Status:** NOT RUN (depends on your GitHub push).
- **What to do:** After pushing, paste:
  `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>/blob/main/EmotionDetection/__init__.py`
- The file is present and exposes `emotion_detector` so
  `from EmotionDetection import emotion_detection` works.

## 7. Terminal output validating `EmotionDetection` package — 1 point

- **Required:** Terminal output proving the package imports.
- **Command:**
  ```powershell
  python -c "from EmotionDetection import emotion_detection; print('package import OK')"
  ```
- **Expected:**
  ```
  package import OK
  ```
- **Status:** PASS — the package import was validated during this audit.

## 8. Unit test source code — 1 point

- **Required:** The `unittest` source file.
- **File:** `test_emotion_detection.py`
- **Status:** PASS (inspected; imports the real `emotion_detector`, mocks
  `requests.post` with the Watson NLP `emotionPredictions` response shape,
  covers all five keys, dominant emotion, output format, HTTP 400, request
  exceptions, malformed JSON, missing emotion node, missing emotion key,
  blank input, and unconfigured service).

## 9. Terminal output showing all unit tests passed — 1 point

- **Required:** Terminal output showing all tests pass.
- **Command:**
  ```powershell
  python -m unittest -v test_emotion_detection.py
  ```
- **Status:** PASS — 11 mocked unit tests passed in the audit environment.
- **Remaining:** Run on Windows; the output must show `OK` and the test
  count. Paste the real output.

## 10. Flask server source code — 1 point

- **Required:** Flask source with the `/emotionDetector` route.
- **File:** `server.py`
- **Status:** PASS (inspected; routes `/` and `/emotionDetector` (GET/POST) with
  the `textToAnalyze` parameter, integrates `emotion_detector`, returns JSON,
  handles blank/whitespace/missing input with 400, and service errors with
  502 without exposing stack traces).

## 11. Screenshot `6b_deployment_test.png` — 1 point

- **Required:** Screenshot of the running app showing real results.
- **Status:** NOT RUN (requires running Flask + Watson).
- **Steps:**
  1. Set `WATSON_NLP_URL` (and `WATSON_NLP_API_KEY` if required).
  2. Run `python server.py`.
  3. Open `http://localhost:5000`.
  4. Type a sentence and press **Analyze Emotion**.
  5. Screenshot the page showing the real emotion cards.
  6. Save as `evidence/6b_deployment_test.png`.

## 12. HTTP 400 handling code — 1 point

- **Required:** The code block handling HTTP 400.
- **File:** `EmotionDetection/emotion_detection.py`:
  ```python
  if response.status_code == 400:
      return dict(_BLANK_RESULT)
  ```
- **Status:** PASS (inspected; returns the all-`None` blank result on 400).

## 13. Blank-input handling code in `server.py` — 1 point

- **Required:** Code handling blank/whitespace/missing input.
- **File:** `server.py`:
  ```python
  if text_to_analyze is None or not str(text_to_analyze).strip():
      return jsonify({...}), 400
  ```
- **Status:** PASS (inspected; returns 400 with a friendly message).

## 14. Screenshot `7c_error_handling_interface.png` — 1 point

- **Required:** Screenshot of the blank-input validation message.
- **Status:** NOT RUN (requires running Flask).
- **Steps:**
  1. Run `python server.py` and open `http://localhost:5000`.
  2. Leave the input empty and press **Analyze Emotion**.
  3. Screenshot the warning message shown by the frontend.
  4. Save as `evidence/7c_error_handling_interface.png`.

## 15. Static analysis implementation / evidence in `server.py` — 1 point

- **Required:** pylint run on `server.py`.
- **Command:**
  ```powershell
  pylint server.py
  ```
- **Status:** NOT RUN — Flask and pylint are not installed in the audit environment.
- **Remaining:** Run on Windows; if your course requires the pylint output
  pasted as a comment at the top of `server.py`, do so **after** the real
  run. Do not fabricate the score.

## 16. Terminal output showing a perfect static-analysis score — 1 point

- **Required:** Terminal output showing `10.00/10` (or the required score).
- **Command:**
  ```powershell
  pylint server.py
  ```
- **Status:** NOT RUN (requires `pylint`).
- **Remaining:** Fix any reported issues, re-run until the real output shows
  the required score, and paste the real output.

---

## Environment / dependency notes

- `requirements.txt` includes `Flask`, `requests`, and `pylint`.
- `.gitignore` excludes `__pycache__/`, `venv/`, `.env`, `*.env`, and
  credential files — secrets and virtual environments are not committed.

## Audit status (executed in Bolt)

| Check                          | Result   |
|--------------------------------|----------|
| Python syntax compilation       | PASS     |
| All required files present      | PASS     |
| Watson NLP integration (inspected; live request not run) | NEEDS LIVE VERIFICATION |
| Frontend connects to `/emotionDetector` (inspected) | PASS |
| Unit tests (mocked Watson responses) | PASS (11 tests) |
| Flask startup (requires `flask`) | NOT RUN |
| pylint (requires `pylint`)       | NOT RUN |

Run on Windows in this order:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set WATSON_NLP_URL=<your Watson NLP service URL from the lab>
set WATSON_NLP_API_KEY=<your-api-key, if required>
python -m unittest -v test_emotion_detection.py
pylint server.py
python server.py
```