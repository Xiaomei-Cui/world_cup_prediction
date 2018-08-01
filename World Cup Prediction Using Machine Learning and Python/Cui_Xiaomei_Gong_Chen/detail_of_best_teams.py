import best_teams
import itertools
import csv
import matplotlib.pyplot as plt

teams = best_teams.teams[:5]
teams_dict = dict()

for item in list(itertools.permutations(teams, 2)):
    teams_dict[item[0]+item[1]] = [0, 0, 0]

with open('data.csv') as f:
    reader = csv.reader(f)

    for home in range(0, 4):
        for row in reader:
            if row[1] == teams[home]:
                if row[2] in teams:
                    if int(row[3]) > int(row[4]):
                        teams_dict[teams[home]+row[2]][0] += 1
                        teams_dict[row[2]+teams[home]][1] += 1
                    elif int(row[3]) < int(row[4]):
                        teams_dict[teams[home]+row[2]][1] += 1
                        teams_dict[row[2]+teams[home]][0] += 1
                    else:
                        teams_dict[teams[home]+row[2]][2] += 1
                        teams_dict[row[2]+teams[home]][2] += 1
        f.seek(0)

for index_1, team in enumerate(teams):
    team_dict = {item: teams_dict[item] for item in teams_dict if item.find(team) == 0}
    vs_teams = teams[:index_1] + teams[index_1 + 1:]
    plt.figure(figsize=(10, 8), dpi=300)
    for index_2, vs_team in enumerate(vs_teams):
        plt.subplot(2, 2, index_2 + 1)
        plt.pie(team_dict[team+vs_team], labels=['Win', 'Lose', 'Draw'], explode=[0.05, 0.05, 0.05], autopct='%1.0f%%')
        plt.title(team+' vs. '+vs_team, fontsize=20)
        plt.axis('equal')
    plt.savefig(team+'.png')
    plt.close()
