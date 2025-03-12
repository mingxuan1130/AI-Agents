#!/usr/bin/env python3
"""
Main entry point for the CVPR Scraper application.
"""
import sys
import os
import pandas as pd

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper import scrape_cvpr_papers
from src.export_utils import csv_to_html

def print_usage():
    """Print usage instructions for the script."""
    print("CVPR Scraper - A tool for scraping CVPR conference papers")
    print("\nUsage:")
    print("  python main.py [number_of_papers]")
    print("  python main.py csv2html input.csv [output.html]")
    print("\nExamples:")
    print("  python main.py 50           # Scrape 50 papers from CVPR 2024")
    print("  python main.py csv2html data/my_papers.csv  # Convert CSV to HTML")

def main():
    """Main function to handle command line arguments and execute the appropriate action."""
    # Check if there are command line arguments
    if len(sys.argv) > 1:
        # If the first argument is 'csv2html', convert an existing CSV to HTML
        if sys.argv[1].lower() == 'csv2html' and len(sys.argv) > 2:
            csv_file = sys.argv[2]
            output_html = sys.argv[3] if len(sys.argv) > 3 else None
            csv_to_html(csv_file, output_html)
        # If the first argument is a number, use it as the number of papers to scrape
        elif sys.argv[1].isdigit():
            num_papers = int(sys.argv[1])
            scrape_cvpr_papers(num_papers)
        # If the argument is 'help' or '-h', print usage instructions
        elif sys.argv[1].lower() in ['help', '-h', '--help']:
            print_usage()
        else:
            print("Invalid argument.")
            print_usage()
    else:
        # Default: scrape 10 papers
        scrape_cvpr_papers(10)

if __name__ == "__main__":
    main() 