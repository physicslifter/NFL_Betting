from games2 import *

year = 2022
weeks = (np.arange(4)+1).tolist()

results = []
for week in weeks:
    games = GamesOfWeek(week = week, year = year)
    games.get_IDs()
    results_file_name = f'../scrape_results/{year}_week{week}_results.txt'
    games.get_data(results_file = results_file_name)