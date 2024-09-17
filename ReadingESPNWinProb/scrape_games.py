from games2 import *

years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
weeks = (np.arange(17)+1).tolist()

results = []
for year in years:
    for week in weeks:
        games = GamesOfWeek(week = week, year = year)
        games.get_IDs()
        results_file_name = f'../scrape_results/{year}_week{week}_results.txt'
        games.get_data(results_file = results_file_name)
