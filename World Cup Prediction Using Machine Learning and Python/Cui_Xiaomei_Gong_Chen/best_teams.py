import csv
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

with open('data.csv') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    win_dict = dict()

    for row in reader:
        if int(row[3]) > int(row[4]):  # Home_team wins
            if win_dict.get(row[1]) is None:
                win_dict[row[1]] = 1
            else:
                win_dict[row[1]] = win_dict[row[1]] + 1
        elif int(row[3]) < int(row[4]):  # Away_team wins
            if win_dict.get(row[2]) is None:
                win_dict[row[2]] = 1
            else:
                win_dict[row[2]] = win_dict[row[2]] + 1
        else:  # ignore
            pass

# Tranform to a list
win_list = list()
for team in win_dict.keys():
    win_list.append({'label': team, 'value': win_dict[team]})

# Sort the list
win_sorted = sorted(win_list, key=lambda dic: dic['value'], reverse=True)

# Get the x_label
teams = list()
for team in win_sorted:
    teams.append(team['label'])

# Set the chart
my_style = LS('#333366', base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 24
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Count of Winning in FIFA'
chart.x_labels = teams
chart.add('', win_sorted)

chart.render_to_file('count_of_winning.svg')
