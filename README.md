# Welcome to the documentation for SearchX
[View the full documentation here](https://red-3.gitbook.io/searchx)

SearchX — an alternative to the googlesearch-python library! SearchX provides a simple and efficient interface for performing search queries, image searches, and translations through Google.

## What is SearchX?

SearchX is a library that allows you to integrate the powerful search capabilities of Google into your Python projects. It is designed to provide an intuitive and extendable tool that gives you flexible control over search queries, images, and translations. SearchX simplifies interaction with Google, bypassing the need for bulky APIs.

## Key Features:

- **Search Queries:** Perform standard text search queries via Google.
- **Image Search:** Easily find images that match your queries.
- **Translations:** Use Google Translate to translate text between different languages.
- **Safe Mode:** Enable or disable safe search at your discretion.

## How to Get Started?

To start using SearchX, follow these steps:

### Installation:

Install the library via pip:

```bash
pip install searchx
```
### Usage Example:
Here’s a simple example of how to use SearchX for searching:

```python
from searchx import Client

client = Client()
results = client.search("Python programming")
print(results)
```
