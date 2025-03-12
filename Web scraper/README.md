# CVPR Scraper

A Python tool for scraping and analyzing papers from the Computer Vision and Pattern Recognition (CVPR) conference.

## Features

- Scrape paper information from CVPR conference website
- Extract titles, authors, and abstracts
- Generate simplified explanations of papers
- Export data to CSV and HTML formats
- Display papers in a readable format in the terminal

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cvpr-scraper.git
   cd cvpr-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Scraping Papers

To scrape papers from the CVPR conference website:

```bash
python main.py [number_of_papers]
```

For example, to scrape 50 papers:
```bash
python main.py 50
```

If no number is specified, the script will scrape 10 papers by default.

### Converting CSV to HTML

If you already have a CSV file with paper data, you can convert it to an HTML table:

```bash
python main.py csv2html path/to/your/file.csv [output.html]
```

If no output filename is specified, the script will use the same name as the input file with an .html extension.

## Project Structure

```
cvpr_scraper/
├── data/                  # Directory for storing scraped data
├── src/                   # Source code
│   ├── __init__.py        # Package initialization
│   ├── abstract_extractor.py  # Functions for extracting abstracts
│   ├── display_utils.py   # Utilities for displaying paper information
│   ├── explanation_generator.py  # Functions for generating paper explanations
│   ├── export_utils.py    # Utilities for exporting data to different formats
│   └── scraper.py         # Main scraping functionality
├── tests/                 # Test files (to be implemented)
├── main.py                # Main entry point
├── README.md              # This file
└── requirements.txt       # Required dependencies
```

## Output

The script generates two types of output files in the `data` directory:

1. CSV file: Contains all the scraped paper information
2. HTML file: A styled HTML table for easy viewing in a web browser

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 