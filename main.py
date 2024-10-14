import re
import json
import logging
from datetime import datetime

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
    
def process_author_name(author): 
    # Split the author name by comma (if it exists)
    parts = author.split(', ')
    
    if len(parts) == 2:
        surname, firstname = parts
        # Return the author name as "firstname surname"
        return f"{firstname} {surname}"
    else:
        # If name doesn't match the format, return it as is
        return author

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
    book, author_raw = match.groups()
    author = process_author_name(author_raw)
    
    # second line: the date
    date_line = lines[1].strip()
    date_match = re.search(r"Added on (.+)$", date_line)

    if not date_match:
        logging.warning(f"No date matched: {date_line} {lines}")
        return None  # skip if the date is not found

    date_string = date_match.group(1)
    date_format = "%A, %d %B %Y %H:%M:%S"
    date = datetime.strptime(date_string, date_format)
    formatted_date = date.strftime("%d/%m/%Y")

    # third line: the quote
    quote = lines[3].strip()
    return { 'book': book,
            'author': author,
            'quote': quote,
            'date': formatted_date } 
            

def process_clippings(clippings):
    quotes = []
    authors_set = set()
    books_set = set()
    
    for clipping in clippings:
        quote_info = extract_quote_info(clipping)
        
        if (quote_info):
            quotes.append(quote_info)
            
            # Add unique author to the set
            author = quote_info["author"]
            authors_set.add(author)
            
            # create list of unique books
            book = quote_info["book"]
            books_set.add(book)
                
    return {
        "quotes": quotes, 
        "authors": sorted(authors_set), # sorted alphabetically
        "books": sorted(books_set)      # sorted alphabetically
    }

def save_to_json(quotes, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False, indent=4)
    
file_path = 'clippings.txt'
clippings = read_clippings(file_path)
totalClippings = len(clippings)

processed_clippings = process_clippings(clippings)
quotes = processed_clippings["quotes"]
authors = processed_clippings["authors"]
books = processed_clippings["books"]
totalQuotes = len(quotes)

print(f"Processed {str(totalQuotes)} quote{'s' [:totalQuotes > 1]} from {str(totalClippings)} clipping{'s' [:totalClippings > 1]}.")
print(f"{str(len(authors))} authors and {str(len(books))} books found")
if (totalClippings != totalQuotes):
    print(f'{totalClippings - totalQuotes} clippings could not be processed. Please see logs in bad_entries.log')

output = {
    "quotes": quotes,
    "authors": authors,
    "books": books
}

# Save to JSON file
save_to_json(output, 'quotes.json')