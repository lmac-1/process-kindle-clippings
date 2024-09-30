# Kindle clippings processor

This is a Python script that processes your Kindle clippings file into a JSON file in the following format:

```
{
    "quotes": [
        {
            "title": "Title of book",
            "author": "Name of author",
            "quote": "Quote you highlighted in Kindle",
            "date": "Date and time"
        },
        ...
    ],
    "authors": ['Author name', ...]
    "books": ['Book name', ...]
}
```

## How to use

1. Fork the repo
2. Add your clippings file to the project and name the file `clippings.txt`
3. Run the python script: `python3 main.py`

This will output the following file(s):

- `quotes.json` file with quotes, authors and books in JSON format
- `bad_entries.log` file, if there were any clippings that couldn't be processed
