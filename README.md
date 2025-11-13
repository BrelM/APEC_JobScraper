# 💼 APEC Job Scraper

A web scraping application that retrieves job offers from the APEC (Association Pour l'Emploi des Cadres) website, specifically for Data Science positions in Paris. The application features a user-friendly Streamlit interface to browse and analyze scraped job listings.

## Overview

This project scrapes job offers from APEC's job search portal using Selenium and BeautifulSoup, then displays the results in an interactive web interface built with Streamlit. It specifically searches for data science positions in Paris (or other configurable locations).

## Features

- 🚀 Web scraping of APEC job listings using Selenium
- 📊 Interactive web interface powered by Streamlit
- 💾 Stores job data including title, company, description, salary, contract type, and publication date
- 🔗 Direct links to job postings
- ⚡ Real-time scraping with progress indicators
- 📈 Display results in a sortable data table

## Prerequisites

Before running the application, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Chrome browser** (required for Selenium web scraping)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd APEC_JobScraper
```

### 2. Create a virtual environment (optional but recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- **Streamlit** - Web application framework
- **Selenium** - Web automation and scraping
- **BeautifulSoup4** - HTML parsing
- **Pandas** - Data manipulation
- **webdriver-manager** - Automatic Chrome driver management

## Running the Application

### Launch the Streamlit app

```bash
streamlit run main.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`.

### Using the Application

1. **Open the interface** - The app displays "💼 APEC Job Scraper (Data science in Paris)" as the title
2. **Click "🚀 Launch Scraping"** - This button triggers the web scraper to fetch job offers from APEC
3. **Wait for completion** - A spinner appears showing "Scraping APEC job offers… please wait (10–15 s)…"
4. **View results** - Once complete, a success message shows the number of offers found
5. **Browse the table** - Job offers are displayed in an interactive data table with columns:
   - Title
   - Company
   - Description
   - Salary
   - Contract
   - Publication date
   - Link

## Configuration

You can customize the scraper by editing `src/scraper.py`:

### Location Filtering

```python
LOCATIONS = {
    "Paris"     : "75",
    "Belfort"   : "90",
    # Add more departments as needed
}
```

Change the selected location:
```python
choice = LOCATIONS.get("Paris", "75")  # Change "Paris" to another location
```

### Search Keywords

Modify the `BASE_URL` to search for different job titles or keywords. The current URL searches for "data science" positions.

## Project Structure

```
APEC_JobScraper/
├── main.py              # Streamlit web application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # License information
└── src/
    └── scraper.py      # Selenium web scraping module
```

## How It Works

1. **Selenium WebDriver** - Automates Chrome browser to access APEC's job search page
2. **Cookie Handling** - Automatically accepts cookie banners and consent modals
3. **BeautifulSoup Parsing** - Extracts job information from the HTML
4. **Data Processing** - Cleans and organizes job data, removes duplicates
5. **Streamlit Display** - Renders results in an interactive table

## Requirements

See `requirements.txt` for the complete list of dependencies. Key packages:
- `streamlit>=1.51.0`
- `selenium>=4.38.0`
- `beautifulsoup4>=4.14.2`
- `pandas>=2.3.3`
- `webdriver-manager>=4.0.2`

## Troubleshooting

### Chrome driver not found
The application uses `webdriver-manager` which automatically downloads the correct Chrome driver version. Ensure Chrome browser is installed.

### Connection timeout
If scraping fails with a timeout error, it may be due to:
- APEC website being down or inaccessible
- Network connectivity issues
- Website structure changes

Try running the scraper again or check APEC's website directly.

### Streamlit not found
Ensure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

## License

See LICENSE file for details.

## Author

BrelM

---

**Note**: This tool is for educational purposes. Respect APEC's terms of service and robots.txt when using this scraper.