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
    print book['name']
    entire_text = hebrew_letters_only(''.join(book['text'][0]))
    first_index = entire_text.find(first_letter)
    print "Starting from the first %s every %s letters:" % (first_letter, spacing)
    print "%s: %s" % (first_index, entire_text[first_index: first_index + (spacing * length): spacing])


verify_code(books[0], u'\u05ea', 50, 4)  
verify_code(books[1], u'\u05ea', 50, 4)  
verify_code(books[2], u'\u05d9', 8, 4)  
verify_code(books[3], u'\u05ea', 50, 4)  
verify_code(books[4], u'\u05d4', 50, 4)  

entire_text = hebrew_letters_only(''.join([verse for book in books for chapter in book['text'] for verse in chapter]))
torah_re = re.compile(ur'\u05ea.{49}\u05d5.{49}\u05e8.{49}\u05d4.{49}') 

# all occurences of a "torah"
result = torah_re.findall(entire_text)
torah_in_hebrew = u'\u05ea\u05d5\u05e8\u05d4'
print "%s occurences of %s found in the entire bible." % (len(result), torah_in_hebrew)

# all occurences of a "torah" backwards
result = torah_re.findall(entire_text[::-1])
print "%s backward occurences of %s found in the entire bible." % (len(result), torah_in_hebrew)



