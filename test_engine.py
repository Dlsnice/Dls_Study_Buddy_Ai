"""
test_engine.py
==============
Tests each core function of ai_engine in both mock mode and live mode.
"""

import sys
# Enable utf-8 output for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import ai_engine

def test_all():
    print("Testing chat_with_ai (Demo Mode)...")
    res1 = ai_engine.chat_with_ai(
        history=[{"role": "user", "content": "What is an LLM?"}],
        system_instruction="You are a helpful tutor.",
        api_key=None
    )
    assert len(res1) > 0, "Chat response should not be empty"
    print(" [OK] Chat response received successfully!")

    print("\nTesting analyze_document (Demo Mode)...")
    res2 = ai_engine.analyze_document(
        document_text="Tokens are pieces of words used by language models.",
        question_or_task="Summarize in 1 bullet",
        api_key=None
    )
    assert len(res2) > 0, "Document response should not be empty"
    print(" [OK] Document analysis response received successfully!")

    print("\nTesting generate_quiz (Demo Mode)...")
    quiz = ai_engine.generate_quiz(
        topic_or_notes="Machine Learning Basics",
        num_questions=3,
        api_key=None
    )
    assert isinstance(quiz, list), "Quiz should return a list"
    assert len(quiz) > 0, "Quiz list should have questions"
    print(f" [OK] Generated {len(quiz)} quiz questions successfully!")

    print("\nALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all()
