import colorama 
import os
import argparse
import re

def remove_images(func):
    def wrapper(content):
        pattern = r'!\[[^\]]+\]\([^)]+\)({[^}]+})?'
        func(re.sub(pattern, '', content))
    return wrapper

def remove_links(func):
    def wrapper(content):
        pattern = r'\[[^\]]+\]\([^)]+\)({[^}]+})?'
        func(re.sub(pattern, '', content))
    return wrapper


def remove_code(func):
    def wrapper(content):
        pattern1 = re.compile('```[^`]*```', re.MULTILINE)
        tempo = re.sub(pattern1, '', content)
        pattern2 = r'`[^`]+`'
        func(re.sub(pattern2, '', tempo))
    return wrapper

@remove_images
@remove_links
@remove_code
def filename_extension_not_in_backticks(content):
    pattern = r'([^A-Z0-9]\.[A-Z]{2})'
    lines = content.splitlines()
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE):
            print("file name extension not in backticks: " + line)

def missing_utm_parameters(content):
    pattern = r'https://(tm-|opentestfactory|squashtest|henix)'
    lines = content.splitlines()
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE):
            if "?utm_source=Doc_AUTOM_DEVOPS&utm_medium=link" not in line:
                print("missing utm parameters: " + line)

def missing_blank_target(content):
    pattern = r'https?:/'
    lines = content.splitlines()
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE):
            if '{:target="_blank"}' not in line:
                print("missing blank target: " + line)

def process_md_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"Processing file: {file_path}")
                        filename_extension_not_in_backticks(content)
                        missing_utm_parameters(content)
                        missing_blank_target(content)
                except IOError as e:
                    print(f"Error reading file {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing file {file_path}: {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Recursively process .md files in a specified directory.")
    parser.add_argument("directory", help="The directory containing .md files to process")
    
    # Parse arguments
    args = parser.parse_args()

    # Check if the specified directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: The specified directory '{args.directory}' does not exist.")
        exit(1)

    # Process the files
    process_md_files(args.directory)
    