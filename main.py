# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
from bs4 import BeautifulSoup

page_url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/royal-challengers-bangalore-vs-mumbai-indians-5th-match-1359479/full-scorecard"

report_file_name_list = {
    "Mumbai Indians": "MI_batsman_list.txt",
    "Royal Challengers Bangalore": "RCB_batsman_list.txt",
    "Chennai Super Kings":"CSK_batsman_list.txt",
    "Gujarat Titans":"GT_batsman_list.txt",
    "Punjab Kings":"PBKS_batsman_list.txt",
    "Kolkata Knight Riders":"KKR_batsman_list.txt",
    "Lucknow Super Giants":"LSG_batsman_list.txt",
    "Delhi Capitals":"DC_batsman_list.txt",
    "Rajasthan Royals":"RR_batsman_list.txt",
    "Sunrisers Hyderabad": "SRH_batsman_list.txt"
}


def get_team_names(soup):
    spans = soup.find_all('span', {'class': 'ds-text-title-xs ds-font-bold ds-capitalize'})
    team_names = []
    for span in spans:
        team_names.append(span.text)
    return team_names

def get_batting_scores(soup):
    tables = soup.find_all('table')
    for table in tables:
        print(table.get('class'))
    score_tables = soup.find_all('table', class_='ci-scorecard-table')
    print(score_tables)

    scores_list = []
    for score_table in score_tables:
        rows = score_table.findChildren(['tr'])
        scores = {}
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 4:
                col_0 = columns[0]
                name_link = col_0.findChildren(['a'])
                if (columns[1].text.strip() == 'not out'):
                    player_score = columns[2].text.strip() + '*'
                else:
                    player_score = columns[2].text.strip()
                scores[name_link[0].get('title')] = player_score
        scores_list.append(scores)
    return scores_list

def get_page_content():
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    team_names = get_team_names(soup)
    batting_scores = get_batting_scores(soup)
    return team_names,batting_scores

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_player_list_from_file(team_name):
    report_batsmen_list_file_name = report_file_name_list[team_name]
    f = open(report_batsmen_list_file_name, "r")
    text = f.read()
    f.close()
    player_list = []
    if "," in text:
        player_list = text.split(",")
    return player_list


def generate_batting_report(team_names,batting_scores):
    batting_reports = []
    for i in range(0, 2):
        report_batsmen_list = get_player_list_from_file(team_names[i])
        #report_batsmen_list = player_list[team_names[i]]
        #print(report_batsmen_list)
        batting_report = {}
        #generate for players already in report list
        for batsman in report_batsmen_list:
            if batsman in batting_scores[i]:
                batting_report[batsman] = batting_scores[i][batsman]
                #print(batting_scores[i][batsman])
            else:
                batting_report[batsman] = " "
                #print(" ")
        #for new players playing first time, add them to the end of the list
        for batsman in batting_scores[i]:
            if batsman not in batting_report:
                batting_report[batsman] = batting_scores[i][batsman]
        batting_reports.append(batting_report)
    return batting_reports

def print_batting_reports(batting_reports):
    for report in batting_reports:
        '''
        for batsman in report:
            print(batsman)
        print("-----")
        '''
        for batsman in report:
            print(report[batsman])

        formatted_batsman_list = ""
        contains_at_least_one_element = False
        for batsman in report:
            if contains_at_least_one_element == True:
                formatted_batsman_list = formatted_batsman_list + "," + batsman
            else:
                formatted_batsman_list = formatted_batsman_list + batsman
                contains_at_least_one_element = True
        formatted_batsman_list  = formatted_batsman_list
        print(formatted_batsman_list)
        print("=======")

def write_player_list_to_file(team_names,batting_reports):
    for i in range(0, 2):
        file_name = report_file_name_list[team_names[i]]
        formatted_batsman_list = ""
        contains_at_least_one_element = False
        for batsman in batting_reports[i]:
            if contains_at_least_one_element == True:
                formatted_batsman_list = formatted_batsman_list + "," + batsman
            else:
                formatted_batsman_list = batsman
                contains_at_least_one_element = True
        f = open(file_name, "w")
        f.write(formatted_batsman_list)
        f.close()


if __name__ == '__main__':
    team_names, batting_scores = get_page_content()
    batting_reports = generate_batting_report(team_names,batting_scores)
    print_batting_reports(batting_reports)
    write_player_list_to_file(team_names, batting_reports)


