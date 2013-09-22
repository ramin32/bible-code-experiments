import requests
import re
import json

books = None

try:
    with open('books.json') as books_file:
        books = json.loads(books_file.read())
except IOError:
    books = [
        {'name': 'Genesis'},
        {'name': 'Exodus'},
        {'name': 'Leviticus'},
        {'name': 'Numbers'},
        {'name': 'Deuteronomy'},
    ]
    sefaria_url = 'http://sefaria.org/api/texts/%s?commentary=0'
    sefaria_url_with_sections = 'http://sefaria.org/api/texts/%s.1-%s?commentary=0'

    for book in books:
        meta_data = requests.get(sefaria_url % book['name']).json()
        book['chapters'] = meta_data['length']
        data = requests.get(sefaria_url_with_sections % (book['name'], book['chapters'])).json()
        book['text'] = data['he']

    with open('books.json', 'w') as books_file:
        books_json = json.dumps(books, indent=4)
        books_file.write(books_json)


word = u'\u05ea\u05d5\u05e8\u05d4'
index = 0
last_occurance = None
entire_text = []
for book in books:
    for chapter_i, chapter in enumerate(book['text']):
        for verse_i, verse in enumerate(chapter):
            verse = re.sub(ur'[^\u0590-\u05EA]','', verse) # punctuation
            verse = re.sub(ur'[\u05b0-\u05c4]', '', verse) # vowels
            entire_text += [(char, book['name'], chapter_i, verse_i) for char in verse]

print entire_text
