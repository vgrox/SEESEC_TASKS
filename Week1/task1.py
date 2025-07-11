def analyze_text_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        
    lines = content.split('\n')
    total_lines = len(lines)
    
    words = content.split()
    total_words = len(words)
    
    total_characters = len(content)
    
    total_characters_no_whitespace = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
    
    return {
        'total_lines': total_lines,
        'total_words': total_words,
        'total_characters': total_characters,
        'total_characters_no_whitespace': total_characters_no_whitespace
    }

def print_analysis_results(results, filename):
    if results is None:
        return
    
    print("\n" + "="*50)
    print(f"TEXT FILE ANALYSIS: {filename}")
    print("="*50)
    print(f"Total number of lines: {results['total_lines']}")
    print(f"Total number of words: {results['total_words']}")
    print(f"Total number of characters (including spaces): {results['total_characters']}")
    print(f"Total number of characters (excluding whitespace): {results['total_characters_no_whitespace']}")
    print("="*50)

def main():
    print("Text File Analyzer")
    print("Enter the path to the .txt file you want to analyze:")
    
    while True:
        filename = input("File path: ").strip()
        
        if filename.startswith('"') and filename.endswith('"'):
            filename = filename[1:-1]
        elif filename.startswith("'") and filename.endswith("'"):
            filename = filename[1:-1]
        
        try:
            results = analyze_text_file(filename)
            print_analysis_results(results, filename)
            break
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Please try again.")
        except Exception as e:
            print(f"Error reading file: {e}. Please try again.")