# brand_intake.py
# This script runs a structured brand intake interview.
# It asks the brand owner a series of questions across five categories,
# captures all answers, and saves them as a structured JSON file.
# The JSON output feeds directly into the brand voice analyser in Step 2.

import json
import os
from datetime import datetime

# ── Intake questions ─────────────────────────────────────────────────────────
# Questions are organised into five categories.
# Each category has a name and a list of questions.
# This structure makes it easy to add or remove questions later.

intake_questions = [
    {
        "category": "Brand Foundations",
        "questions": [
            "What is your brand name and what do you sell?",
            "When was the brand founded and what was the founding reason?",
            "What problem does your brand solve for your customer?",
            "What is your brand's single most important belief or value?"
        ]
    },
    {
        "category": "Target Customer",
        "questions": [
            "Describe your ideal customer in as much detail as possible. Who are they, how old are they, what do they do?",
            "What does your ideal customer care about most in their daily life?",
            "What frustrates your ideal customer about other brands in your space?",
            "What does your customer want to feel when they buy from you?"
        ]
    },
    {
        "category": "Brand Personality",
        "questions": [
            "If your brand were a person, how would you describe their personality in three words?",
            "Describe your brand's communication style. How does it talk to customers?",
            "Name one brand outside your industry that your brand feels similar to in terms of voice and personality. Why?",
            "What words or phrases should your brand NEVER use?"
        ]
    },
    {
        "category": "Competitive Position",
        "questions": [
            "Who are your top two or three competitors?",
            "What do you do better than any competitor?",
            "Why would a customer choose you over a cheaper alternative?",
            "What is the one thing you want customers to remember about your brand?"
        ]
    },
    {
        "category": "Content and Marketing",
        "questions": [
            "What marketing channels do you currently use or plan to use?",
            "What type of content performs best with your audience so far?",
            "What topics could your brand talk about with genuine authority?",
            "What is one piece of content you wish you had but have never made?"
        ]
    }
]


# ── Interview function ───────────────────────────────────────────────────────

def run_intake_interview():
    """
    Runs the full brand intake interview in the terminal.
    Asks all questions across all categories and captures answers.

    Returns:
        dict: All answers organised by category, plus metadata.
    """

    print("\n" + "=" * 60)
    print("FEMFIT.FIT — BRAND INTAKE INTERVIEW")
    print("Answer each question as the brand owner would.")
    print("Press Enter after each answer to move to the next question.")
    print("=" * 60)

    # This dictionary will hold all the answers when we are done.
    # We start by recording the brand name and the date of the interview.
    all_answers = {
        "brand_name": "FemFit.fit",
        "interview_date": datetime.now().strftime("%d %B %Y"),
        "categories": []
    }

    # Loop through each category of questions.
    for category in intake_questions:

        print(f"\n{'─' * 60}")
        print(f"CATEGORY: {category['category'].upper()}")
        print(f"{'─' * 60}")

        # This list will hold the answers for the current category.
        category_answers = {
            "category": category["category"],
            "answers": []
        }

        # Loop through each question in the current category.
        # enumerate() gives us the question number (i) and the question text.
        for i, question in enumerate(category["questions"], start=1):

            print(f"\nQ{i}: {question}")

            # input() pauses the script and waits for the user to type an answer.
            # The answer is stored as a string in the variable 'answer'.
            answer = input("Your answer: ").strip()

            # If the user pressed Enter without typing anything,
            # we record it as "No answer provided" so the JSON stays complete.
            if not answer:
                answer = "No answer provided"

            # Add this question and answer pair to the category answers list.
            category_answers["answers"].append({
                "question": question,
                "answer": answer
            })

        # Once all questions in a category are done, add the category to our main dictionary.
        all_answers["categories"].append(category_answers)

    return all_answers


# ── Save function ────────────────────────────────────────────────────────────

def save_intake_results(answers):
    """
    Saves the intake answers to a JSON file in the outputs folder.

    Parameters:
        answers (dict): The full set of interview answers.

    Returns:
        str: The path to the saved file.
    """

    # Create the outputs folder if it does not exist yet.
    os.makedirs("outputs", exist_ok=True)

    # Define the output file path.
    filepath = "outputs/brand_intake_answers.json"

    # Open the file and write the answers as formatted JSON.
    # indent=2 makes the JSON human-readable with 2-space indentation.
    # ensure_ascii=False allows special characters to save correctly.
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)

    return filepath


# ── Main runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run the interview and capture all answers.
    answers = run_intake_interview()

    # Save the answers to a JSON file.
    filepath = save_intake_results(answers)

    print("\n" + "=" * 60)
    print("INTERVIEW COMPLETE")
    print(f"Answers saved to: {filepath}")
    print("Run brand_analyser.py next to generate the brand voice document.")
    print("=" * 60)