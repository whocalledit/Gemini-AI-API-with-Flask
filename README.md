Gemini AI API with Flask — Code Explanation, Idea Generation & More

---

A Python Flask API integrating Google Gemini AI model for tasks like code explanation, idea generation, tone detection, and image captioning. Ready to deploy and extend!

---

````markdown
# Gemini AI API with Flask

A lightweight Python Flask API that integrates Google’s Gemini AI model to perform multiple NLP tasks such as:

- Code explanation  
- Idea generation  
- Tone detection  
- Image captioning

This project serves as a backend API to interact with Gemini AI through RESTful endpoints. It’s designed to be easily deployable, extendable, and ready for integration into your applications.

---

## Features

- Uses Gemini API for generating AI-powered responses  
- Supports multiple tasks with structured inputs  
- Simple Flask server with clean codebase  
- Ready for deployment on Railway, Replit, or similar platforms  
- Includes test script for quick validation  

---

## Getting Started

### Prerequisites

- Python 3.7+  
- Gemini API key (from Google Cloud Generative AI API)  
- `pip` package manager  

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gemini-ai-flask-api.git
   cd gemini-ai-flask-api
````

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your Gemini API key in an environment variable:

   ```bash
   export GEMINI_API_KEY="your_actual_api_key"  # Windows: set GEMINI_API_KEY=your_actual_api_key
   ```

### Running the API

Start the Flask server:

```bash
python main.py
```

The API will be available at `http://localhost:5000`.

### Testing the API

Run the test script to validate functionality:

```bash
python test.py
```

---

## API Usage

### Endpoint: `/api/gemini`

* **Method:** POST
* **Request JSON body:**

```json
{
  "task": "code_explain",   // or "idea_generator", "tone_detector", "image_caption"
  "input": "your input text or image URL"
}
```

* **Response:**

```json
{
  "status": "success",
  "task": "code_explain",
  "input": "...",
  "output": "...",
  "timestamp": "..."
}
```

---

## Project Structure

```
├── main.py        # Flask API server
├── test.py        # Test script for API endpoints
├── requirements.txt
├── README.md
```

---

## Deployment

Recommended platforms that don’t require a credit card:

* [Railway.app](https://railway.app/)
* [Replit.com](https://replit.com/)

Simply push your repo and configure environment variables to deploy.

---

## Notes

* The image caption task currently cannot process image URLs fully due to Gemini model limitations.
* Ensure your Gemini API key has proper permissions for the generative AI API.

---

## License

MIT License © 2025 Hiranmay Roy
---

## Contact

Feel free to open issues or submit pull requests.
For questions, reach out at [hiranmayroy183@gmail.com](mailto:hiranmayroy183@gmail.com)