from selenium import webdriver

import pandas as pd
import time

page = int(input("Specify which page do you want to fetch books from ? [1 - 25]\npage number: "))

driver = webdriver.Chrome()
driver.get('https://www.audible.com/search')

# data structure (dict)
books = {
    'title': [],
    'author': [],
    'read-length': []
}

def find_all_books(driver: webdriver.Chrome, page: int):

    # error handling
    if page < 1 or page > 25:
        print("Page must be in the range [1 - 25]")
        return

    # find the page given as an argument
    current_page = 1
    while not current_page == page:
        current_page = [int(x.text) for x in driver.find_elements('xpath', '//ul[contains(@class, "pagingElements")]//span[contains(@class, "pageNumberElement")]') if x.text.isdigit()][0]
        if current_page < page:
            driver.find_element('xpath', '//ul[contains(@class, "pagingElements")]//span[contains(@class, "nextButton")]').click()
            current_page += 1
            time.sleep(0.5)
        else:
            driver.find_element('xpath', '//ul[contains(@class, "pagingElements")]//span[contains(@class, "previousButton")]').click()
            current_page -= 1
            time.sleep(0.5)

    # finding all book cards in the page
    books_lib = driver.find_elements('xpath', value='//li[contains(@class, "productListItem")]')

    for book in books_lib:

        # gathering data for each book
        author = book.find_element('xpath', value='.//li[contains(@class, "authorLabel")]//a').text
        title = book.get_attribute('aria-label')
        length = book.find_element('xpath', value='.//li[contains(@class, "runtimeLabel")]//span').text[8:]
        # structuring data in form of dict
        books['title'].append(title)
        books['author'].append(author)
        books['read-length'].append(length)

        print(books)

find_all_books(driver, page)

# saving the data in excel file
df = pd.DataFrame(books)
df['ID'] = [x+1 for x in range(len(books['author']))]
df = df.set_index('ID')
df.to_csv(f'./pages/page_{page}.csv', columns=df.columns)

driver.quit()