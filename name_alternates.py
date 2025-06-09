alternate_name_dict = {
    'Maheesh Theekshana':['M Theekshana'],
    'Nicholas Pooran': ['Pooran'],
    'Shardul Thakur':['Thakur'],
    'Virat Kohli':['Kohli'],
    'Quinton de Kock':['de Kock'],
    'Philip Salt':['Phil Salt'],
    'Liam Livingstone':['Livingstone'],
    'Josh Hazlewood':['Hazlewood'],
    'Rohit Sharma':['Rohit'],
    'Ryan Rickelton':['Rickelton'],
    'Mitchell Santner':['Santner'],
     'Prasidh Krishna':['Prasidh'],
     'Trent Boult':['Boult'],
     'Deepak Chahar':['D Chahar'],
     'Sai Kishore':['Ravisrinivasan Sai Kishore'],
     'Mohammed Siraj':['Siraj'],
     'Kagiso Rabada':['Rabada'],
    'Prabhsimran Singh':['Prabhsimran'],
    'Yuzvendra Chahal':['Chahal'],
    'Glenn Maxwell':['Maxwell'],
    'Marcus Stoinis':['Stoinis'],
    'Ishant Sharma':['Ishant'],
    'Rasikh Salam':['Rasikh Dar Salam'],
    'Devdutt Padikkal':['Padikkal'],
    'Sanju Samson':['Samson'],
    'Shimron Hetmyer':['Hetmyer'],
     'Rishab Pant':['Pant','Rishabh Pant'],
     'Sunil Narine':['Narine'],
     'Travis Head':['Head'],
    'Pat Cummins':['Cummins'],
    'Heinrich Klaasen':['Klaasen'],
    'Mohammed Shami':['Shami'],
    'Nitish Kumar Reddy':['Nitish Reddy'],
    'Wiaan Mulder':['Mulder'],
    'Aiden Markram':['Markram'],
    'Digvesh Rathi':['Digvesh Singh Rathi'],
    'Azmatullah Omarzai':['Azmatullah'],
    'Axar Patel':['Axar'],
    'KL Rahul':['Rahul'],
    'Tristan Stubbs':['Stubbs'],
    'Andre Russell':['Russell'],
    'MS Dhoni':['Dhoni'],
    'Ravichandran Ashwin':['Ashwin'],
    'Rahul Tripathi':['Tripathi'],
    'Devon Conway':['Conway'],
    'Bhuvneshwar Kumar':['Bhuvneshwar'],
    'Jasprit Bumrah':['Bumrah'],
    'Wanindu Hasaranga':['W Hasaranga','Hasaranga'],
    'Faf du Plessis':['du Plessis'],
    'Dushmantha Chameera':['Chameera'],
    'Yudhvir Singh Charak':['Yudhvir Singh'],
    'Rahmanullah Gurbaz':['Gurbaz'],
    'Mustafizur Rahman':['Mustafizur'],
    'Kyle Jamieson':['Jamieson'],
    'Jonny Bairstow':['Bairstow'],
# '':[''],
# '':[''],

}

def to_lowercase(string_list):
    return [s.lower() for s in string_list]

def convert_names_dict_to_lower(names_dict):
    for key in names_dict:
        names_dict[key] = to_lowercase(names_dict[key])
    return names_dict

alternate_name_dict_lower_case = convert_names_dict_to_lower(alternate_name_dict)

def return_standard_name(name_in_website):
    for player_name in alternate_name_dict:
        if name_in_website.lower() in alternate_name_dict_lower_case[player_name]:
            return player_name
    return name_in_website


