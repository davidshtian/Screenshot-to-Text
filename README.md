# Screenshot-to-Text Analysis Tool

A Python tool that analyzes screenshots using Amazon Bedrock's AI models and generates detailed markdown reports viewable in a browser.

*Screenshot:*

<img width="396" alt="image" src="https://github.com/user-attachments/assets/40634de6-cd87-49f7-aeeb-5d07ff970446" />

*Result:*

<img width="472" alt="image" src="https://github.com/user-attachments/assets/dc419a71-c185-4867-bb1d-8dfa291ca55e" />


## Features

- Captures screenshots from clipboard
- Analyzes images using Amazon Bedrock's nova-lite-v1 model
- Generates detailed reports in markdown format
- Converts reports to styled HTML
- Opens results automatically in Chrome browser
- Maintains analysis history in user's home directory
- Automatic cleanup of old analysis files

## Prerequisites

- Python 3.7+
- Google Chrome browser (recommended)
- AWS credentials configured with Bedrock access
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd screenshot-analysis-tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure AWS credentials are configured with appropriate Bedrock access:
```bash
aws configure
```

## Usage
1. Take a screenshot or copy an image to your clipboard
2. Run the script:
```bash
python app.py
```

3. The analysis will automatically open in your default browser

> Or like myself I create a quick script using Automator on Mac.
<img width="118" alt="image" src="https://github.com/user-attachments/assets/2af8b983-4658-4a59-99a4-ae979743efff" />


## Output Location
Analysis reports are stored in:

- Windows: ```C:\Users\[username]\screenshot_analysis\```
- macOS/Linux: ```~/screenshot_analysis/```

## Configuration
The tool uses the following default settings:

- Model: ```amazon.nova-lite-v1:0```
- Output format: HTML with custom CSS styling
- Browser: Chrome (falls back to default browser if Chrome isn't available)
