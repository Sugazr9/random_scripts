import requests
import json
import eyed3
import os
from datetime import datetime


def searchNnarrow(search_info, song_mode, comparison, second_try=False):
	base_url = 'https://itunes.apple.com/search?term='
	add_criteria_song = "&entity=song"
	add_criteria_album = "&entity=album"
	country = input("What is your country code? Default is US").lower()
	search_info = search_info.replace(' ', '+').replace('[', '').replace(']', '')
	if song_mode:
		url = base_url + search_info + add_criteria_song + '&country=' + country
	else:
		url = base_url + search_info + add_criteria_album + '&country=' + country
	result = requests.get(url).json()
	searches = result['results']

	reduced = []
	cache = []
	for i in range(2):
		for search in searches:
			search_album = search['collectionName']
			search_artist = search['artistName']
			if song_mode:
				artist = comparison['artist']
				if artist is None:
					artist = "none"
				artist = artist.lower()
				track_name = comparison['track'].lower()
				search_track = search['trackName']
				lower_search_artist = search_artist.lower()
				lower_search_track = search_track.lower()
				if ((artist in lower_search_track or artist in lower_search_artist) and track_name in lower_search_track) and i == 0:	
					dets = [search_track, search_artist, search_album]
				elif i == 1:
					dets = [search_track, search_artist, search_album]
				else:
					continue
			else:
				album = comparison['album']
				if album in search_album:
					dets = search_album
				elif i == 1:
					dets = search_album
				else:
					continue
			if dets in cache:
					continue
			cache.append(dets)
			reduced.append(search)
		if len(reduced) > 0:
			break
	for i in range(len(reduced)):
		curr = reduced[i]
		search_album = curr['collectionName']
		search_artist = curr['artistName']
		if song_mode:
			search_track = curr['trackName']
			print_message = 'Option ' + str(i) + ': {track:' + search_track + ', artist:' + search_artist + ', album:' + search_album + "}"
		else:
			print_message = 'Option ' + str(i) + ': {album:' + search_album + ', artist:' + search_artist + "}"
		print(print_message)
	search_num = None
	move_on = False
	chosen_one = None
	while True:
		search_num = input("Which option do you choose? Type 'None' if you can't find anything. ")
		if search_num.lower() == 'none':
			move_on = True
			break
		num_response = search_num.isnumeric()
		if num_response and int(search_num) in range(len(reduced)):
			print("Chose option: " + search_num)
			chosen_one = reduced[int(search_num)]
			break
	return move_on, chosen_one



directory = "C:/Users/go_ar/Music/Name Modified/"
destination = "C:/Users/go_ar/Music/Metadata Added/"

for file in os.listdir(directory):
	print("The file you are currently editing is: " + file)
	edit = input("Want to edit this file?(Y/y)")
	if edit.lower() != 'y':
		pass
	else:
		path = os.path.join(directory, file)
		new_path = os.path.join(destination, file)
		track = eyed3.load(path)
		tags = track.tag
		track_name = tags.title
		artist = tags.artist
		track_not_found = True
		search_criteria = track_name
		while track_not_found:
			track_not_found, chosen_search = searchNnarrow(search_info=search_criteria, song_mode=True, comparison={'artist': artist, 'track': track_name})
			if track_not_found:
				search_criteria = input("What is your track search criteria? (Only alphanumeric searches) ")
			if search_criteria.lower() == "none":
				break
		if track_not_found:
			tags = None
			continue
		tags._setArtist(chosen_search['artistName'])
		tags._setTitle(chosen_search['trackName'])
		tags._setAlbum(chosen_search['collectionName'])
		tags._setGenre(chosen_search['primaryGenreName'])
		tags.artist_url = chosen_search['artistViewUrl']
		tags.audio_file_url = chosen_search['trackViewUrl']
		tags._setDiscNum(chosen_search['discNumber'])
		tags._setReleaseDate(chosen_search['releaseDate'])
		tags._setTrackNum((chosen_search['trackNumber'], chosen_search['trackCount']))
		import pdb; pdb.set_trace()
		try:
			tags.save()
		except UnicodeEncodeError as e:
			print(e)
			tags = None
			continue
		album_not_found = True
		search_criteria1 = tags.album
		while album_not_found:
			album_not_found, chosen_album = searchNnarrow(search_info=search_criteria1, song_mode=False,  comparison={'album': tags.album})
			if album_not_found:
				search_criteria1 = input("What is your album search criteria? (Only alphanumeric searches) ")
		tags._setAlbumArtist(chosen_album['artistName'])
		tags.save()
		tags = None

		os.rename(path, new_path)
