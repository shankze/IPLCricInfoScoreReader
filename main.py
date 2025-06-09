import requests
from bs4 import BeautifulSoup

from name_alternates import return_standard_name

page_url = "https://www.cricbuzz.com/live-cricket-scorecard/118928/rcb-vs-pbks-final-indian-premier-league-2025"

report_batting_file_name_list = {
    "Mumbai Indians": "MI_batsman_list.txt",
    "Royal Challengers Bengaluru": "RCB_batsman_list.txt",
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
    "Royal Challengers Bengaluru": "RCB_bowling_list.txt",
    "Chennai Super Kings":"CSK_bowling_list.txt",
    "Gujarat Titans":"GT_bowling_list.txt",
    "Punjab Kings":"PBKS_bowling_list.txt",
    "Kolkata Knight Riders":"KKR_bowling_list.txt",
    "Lucknow Super Giants":"LSG_bowling_list.txt",
    "Delhi Capitals":"DC_bowling_list.txt",
    "Rajasthan Royals":"RR_bowling_list.txt",
    "Sunrisers Hyderabad": "SRH_bowling_list.txt"
}

team_short_names = {
    "Mumbai Indians": "MI","Royal Challengers Bengaluru": "RCB","Chennai Super Kings": "CSK","Gujarat Titans": "GT","Punjab Kings": "PBKS","Kolkata Knight Riders": "KKR","Lucknow Super Giants": "LSG","Delhi Capitals": "DC","Rajasthan Royals": "RR","Sunrisers Hyderabad": "SRH"
}

def get_team_names(soup):
    spans = soup.find_all('span', {'class': 'ds-text-title-xs ds-font-bold ds-capitalize'})
    team_names = []
    for span in spans:
        team_names.append(span.text)
    return team_names

def get_location(soup):
    try:
        match_header_text = soup.find_all('h1', class_='ds-text-title-xs ds-font-bold ds-mb-2 ds-m-1')[0].text.strip()
        venue = match_header_text.split("at ", 1)[1].split(" ")[0]
        return venue.rstrip(',')
    except:
        print('Exception fetching location')
        return ''

def get_location_cricbuzz(soup):
    try:
        match_info_items = soup.find_all('div', class_='cb-mtch-info-itm')
        #match_info_div = match_info_div
        #match_info_lines = match_info_div.find_all('div',class_='cb-col-100')
        for match_info_item in match_info_items:
            if match_info_item.find('div',class_='cb-col-27').text == 'Venue':
                return match_info_item.find('div',class_='cb-col-73').text.split(',')[1].strip()
        return ''
    except:
        print('Exception fetching location')
        return ''

def get_batting_scores_cricbuzz(soup):
    innings_list = ['innings_1','innings_2']
    all_team_names = []
    all_scores_list = []
    all_team_scores_list = []
    for innings in innings_list:
        innings_div = soup.find('div', id=innings)
        inner_div = innings_div.find_all('div',class_='cb-col cb-col-100 cb-ltst-wgt-hdr')
        scoreboard_div = inner_div[0]
        score_board_div_contents = scoreboard_div.find_all('div',class_='cb-col cb-col-100 cb-scrd-itms') #cb-col cb-col-100 cb-scrd-itms
        scores = {}
        for score_item in score_board_div_contents:
            try:
                score_line_elements = score_item.find_all('a',href=True)
                if len(score_line_elements) > 0:
                    batsman_name = score_line_elements[0].text.strip()
                    if '(' in batsman_name:
                        batsman_name = batsman_name[:batsman_name.find("(")].strip()
                    batsman_name = return_standard_name(batsman_name)
                    is_not_out = score_item.find('span', class_='text-gray').text.strip() == 'not out'
                    score = score_item.find('div', class_='cb-col cb-col-8 text-right text-bold').text.strip()
                    scores[batsman_name] = f'{score}*' if is_not_out else score
            except:
                pass
        team_score_elements = scoreboard_div.find('div',class_='cb-scrd-hdr-rw')
        team_score_spans = team_score_elements.find_all('span')
        team_name = team_score_spans[0].text.strip()
        all_team_names.append(team_name.split(' Innings')[0])
        team_score = team_score_spans[1].text.strip().split('-')[0]
        team_wickets = team_score_spans[1].text.split('-')[1].split(' ')[0]
        team_overs = team_score_spans[1].text.split('(')[1].split(' ')[0]
        all_team_scores_list.append((team_score, team_wickets, team_overs))
        all_scores_list.append(scores)
    return all_team_names, all_scores_list, all_team_scores_list


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
        "class": "ds-font-bold ds-bg-fill-content-alternate ds-text-tight-m ds-min-w-max ds-text-right ds-text-typo"})
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
                bowler_name = columns[0].text
                overs_bowled = columns[1].text
                wickets = columns[4].text
                bowling_scores[bowler_name] = (overs_bowled,wickets)
        bowling_scores_list.append(bowling_scores)
    return bowling_scores_list

def get_bowling_scores_cricbuzz(soup):
    innings_list = ['innings_1', 'innings_2']
    all_bowling_scores_list = []
    for innings in innings_list:
        bowling_scores = {}
        innings_div = soup.find('div', id=innings)
        inner_div = innings_div.find_all('div',class_='cb-col cb-col-100 cb-ltst-wgt-hdr')
        scoreboard_div = inner_div[1]
        bowling_div_contents = scoreboard_div.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
        for bowl_item in bowling_div_contents:
            bowling_line_elemets = bowl_item.find_all('a', href=True)
            if len(bowling_line_elemets) > 0:
                bowler_name = bowling_line_elemets[0].text.strip()
                if '(' in bowler_name:
                    bowler_name = bowler_name.split('(')[0].strip()
                bowler_name = return_standard_name(bowler_name)
                overs_bowled = bowl_item.find_all('div', class_='cb-col-8')[0].text.strip()
                wickets = bowl_item.find_all('div', class_='cb-col-8')[2].text.strip()
                bowling_scores[bowler_name] = (overs_bowled, wickets)
        all_bowling_scores_list.append(bowling_scores)
    return all_bowling_scores_list

def get_page_content():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    page = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    team_names = get_team_names(soup)
    #batting_scores,team_scores = get_batting_scores(soup)
    team_names, batting_scores,team_scores = get_batting_scores_cricbuzz(soup)
    #bowling_scores = get_bowling_scores(soup)
    bowling_scores = get_bowling_scores_cricbuzz(soup)
    venue = get_location_cricbuzz(soup)
    return team_names,batting_scores,bowling_scores, team_scores, venue

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


def print_batting_reports(batting_reports, team_scores, team_names, venue):
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
        print(f'{team_names[i]} batting')
        print('---')
        for batsman_name in batsman_names_list:
            print(batsman_name)
        print('---')
        print(venue)
        print(team_short_names[team_names[0 if i ==1 else 1]])
        for batsman in batting_reports[i]:
            print(batting_reports[i][batsman])


        #print(formatted_batsman_list)
        print('----')

        for j in range(0,3):
            print(team_scores[i][j])
        order = "B" if i==0 else "C"
        print(order)
        print("=======")

def print_bowling_reports(bowling_reports, team_names):
    team_name_index = 1
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
        print(f'{team_names[team_name_index]} bowling')
        print('---')
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
        team_name_index -= 1

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
    team_names, batting_scores, bowling_scores, team_scores, venue = get_page_content()
    batting_reports = generate_batting_report(team_names,batting_scores)
    bowling_reports = generate_bowling_report(team_names, bowling_scores)
    print_batting_reports(batting_reports, team_scores,team_names, venue)
    print_bowling_reports(bowling_reports,team_names)
    write_batsman_player_list_to_file(team_names, batting_reports)
    write_bowler_player_list_to_file(team_names, bowling_reports)


