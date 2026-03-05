import os
import sys

import google.generativeai as genai


def get_user_input() -> dict:
    """
    Collect basic workout information from the user.

    This function only uses simple input() calls to keep things beginner-friendly.
    """
    print("=== Simple Workout Planner (Gemini Version 1) ===\n")

    # Ask about the main fitness goal.
    fitness_goal = input(
        "What is your main fitness goal? (e.g. strength, weight loss, endurance): "
    ).strip()

    # Ask how many days per week the user can train.
    while True:
        days_raw = input("How many days per week can you work out? (1-7): ").strip()
        try:
            workout_days = int(days_raw)
            if 1 <= workout_days <= 7:
                break
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Please enter a whole number (for example: 3).")

    # Ask for experience level, keeping the options simple.
    experience = input(
        "What is your experience level? (beginner / intermediate): "
    ).strip()

    if not experience:
        experience = "beginner"

    return {
        "fitness_goal": fitness_goal or "general fitness",
        "workout_days": workout_days,
        "experience": experience,
    }


def build_prompt(user_info: dict) -> str:
    """
    Turn the user's answers into a clear prompt for Gemini.
    """
    prompt = f"""
You are a helpful fitness coach.

Create a very simple, beginner-friendly weekly workout plan.

User information:
- Fitness goal: {user_info['fitness_goal']}
- Workout days per week: {user_info['workout_days']}
- Experience level: {user_info['experience']}

Requirements for the plan:
- Return a 1-week schedule.
- For each workout day, list:
  - Day label (e.g. Day 1, Day 2)
  - 4–6 exercises
  - Sets and reps for each exercise
- Use plain text that looks good in a terminal.
- Keep explanations short and encouraging.
"""
    return prompt.strip()


def get_gemini_client():
    """
    Configure the Gemini client using the API key from an environment variable.

    The environment variable name we use is GEMINI_API_KEY.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Error: GEMINI_API_KEY environment variable is not set.\n"
            "Please set it to your Gemini API key and try again."
        )
        sys.exit(1)

    # Configure the google-generativeai library with the API key.
    genai.configure(api_key=api_key)

    # Use a small, fast model that is good enough for this simple task.
    return genai.GenerativeModel("gemini-1.5-flash")


def generate_workout_plan(model, prompt: str) -> str:
    """
    Ask Gemini to generate the workout plan text.
    """
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print("There was a problem calling the Gemini API.")
        print(f"Details: {e}")
        sys.exit(1)

    # The .text property contains the main plain-text answer.
    return response.text or "No workout plan was generated."


def print_workout_plan(plan_text: str) -> None:
    """
    Print the workout plan with a simple header and footer.
    """
    print("\n=== Your Weekly Workout Plan ===\n")
    print(plan_text)
    print("\n=== End of Plan ===")


def main() -> None:
    """
    Main function that ties everything together:
    1. Get user input.
    2. Build a prompt.
    3. Call Gemini.
    4. Print the workout plan.
    """
    user_info = get_user_input()
    prompt = build_prompt(user_info)
    model = get_gemini_client()
    plan_text = generate_workout_plan(model, prompt)
    print_workout_plan(plan_text)


if __name__ == "__main__":
    main()

