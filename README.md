# Medium Markdown Fetcher

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=loncarales_medium-md-fetcher&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=loncarales_medium-md-fetcher)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=loncarales_medium-md-fetcher&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=loncarales_medium-md-fetcher)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=loncarales_medium-md-fetcher&metric=coverage)](https://sonarcloud.io/summary/new_code?id=loncarales_medium-md-fetcher)

A command-line tool and Python library for fetching Medium articles. This tool allows you to download articles from Medium using their URLs and save them as Markdown files for offline reading, archiving, or content repurposing.

## Features

- Download Medium articles by URL
- Save articles as Markdown format
- Support for batch processing multiple URLs
- Caching system to avoid redundant API calls
- Interactive mode for entering URLs
- Rich terminal output with progress indicators

## Requirements and Dependencies

### Core Requirements

- Python 3.13 or higher
- RapidAPI key for Medium API access (free tier: 150 requests/month)

### Python Dependencies

- click >= 8.2.1 - Command line interface creation
- diskcache >= 5.6.3 - Disk-based cache implementation
- pydantic >= 2.11.7 - Data validation and settings management
- python-dotenv >= 1.1.1 - Environment variable management
- requests >= 2.32.4 - HTTP requests
- rich >= 14.0.0 - Rich text and formatting in the terminal

### Development Dependencies

- pre-commit >= 4.2.0 - Git hook scripts
- pytest >= 8.4.1 - Testing framework
- ruff >= 0.12.4 - Fast Python linter and formatter

## Installation

### Prerequisites

1. **Python 3.13+**: Ensure you have Python 3.13 or higher installed.

2. **RapidAPI Key**: Sign up at [RapidAPI](https://rapidapi.com/) and subscribe to the [Medium API](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2) to get your API key.

### Option 1: Using mise (Recommended)

If you use [mise](https://mise.jdx.dev/) for managing Python versions and dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/medium-md-fetcher.git
cd medium-md-fetcher

# Install Python and dependencies with mise
mise use -g python@3.13

# Install project dependencies with uv
uv sync
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/medium-md-fetcher.git
cd medium-md-fetcher

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your RapidAPI key:

```
RAPIDAPI_KEY=your_rapidapi_key_here
```

Alternatively, you can pass the API key directly using the `--api-key` option.

## Usage

### Command Line Interface

The tool provides a command-line interface for downloading Medium articles:

```bash
# Download articles from URLs
python medium.py download --urls https://medium.com/article1-url https://medium.com/article2-url

# Download articles from a file (one URL per line)
python medium.py download --file articles.txt

# Interactive mode
python medium.py download --interactive

# Specify output directory
python medium.py download --urls https://medium.com/article-url --articles-path custom/output/path
```

### Options

- `--urls, -u`: Medium URLs to download (can be used multiple times)
- `--file, -f`: File containing URLs (one per line)
- `--interactive, -i`: Interactive URL input
- `--api-key`: RapidAPI key (overrides environment variable)
- `--cache-path`: Cache database path (default: "data/cache")
- `--articles-path`: Saved articles path (default: "data/articles")
- `--verbose, -v`: Verbose output

### Python API

You can also use the library programmatically in your Python code:

```python
import os
from src.medium_api_client.client import MediumAPIClient

# Load API key from environment
api_key = os.getenv('RAPIDAPI_KEY')

# Create client
client = MediumAPIClient(api_key=api_key)

# Get article by URL
article_url = "https://medium.com/@author/article-title-123abc"
article = client.get_article_by_url(article_url)

if article:
    print(f"Title: {article.title}")
    print(f"Author: {article.author}")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/medium-md-fetcher.git
cd medium-md-fetcher

# Install Python and dependencies with mise
mise use -g python@3.13

# Install development dependencies
uv pip sync
```

### Code Formatting and Linting

The project uses ruff for code formatting and linting:

```bash
# Format code
make format

# Lint code
make lint
```

### Running Tests

```bash
# Run all tests
pytest tests/
```

## 🧾 License

MIT License. See the [LICENSE](LICENSE) file.

## Credits

- [Medium API on RapidAPI](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2) - API for accessing Medium content
- Put together with ❤️ by Aleš Lončar

## Contributing

Issues, feedback, and PRs are welcome. Fork and submit your ideas!

### Code Style

- Follow PEP 8 guidelines
- Use ruff for formatting and linting
- Write docstrings for all functions, classes, and modules
- Add type hints where appropriate
- Write tests for new features and bug fixes
