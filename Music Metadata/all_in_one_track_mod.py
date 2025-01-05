import requests
import os
import eyed3

origin_dir = "C:/Users/go_ar/OneDrive/Documents/Audacity/macro-output/"
starting_dir = "C:/Users/go_ar/Music/Audacity Modified/"
named_dir = "C:/Users/go_ar/Music/Name Modified/"
details_dir = "C:/Users/go_ar/Music/Metadata Added/"


def searchNnarrow(search_info: str, song_mode: bool, comparison: dict) -> tuple:
    """
    Function that searches iTunes using iTunes API to obtain track or album information. Search results are narrowed
    down by comparing to track/album details passed into the function

    :param search_info: search info used for the API search
    :param song_mode: whether the search is for a song or an album
    :param comparison: a dictionary containing track/album info to compare to and narrow down search results
    :return:
    """
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
                if (artist in lower_search_track or artist in lower_search_artist) and track_name in lower_search_track and i == 0:
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
            print_message = f'Option {i}: {{track: {search_track}, artist: {search_artist}, album: {search_album}}}'
        else:
            print_message = f'Option {i}: {{album: {search_album}, artist: {search_artist}}}'
        print(print_message)
    move_on = False
    chosen_one = None
    while True:
        search_num = input("Which option do you choose? Type 'None' if you can't find anything. ")
        if search_num.lower() == 'none':
            move_on = True
            break
        num_response = search_num.isnumeric()
        if num_response and int(search_num) in range(len(reduced)):
            print(f"Chose option: {search_num}")
            chosen_one = reduced[int(search_num)]
            break
    return move_on, chosen_one


tracking = {}
for file in os.listdir(origin_dir):
    tracking[file] = "Nothing"

for file in os.listdir(origin_dir):
    print(f"\nAttempting to move file {file}")
    path = origin_dir + file
    new_path = starting_dir + file
    try:
        os.rename(path, new_path)
        tracking[file] = "Moved to Start"
    except FileExistsError as e:
        print(f"File name {file} already exists in {starting_dir}. Not moving file.\n")
        continue

    print(f"\nThe file you are currently editing is: {file}")
    new_name = input("What is the title of the song? Skip 'skip' if you want to skip this one. ")
    if new_name == 'skip' or new_name == "":
        pass
    else:
        path = starting_dir + file
        new_file_name = new_name + ".mp3"
        new_path = named_dir + new_file_name
        move_success = False
        while not move_success and new_name:
            try:
                os.rename(path, new_path)
                move_success = True
            except FileExistsError as e:
                print("File name already exists in new directory. Please choose a different name")
                new_name = input("What is the new file name of the song? (Entry will be the song title, for now) ")
                new_path = f"{named_dir}{new_name}.mp3"
        try:
            track = eyed3.load(new_path)
            tags = track.tag
            tags.title = new_name
            if tags.artist is not None:
                correct_artist = input(f"The current artist is {tags.artist}. Is this correct? (Y/y)")
                if correct_artist.lower() == 'y':
                    tags = None
                    continue
            artist = input("What is the artist for this track? ")
            tags.artist = artist
            tags.save()
            tags = None
            tracking[file] = "Named Modified"
        except Exception as e:
            print(f"Unable to add track title and artist details to {new_file_name}. Displaying error message and "
                  f"moving on")
            print(f"{e}\n")
            tags = None
            continue

        path = os.path.join(named_dir, new_file_name)
        new_path = os.path.join(details_dir, new_file_name)
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
        tags.title = chosen_search['trackName']
        tags.artist = chosen_search['artistName']
        tags.album = chosen_search['collectionName']
        tags.genre = chosen_search['primaryGenreName']
        tags.artist_url = chosen_search['artistViewUrl']
        tags.audio_file_url = chosen_search['trackViewUrl']
        tags.disc_num = (chosen_search['discNumber'], chosen_search['discCount'])
        tags.release_date = eyed3.core.Date.parse(chosen_search['releaseDate'])
        tags.track_num = (chosen_search['trackNumber'], chosen_search['trackCount'])
        tags.comments.set("")
        try:
            tags.save()
            tracking[file] = "Track Details"
        except UnicodeEncodeError as e:
            print(f"Unable to add track details to {file}. Displaying error message and moving on")
            print(f"{e}\n")
            tags = None
            continue
        album_not_found = True
        search_criteria1 = tags.album
        while album_not_found:
            album_not_found, chosen_album = searchNnarrow(search_info=search_criteria1, song_mode=False,  comparison={'album': tags.album})
            if album_not_found:
                search_criteria1 = input("What is your album search criteria? (Only alphanumeric searches) ")
        tags.album_artist = chosen_album['artistName']
        try:
            tags.save()
            tracking[file] = "Album Artist"
        except UnicodeEncodeError as e:
            print(f"Unable to add album artist to {file}. Displaying error message and moving on")
            print(f"{e}\n")
            tags = None
            continue

        tags = None
        os.rename(path, new_path)
        tracking[file] = "Success"

print("\nThese files were unsuccessful:")
for file, status in tracking.items():
    if status == "Nothing":
        print(file)

print("\nThese files were moved to starting dir:")
for file, status in tracking.items():
    if status == "Moved to Start":
        print(file)

print("\nThese files were successful:")
for file, status in tracking.items():
    if status == "Name Modified":
        print(file)

print("\nThese files had track details modified:")
for file, status in tracking.items():
    if status == "Track Details":
        print(file)

print("\nThese files had album artist modified:")
for file, status in tracking.items():
    if status == "Album Artist":
        print(file)

print("\nThese files were successful:")
for file, status in tracking.items():
    if status == "Success":
        print(file)
