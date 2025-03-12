"""
Module for displaying paper information in various formats.
"""

def format_paper_info(paper):
    """
    Format paper information for display in the terminal.
    
    Args:
        paper (dict): Dictionary containing paper information
        
    Returns:
        str: Formatted string representation of the paper
    """
    try:
        title = paper.get('title', 'No title available')
        authors = paper.get('authors', 'No authors available')
        abstract = paper.get('abstract', 'Abstract not available')
        simple_explanation = paper.get('simple_explanation', 'No explanation available')
        
        return (
            f"\n{'='*120}\n"
            f"📑 Title: {title}\n"
            f"👥 Authors: {authors}\n"
            f"\n📝 Abstract:\n{abstract[:500]}{'...' if len(abstract) > 500 else ''}\n"
            f"\n💫 Quick Take:\n{simple_explanation}\n"
            f"{'='*120}"
        )
    except Exception as e:
        return f"Error formatting paper info: {str(e)}"

def display_as_blocks(df, papers_per_row=4):
    """
    Display the DataFrame in a block format with multiple papers per row.
    
    Args:
        df (pandas.DataFrame): DataFrame containing paper information
        papers_per_row (int): Number of papers to display per row (default: 4)
    """
    total_papers = len(df)
    for start_idx in range(0, total_papers, papers_per_row):
        end_idx = min(start_idx + papers_per_row, total_papers)
        row_papers = df.iloc[start_idx:end_idx]
        
        # Print titles in one row
        print("\n" + "="*120)
        for _, paper in row_papers.iterrows():
            print(f"\n📑 {paper['title'][:50]}...")
        
        # Print authors in one row
        print("\n" + "-"*120)
        for _, paper in row_papers.iterrows():
            print(f"\n👥 {paper['authors'][:50]}...")
        
        # Print explanations in one row
        print("\n" + "-"*120)
        for _, paper in row_papers.iterrows():
            print(f"\n💫 {paper['simple_explanation'][:100]}...")
        
        print("\n" + "="*120 + "\n") 