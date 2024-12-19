import requests
import json
import eyed3
import os


def searchNnarrow(search_info):
	base_url = 'https://itunes.apple.com/search?term='
	add_criteria_album = "&entity=album"
	country = input("What is your country code? Default is US").lower()
	search_info = search_info.replace(' ', '+').replace('[', '').replace(']', '')
	if country == "":
		add_criteria_album = add_criteria_album + '&country=' + country
	url = base_url + search_info + add_criteria_album
	result = requests.get(url).json()
	searches = result['results']

	reduced = []
	cache = []
	for search in searches:
		search_album = search['collectionName']
		dets = search_album
		
		if dets in cache:
			continue
		cache.append(dets)
		reduced.append(search)
	
	for i in range(len(reduced)):
		curr = reduced[i]
		search_album = curr['collectionName']
		search_artist = curr['artistName']
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

directory = "C:/Users/go_ar/Music/Metadata Added/"
destination = "C:/Users/go_ar/Music/Final Destination/"

for file in os.listdir(directory):
	print("The file you are currently editing is: " + file)
	path = os.path.join(directory, file)
	new_path = os.path.join(destination, file)
	track = eyed3.load(path)
	tags = track.tag
	if not tags.album_artist:
		chosen_one = None
		while chosen_one is None:
			search_criteria = input("What is your album search criteria? (Only alphanumeric searches) ")
			search_criteria = search_criteria.replace(" ", "+")
			move_on, chosen_one = searchNnarrow(search_criteria)
		if move_on:
			continue
		tags._setAlbumArtist(chosen_one['artistName'])
		tags.save()
	
	try:
		os.rename(path, new_path)
	except:
		print("File " + file + " already exists in destination.")
	tags = None

files = os.listdir(destination)
flagged_tracks = []
for i in range(len(files)):
        file_1 = files[i]
        path_1 = os.path.join(destination, file_1)
        name_1 = eyed3.load(path_1).tag.title
        if name_1 in flagged_tracks:
                continue
        for j in range(i + 1, len(files)):
                file_2 = files[j]
                path_2 = os.path.join(destination, file_2)
                name_2 = eyed3.load(path_2).tag.title
                if name_2 == name_1 and name_1 not in flagged_tracks:
                        flagged_tracks.append(name_1)
                        break

print("\nTracks flagged for possible clean up")
for track in flagged_tracks:
        print(track)
