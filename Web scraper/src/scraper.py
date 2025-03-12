"""
Main scraper module for fetching CVPR conference papers.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import os
from .abstract_extractor import get_paper_abstract
from .explanation_generator import generate_simple_explanation
from .display_utils import display_as_blocks, format_paper_info
from .export_utils import export_to_html

def scrape_cvpr_papers(num_papers=50):
    """
    Scrape papers from the CVPR conference website.
    
    Args:
        num_papers (int): Number of papers to scrape (default: 50)
        
    Returns:
        pandas.DataFrame: DataFrame containing the scraped paper information
    """
    base_url = "https://openaccess.thecvf.com/"
    url = f"{base_url}CVPR2024?day=all"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = []
        
        # Find all paper entries (both title and content)
        paper_entries = []
        for dt in soup.find_all('dt', class_='ptitle'):
            if dt.find_next_sibling('dd'):
                paper_entries.append((dt, dt.find_next_sibling('dd')))
        
        # Limit to the first num_papers
        paper_entries = paper_entries[:num_papers]
        
        print(f"\nScraping the first {num_papers} papers from CVPR 2024...")
        for dt, dd in tqdm(paper_entries, desc="Scraping papers", total=num_papers):
            try:
                paper_info = {
                    'title': 'No title available',
                    'authors': 'No authors available',
                    'abstract': 'Abstract not available',
                    'simple_explanation': 'No explanation available'
                }
                
                # Extract paper title
                title_link = dt.find('a')
                if title_link:
                    paper_info['title'] = title_link.text.strip()
                else:
                    paper_info['title'] = dt.text.strip()
                
                # Extract authors
                authors = dd.find_all('a')
                if authors:
                    paper_info['authors'] = ', '.join([author.text.strip() for author in authors])
                
                # Get abstract
                if title_link and 'href' in title_link.attrs:
                    paper_url = f"{base_url.rstrip('/')}/{title_link['href'].lstrip('/')}"
                    paper_info['abstract'] = get_paper_abstract(paper_url)
                    time.sleep(0.5)
                
                # Generate simple explanation
                paper_info['simple_explanation'] = generate_simple_explanation(
                    paper_info['title'],
                    paper_info['abstract']
                )
                
                papers.append(paper_info)
                
            except Exception as e:
                print(f"\nError processing paper: {str(e)}")
                continue
        
        if not papers:
            print("No papers were successfully scraped.")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(papers)
        
        # Save to CSV with proper encoding and all columns
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'cvpr2024_first_{num_papers}_papers.csv')
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\nSuccessfully scraped {len(papers)} papers. Data saved to '{output_file}'")
        print("\nDisplaying papers in blocks:")
        
        # Display papers in a block format
        display_as_blocks(df, papers_per_row=4)
        
        # Export to HTML
        html_file = export_to_html(df, f'cvpr2024_first_{num_papers}_papers.html')
        
        # Display DataFrame info to confirm all columns are present
        print("\nDataFrame Information:")
        print(df.info())
        
        return df
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 