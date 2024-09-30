import re
import json
import logging

logging.basicConfig(
    filename='bad_entries.log', 
    filemode='w',  # overwrites logs each time
    level=logging.WARNING, 
    format='%(levelname)s - %(message)s'
)

def read_clippings(file_path): 
    with open(file_path, 'r', encoding = 'utf-8') as file:
        content = file.read()

        # each entry in clippings is separated by ==========
        clippings = content.split("==========\n")
        return clippings

def extract_quote_info(clipping):
    lines = clipping.strip().split('\n')

    if len(lines) < 4:
        logging.warning(f"Not enough lines: {lines}")
        return None # skip if not a complete clipping
    
    # first line: book and author
    book_info = lines[0].strip()
    match = re.match(r"^(.*) \((.*)\)$", book_info)
    if not match: 
        logging.warning(f"No book info matched: {book_info} {lines}")
        return None # skip if book title and author missing
    title, author = match.groups()

    # second line: the date
    date_line = lines[1].strip()
    date_match = re.search(r"Added on (.+)$", date_line)

    if not date_match:
        logging.warning(f"No date matched: {date_line} {lines}")
        return None  # skip if the date is not found

    date = date_match.group(1)

    # third line: the quote
    quote = lines[3].strip()
    return { 'title': title,
            'author': author,
            'quote': quote,
            'date': date } 
            

def process_clippings(clippings):
    quotes = []
    for clipping in clippings:
        quote_info = extract_quote_info(clipping)
        if (quote_info):
            quotes.append(quote_info)
    return quotes

def save_to_json(quotes, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False, indent=4)
    
file_path = 'clippings.txt'
clippings = read_clippings(file_path)
totalClippings = len(clippings)
quotes = process_clippings(clippings)
totalQuotes = len(quotes)

print(f"Processed {str(totalQuotes)} quote{'s' [:totalQuotes > 1]} from {str(totalClippings)} clipping{'s' [:totalClippings > 1]}.")

if (totalClippings != totalQuotes):
    print(f'{totalClippings - totalQuotes} clippings could not be processed. Please see logs in bad_entries.log')

# Save to JSON file
save_to_json(quotes, 'quotes.json')