# TLE API

Simple API that returns the position of a spacecraft based on a Two Line Element set (TLE).

## Installation

1. Clone this repo
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Visit the docs at: `http://127.0.0.1:8000/docs`

## Example Request

**POST** `/position`

Request body:

```json
{
  "line1": "1 25544U 98067A   08264.51782528  -.00002182  00000-0  -11606-4 0  2927",
  "line2": "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537",
  "timestamp": "2024-01-01T12:00:00"
}
```

> The `timestamp` field is optional. If omitted, the current time will be used.

## Example Response

```json
{
  "x": -599.34,
  "y": 2865.72,
  "z": 5364.12
}
```

## Running Tests

To run the tests, use the command:

```bash
pytest
```

Tests cover:

- Valid and invalid TLE input
- Empty or missing fields
- Optional and invalid timestamps
