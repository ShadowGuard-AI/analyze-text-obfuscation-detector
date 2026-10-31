import argparse
import logging
import pandas as pd
import re
import sys
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description='Analyze text for obfuscation techniques.')
    parser.add_argument('input_file', type=str, help='Path to the input text file.')
    parser.add_argument('-o', '--output_file', type=str, help='Path to the output CSV file for results.', default='obfuscation_analysis.csv')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging.')
    return parser.parse_args()

def detect_character_substitution(text):
    """
    Detects character substitution obfuscation techniques.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if character substitution is detected, False otherwise.
    """
    # Leet digits that stand in for letters: 1, 0, 3, 4, 5, 7.
    # A digit only counts inside a token that also holds a letter. Testing
    # the raw text for any of these digits, as an earlier version did,
    # flagged ordinary prose such as "call 2024 now" as substitution.
    for token in re.findall(r"[A-Za-z0-9]+", text):
        if any(ch.isalpha() for ch in token) and any(ch in "013457" for ch in token):
            logging.debug(f"Character substitution suspected in token: {token}")
            return True
    return False

def _whole_blob_decodes(text):
    """Original whole text test: decode the text as one base64 blob."""
    try:
        stripped = text.strip().rstrip('=')
        missing_padding = len(stripped) % 4
        if missing_padding:
            stripped += '=' * (4 - missing_padding)
        decoded_text = base64.b64decode(stripped, validate=True).decode('utf-8', 'ignore')
        return bool(decoded_text)
    except Exception as e:
        logging.debug(f"Base64 blob detection failed: {e}")
        return False


def _token_decodes(token):
    """Test one candidate token extracted from running text.

    A token counts only when it is canonical base64 (re-encoding the
    decoded bytes reproduces the token) and the decoded bytes are
    readable text. That keeps long ordinary words from counting.
    """
    try:
        padded = token + '=' * (-len(token) % 4)
        decoded_bytes = base64.b64decode(padded, validate=True)
        if not decoded_bytes:
            return False
        decoded_text = decoded_bytes.decode('utf-8')
        if not decoded_text or not decoded_text.isprintable():
            return False
        return base64.b64encode(decoded_bytes).decode('ascii') == padded
    except Exception:
        return False


def detect_base64_encoding(text):
    """
    Detects Base64 encoding obfuscation techniques.

    The whole text is tested as one blob, and candidate base64 tokens
    embedded in the text are also extracted and tested one by one, so
    a base64 string inside ordinary prose is detected as well.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if Base64 encoding is detected, False otherwise.
    """
    if _whole_blob_decodes(text):
        logging.debug("Base64 encoding detected in the whole text.")
        return True
    for token in re.findall(r"[A-Za-z0-9+/]{16,}={0,2}", text):
        if _token_decodes(token):
            logging.debug("Base64 encoding detected in an embedded token.")
            return True
    return False

def detect_whitespace_insertion(text):
    """
    Detects whitespace insertion obfuscation techniques.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if whitespace insertion is detected, False otherwise.
    """
    # Check for excessive whitespace.
    if re.search(r'\s{3,}', text):  # Three or more consecutive whitespace characters.
        logging.debug("Whitespace insertion detected.")
        return True
    return False

def analyze_text(text):
    """
    Analyzes the given text for various obfuscation techniques.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    results = {
        'character_substitution': detect_character_substitution(text),
        'base64_encoding': detect_base64_encoding(text),
        'whitespace_insertion': detect_whitespace_insertion(text),
    }
    # Severity comes from how many of the three checks hit:
    # 0 is none, 1 is low, 2 is medium, and 3 is high.
    hit_count = sum(1 for value in results.values() if value)
    results['severity'] = {0: 'none', 1: 'low', 2: 'medium', 3: 'high'}[hit_count]
    return results

def main():
    """
    Main function to execute the text obfuscation analysis.
    """
    try:
        args = setup_argparse()

        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug("Verbose logging enabled.")

        # Input file path from command line
        input_file_path = args.input_file

        # Output file path from command line
        output_file_path = args.output_file

        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            logging.error(f"Input file not found: {input_file_path}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error reading input file: {e}")
            sys.exit(1)

        # Perform the analysis
        analysis_results = analyze_text(text)

        # Convert the results to a Pandas DataFrame
        df = pd.DataFrame([analysis_results])

        # Save the results to a CSV file
        try:
            df.to_csv(output_file_path, index=False)
            logging.info(f"Analysis results saved to: {output_file_path}")
        except Exception as e:
            logging.error(f"Error saving results to CSV: {e}")
            sys.exit(1)

        # Print a summary of the results
        print("\nAnalysis Summary:")
        for technique, detected in analysis_results.items():
            if technique == 'severity':
                print(f"- Severity: {detected}")
            else:
                print(f"- {technique.replace('_', ' ').title()}: {'Detected' if detected else 'Not Detected'}")

    except SystemExit:
        raise
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
