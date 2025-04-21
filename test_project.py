import os
import importlib.util

# Test 1: truncate_headlines
def test_truncate_headlines():
    from project import truncate_headlines

    headlines = ["Short headline", "Another short one"]
    result = truncate_headlines(headlines, max_length=80)
    assert result == headlines

    long_headline = "This is a very long headline that should be truncated because it exceeds the maximum length allowed"
    headlines = [long_headline, "Short one"]
    result = truncate_headlines(headlines, max_length=30)

    assert result[0] == long_headline[:30] + "..."
    assert result[1] == "Short one"

# Test 2: api_key_presence
def test_api_key_presence():
    with open('project.py', 'r') as file:
        code = file.read().lower()
        assert 'api_key' in code
        assert 'your_api_key' not in code

# Test 3: required imports
def test_imports():
    try:
        import requests
        import pyttsx3
        import threading
        import time
        from kivy.app import App
    except ImportError as e:
        assert False, f"Import error: {e}"

# Optional: Manual instructions for the developer
def test_manual_instructions():
    print("\n===== MANUAL TESTING INSTRUCTIONS =====")
    print("Since automated testing of GUI and TTS requires complex setup,")
    print("here are steps to manually test the application:")
    print("\n1. Run the application: python project.py")
    print("2. Click 'Fetch News' and verify headlines appear")
    print("3. Click on a headline to test individual TTS")
    print("4. Click 'Start Auto-Reading' to test continuous TTS")
    print("5. Click 'Stop Auto-Reading' to verify it stops")
    print("\nCheck console output for debugging information.")
    print("======================================\n")
