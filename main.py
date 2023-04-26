import requests
from bs4 import BeautifulSoup

page_url = "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/gujarat-titans-vs-mumbai-indians-35th-match-1359509/full-scorecard"

report_batting_file_name_list = {
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
report_bowling_file_name_list = {
    "Mumbai Indians": "MI_bowling_list.txt",
    "Royal Challengers Bangalore": "RCB_bowling_list.txt",
    "Chennai Super Kings":"CSK_bowling_list.txt",
    "Gujarat Titans":"GT_bowling_list.txt",
    "Punjab Kings":"PBKS_bowling_list.txt",
    "Kolkata Knight Riders":"KKR_bowling_list.txt",
    "Lucknow Super Giants":"LSG_bowling_list.txt",
    "Delhi Capitals":"DC_bowling_list.txt",
    "Rajasthan Royals":"RR_bowling_list.txt",
    "Sunrisers Hyderabad": "SRH_bowling_list.txt"
}

def get_team_names(soup):
    spans = soup.find_all('span', {'class': 'ds-text-title-xs ds-font-bold ds-capitalize'})
    team_names = []
    for span in spans:
        team_names.append(span.text)
    return team_names

def get_batting_scores(soup):
    tables = soup.find_all('table')
    #for table in tables:
    #    print(table.get('class'))
    score_tables = soup.find_all('table', class_='ci-scorecard-table')
    #print(score_tables)

    scores_list = []
    team_scores_list = []
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
        team_scores = get_team_total_scores(score_table)
        team_scores_list.append(team_scores)
    return scores_list,team_scores_list

def get_team_total_scores(score_table):
    total_score_col = score_table.find("td", {
        "class": "ds-font-bold ds-bg-fill-content-alternate ds-text-tight-m ds-min-w-max ds-text-right"})
    runs_and_wickets = total_score_col.text.split("/")
    overs_col = score_table.find("td", {
        "class": "ds-font-bold ds-bg-fill-content-alternate ds-text-tight-m ds-min-w-max ds-flex ds-items-center !ds-pl-[100px]"})
    overs = overs_col.findChildren(['span'])
    total_overs = overs[0].text.split(" ")
    total_wickets = 10
    if len(runs_and_wickets) > 1:
        total_wickets = runs_and_wickets[1]
    return (runs_and_wickets[0],total_wickets,total_overs[0])

def get_bowling_scores(soup):
    bowling_tables = soup.find_all('table', class_='ds-w-full ds-table ds-table-md ds-table-auto')
    bowling_scores_list = []
    for bowling_table in bowling_tables:
        rows = bowling_table.findChildren(['tr'])
        bowling_scores = {}
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 4:
                col_0 = columns[0]
                bowler_name = columns[0].text
                overs_bowled = columns[1].text
                wickets = columns[4].text
                bowling_scores[bowler_name] = (overs_bowled,wickets)
        bowling_scores_list.append(bowling_scores)
    return bowling_scores_list


def get_page_content():
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    team_names = get_team_names(soup)
    batting_scores,team_scores = get_batting_scores(soup)
    bowling_scores = get_bowling_scores(soup)
    return team_names,batting_scores,bowling_scores, team_scores

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_player_list_from_file(team_name, type):
    if type == 'BAT':
        report_batsmen_list_file_name = report_batting_file_name_list[team_name]
    else:
        report_batsmen_list_file_name = report_bowling_file_name_list[team_name]
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
        report_batsmen_list = get_player_list_from_file(team_names[i],'BAT')
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

def generate_bowling_report(team_names,bowling_scores):
    bowling_reports = []
    team_names_reversed = [team_names[1],team_names[0]]
    for i in range(0, 2):
        report_bowler_list = get_player_list_from_file(team_names_reversed[i],'BOWL')
        #report_batsmen_list = player_list[team_names[i]]
        #print(report_batsmen_list)
        bowling_report = {}
        #generate for players already in report list
        for bowler in report_bowler_list:
            if bowler in bowling_scores[i]:
                bowling_report[bowler] = bowling_scores[i][bowler]
            else:
                bowling_report[bowler] = (" ", " ")
                #print(" ")
        #for new players playing first time, add them to the end of the list
        for bowler in bowling_scores[i]:
            if bowler not in bowling_report:
                bowling_report[bowler] = bowling_scores[i][bowler]
        bowling_reports.append(bowling_report)
    return bowling_reports
def print_batting_reports(batting_reports, team_scores):
    #for report in batting_reports:
    for i in range(0, 2):
        formatted_batsman_list = ""
        batsman_names_list = []
        contains_at_least_one_element = False
        for batsman in batting_reports[i]:
            batsman_names_list.append(batsman)
            if contains_at_least_one_element == True:
                formatted_batsman_list = formatted_batsman_list + "," + batsman
            else:
                formatted_batsman_list = formatted_batsman_list + batsman
                contains_at_least_one_element = True
        for batsman_name in batsman_names_list:
            print(batsman_name)
        print('---')
        for batsman in batting_reports[i]:
            print(batting_reports[i][batsman])


        #print(formatted_batsman_list)
        print('----')

        for j in range(0,3):
            print(team_scores[i][j])
        order = "B" if i==0 else "C"
        print(order)
        print("=======")

def print_bowling_reports(bowling_reports):
    for report in bowling_reports:
        formatted_bowler_list = ""
        contains_at_least_one_element = False
        bowler_names_list = []
        for bowler in report:
            bowler_names_list.append(bowler)
            if contains_at_least_one_element == True:
                formatted_bowler_list = formatted_bowler_list + "," + bowler
            else:
                formatted_bowler_list = formatted_bowler_list + bowler
                contains_at_least_one_element = True
        #print(formatted_bowler_list)
        for bowler_name in bowler_names_list:
            print(bowler_name)
        print('---')
        print('WICKETS:')
        for bowler in report:
            print(report[bowler][1])
        print('OVERS:')
        for bowler in report:
            print(report[bowler][0])


        print("=======")
def write_batsman_player_list_to_file(team_names,batting_reports):
    for i in range(0, 2):
        file_name = report_batting_file_name_list[team_names[i]]
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

def write_bowler_player_list_to_file(team_names,bowling_reports):
    team_names_reversed = [team_names[1], team_names[0]]
    for i in range(0, 2):
        file_name = report_bowling_file_name_list[team_names_reversed[i]]
        formatted_bowler_list = ""
        contains_at_least_one_element = False
        for bowler in bowling_reports[i]:
            if contains_at_least_one_element == True:
                formatted_bowler_list = formatted_bowler_list + "," + bowler
            else:
                formatted_bowler_list = bowler
                contains_at_least_one_element = True
        f = open(file_name, "w")
        f.write(formatted_bowler_list)
        f.close()

if __name__ == '__main__':
    team_names, batting_scores, bowling_scores,team_scores = get_page_content()
    batting_reports = generate_batting_report(team_names,batting_scores)
    bowling_reports = generate_bowling_report(team_names, bowling_scores)
    print_batting_reports(batting_reports, team_scores)
    print_bowling_reports(bowling_reports)
    write_batsman_player_list_to_file(team_names, batting_reports)
    write_bowler_player_list_to_file(team_names, bowling_reports)


