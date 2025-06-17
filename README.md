# Gym Management System

An AI-powered gym management system that provides personalized workout plans, nutrition advice, and exercise details using the Groq LLM and MCP framework.

## Features

- Generate personalized workout plans
- Get nutrition advice based on goals and restrictions
- Access detailed exercise information
- Create custom workout plans
- Interactive chat interface with memory

## Prerequisites

- Python 3.8+
- Groq API key
- RapidAPI key for the workout planner API

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gym-management.git
cd gym-management
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```
GROQ_API_KEY=your_groq_api_key
RAPID_APIKEY=your_rapidapi_key
```

## Usage

1. Start the gym server:

```bash
python gym.py
```

2. In a separate terminal, run the client:

```bash
python client.py
```

3. Interact with the system using natural language commands like:

- "Generate a workout plan for weight loss"
- "What's the proper form for squats?"
- "Give me nutrition advice for muscle gain"
- "Create a custom workout plan for marathon training"

## Configuration

The system uses two main configuration files:

- `gym.json`: MCP server configuration
- `.env`: API keys and environment variables

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Groq for providing the LLM API
- RapidAPI for the workout planner API
- MCP framework for the server infrastructure
