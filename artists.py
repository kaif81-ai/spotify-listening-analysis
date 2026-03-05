"""Summarizes a user's music streaming history based on musical artist."""

def find_favorites(tracks_by_artist, min_tracks):
    """Returns a list of artists with at least min_tracks different (unique) tracks."""
    favorites = []
    for artist, tracks in tracks_by_artist.items():
        if len(tracks) >= min_tracks:
            favorites.append(artist)
    return favorites


def list_tracks(streams):
    """Returns a dict mapping artist name -> list of unique tracks (no repeats)."""
    tracks_by_artist = {}
    seen_by_artist = {}  # artist- set of tracks already added

    for stream in streams:
        artist = stream.get("artistName")
        track = stream.get("trackName")

        if artist not in tracks_by_artist:
            tracks_by_artist[artist] = []
            seen_by_artist[artist] = set()

        if track not in seen_by_artist[artist]:
            tracks_by_artist[artist].append(track)
            seen_by_artist[artist].add(track)

    return tracks_by_artist


def find_most_played(playtime_by_artist):
    """Returns the name of the artist with the most ms of playtime."""
    top_artist = ""
    for artist, ms in playtime_by_artist.items():
        if ms > playtime_by_artist.get(top_artist, 0):
            top_artist = artist
    return top_artist


def count_playtime(streams):
    """
    Returns a dict mapping artist name -> total playtime in ms (includes repeats).

    REQUIRED: uses nesting (artist loop + streams loop).
    """
    playtime_by_artist = {}

    # Use list_tracks to get the set of artists first
    tracks_by_artist = list_tracks(streams)

    # for each artisst, scan streams and sum msPlayed
    for artist in tracks_by_artist.keys():
        total_ms = 0
        for stream in streams:
            if stream.get("artistName") == artist:
                total_ms += stream.get("msPlayed", 0)
        playtime_by_artist[artist] = total_ms

    return playtime_by_artist
