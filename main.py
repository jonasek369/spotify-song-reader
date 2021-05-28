import spotipy
import time

class getPlayingSong:
    def __init__(self, spotipy_id, spotipy_secret, spotipy_redirect_uri, username, scope='user-read-currently-playing'):
        self.spotipy_id = spotipy_id
        self.spotipy_secret = spotipy_secret
        self.spotipy_red_url = spotipy_redirect_uri
        self.username = username
        self.scope = scope
        self.current_token = ""
        print("getting token")
        getPlayingSong.get_token(self)

    def get_token(self):
        self.current_token = spotipy.util.prompt_for_user_token(self.username, self.scope, self.spotipy_id, self.spotipy_secret, self.spotipy_red_url, "save")
        return

    def get_current(self, songtype="full"):
        if len(self.current_token) == 0:
            getPlayingSong.get_token(self)
            return getPlayingSong.get_current(self)

        else:
            sp = spotipy.Spotify(auth=self.current_token)
            current_song = sp.currently_playing()
            song_name = current_song["item"]["name"]
            artists = current_song["item"]["album"]["artists"]
            all_ = ""

            for pos, artist in enumerate(artists):
                if pos + 1 == len(artists):
                    all_ += artist["name"]
                else:
                    all_ += artist["name"] + ", "

            if songtype == "full":
                return all_ + " - " + song_name
            if songtype == "artist":
                return all_
            if songtype == "songname":
                return song_name

    def loop_over(self):
        current_song = ""
        while True:
                try:
                    get_ = getPlayingSong.get_current(self)
                    if get_ == current_song:
                        continue
                    else:
                        current_song = get_
                        print(current_song)
                        with open("current_playing.txt", "r+") as save:
                            save.truncate(0)
                            save.write(current_song)
                            save.close()
                    time.sleep(1)
                except:
                    time.sleep(2.5)
                    sp = spotipy.Spotify(auth=self.current_token)
                    try_song = sp.currently_playing()
                    print(try_song)
                    if try_song == "none" or try_song == None:
                        continue
                    else:
                        if len(try_song) < 600:
                            continue
                        print("refreshing token")
                        getPlayingSong.get_token(self)


with open("config.cfg", "r") as read_config:
    all = read_config.readlines(0)
    client_id = all[0].split('=')[1][1:99999].replace('"', "").strip()
    client_secret = all[1].split('=')[1][1:99999].replace('"', "").strip()
    redirection_url = all[2].split('=')[1][1:99999].replace('"', "").strip()
    username = all[3][11:99999].replace('"', "").strip()

gps = getPlayingSong(spotipy_id=client_id, spotipy_secret=client_secret, spotipy_redirect_uri=redirection_url, username=username)
print(gps.loop_over())
