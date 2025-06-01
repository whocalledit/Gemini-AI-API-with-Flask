import requests
import json

BASE_URL = "http://localhost:8000/ai-multitool"

test_cases = [
    {
        "description": "Code explanation test",
        "payload": {
            "task": "code_explain",
            "input": "def greet():\n    print('Hello, AI!')"
        }
    },
    {
        "description": "Idea generator test",
        "payload": {
            "task": "idea_generator",
            "input": "mental health, app, students"
        }
    },
    {
        "description": "Tone detection test",
        "payload": {
            "task": "tone_detector",
            "input": "I'm absolutely devastated by the outcome."
        }
    },
    {
        "description": "Image caption test with URL",
        "payload": {
            "task": "image_caption",
            "input": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/800px-Example.jpg"
        }
    },
    {
        "description": "Invalid task test",
        "payload": {
            "task": "invalid_task",
            "input": "this should fail"
        }
    },
    {
        "description": "Empty input test",
        "payload": {
            "task": "code_explain",
            "input": ""
        }
    }
]

def run_tests():
    print("🔍 Running tests...\n")
    for idx, test in enumerate(test_cases, 1):
        print(f"Test {idx}: {test['description']}")
        try:
            response = requests.post(BASE_URL, json=test["payload"])
            print(f"Status: {response.status_code}")
            try:
                print("Response:", json.dumps(response.json(), indent=2), "\n")
            except json.JSONDecodeError:
                print("❌ Error: Non-JSON response")
                print("Raw response:", response.text[:300], "\n")
        except Exception as e:
            print(f"❌ Error connecting to API: {e}\n")

if __name__ == "__main__":
    run_tests()
