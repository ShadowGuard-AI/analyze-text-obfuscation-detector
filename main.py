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

def detect_base64_encoding(text):
    """
    Detects Base64 encoding obfuscation techniques.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if Base64 encoding is detected, False otherwise.
    """
    try:
        # The whole file is decoded as one blob, so a base64 string embedded
        # in surrounding prose is missed: with validate=True the spaces and
        # words around it fail the decode. Whole blob files are the case
        # this detector can actually judge.
        # Attempt to decode the text as Base64.  This is a heuristic; it might
        # produce garbage if the text isn't actually Base64, but we're just
        # looking for the *possibility* of obfuscation.  Reject anything that
        # isn't valid base64 encoding.

        # Remove padding first (padding is not needed)
        text = text.rstrip('=')

        # Add padding if necessary to make length a multiple of 4
        missing_padding = len(text) % 4
        if missing_padding:
            text += '=' * (4 - missing_padding)

        decoded_text = base64.b64decode(text, validate=True).decode('utf-8', 'ignore')

        # Check if the decoded text produces *something*. An empty decoded string is not helpful.
        if decoded_text:
            logging.debug("Base64 encoding detected.")
            return True
        else:
            return False

    except Exception as e:
        # Not a valid Base64 string or other error.
        logging.debug(f"Base64 detection failed: {e}")
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
            print(f"- {technique.replace('_', ' ').title()}: {'Detected' if detected else 'Not Detected'}")

    except SystemExit:
        raise
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
