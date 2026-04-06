# Splitaroo

Splitaroo is a web API that takes a photo of a receipt, extracts the items and prices using AI, and calculates how much each person owes based on what they ordered. No more manual math or awkward Venmo guesswork.

## How It Works

1. **Upload a receipt** — Send a photo of your receipt to the `/receipt/uploadReciept` endpoint. An OpenAI vision model extracts the items and prices into structured data.
2. **Describe who got what** — Send a plain-text description (e.g. "Bob and Alice split the burger, Carol got the salad") to `/receipt/unstructuredData`. The AI parses it into a structured breakdown.
3. **Get the split** — Send the itemized receipt and the split breakdown to `/receipt/get_split`. The API returns a dictionary of each person and what they owe.

## Project Structure

```
app/
  main.py                  # FastAPI app entrypoint
  api/routes/routers.py    # API route definitions
  core/
    llm.py                 # OpenAI integration for receipt parsing
    calculations.py        # Split calculation logic
  schemas/models.py        # Pydantic data models
```

## Setup

**Requirements:** Python 3.13+

```bash
# Install dependencies
pip install -e .

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Run the server
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/receipt/uploadReciept` | Upload a receipt image, returns itemized data |
| POST | `/receipt/unstructuredData` | Parse free-text description of who got what |
| POST | `/receipt/get_split` | Calculate the per-person split |

Interactive API docs are available at `/docs` when the server is running.
