import random
from itertools import combinations
import pandas as pd
import time

from luck_game_utils import generate_weekly_fixture_schedule


def play_match(team_1,team_2):
    count = 0
    total_heads = 0
    total_tails = 0
    #max_counter = 101
    max_counter = 99999
    while count < max_counter:
        coin = random.randint(1, 2)
        if coin == 1:
            total_heads += 1
            count += 1
        elif coin == 2:
            total_tails += 1
            count += 1
        #print("{0}: {1}, {2}: {3}".format(team_1, total_heads, team_2, total_tails))
    winner = team_1 if total_heads > total_tails else team_2
    loser = team_1 if winner == team_2 else team_2
    print("{0}: {1}, {2}: {3} ".format(team_1,total_heads,team_2,total_tails))
    print("{0}: {1:.2f}%, {2}: {3:.2f}% ".format(team_1, total_heads*100/max_counter, team_2, total_tails*100/max_counter))
    print('{0} beat {1} by {2}  :   {3:.2f}%'.format(winner,loser, abs(total_heads-total_tails), abs((total_heads*100/max_counter) - (total_tails*100/max_counter))))
    return winner, loser, total_heads, total_tails

def get_team_list_from_file():
    f = open("C:\Dev\IPLCricInfoScoreReader\luck_game_teams.txt", "r")
    teams_list = f.readlines()
    f.close()
    teams_list = [x.strip() for x in teams_list]
    return teams_list


def play_schedule(teams_list):
    #global for_score, against_score, wins_list
    for_score = [0] * len(teams_list)
    against_score = [0] * len(teams_list)
    wins_list = [0] * len(teams_list)
    loss_list = [0] * len(teams_list)
    #r = 2
    #matches_list = list(combinations(teams_list, r))
    no_of_weeks_in_schedule = len(fixure_list_by_week)
    week_no=1
    for week in fixure_list_by_week:
        for match in week:
            winner, loser, team_1_score, team_2_score = play_match(match[0], match[1])
            w_idx = teams_list.index(winner)
            wins_list[w_idx] = wins_list[w_idx] + 1
            l_idx = teams_list.index(loser)
            loss_list[l_idx] = loss_list[l_idx] + 1
            team_1_idx = teams_list.index(match[0])
            for_score[team_1_idx] = for_score[team_1_idx] + team_1_score
            against_score[team_1_idx] = against_score[team_1_idx] + team_2_score
            team_2_idx = teams_list.index(match[1])
            for_score[team_2_idx] = for_score[team_2_idx] + team_2_score
            against_score[team_2_idx] = against_score[team_2_idx] + team_1_score
            print('---')
        points_table_df = pd.DataFrame({'team': teams_list, 'wins': wins_list, 'losses': loss_list,'points_for':for_score,'points_against':against_score})

        points_table_df['win_pct'] = points_table_df['wins'].div(points_table_df['losses'].replace(0, 1)).round(2)
        points_table_df['played'] = points_table_df['wins'] + points_table_df['losses']
        points_table_df['point_diff'] = points_table_df['points_for'] - points_table_df['points_against']
        points_table_df['avg_point_diff'] = points_table_df['point_diff'] / points_table_df['played']
        points_table_df=points_table_df[["team","wins","losses","win_pct","avg_point_diff","played"]]
        print(points_table_df.sort_values(by=['win_pct','avg_point_diff'], ascending=False).reset_index(drop=True))
        if week_no != no_of_weeks_in_schedule:
            print(' ')
            print('Rounds to go: {0}'.format(no_of_weeks_in_schedule-week_no))
            time.sleep(5)
        week_no = week_no+1
    return for_score, against_score, wins_list



#teams_list = ['team_1','team_2','team_3','team_4','team_5','team_6','team_7','team_8','team_9','team_10','team_11','team_12','team_13','team_14','team_15','team_16','team_17','team_18','team_19','team_20']
#teams_list = ["Angola","Cameroon","Equatorial Guinea","Gabon","Congo","Chad","Central African Republic","Congo","Sao Tome and Principe"]
teams_list = get_team_list_from_file()

fixure_list_by_week = generate_weekly_fixture_schedule(teams_list)

for_score, against_score, wins_list = play_schedule(teams_list)

print(" ")
print(" ")
print(" ")
results_df = pd.DataFrame(
    {
        'team': teams_list,
        'wins': wins_list,
        'points_for':for_score,
        'points_against': against_score
    }
)
results_df['point_diff'] = results_df['points_for']-results_df['points_against']
#results_df['avg_points_for'] = results_df['points_for']/(len(teams_list)-1)
#results_df['avg_points_against'] = results_df['points_against']/(len(teams_list)-1)
results_df['avg_point_diff'] = results_df['point_diff']/(len(teams_list)-1)
print(results_df.sort_values(by=["wins","point_diff"],ascending=False).set_index('team'))





