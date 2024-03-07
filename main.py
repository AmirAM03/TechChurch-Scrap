import json
import sys
import time

import texttable

import WebHandler
import DBController
import threading



categories = {'apps': 577051039, 'startups': 20429, 'venture': 577030455, 'security': 21587494, 'ai': 577047203, 'cryptocurrency': 576601119, 'fintech': 577030453}


def print_results_table(magazines_list):
    table = texttable.Texttable(120)
    table.set_cols_align(["c", "c", "c", "c", "c", "c"])
    table.set_cols_dtype(["t", "t", "t", "t", "t", "t"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m"])
    table.add_row(
        ["Title", "Author(s)", "Category/Subject", "Tags", "Publication Date", "Link"])
    for record in magazines_list:
        tmp = record["yoast_head_json"]
        try :  # This catching is for when one of this fields is empty and not existed in parsed response
            table.add_row([tmp['title'], tmp['author'], tmp['schema']['@graph'][0]['articleSection'], tmp["schema"]["@graph"][0]['keywords'] if 'keywords' in tmp["schema"]["@graph"][0].keys() else '',
                           record['date'], record['link']])
        except :
            print("Special data returned from tech crunch. Can't be parsed in our tables")
            print(tmp["schema"]["@graph"][0])
            
    print(table.draw())

def periodically_scrap():
    while True:
        #DBController.clean_db_table('magazines')
        time.sleep(3600)
        for category in list(categories.values()):
            resp = WebHandler.get_certain_subject_publications(category,1)
            DBController.insert_magazine_records_to_db(resp['body'])
        print('periodically scraping worker finished successfully ...')



def enable_auto_scraper():
    worker = threading.Thread(target=periodically_scrap)
    worker.daemon = True
    worker.start()
    print('auto scrapper turned on !')

def show_subject_selection_menu():
    print('Nice, Welcome to the subject selection section. '
          'Please select your intended fetching procedure based on following guid table')

    tableObj = texttable.Texttable(120)
    tableObj.set_cols_align(["c", "c"])
    tableObj.set_cols_dtype(["i", "t"])
    tableObj.set_cols_valign(["m", "m"])
    tableObj.add_rows([
        ["Activation Key", "Subject"],
        [1, 'Live Fetching From Website'],
        [2, 'Fetching From DB (Stored Records)']
    ])
    print(tableObj.draw())
    online = input('Your selection option: ')

    print('Please select your intended subject based on following guid table')

    tableObj = texttable.Texttable(120)
    tableObj.set_cols_align(["c", "c"])
    tableObj.set_cols_dtype(["i", "t"])
    tableObj.set_cols_valign(["m", "m"])
    tableObj.add_rows([
        ["Activation Key", "Subject"],
        [1, 'Apps'],
        [2, 'Startups'],
        [3, 'Venture'],
        [4, 'Security'],
        [5, 'AI'],
        [6, 'Crypto'],
        [7, 'Fintech']
    ])
    print(tableObj.draw())
    subj = input('Your selection option: ')

    if subj.isnumeric():
        category_code = list(WebHandler.categories.values())[int(subj) - 1]
        if online == '1':
            resp = WebHandler.get_certain_subject_publications(category_code, 1)
            print_results_table(resp['body'])
            DBController.insert_magazine_records_to_db(resp['body'])

        elif online == '2':
            DBController.fetch_db_record_using_certain_value_at_certain_column('category', category_code)



if __name__ == '__main__':
    #DBController.setup_table_in_db()
    #show_subject_selection_menu()
    #DBController = DBController.clean_db_table('magazines')
    enable_auto_scraper()
    print('Hi, Welcome to the feature selection section. '
          'Please select your intended option based on following guid table')

    tableObj = texttable.Texttable(120)
    tableObj.set_cols_align(["l", "c", "c", "r"])
    tableObj.set_cols_dtype(["i", "t", "t", "t"])
    tableObj.set_cols_valign(["t", "t", "m", "b"])
    tableObj.add_rows([
        ["Activation Key", "Option Name", "Need Connection", "Option Description"],
        [1, 'Search For Relevant Publications to a term', '✅❌',
         'Give a term to program then get all existed relevant pubs in tech crunch or in our DB'],
        [2, 'Get Cached Subjects', '❌', 'Get the list of already fetched pubs and cached in program data base'],
        [3, 'Publication Counter', '❌', 'How many pubs existed with a certain subject'],
        [4, 'Clean DB', '❌', 'Clear all Data Base records (Reset DB)']
    ])
    print(tableObj.draw())

    entry_term = input('Now, Input your intended option -> : ')

    if entry_term == '1':
        show_subject_selection_menu()
    elif entry_term == '2':
        resp = DBController.fetch_db_column('category')
        for i in resp:
            print(i)
    elif entry_term == '3':
        print('Which subject do you want to check for existence?')
        tableObj = texttable.Texttable(120)
        tableObj.set_cols_align(["c", "c"])
        tableObj.set_cols_dtype(["i", "t"])
        tableObj.set_cols_valign(["m", "m"])
        tableObj.add_rows([
            ["Activation Key", "Subject"],
            [1, 'Apps'],
            [2, 'Startups'],
            [3, 'Venture'],
            [4, 'Security'],
            [5, 'AI'],
            [6, 'Crypto'],
            [7, 'Fintech']
        ])
        print(tableObj.draw())
        selections = ['Apps', 'Startups', 'Venture', 'Security', 'AI', 'Crypto', 'Fintech']
        entry_term = input('Now, Input your intended term to check status -> : ')
        db_result = DBController.fetch_db_column('category')
        print('\n<!!!!!!!!!!!!!!!>')
        ans = str(db_result).count(selections[int(entry_term)-1])
        if ans:
            print(f'There is {ans} relevant records to "{selections[int(entry_term)-1]}" subject '
                  f'in our database so this term was already fetched !')
        else:
            print('Not Found any related records, you should fetch this term for first time using option number 1')
        print('<!!!!!!!!!!!!!!!>\n')
    elif entry_term == '4':
        DBController.clean_db_table('magazines')
        print('Data Base Cleared Successfully!')




















'''
def fetch_term(term):
    # Will return all extracted book information from response table as a list of bs4 objects
    base_url = ("https://www.libgen.is/search.php?&res=100&req={term}"
                "&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page={page_number}")
    page_counter = 1
    books = []
    while True:
        resp = requests.get(base_url.format(term=term, page_number=page_counter))
        bs_obj = BeautifulSoup(resp.text, "html.parser")
        if bs_obj.title.string == '504 Gateway Time-out':
            sys.exit('504 Gateway Time :(')
        with open('typically-fetched.html', 'w', encoding="utf-8") as file:
            file.write(resp.text)
        with open('typically-fetched.html', 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, "html.parser")
        if len(soup.select('body > table.c')) <= 0:  # Last table page
            break
        books_table = soup.select('body > table.c')[0]  # A tag object
        # First book is in the 1st index and all even indexes are empty
        # So you should just crawl on even indexes that starts from 1 and smaller than length
        if len(books_table) <= 1:
            #  Last table page
            break
        for counter in range(1, len(books_table), 2):
            next_book_index = list(books_table.contents[counter].children)
            # A record of books table in html response page
            # for catching exceptions due to " and ' chars while inserting to sql (sql query interference)
            # .replace('\"','\'')
            # print(next_book_index)
            books.append({'fetched_term': term, 'author': next_book_index[2].get_text().replace('\"', '\''),
                          'title': next_book_index[4].get_text().replace('\"', '\''),
                          'publisher': next_book_index[6].get_text().replace('\"', '\''),
                          'year': next_book_index[8].get_text(),
                          'pages_count': next_book_index[10].get_text(), 'language': next_book_index[12].get_text(),
                          'size': next_book_index[14].get_text(), 'extension': next_book_index[16].get_text(),
                          'link1': next_book_index[18].contents[0]['href'],
                          'link2': next_book_index[19].contents[0]['href']})
        #  print(books)
        print(f'page number {page_counter} of this term fetched successfully ...')
        page_counter += 1
    return books
'''
'''
def print_already_fetched_terms():
    connection = sqlite3.connect("cached.db")
    with connection:
        cursor = connection.cursor()
        resp = cursor.execute(f"SELECT (fetched_term) FROM books;").fetchall()
        print('\n<======= List Of All Fetched Terms =======>')
        for i in set(resp):
            print(f' - {i[0]}')
        print('<========================================>')'''