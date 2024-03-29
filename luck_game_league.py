import random
from itertools import combinations
import pandas as pd

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
    return winner, total_heads, total_tails

teams_list = ['team_1','team_2','team_3','team_4','team_5','team_6','team_7','team_8','team_9','team_10','team_11','team_12','team_13','team_14','team_15','team_16','team_17','team_18','team_19','team_20']
for_score = [0] * len(teams_list)
against_score = [0] * len(teams_list)
wins_list =[0] * len(teams_list)
r=2
matches_list = list(combinations(teams_list, r))
for match in matches_list:
    winner, team_1_score, team_2_score = play_match(match[0],match[1])
    idx = teams_list.index(winner)
    wins_list[idx] = wins_list[idx] + 1
    team_1_idx = teams_list.index(match[0])
    for_score[team_1_idx] = for_score[team_1_idx] + team_1_score
    against_score[team_1_idx] = against_score[team_1_idx] + team_2_score
    team_2_idx = teams_list.index(match[1])
    for_score[team_2_idx] = for_score[team_2_idx] + team_2_score
    against_score[team_2_idx] = against_score[team_2_idx] + team_1_score
    print('---')

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
print(results_df.sort_values(by=["wins","point_diff"],ascending=False))

