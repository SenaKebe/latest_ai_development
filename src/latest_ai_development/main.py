# src/latest_ai_development/main.py

from latest_ai_development.crew import BlogContentCrew

def run():
    inputs = {
        "topic": "AI for Content Creators",
        "tone": "witty",                    # ✅ Add this
        "audience": "tech-savvy creators",  # ✅ Add this
        "platform": "Medium"                # ✅ Add this
    }

    BlogContentCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()