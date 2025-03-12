"""
Module for exporting paper information to different formats (HTML, CSV).
"""
import os
import pandas as pd

def export_to_html(df, output_file='cvpr2024_papers.html'):
    """
    Export the DataFrame to a styled HTML file.
    
    Args:
        df (pandas.DataFrame): DataFrame containing paper information
        output_file (str): Name of the output HTML file (default: 'cvpr2024_papers.html')
        
    Returns:
        str: Path to the created HTML file
    """
    # Ensure the output directory exists
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Update the output file path to be in the data directory
    output_file = os.path.join(output_dir, os.path.basename(output_file))
    
    # Define CSS styles for the HTML table
    html_style = """
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            vertical-align: top;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .abstract {
            max-height: 150px;
            overflow-y: auto;
            color: #555;
        }
        .explanation {
            color: #0066cc;
            font-style: italic;
        }
        .paper-title {
            font-weight: bold;
            color: #333;
        }
        .authors {
            color: #666;
        }
    </style>
    """
    
    # Create HTML header
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CVPR 2024 Papers</title>
        {html_style}
    </head>
    <body>
        <h1>CVPR 2024 Papers</h1>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Authors</th>
                    <th>Quick Take</th>
                    <th>Abstract</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Add each paper as a row in the table
    for _, paper in df.iterrows():
        title = paper.get('title', 'No title available')
        authors = paper.get('authors', 'No authors available')
        abstract = paper.get('abstract', 'Abstract not available')
        simple_explanation = paper.get('simple_explanation', 'No explanation available')
        
        # Create a table row for this paper
        html_content += f"""
                <tr>
                    <td class="paper-title">{title}</td>
                    <td class="authors">{authors}</td>
                    <td class="explanation">{simple_explanation}</td>
                    <td class="abstract">{abstract[:500]}{'...' if len(abstract) > 500 else ''}</td>
                </tr>
        """
    
    # Close the HTML tags
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Write the HTML content to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML table exported to '{output_file}'")
    return output_file

def csv_to_html(csv_file, output_html=None):
    """
    Convert an existing CSV file to an HTML table with styling.
    
    Args:
        csv_file (str): Path to the CSV file
        output_html (str, optional): Name of the output HTML file
        
    Returns:
        str: Path to the created HTML file or None if an error occurred
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        
        # If output HTML file name is not provided, use the CSV filename with .html extension
        if output_html is None:
            output_html = os.path.basename(csv_file).replace('.csv', '.html')
        
        # Export to HTML
        html_file = export_to_html(df, output_html)
        
        print(f"Successfully converted '{csv_file}' to HTML table at '{html_file}'")
        return html_file
    except Exception as e:
        print(f"Error converting CSV to HTML: {str(e)}")
        return None 