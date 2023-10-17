from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv

def scrapper(link, csv_file):
    driver = webdriver.Chrome()

    game_time = []
    home_teams = []
    away_teams = []
    home_scores = []
    away_scores = []
    driver.get(link)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    team_pattern = re.compile('^ScoreCell__TeamName*')
    score_pattern = re.compile('^ScoreCell__Score*')


    for day in soup.find_all('section', class_=re.compile("Card gameModules")):
        time = day.find('h3', class_=re.compile("Card__Header__Title"))
        time_text = time.text

        for div in day.find_all('ul', class_=re.compile("ScoreboardScoreCell__Competitors")):
            game_time.append(time_text)

            teams = div.find_all('div', class_ = team_pattern)
            home_teams.append(teams[1].text)
            away_teams.append(teams[0].text)

            scores = div.find_all('div', class_ = score_pattern)
            home_scores.append(scores[1].text)
            away_scores.append(scores[0].text)

    print("time:", game_time)

    print("home teams:", home_teams)
    print("away teams:", away_teams)

    game_data = [game_time, home_teams, home_scores, away_teams, away_scores]

    if len(game_time) == len(home_teams) == len(away_teams) == len(home_scores) == len(away_scores):
        fieldnames = ["game time", "home team", "home score", "away team", "away score"]
        transposed_data = list(zip(*game_data))

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fieldnames)

            for row in transposed_data:
                writer.writerow(row)

if __name__ == "__main__":
    nfl = "https://www.espn.com/nfl/scoreboard"
    nba = "https://www.espn.com/nba/scoreboard/_/date/20231016"
    scrapper(nba, "nba.csv")