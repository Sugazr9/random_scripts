import os
import eyed3

directory = "C:/Users/go_ar/OneDrive/Documents/Audacity/macro-output/"
interim_destination = "C:/Users/go_ar/Music/Audacity Modified/"
destination = "C:/Users/go_ar/Music/Name Modified/"

print(f"Moving files from {directory} to {interim_destination}\n")
for file in os.listdir(directory):
    print(f"\nAttempting to move file {file}")
    path = directory + file
    new_path = interim_destination + file
    try:
        os.rename(path, new_path)
    except FileExistsError as e:
        print(f"File name {file} already exists in {interim_destination}. Not moving file.\n")

print(f"\n\nAdding track and artist names for files")
for file in os.listdir(interim_destination):
    print(f"\nThe file you are currently editing is: {file}")
    new_name = input("What is the title of the song? Skip 'skip' if you want to skip this one. ")
    if new_name == 'skip' or new_name == "":
        pass
    else:
        file_name = new_name + ".mp3"
        path = interim_destination + file
        new_path = destination + file_name
        move_success = False
        while not move_success and new_name:
            try:
                os.rename(path, new_path)
                move_success = True
            except FileExistsError as e:
                print("File name already exists in new directory. Please choose a different name")
                new_name = input("What is the new file name of the song? (Song title will be first entry) ")
                new_path = f"{destination}{new_name}.mp3"
        try:
            track = eyed3.load(new_path)
            tags = track.tag
            if tags.artist is not None:
                correct_artist = input(f"The current artist is {tags.artist}. Is this correct? (Y/y)")
                if correct_artist.lower() == 'y':
                    tags = None
                    continue
            artist = input("What is the artist for this track? ")
            tags._setTitle(new_name)
            tags._setArtist(artist)
            tags.save()
            tags = None
        except:
            print(f"Track details for {new_name} not changed.")
