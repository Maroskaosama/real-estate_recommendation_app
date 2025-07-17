# Real Estate Chatbot

A smart chatbot that helps users find and compare real estate properties in Egypt. The chatbot supports both text and voice interactions, making it easy to search for properties based on various criteria.

## Features

- 🗨️ **Chatbot Interface**: Text and voice-based interaction
- 🔍 **Filter by Budget**: Find properties within your budget
- 📐 **Filter by Area**: Search for properties by size
- 💰 **Filter by Price/m²**: Find properties with good value per square meter
- 🏘️ **Compare Properties**: Compare two or more properties side by side
- 🧾 **Show Listing Details**: View detailed information about specific properties
- 💾 **Save Favorites**: Save interesting properties for later reference
- 🗣️ **Text-to-Speech**: Hear responses in voice mode
- 🎙️ **Speech Recognition**: Speak your queries in voice mode

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have the `egypt_House_prices.csv` file in the project directory

## Usage

Run the chatbot:
```bash
python main.py
```

### Text Mode Commands

- Filter by budget: "show me houses under 2 million"
- Filter by area: "I want a house with at least 150 m²"
- Filter by price per m²: "show properties with price per m² under 10000"
- Compare properties: "compare properties 123 and 456"
- Show details: "show details for property 123"
- Save to favorites: "save property 123 to favorites"
- Remove from favorites: "remove property 123 from favorites"

### Voice Mode

- Say "voice" to switch to voice mode
- Say "text" to switch back to text mode
- Speak your queries naturally
- Say "quit" to exit

## Data Format

The chatbot expects a CSV file named `egypt_House_prices.csv` with the following columns:
- id: Property ID
- type: Property type (apartment, villa, etc.)
- city: City location
- compound: Compound name
- price: Property price
- area: Property area in square meters
- bedrooms: Number of bedrooms
- bathrooms: Number of bathrooms
- furnished: Whether the property is furnished

## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- python-dotenv
- spacy
- pyttsx3
- SpeechRecognition
- matplotlib
- seaborn

## Contributing

Feel free to submit issues and enhancement requests! 