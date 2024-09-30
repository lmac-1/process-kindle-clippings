# Kindle clippings processor

This is a Python script that processes your Kindle clippings file into a JSON file in the following format:

```
[
    {
        "title": "Title of book",
        "author": "Name of author",
        "quote": "Quote you highlighted in Kindle",
        "date": "Date and time"
    },
    ...
]
```

## How to use

1. Fork the repo
2. Add your clippings file to the project and name the file `clippings.txt`
3. Run the python script: `python3 main.py`

This will output a `quotes.json` file.
