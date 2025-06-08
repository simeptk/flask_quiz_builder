from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g
import json
import os
import random
import sqlite3
from datetime import datetime, timedelta, timezone
import markdown # Import the markdown library

# --- Configuration ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
QUIZ_DATA_FILE = os.path.join(BASE_DIR, 'quiz_data.json')
DATABASE = os.path.join(BASE_DIR, 'quiz_progress.db')
CHEATSHEET_FILE = os.path.join(BASE_DIR, 'CheatSheet-set001.md') # Define cheat sheet file path


# Timed Quiz Configuration
TIMED_QUIZ_QUESTION_COUNT = 50
TIMED_QUIZ_DURATION_MINUTES = 90
TIMED_QUIZ_PER_QUESTION_SECONDS = 120


# --- Flask App Initialization ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace_with_a_very_long_and_random_secret_key_of_your_own_seriously' # TODO: Set a real secret key!

# --- Database Setup ---
def get_db():
    """Connect to the application's configured database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """If the database connection exists, close it."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    print("Database initialized.")

import click
@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
app.cli.add_command(init_db_command)

# --- Data Loading ---
quiz_questions = []
unique_topics = []
question_lookup = {}
cheatsheet_html = "" # Global variable to store the rendered cheat sheet HTML

def load_quiz_data():
    """Loads quiz data from the JSON file, extracts topics, and creates lookup."""
    global quiz_questions, unique_topics, question_lookup
    print(f"Attempting to load quiz data from: {QUIZ_DATA_FILE}")
    try:
        with open(QUIZ_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            quiz_questions = data.get("google_cloud_architect_questions", [])
            print(f"Successfully loaded {len(quiz_questions)} questions.")

            topics_set = set()
            for q in quiz_questions:
                question_id = q.get('id')
                if question_id:
                    question_lookup[question_id] = q # Store question by ID

                topic_name = q.get('category') or q.get('topic')
                if topic_name:
                    topics_set.add(topic_name.strip())

            unique_topics = sorted(list(topics_set))

            print(f"Extracted {len(unique_topics)} unique topics.")
            print(f"Created lookup for {len(question_lookup)} questions.")
            if not quiz_questions:
                 print("Warning: JSON file loaded successfully, but found 0 questions under 'google_cloud_architect_questions' key.")
    except FileNotFoundError:
        print(f"Error: Quiz data file not found at {QUIZ_DATA_FILE}. Please ensure quiz_data.json is in the same directory as app.py")
        quiz_questions = []
        unique_topics = []
        question_lookup = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {QUIZ_DATA_FILE}. Check file format.")
        quiz_questions = []
        unique_topics = []
        question_lookup = {}
    except Exception as e:
        print(f"An unexpected error occurred loading quiz data: {e}")
        quiz_questions = []
        unique_topics = []
        question_lookup = {}

def load_cheatsheet_data():
    """Loads and renders the cheat sheet Markdown file to HTML."""
    global cheatsheet_html
    print(f"Attempting to load cheat sheet from: {CHEATSHEET_FILE}")
    try:
        with open(CHEATSHEET_FILE, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
            # Render markdown to HTML
            cheatsheet_html = markdown.markdown(markdown_text)
            print("Successfully loaded and rendered cheat sheet.")
    except FileNotFoundError:
        print(f"Error: Cheat sheet file not found at {CHEATSHEET_FILE}. Please ensure CheatSheet-set001.md is in the same directory as app.py")
        cheatsheet_html = "<p>Error loading cheat sheet file.</p>" # Set error message
    except Exception as e:
        print(f"An unexpected error occurred loading cheat sheet: {e}")
        cheatsheet_html = f"<p>Error loading cheat sheet: {e}</p>"


# Load the data when the application starts
load_quiz_data()
load_cheatsheet_data() # Load cheat sheet data


# --- Spaced Repetition Logic ---
def calculate_next_review_date(current_time, streak, is_correct):
    """
    Calculates the next review date based on spaced repetition rules.
    This is a simple example algorithm.

    Args:
        current_time (datetime): The time of the current attempt (should be naive UTC).
        streak (int): The current consecutive correct streak *before* this attempt.
        is_correct (bool): Whether the current attempt was correct.

    Returns:
        datetime: The calculated date for the next review (should be naive UTC).
    """
    if current_time.tzinfo is not None:
        current_time = current_time.replace(tzinfo=None)

    if not is_correct:
        return current_time + timedelta(days=1)
    else:
        new_streak = streak + 1
        if new_streak == 1:
            interval_days = 1
        elif new_streak == 2:
            interval_days = 3
        elif new_streak == 3:
            interval_days = 7
        elif new_streak == 4:
            interval_days = 30
        else:
            interval_days = 90

        return current_time + timedelta(days=interval_days)


# --- Routes ---
@app.route('/')
def index():
    """Renders the index page with quiz mode options."""
    return render_template('index.html', question_count=len(quiz_questions), topics=unique_topics, cheatsheet_available=bool(cheatsheet_html)) # Pass availability


@app.route('/select_topic')
def select_topic():
    """Renders the page to select a quiz topic."""
    if not unique_topics:
        return "No topics available for topic-specific quiz.", 500
    return render_template('select_topic.html', topics=unique_topics)


@app.route('/start_quiz')
def start_quiz():
    """Initializes the session with questions based on mode and topic."""
    if not quiz_questions:
         return "No quiz questions available to start.", 500

    mode = request.args.get('mode', 'practice')
    topic = request.args.get('topic')

    selected_questions = []
    db = get_db()
    current_time = datetime.utcnow()

    # Clear any previous quiz session data
    session.pop('quiz_question_ids', None)
    session.pop('current_question_index', None)
    session.pop('quiz_mode', None)
    session.pop('quiz_topic', None)
    session.pop('quiz_title', None)
    session.pop('quiz_start_time_ts', None)
    session.pop('current_question_start_time_ts', None)
    session.pop('timed_quiz_results', None)


    if mode == 'practice':
        selected_questions = list(quiz_questions)
        random.shuffle(selected_questions)
        print(f"Starting Practice quiz with {len(selected_questions)} questions.")
        session['quiz_mode'] = 'practice'
        session['quiz_title'] = "Practice Quiz"


    elif mode == 'timed':
        if len(quiz_questions) < TIMED_QUIZ_QUESTION_COUNT:
             print(f"Warning: Not enough questions ({len(quiz_questions)}) for Timed quiz ({TIMED_QUIZ_QUESTION_COUNT}). Using all available.")
             selected_questions = list(quiz_questions)
        else:
            selected_questions = random.sample(quiz_questions, TIMED_QUIZ_QUESTION_COUNT)

        random.shuffle(selected_questions)

        print(f"Starting Timed quiz with {len(selected_questions)} questions, {TIMED_QUIZ_DURATION_MINUTES} mins total, {TIMED_QUIZ_PER_QUESTION_SECONDS} secs per question.")
        session['quiz_mode'] = 'timed'
        session['quiz_title'] = f"Timed Quiz ({TIMED_QUIZ_DURATION_MINUTES} mins total)"
        session['quiz_start_time_ts'] = datetime.utcnow().timestamp()
        session['timed_quiz_results'] = [] # Initialize list to store results


    elif mode == 'topic' and topic:
        selected_questions = [q for q in quiz_questions if (q.get('category') == topic or q.get('topic') == topic)]
        random.shuffle(selected_questions)
        print(f"Starting Topic quiz for '{topic}' with {len(selected_questions)} questions.")
        session['quiz_mode'] = 'topic'
        session['quiz_topic'] = topic
        session['quiz_title'] = f"Quiz on {topic}"


    elif mode == 'review':
        questions_to_review_ids = db.execute(
            'SELECT question_id, next_review, incorrect_attempts, streak FROM question_progress WHERE next_review <= ? ORDER BY next_review ASC, incorrect_attempts DESC LIMIT 50',
            (current_time,)
        ).fetchall()

        question_ids_for_review = [row['question_id'] for row in questions_to_review_ids]

        question_lookup_local = {q['id']: q for q in quiz_questions}
        selected_questions = [question_lookup_local.get(q_id) for q_id in question_ids_for_review if q_id in question_lookup_local]
        selected_questions = [q for q in selected_questions if q is not None]

        print(f"Starting Review quiz with {len(selected_questions)} questions due for review.")
        session['quiz_mode'] = 'review'
        session['quiz_title'] = "Review Questions"


    else:
        print(f"Invalid mode '{mode}'. Redirecting to index.")
        return redirect(url_for('index'))

    if not selected_questions:
        print(f"No questions found for mode '{mode}' and topic '{topic}'.")
        message = f"No questions found for {session.get('quiz_title', 'this selection')}."
        if mode == 'review':
             message = "No questions are currently due for review! Keep up the great work, or try a different quiz mode."
        return render_template('quiz_finished.html', quiz_title=session.get('quiz_title', 'Quiz'), message=message)


    session['quiz_question_ids'] = [q['id'] for q in selected_questions]
    session['current_question_index'] = 0 # Start at the first question

    print(f"Session initialized with {len(session['quiz_question_ids'])} question IDs for {session['quiz_mode']} mode.")

    return redirect(url_for('show_question'))


@app.route('/quiz')
def show_question():
    """Displays the current question from the session's question list."""
    quiz_question_ids = session.get('quiz_question_ids')
    current_index = session.get('current_question_index')
    quiz_mode = session.get('quiz_mode')

    # Basic session state validation
    if quiz_question_ids is None or current_index is None or not isinstance(current_index, int) or current_index < 0:
        print("Quiz session data missing or invalid. Redirecting to start.")
        session.pop('quiz_question_ids', None)
        session.pop('current_question_index', None)
        session.pop('quiz_mode', None)
        session.pop('quiz_topic', None)
        session.pop('quiz_title', None)
        session.pop('quiz_start_time_ts', None)
        session.pop('current_question_start_time_ts', None)
        session.pop('timed_quiz_results', None)
        return redirect(url_for('index'))

    # Check if the quiz is finished (by reaching the end of the question list)
    if current_index >= len(quiz_question_ids):
        print("Quiz finished (reached end of question list).")
        return redirect(url_for('quiz_finished'))

    current_question_id = quiz_question_ids[current_index]
    current_question = question_lookup.get(current_question_id)

    if not current_question:
        print(f"Error: Question with ID {current_question_id} not found in global data lookup. Resetting quiz.")
        return redirect(url_for('index'))

    print(f"Displaying question index {current_index} (ID: {current_question_id}) from session list.")

    # --- Timed Quiz Specifics ---
    per_question_duration_seconds = None
    per_question_time_remaining_seconds = None
    overall_duration_seconds = None
    overall_time_remaining_seconds = None
    overall_start_time_ts = None


    if quiz_mode == 'timed':
         per_question_duration_seconds = TIMED_QUIZ_PER_QUESTION_SECONDS
         overall_duration_seconds = TIMED_QUIZ_DURATION_MINUTES * 60

         # Get or set the start time for *this* question
         current_question_start_time_ts = session.get('current_question_start_time_ts')
         if current_question_start_time_ts is None:
              # This is the first time viewing this question in this session
              current_question_start_time_ts = datetime.utcnow().timestamp()
              session['current_question_start_time_ts'] = current_question_start_time_ts
              print(f"Timed quiz: Set start time for question {current_index + 1} to {current_question_start_time_ts}")

         # Calculate time remaining for *this* question
         elapsed_time_on_question = datetime.utcnow().timestamp() - current_question_start_time_ts
         per_question_time_remaining_seconds = max(0, per_question_duration_seconds - elapsed_time_on_question)

         # Calculate overall time remaining
         overall_start_time_ts = session.get('quiz_start_time_ts')
         if overall_start_time_ts is not None:
              overall_elapsed_time = datetime.utcnow().timestamp() - overall_start_time_ts
              overall_time_remaining_seconds = max(0, overall_duration_seconds - overall_elapsed_time)
              # print(f"Timed quiz overall: Elapsed {overall_elapsed_time:.1f}s, Remaining {overall_time_remaining_seconds:.1f}s")

         # Check if overall time has run out on page load
         # This check is critical for overall timer expiry
         if overall_time_remaining_seconds <= 0:
             print("Overall time expired on page load. Redirecting to quiz finished.")
             # Redirect to quiz_finished with a message
             return redirect(url_for('quiz_finished', message='Time for the overall quiz has expired.'))


    return render_template('question.html',
                           question=current_question,
                           question_number=current_index + 1,
                           total_questions=len(quiz_question_ids),
                           quiz_title=session.get('quiz_title', 'Quiz'),
                           quiz_mode=quiz_mode,
                           # Pass per-question timer data
                           per_question_duration_seconds=per_question_duration_seconds,
                           per_question_time_remaining_seconds=per_question_time_remaining_seconds,
                           # Pass overall timer data
                           overall_duration_seconds=overall_duration_seconds,
                           overall_time_remaining_seconds=overall_time_remaining_seconds # Pass calculated overall remaining time
                           )

# Route to handle the submitted answer
@app.route('/answer', methods=['POST'])
def handle_answer():
    """Processes the user's answer, updates database and session, and shows the result."""
    quiz_question_ids = session.get('quiz_question_ids')
    current_index = session.get('current_question_index')
    quiz_mode = session.get('quiz_mode')

    # Basic session state validation
    if quiz_question_ids is None or current_index is None or not isinstance(current_index, int) or not (0 <= current_index < len(quiz_question_ids)):
         print("Quiz session data missing or invalid during answer submission. Redirecting to start.")
         # Clear all quiz session data on error
         session.pop('quiz_question_ids', None)
         session.pop('current_question_index', None)
         session.pop('quiz_mode', None)
         session.pop('quiz_topic', None)
         session.pop('quiz_title', None)
         session.pop('quiz_start_time_ts', None)
         session.pop('current_question_start_time_ts', None)
         session.pop('timed_quiz_results', None)
         return redirect(url_for('index'))

    current_question_id = quiz_question_ids[current_index]
    question = question_lookup.get(current_question_id)

    if not question:
        print(f"Error: Question with ID {current_question_id} not found in global data lookup during answer processing. Resetting quiz.")
        return redirect(url_for('index'))

    submitted_question_id = request.form.get('question_id')
    user_answer = request.form.get('user_answer') # This will be None if no radio button was selected

    # Check if the answer is correct
    # Handle case where user_answer is None (timed out or skipped)
    is_correct = (user_answer is not None and user_answer == question.get('correct_answer'))
    # If user_answer is None, is_correct will be False

    # --- Timed Quiz Specifics & Scoring Update ---
    per_question_expired = False
    if quiz_mode == 'timed':
        # Check if the per-question timer expired *before* submission
        current_question_start_time_ts = session.get('current_question_start_time_ts')
        if current_question_start_time_ts is not None:
            elapsed_time_on_question = datetime.utcnow().timestamp() - current_question_start_time_ts
            if elapsed_time_on_question > TIMED_QUIZ_PER_QUESTION_SECONDS:
                per_question_expired = True
                print(f"Timed quiz: Per-question timer expired for Q ID {current_question_id} during submission.")

        # If the per-question timer expired, the answer is incorrect/unanswered regardless of user selection
        if per_question_expired:
             is_correct = False # Mark as incorrect due to timeout
             # Note: user_answer remains what the user selected (or None)

        # Append the result of this question to the session list for timed mode scoring
        if 'timed_quiz_results' not in session or not isinstance(session['timed_quiz_results'], list):
              session['timed_quiz_results'] = [] # Re-initialize if needed
        session['timed_quiz_results'].append(is_correct) # Append the final correctness status
        print(f"Timed quiz: Appended result {is_correct}. Current results count: {len(session['timed_quiz_results'])}")

        # Clear the per-question start time now that the question is processed
        session.pop('current_question_start_time_ts', None)

        # --- Overall Timed Quiz Check ---
        # Check if overall time has run out *after* processing this question
        overall_start_time_ts = session.get('quiz_start_time_ts')
        if overall_start_time_ts is not None:
             overall_elapsed_time = datetime.utcnow().timestamp() - overall_start_time_ts
             overall_duration_seconds = TIMED_QUIZ_DURATION_MINUTES * 60
             overall_time_remaining_seconds = max(0, overall_duration_seconds - overall_elapsed_time)

             if overall_time_remaining_seconds <= 0:
                  print("Overall time expired after processing answer. Redirecting to quiz finished.")
                  # Redirect directly to quiz_finished if overall time is up
                  return redirect(url_for('quiz_finished', message='Time for the overall quiz has expired.'))


    # --- End Timed Quiz Specifics & Scoring Update ---


    # --- Database Interaction ---
    db = get_db()
    current_time = datetime.utcnow()
    q_id = question.get('id', 'unknown')
    question_topic = question.get('category') or question.get('topic', 'General')

    try:
        # Record the attempt
        # For timed mode where per_question_expired is True, maybe store user_answer as '' or 'timeout'?
        # Let's keep user_answer as what they selected (or None) but rely on is_correct for outcome.
        db.execute(
            'INSERT INTO attempts (question_id, timestamp, user_answer, is_correct, quiz_mode, topic)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (q_id, current_time, user_answer, is_correct, quiz_mode, question_topic)
        )

        # Update or insert question progress (Applies to all modes for now, including timed)
        # If you don't want Timed mode affecting spaced repetition, add:
        # if quiz_mode != 'timed':
        progress = db.execute(
            'SELECT * FROM question_progress WHERE question_id = ?', (q_id,)
        ).fetchone()

        if progress is None:
            correct_count = 1 if is_correct else 0
            incorrect_count = 0 if is_correct else 1
            streak = 1 if is_correct else 0
            next_review_date = calculate_next_review_date(current_time, 0, is_correct)

            db.execute(
                'INSERT INTO question_progress (question_id, correct_attempts, incorrect_attempts, streak, next_review, last_attempt)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (q_id, correct_count, incorrect_count, streak, next_review_date, current_time)
            )
            # print(f"Inserted initial progress for question ID {q_id}. Correct: {correct_count}, Incorrect: {incorrect_count}, Streak: {streak}, Next Review: {next_review_date}.")

        else:
            correct_count = progress['correct_attempts'] + (1 if is_correct else 0)
            incorrect_count = progress['incorrect_attempts'] + (0 if is_correct else 1)
            new_streak = progress['streak'] + 1 if is_correct else 0
            next_review_date = calculate_next_review_date(current_time, progress['streak'], is_correct)

            db.execute(
                'UPDATE question_progress SET correct_attempts = ?, incorrect_attempts = ?, streak = ?, next_review = ?, last_attempt = ?'
                ' WHERE question_id = ?',
                (correct_count, incorrect_count, new_streak, next_review_date, current_time, q_id)
            )
            # print(f"Updated progress for question ID {q_id}. Correct: {correct_count}, Incorrect: {incorrect_count}, Streak: {new_streak}, Next Review: {next_review_date}.")

        db.commit()

    except sqlite3.Error as e:
        print(f"Database error processing answer for question ID {q_id}: {e}")
        db.rollback()

    # --- End Database Interaction ---

    # Increment the question index for the next question
    session['current_question_index'] = current_index + 1

    print(f"Answer submitted for Q ID {q_id}. Correct: {is_correct}. Moving to index {session['current_question_index']}.")

    # Check if the quiz is now finished by answering the last question
    # This check should happen *after* incrementing the index
    if session['current_question_index'] >= len(quiz_question_ids):
         print("Quiz completed by answering the last question.")
         # Redirect directly to quiz_finished if this was the last question
         return redirect(url_for('quiz_finished'))


    return render_template('result.html',
                           question=question,
                           user_answer=user_answer,
                           is_correct=is_correct,
                           next_question_url=url_for('show_question'),
                           quiz_title=session.get('quiz_title', 'Quiz'),
                           quiz_mode=quiz_mode,
                           )


@app.route('/quiz_finished')
def quiz_finished():
    """Renders the quiz finished page."""
    print("Rendering quiz finished page.")
    quiz_title = session.get('quiz_title', 'Quiz')
    message = request.args.get('message') # Optional message passed via redirect

    # Calculate time taken if it was a timed quiz
    time_taken_seconds = None
    quiz_mode = session.get('quiz_mode')
    quiz_start_time_ts = session.get('quiz_start_time_ts')
    timed_quiz_results = session.get('timed_quiz_results', [])

    if quiz_mode == 'timed' and quiz_start_time_ts is not None:
         time_taken_seconds = datetime.utcnow().timestamp() - quiz_start_time_ts
         time_taken_seconds = max(0, time_taken_seconds)

         timed_score = sum(timed_quiz_results)
         total_timed_questions_attempted = len(timed_quiz_results) # Use attempted count


         print(f"Timed quiz finished. Time taken: {time_taken_seconds:.1f} seconds. Score: {timed_score}/{total_timed_questions_attempted}.")

    # Clear session for this specific quiz run
    session.pop('quiz_question_ids', None)
    session.pop('current_question_index', None)
    session.pop('quiz_mode', None)
    session.pop('quiz_topic', None)
    session.pop('quiz_title', None)
    session.pop('quiz_start_time_ts', None)
    session.pop('current_question_start_time_ts', None)
    session.pop('timed_quiz_results', None)


    # Format time taken for display
    time_taken_formatted = None
    if time_taken_seconds is not None:
         minutes = int(time_taken_seconds // 60)
         seconds = int(time_taken_seconds % 60)
         time_taken_formatted = f"{minutes} minutes {seconds} seconds"

    # Prepare score for display
    timed_score_data = None
    # Check if quiz_mode was timed AND we have results
    if quiz_mode == 'timed' and 'timed_score' in locals():
        timed_score_data = {
            'score': timed_score,
            'total': total_timed_questions_attempted # Total questions *attempted* in this run
        }


    return render_template('quiz_finished.html',
                           quiz_title=quiz_title,
                           message=message,
                           quiz_mode=quiz_mode,
                           time_taken_formatted=time_taken_formatted,
                           timed_score_data=timed_score_data
                           )

# New route to end the current quiz session prematurely
@app.route('/end_quiz')
def end_quiz():
    """Clears quiz session data and redirects to home."""
    print("Ending quiz session.")
    session.pop('quiz_question_ids', None)
    session.pop('current_question_index', None)
    session.pop('quiz_mode', None)
    session.pop('quiz_topic', None)
    session.pop('quiz_title', None)
    session.pop('quiz_start_time_ts', None)
    session.pop('current_question_start_time_ts', None)
    session.pop('timed_quiz_results', None)

    return redirect(url_for('index'))

# New route for the progress dashboard
@app.route('/progress')
def progress_dashboard():
    """Renders the progress dashboard page."""
    db = get_db()
    current_time = datetime.utcnow()

    # 1. Overall Stats
    total_questions_loaded = len(quiz_questions)
    total_attempts_row = db.execute('SELECT COUNT(*) AS total FROM attempts').fetchone()
    total_attempts = total_attempts_row['total'] if total_attempts_row else 0

    correct_attempts_row = db.execute('SELECT COUNT(*) AS total FROM attempts WHERE is_correct = 1').fetchone()
    correct_attempts = correct_attempts_row['total'] if correct_attempts_row else 0

    incorrect_attempts = total_attempts - correct_attempts
    overall_correct_percentage = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0

    # 2. Progress per Topic
    topic_stats_rows = db.execute(
        'SELECT topic, COUNT(*) as total_attempts, SUM(is_correct) as correct_attempts '
        'FROM attempts GROUP BY topic ORDER BY topic'
    ).fetchall()

    topic_stats = []
    for row in topic_stats_rows:
        topic_total_attempts = row['total_attempts']
        topic_correct_attempts = row['correct_attempts'] or 0
        topic_incorrect_attempts = topic_total_attempts - topic_correct_attempts
        topic_correct_percentage = (topic_correct_attempts / topic_total_attempts * 100) if topic_total_attempts > 0 else 0
        topic_stats.append({
            'topic': row['topic'],
            'total_attempts': topic_total_attempts,
            'correct_attempts': topic_correct_attempts,
            'incorrect_attempts': topic_incorrect_attempts,
            'correct_percentage': f"{topic_correct_percentage:.1f}%"
        })

    # Identify weak areas (e.g., topics with > 0 incorrect attempts and low correct %)
    weak_areas = [
        stats for stats in topic_stats
        if stats['incorrect_attempts'] > 0 and (float(stats['correct_percentage'].strip('%')) < 70) # Example threshold
    ]
    weak_areas.sort(key=lambda x: x['correct_percentage'])

    # 4. Questions Due for Review
    questions_due_for_review_rows = db.execute(
        'SELECT question_id, next_review, incorrect_attempts, streak FROM question_progress WHERE next_review <= ? ORDER BY next_review ASC, incorrect_attempts DESC',
        (current_time,)
    ).fetchall()

    questions_due_for_review = []
    for row in questions_due_for_review_rows:
        q_id = row['question_id']
        question_data = question_lookup.get(q_id)
        if question_data:
            questions_due_for_review.append({
                'id': q_id,
                'text_snippet': question_data['text'][:100] + '...' if len(question_data['text']) > 100 else question_data['text'],
                'next_review': row['next_review'],
                'incorrect_attempts': row['incorrect_attempts'],
                'streak': row['streak'],
                'topic': question_data.get('category') or question_data.get('topic', 'General')
            })
        else:
             print(f"Warning: Question ID {q_id} found in progress but not in quiz_data.json.")


    return render_template('progress.html',
                           total_questions_loaded=total_questions_loaded,
                           total_attempts=total_attempts,
                           correct_attempts=correct_attempts,
                           incorrect_attempts=incorrect_attempts,
                           overall_correct_percentage=overall_correct_percentage,
                           topic_stats=topic_stats,
                           weak_areas=weak_areas,
                           questions_due_for_review=questions_due_for_review
                           )


# New route to display the Cheat Sheet
@app.route('/cheatsheet')
def cheatsheet():
    """Renders the cheat sheet page."""
    # The rendered HTML is already loaded into the global cheatsheet_html variable
    if not cheatsheet_html:
         # Fallback message if loading failed
         return render_template('cheatsheet.html', cheat_sheet_content="<p>Could not load cheat sheet content.</p>")

    return render_template('cheatsheet.html', cheat_sheet_content=cheatsheet_html)


# Example routes for debugging database content
@app.route('/api/questions')
def get_questions_api():
    """Returns the raw quiz data as JSON."""
    return jsonify(quiz_questions)

@app.route('/api/progress')
def get_progress_api():
    """Returns basic question progress data from the database."""
    db = get_db()
    progress_data = db.execute('SELECT * FROM question_progress').fetchall()
    return jsonify([dict(row) for row in progress_data])

@app.route('/api/attempts')
def get_attempts_api():
    """Returns recent attempts from the database (for debugging)."""
    db = get_db()
    attempts_data = db.execute('SELECT * FROM attempts ORDER BY timestamp DESC LIMIT 100').fetchall()
    formatted_attempts = []
    for row in attempts_data:
        attempt_dict = dict(row)
        attempt_dict['timestamp'] = attempt_dict['timestamp'].isoformat() if isinstance(attempt_dict['timestamp'], datetime) else str(attempt_dict['timestamp'])
        formatted_attempts.append(attempt_dict)
    return jsonify(formatted_attempts)

# Add a check to initialize the database if it doesn't exist
@app.before_request
def initialize_database_if_needed():
    """Initializes the database if the file does not exist."""
    # Check if the database file exists
    if not os.path.exists(DATABASE):
        print("Database file not found. Initializing database...")
        try:
            init_db()
            print("Database initialization complete.")
        except Exception as e:
            print(f"Error during database initialization: {e}")
            # Depending on severity, you might want to stop the app or log this error
            # For now, we'll just print the error.

# --- Running the App ---
if __name__ == '__main__':
    print("Starting Flask development server...")
    # Use host='0.0.0.0' to make it accessible externally if needed (e.g., in Docker)
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0')
