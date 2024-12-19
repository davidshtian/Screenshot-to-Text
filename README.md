# Screenshot Analysis Tool

A Python tool that analyzes screenshots using Amazon Bedrock's AI model and generates detailed markdown reports viewable in a browser.

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
