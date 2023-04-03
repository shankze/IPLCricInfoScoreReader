# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
from bs4 import BeautifulSoup

LSG_player_list = [
    "KL Rahul",
    "Kyle Mayers",
    "Deepak Hooda",
    "Krunal Pandya",
    "Marcus Stoinis",
    "Nicholas Pooran",
    "Ayush Badoni",
    "Krishnappa Gowtham"
]

def get_page_content():
    page = requests.get("https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-delhi-capitals-3rd-match-1359477/full-scorecard")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="main-container")
    #print(results)
    #score = results.find_all("div", class_="ci-scorecard-table")
    #print(score)
    #for table in results.find_all('table'):
    #    print(table.get('class'))
    tables = soup.find_all('table')
    for table in tables:
        print(table.get('class'))
    score_tables = soup.find_all('table', class_='ci-scorecard-table')
    print(score_tables)

    for score_table in score_tables:
        rows = score_table.findChildren(['tr'])
        scores = {}
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 4:
                col_0 = columns[0]
                name_link = col_0.findChildren(['a'])
                not_out  = False
                player_score = 0
                if (columns[1].text.strip() == 'not out'):
                    #print(columns[2].text.strip(),'*')
                    player_score = columns[2].text.strip()+'*'
                else:
                    #print(columns[2].text.strip())
                    player_score = columns[2].text.strip()
                scores[name_link[0].get('title')] =player_score
        print(scores)


        '''
        for row in score_table.tbody.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')
            print(columns[0])
        '''

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    get_page_content()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
