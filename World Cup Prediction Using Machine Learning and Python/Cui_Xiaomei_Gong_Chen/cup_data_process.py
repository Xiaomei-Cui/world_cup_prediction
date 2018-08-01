import pandas as pd
import matplotlib.pyplot as plt

# 解决matplotlib显示中文问题
# 指定默认字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 存放所有数据的Dataframe
df = pd.read_csv('result.csv')


# 获得所有与世界杯相关的数据（包括预选赛）
mask = df['home_score'] - df['away_score']
df.loc[mask > 0, 'win_team'] = df.loc[mask > 0, 'home_team']
df.loc[mask < 0, 'win_team'] = df.loc[mask < 0, 'away_team']
df.loc[mask == 0, 'win_team'] = 'Draw'
df_FIFA_all = df[df['tournament'].str.contains('FIFA', regex=True)]


# 五支夺冠热门队伍
team_top5 = ['Germany', 'Argentina', 'Brazil', 'France', 'Spain']
# 五支队伍在世界杯相关比赛中相互对战的数据
df_FIFA_top5 = df_FIFA_all[(df_FIFA_all['home_team'].isin(team_top5))&
                                        (df_FIFA_all['away_team'].isin(team_top5))]

# 两支球队获胜场数情况
def team_vs(df,team_A,team_B):
	df_team_A_B = df[(df['home_team'].isin([team_A,team_B]))&
					 (df['away_team'].isin([team_A,team_B]))]
	s_win_team = df_team_A_B.groupby('win_team')['win_team'].count()
	return s_win_team

# 画热门队伍两两对战胜利、平局数的饼图
def top_plot(df, team_A, team_B):
	result = team_vs(df, team_A, team_B)
	plt.bar([team_A], [result[team_A]])
	plt.bar([team_B], [result[team_B]])
	if result.size > 2:
		plt.bar(["Draw"], [result["Draw"]])
	plt.title(team_A + " vs " + team_B)
	plt.show()

top_plot(df_FIFA_all, 'Germany', 'France')



# 分析今年世界杯八强数据
team_top8 = ['Uruguay', 'France', 'Brazil', 'Belgium', 'Russia','Croatia',
			 'Sweden', 'England']
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# 获取球队某年至今获胜比例函数
def probability(df,year,team_A,team_B):
    prob = []
    df_year = df[df['year']>= year]
    s = team_vs(df_year,team_A,team_B)
    s_team_A = 0 if s.get(team_A) is None else s.get(team_A)
    s_A_win = s_team_A/s.sum()
    s_team_B = 0 if s.get(team_B) is None else s.get(team_B)
    s_B_win = s_team_B/s.sum()
    s_draw = 1 - s_A_win - s_B_win
    prob.append(year)
    prob.append(s_A_win)
    prob.append(s_B_win)
    prob.append(s_draw)
    return prob

# 获取两支球队历史获胜情况对比函数
def his_team_data(df,year_start,year_end,team_A,team_B):
    row_team = []
    for yr in list(range(year_start,year_end+1)):
        team_A_vs_team_B = probability(df,yr,team_A,team_B)
        row_team.append(team_A_vs_team_B)
    team_A_win = team_A + '_win_percentage'
    team_B_win = team_B + '_win_percentage'
    df_team = pd.DataFrame(row_team, columns=('year', team_A_win, team_B_win, 'draw_percentage'))
    return df_team

# 两支球队各自获胜和平局占总局数的百分比，折线图
def his_plot(df, start_year, end_year, team_A, team_B):
	match_result = his_team_data(df, start_year, end_year, team_A, team_B)
	total_row = end_year - start_year
	i = total_row
	while i > 0:
		if match_result["draw_percentage"][i] == match_result[
			"draw_percentage"][i]:
			break
		else:
			i -= 1
	if i == 0:
		print("There were no games between the two teams.")
		return

	idx_A = team_A + "_win_percentage"
	idx_B = team_B + "_win_percentage"

	A_win_percentage = []
	B_win_percentage = []
	draw_percentage = []
	year_between = []

	for j in range(i+1):
		year_between.append(j+start_year)
		A_win_percentage.append(match_result[idx_A][j])
		B_win_percentage.append(match_result[idx_B][j])
		draw_percentage.append(match_result["draw_percentage"][j])

	plt.title(team_A + " vs " + team_B)
	plt.plot(year_between, A_win_percentage, label=idx_A)
	plt.plot(year_between, B_win_percentage, label=idx_B)
	plt.plot(year_between, draw_percentage, label="draw_percentage")
	plt.xlabel('Year')
	plt.ylabel('Percentage')
	plt.legend()
	plt.show()

his_plot(df, 1940, 2018, 'France', 'Brazil')

