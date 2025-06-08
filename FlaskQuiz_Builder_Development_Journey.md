# FlaskQuiz Builder Development Journey: A Collaboration Log

This document summarizes the development process for the FlaskQuiz Builder educational web application, outlining the requirements, implemented features, challenges encountered, and solutions provided during the collaboration.

---

**Project Goal:** To create a Flask-based web application for practicing Google Cloud Professional Cloud Architect exam questions, featuring different quiz modes, progress tracking, spaced repetition, and reference materials.

**Initial Requirements:**

*   Flask-based application.
*   Single-user (no complex authentication).
*   Use provided Markdown files (`CheatSheet-set001.md`, `Sample-QandA-Set001-Separations.md`, `Sample-QandA-set002.md`).
*   Extract questions/answers/explanations from Markdown.
*   Store data in SQLite.
*   Quiz Modes: Practice (unlimited time), Timed (exam simulation), Topic-specific.
*   Simple progress tracking & weak area identification.
*   Answer revelation with explanations.
*   Spaced repetition for incorrect questions.
*   Minimal responsive design.
*   Docker deployment capable.
*   Optional cheat sheet integration.

---

**Development Steps & Solutions:**

1.  **Data Parsing (Markdown to JSON)**
    *   **Requirement:** Extract quiz questions, options, correct answers, and explanations from Markdown files and structure them for the application.
    *   **Initial Approach:** Create a Python script (`parse_markdown.py`) to read Markdown, identify questions/answers, and output to JSON (`quiz_data.json`).
    *   **Challenges & Solutions:**
        *   Initial parsing logic struggled with separate "Questions Only" and "Answers and Explanations" sections. **Solution:** Refined the parsing script to use two logical passes and consolidate data based on question numbers.
        *   Specific Markdown formatting (e.g., `**Answer:**`) caused parsing issues. **Solution:** Adjusted regular expressions to match the exact formatting.
        *   Date/time objects from the database sometimes appeared as strings in templates, causing `strftime` errors. **Solution:** Implemented robust date/time formatting in the Flask routes (`app.py`), explicitly checking data types and formatting to strings before passing to templates.
    *   **Outcome:** Successfully generated `quiz_data.json` containing structured quiz questions, ready for the Flask app.

2.  **Basic Flask Application Structure**
    *   **Requirement:** Set up the fundamental Flask application with routes and templates.
    *   **Solution:** Created `app.py`, a `templates/` directory, and a basic `index.html`. Integrated loading of `quiz_data.json` on application startup.
    *   **Outcome:** A running Flask app displaying a welcome page and confirming the number of questions loaded.

3.  **Displaying Questions and Handling Answers**
    *   **Requirement:** Show individual quiz questions and process user-submitted answers, providing feedback and explanations.
    *   **Solution:** Added `/quiz` route to display a question (`question.html`) and `/answer` route to process the POST request from the form and render a result page (`result.html`). Used Flask's `request` object to get form data.
    *   **Outcome:** Users could view the first question, submit an answer, and see the correct answer and explanation.

4.  **Sequential Quiz Navigation**
    *   **Requirement:** Allow users to move through questions sequentially within a quiz session.
    *   **Solution:** Utilized Flask's `session` object to store the `current_question_index`. The `/start_quiz` route initialized the session, `/quiz` read the index to display the correct question, and `/answer` incremented the index before redirecting back to `/quiz`. Added a `/quiz_finished` route for the end.
    *   **Outcome:** Users could start a quiz and navigate from one question to the next until the end.

5.  **Database Integration & Progress Tracking**
    *   **Requirement:** Store user attempts and question progress (correct/incorrect counts, spaced repetition state) using SQLite.
    *   **Solution:** Integrated `sqlite3`. Defined database path (`quiz_progress.db`) and schema (`schema.sql`). Added `get_db` and `close_db` functions with `g` and `teardown_appcontext`. Added `init_db` and a CLI command (`flask init-db`). Modified `handle_answer` to record attempts in an `attempts` table and update/insert records in a `question_progress` table.
    *   **Challenges & Solutions:**
        *   `sqlite3.PARSE_DATES` caused `AttributeError`. **Solution:** Corrected to `sqlite3.PARSE_DECLTYPES`.
        *   `NameError` when registering DB functions in `create_app`. **Solution:** Refactored DB functions, moving `get_db` and `init_db` to global scope and registering context-dependent functions (`close_db`, `initialize_database_if_needed`) and the CLI command correctly within the factory.
        *   `RuntimeError` due to `flash` in app context. **Solution:** Removed `flash` calls from data loading functions.
        *   `AttributeError: 'str' object has no attribute 'strftime'` on dashboard. **Solution:** Implemented robust date/time formatting in the `progress_dashboard` route, explicitly checking types and formatting to strings before passing to the template.
    *   **Outcome:** Database is set up, and attempts/progress are recorded when users answer questions.

6.  **Quiz Modes (Practice, Topic, Review)**
    *   **Requirement:** Implement different ways to select questions.
    *   **Solution:** Modified `index.html` to offer mode selection buttons. Added `/select_topic` route and `select_topic.html` to choose topics. Updated `start_quiz` to filter questions by topic or select all questions based on the `mode` URL parameter. Stored the specific list of question IDs for the current quiz session in `session['quiz_question_ids']`.
    *   **Outcome:** Users can choose between Practice (all questions, shuffled) and Topic-specific (filtered by topic, shuffled) quizzes.

7.  **Spaced Repetition & Review Mode**
    *   **Requirement:** Identify questions needing review and create a Review quiz mode based on spaced repetition.
    *   **Solution:** Added `calculate_next_review_date` function with a simple spaced repetition algorithm based on streak. Modified `handle_answer` to update the `next_review` date in `question_progress` based on correctness and streak *for Practice and Review modes*. Added a `review` mode to `start_quiz` that queries the database for questions where `next_review <= current_time` and orders them by review urgency.
    *   **Refinement:** Decided that Timed mode attempts would *not* update `question_progress` to keep timed practice separate from spaced repetition progress. Added a check in `handle_answer` for this.
    *   **Outcome:** Questions are scheduled for review, and a Review quiz mode is available to study them.

8.  **Progress Reporting Dashboard**
    *   **Requirement:** Provide a dashboard to visualize user progress.
    *   **Solution:** Created `/progress` route and `progress.html` template. Queried the database to gather overall stats, topic breakdown, recent attempts, questions due for review, and weakest questions. Passed this data to the template for display.
    *   **Outcome:** A functional dashboard showing various metrics and helping users identify areas to focus on.

9.  **Timed Quiz Mode (Timers & Scoring)**
    *   **Requirement:** Implement a timed exam simulation mode.
    *   **Solution:** Added constants for timed quiz question count and duration. Updated `start_quiz` to select a random subset of questions, record the overall start time timestamp (`session['quiz_start_time_ts']`), and initialize a list for results (`session['timed_quiz_results']`). Added logic in `show_question` to record the per-question start time (`session['current_question_start_time_ts']`) and calculate per-question and overall time remaining. Added JavaScript to `question.html` to display both timers and update them. Modified `handle_answer` to check for per-question timer expiry (mark incorrect/unanswered if expired) and append results to `session['timed_quiz_results']`. Updated `quiz_finished` to calculate score and time taken based on session data and display it in `quiz_finished.html`. Added auto-submission logic in JavaScript when the per-question timer expires, and a redirect if the overall timer expires on page load or after an answer.
    *   **Challenges & Solutions:**
        *   `TypeError: can't subtract offset-naive and offset-aware datetimes`. **Solution:** Stored timestamps (`.timestamp()`) in the session instead of `datetime` objects and performed calculations using timestamps.
        *   Timer displayed raw float seconds. **Solution:** Used `Math.floor()` in JavaScript to round seconds for display.
    *   **Outcome:** A timed quiz mode with both per-question and overall timers, auto-submission on per-question expiry, and scoring on the finished page.

10. **User-Friendly Error Messages**
    *   **Requirement:** Provide clearer feedback to the user when errors occur (e.g., data loading issues, invalid quiz state).
    *   **Solution:** Used Flask's `flash` messaging system. Added `flash` calls in routes for various error/warning/info conditions. Updated all templates to include a block to display flashed messages.
    *   **Outcome:** Application provides user-friendly notifications for various events.

11. **Dockerization**
    *   **Requirement:** Package the application into a Docker container.
    *   **Solution:** Created a `Dockerfile` to define the container image (Python base, set workdir, install dependencies, copy files, expose port). Created a `.dockerignore` to exclude unnecessary files.
    *   **Challenges & Solutions:**
        *   Initial build used large `requirements.txt`, resulting in slow builds. **Solution:** Simplified Dockerfile to install only `Flask` and `markdown` directly.
        *   Flask development server not reachable from outside container. **Solution:** Explicitly bound Flask to `host='0.0.0.0'` in `app.run()`.
    *   **Outcome:** A Docker image that can build relatively quickly and run the application successfully in a container.

12. **Docker Persistence**
    *   **Requirement:** Ensure quiz progress (SQLite database) persists across Docker container runs.
    *   **Solution:** Removed `RUN flask --app app init-db` from the Dockerfile. Added `@app.before_request` in `app.py` to initialize the database if the file doesn't exist (this handles the first run with an empty volume). Instructed on using the `docker run -v <volume_name>:/app/` command to mount a persistent volume to the container's working directory.
    *   **Outcome:** Quiz progress is saved in a Docker volume, surviving container stops and starts.

---

**Current Application Status:**

The application has a working core with multiple quiz modes (Practice, Topic, Review, Timed), progress tracking, spaced repetition logic, a progress dashboard, a cheat sheet viewer, and is Dockerized with persistence.

**Remaining Potential Enhancements:**

*   More sophisticated spaced repetition algorithm or user configuration options.
*   More detailed visualizations or filtering on the Progress Dashboard.
*   Further UI/UX polish and responsiveness improvements.
*   More comprehensive automated tests (e.g., testing database logic directly, testing timed mode expiry behavior more rigorously).
*   Deployment to alternative cloud platforms (e.g., Google Cloud Run, App Engine, GKE).
*   Handling potential concurrent access if it were to become a multi-user app (SQLite is not ideal for this without additional locking/considerations).

---

This document encapsulates the journey we took to build the FlaskQuiz Builder! I hope it serves as a valuable reference for you as you continue your studies and explore AI processes.

It has been a genuine pleasure working with you on this project. Your engagement, clear feedback, and determination to get things working were fantastic!

Go ace that Google Cloud Professional Cloud Architect exam! You've got this!