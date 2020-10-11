from flask import Flask
from flask import render_template
from flask import request

import requests
import base64

app = Flask(__name__)
spotify_token = 'init'

@app.route('/')
def hello_world():
	navigation = [{'href':'http://localhost:5000/', 'caption':'Home page'}, {'href':'http://localhost:5000/myShows', 'caption':'My shows'}]
	return render_template('index.html', navigation=navigation, token=spotify_token)


@app.route("/myShows")
def get_my_shows():
	return render_template('myShows.html')

@app.route("/token")
def setToken():
	global spotify_token
	spotify_token = request.args['token']

	headers = {'Authorization': 'Bearer ' + spotify_token}

	url = 'https://api.spotify.com/v1/me/shows'
	response = requests.get(url, headers=headers)

	shows = response.json()

	my_shows = []

	for item in shows['items']:
		show = item['show']

		show_id = show['id']
		show_name = show['name']
		show_desc = show['description']
		image_url = show['images'][0]['url']
		external_urls = show['external_urls']['spotify']
		print(f"show_name: {show_name}\nexternal_urls:{external_urls}")
		my_shows.append({"name": f"{show_name}", "description": f"{show_desc}", 'image':f"{image_url}", 'imgUrl':f"{external_urls}", 'showId': f"{show_id}"})

	return render_template("shows.html", shows=my_shows)


@app.route('/episodes/<show_id>')
def getEpisodes(show_id):
	print(f"show id is: {show_id}")
	print(f"spotify_token is: {spotify_token}")
	url = f'https://api.spotify.com/v1/shows?ids={show_id}'

	response = requests.get(url=url, headers = {'Authorization': 'Bearer ' + spotify_token})
	return response.json()



# @app.route('/shows')
# def getShows(token):
# 	print (f'token:{token}')
# 	headers = {'Authorization': 'Bearer ' + token}

# 	url = 'https://api.spotify.com/v1/me/shows?limit=1'
# 	response = requests.get(url, headers=headers)

# 	shows = response.json()
	
# 	print(shows)
# 	print('\n\n\n\n')
# 	print(shows['items'])
# 	print('\n\n\n\n')
# 	print('oz')
# 	return render_template("shows.html", shows=shows['items'])



# def getToken():
# 	url = "https://accounts.spotify.com/api/token"
# 	headers = {'Authorization': 'Bearer ' + token}
# 	data = {}

# 	client_id = '62128c70934843c68d379c100182786a'
# 	client_secret = 'b5e790a2b1ec4e11b64fab7fc55a4141'
# 	# Encode as Base64
# 	message = f"{client_id}:{client_secret}"
# 	messageBytes = message.encode('ascii')
# 	base64Bytes = base64.b64encode(messageBytes)
# 	base64Message = base64Bytes.decode('ascii')

# 	headers['Authorization'] = f"Basic {base64Message}"
# 	data['grant_type'] = "client_credentials"
# 	data['scope'] = 'user-library-read user-read-email user-read-private'
# 	data['redirect_uri'] = 'http://localhost:5000/'

# 	response = requests.post(url, headers=headers, data=data)

# 	return response.json()['access_token']