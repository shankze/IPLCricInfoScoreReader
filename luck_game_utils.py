
def generate_weekly_fixture_schedule(teams_list):
    if(len(teams_list) % 2) != 0:
        teams_list.append(0)
    top_list,bottom_list = generate_cyclic_lists(teams_list)
    full_schedule = []
    for i in range(0,(len(teams_list))-1):
        if i != 0:
            top_list.insert(1,bottom_list.pop(0))
            bottom_list.append(top_list.pop())
        week_matches = []
        for j in range(len(top_list)):
            if top_list[j] == 0 or bottom_list[j] == 0:
                pass
            else:
                week_matches.append([top_list[j],bottom_list[j]])
        full_schedule.append(week_matches)
    if teams_list[len(teams_list)-1] == 0:
        teams_list.pop()
    return full_schedule

def generate_cyclic_lists(teams_list):
    mid_index = int(len(teams_list)/2)
    print('mid index: ', mid_index)
    top_list = teams_list[:mid_index]
    bottom_list = teams_list[mid_index:]
    return top_list,bottom_list


# full_schedule_by_week = generate_weekly_fixtures_for_even_teams(['1','2','3','4','5','6'])
# for week in full_schedule_by_week:
#     print(week)