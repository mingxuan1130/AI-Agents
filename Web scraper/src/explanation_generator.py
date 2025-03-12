"""
Module for generating simple explanations of papers based on titles and abstracts.
"""
import random

def generate_simple_explanation(title, abstract):
    """
    Generate a more engaging explanation of what the paper is trying to achieve.
    
    Args:
        title (str): The title of the paper
        abstract (str): The abstract of the paper
        
    Returns:
        str: A simplified, engaging explanation of the paper
    """
    try:
        if abstract == "Abstract not available":
            starters = [
                f"Want to know about {title.lower()}? This innovative paper explores",
                f"Diving into {title.lower()}, the researchers investigate",
                f"In an exciting development for {title.lower()}, this work presents",
                f"Curious about {title.lower()}? This research tackles",
                f"Breaking new ground in {title.lower()}, this study examines"
            ]
            return random.choice(starters) + " new approaches in this field."
        
        # Get the first two sentences of the abstract for more context
        sentences = abstract.split('.')[:2]
        if len(sentences) >= 2:
            context = '. '.join(sentences).strip() + '.'
        else:
            context = abstract.split('.')[0].strip() + '.'
            
        starters = [
            f"🔍 Exciting research alert! This paper tackles {title.lower()} by",
            f"🚀 Innovation in action: The team explores {title.lower()} through",
            f"💡 Breakthrough approach: This work revolutionizes {title.lower()} with",
            f"🎯 Research spotlight: A novel solution for {title.lower()} that",
            f"⭐ Key advancement: This study enhances {title.lower()} by"
        ]
        
        return f"{random.choice(starters)} {context}"
    except:
        return f"An innovative approach to {title.lower()}" 