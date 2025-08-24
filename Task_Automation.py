import re
import os
import argparse
from pathlib import Path
import csv
from typing import List, Set

def extract_emails(text: str) -> Set[str]:
    """
    Extract all valid email addresses from text using regex
    """
    # Comprehensive email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return set(emails)  # Remove duplicates

def read_file(file_path: str) -> str:
    """
    Read content from a text file with error handling
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied to read '{file_path}'.")
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except:
            raise ValueError(f"Could not decode file '{file_path}'. Please check the file encoding.")

def save_emails(emails: Set[str], output_path: str, format: str = 'txt') -> None:
    """
    Save extracted emails to a file in specified format
    """
    if not emails:
        print("No email addresses found to save.")
        return

    try:
        if format.lower() == 'csv':
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Email Address'])
                for email in sorted(emails):
                    writer.writerow([email])
        else:
            with open(output_path, 'w', encoding='utf-8') as file:
                for email in sorted(emails):
                    file.write(email + '\n')
        
        print(f"Successfully saved {len(emails)} email addresses to {output_path}")
        
    except Exception as e:
        raise Exception(f"Error saving to file: {e}")

def process_file(input_file: str, output_file: str = None, format: str = 'txt') -> None:
    """
    Process a single file to extract and save emails
    """
    print(f"\n Processing file: {input_file}")
    
    # Read file content
    try:
        content = read_file(input_file)
    except Exception as e:
        print(f" Error reading file: {e}")
        return
    
    # Extract emails
    emails = extract_emails(content)
    
    if not emails:
        print(" No email addresses found in the file.")
        return
    
    print(f" Found {len(emails)} unique email address(es)")
    
    # Display found emails
    print("\n Extracted emails:")
    for i, email in enumerate(sorted(emails), 1):
        print(f"  {i:2d}. {email}")
    
    # Determine output filename if not provided
    if not output_file:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_emails.{format}"
    
    # Save emails
    try:
        save_emails(emails, output_file, format)
    except Exception as e:
        print(f" Error saving results: {e}")

def process_directory(directory: str, output_dir: str = None, format: str = 'txt') -> None:
    """
    Process all .txt files in a directory
    """
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f" Directory '{directory}' does not exist.")
        return
    
    txt_files = list(directory_path.glob('*.txt'))
    
    if not txt_files:
        print(f" No .txt files found in '{directory}'.")
        return
    
    print(f" Found {len(txt_files)} .txt file(s) in directory")
    
    # Create output directory if specified and doesn't exist
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    for txt_file in txt_files:
        if output_dir:
            output_file = Path(output_dir) / f"{txt_file.stem}_emails.{format}"
        else:
            output_file = None
        
        process_file(str(txt_file), str(output_file) if output_file else None, format)
        print("-" * 50)

def main():
    """Main function to run the email extractor"""
    parser = argparse.ArgumentParser(
        description="Extract email addresses from text files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.txt
  %(prog)s document.txt -o emails.csv -f csv
  %(prog)s ./documents -d -o ./output -f txt
        """
    )
    
    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('-o', '--output', help='Output file or directory path')
    parser.add_argument('-f', '--format', choices=['txt', 'csv'], default='txt',
                       help='Output format (txt or csv)')
    parser.add_argument('-d', '--directory', action='store_true',
                       help='Process all .txt files in directory')
    
    args = parser.parse_args()
    
    print(" Email Address Extractor")
    print("=" * 40)
    
    try:
        if args.directory:
            process_directory(args.input, args.output, args.format)
        else:
            process_file(args.input, args.output, args.format)
            
    except KeyboardInterrupt:
        print("\n\n  Operation cancelled by user.")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
    
    print("\n Email extraction completed!")

if __name__ == "__main__":
    main()

