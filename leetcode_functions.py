import requests
import json

data = requests.get ("https://leetcode-api-faisalshohag.anga.codes/Anga205")

data = json.loads(data.text)

get_leetcode_solves = lambda: data.get("totalSolved", 0)

get_leetcode_ranking = lambda: data.get("ranking", 0)
