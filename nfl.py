# -*- coding: utf-8 -*-
"""!nfl will return this week's scores.  Unless ESPN breaks stuff."""

from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup
import json

def get_scores(team):
	out_string = ''
	# Use requests and bs4 to parse
	r = requests.get('http://espn.go.com/nfl/scoreboard')
	soup = BeautifulSoup(r.text,"html.parser")
	# Scrape scripts out of page.
	scripts = soup.findAll('script')
	# Loop through scripts to find scoreboard data.
	for s in scripts:
		if 'window.espn.scoreboardData' in s.text:
			break
	# Get text of script.
	script_text = s.text
	# This breaks off the second variable so we can get at the scoreboard
	vars = script_text.split(';window.espn')
	# Add the semicolon back in stripped out above.
	script_text = vars[0]+';'
	# jsonify the javascript via regex magic
	jsonValue = '{%s}' % (script_text.split('{', 1)[1].rsplit('}', 1)[0],)
	# Use json to parse
	score_data_struct = json.loads(jsonValue)
	# score_data_struct is a big and complicated data structure
	# containing schedule info, game info, and lots of custom stuff.
	# The below was determined by poking around in the data to find useful stuff.

	list_o_games = score_data_struct['events']

	for game in list_o_games:
		status = game['competitions'][0]['status']['type']['description']
		if status == 'Final':
			time_left = 'Final'
		else:
			time_left = game['competitions'][0]['status']['type']['shortDetail']
		team1 = game['competitions'][0]['competitors'][0]
		team2 = game['competitions'][0]['competitors'][1]
		team1_name = team1['team']['name']
		team2_name = team2['team']['name']
		team1_score = team1['score']
		team2_score = team2['score']
		#
		if team1_score >= team2_score:
			if team1['homeAway'] == 'home':
				homeaway = 'vs.'
			else:
				homeaway = ' @ '
			result = '{0:12} {1:3} {2} {3:12} {4:3} {5}'.format(
				team1_name,team1_score,homeaway,team2_name,team2_score,time_left)
		else: #team2 wins
			if team2['homeAway'] == 'home':
				homeaway = 'vs.'
			else:
				homeaway = ' @ '
			result = '{0:12} {1:3} {2} {3:12} {4:3} {5}'.format(
				team2_name,team2_score,homeaway,team1_name,team1_score,time_left)
		# 
		out_string += result+'\n'
	return out_string
#


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!nfl", text)
    if not match:
        return

    return get_scores('all')
