import requests
import re
import json

books = None
sefaria_url = 'http://sefaria.org/api/texts/%s?commentary=0'
sefaria_url_with_sections = 'http://sefaria.org/api/texts/%s.1-%s?commentary=0'

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

    for book in books:
        meta_data = requests.get(sefaria_url % book['name']).json()
        book['chapters'] = meta_data['length']
        data = requests.get(sefaria_url_with_sections % (book['name'], book['chapters'])).json()
        book['text'] = data['he']

    with open('books.json', 'w') as books_file:
        books_json = json.dumps(books, indent=4)
        books_file.write(books_json)

def hebrew_letters_only(string):
    '''Removes vowelization, whitespace and punctuation.'''

    string = re.sub(ur'[^\u05D0-\u05EA]', '', string) 
    return string

def verify_code(book, first_letter, spacing, length):
    entire_text = hebrew_letters_only(''.join(book['text'][0]))
    first_index = entire_text.find(first_letter)
    return entire_text[first_index: first_index + (spacing * length): spacing]


print 'Genesis - "Torah" - from first "Tav" - every 50 letters:'
print verify_code(books[0], u'\u05ea', 50, 4)  
print 'Exodus - "Torah" - from first "Tav" - every 50 letters:'
print verify_code(books[1], u'\u05ea', 50, 4)  
print 'Leviticus - "YHWH" - from first "Yod" - every 8 letters:'
print verify_code(books[2], u'\u05d9', 8, 4)  
print 'Numbers - Torah - from first "He" - every 50 letters:'
print verify_code(books[3], u'\u05d4', 50, 4)  
print 'Deuteronomy - Torah - from first "He" -- every 50 letters:'
print verify_code(books[4], u'\u05d4', 50, 4)  

