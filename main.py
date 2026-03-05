import artists
import streaming_history


def run_tests():
    # Test cases (required) — tiny dataset
    sample = [
        {"artistName": "A", "trackName": "t1", "msPlayed": 1000},
        {"artistName": "A", "trackName": "t1", "msPlayed": 2000},  # repeat track
        {"artistName": "A", "trackName": "t2", "msPlayed": 3000},
        {"artistName": "B", "trackName": "x",  "msPlayed": 500},
    ]

    tracks = artists.list_tracks(sample)
    assert tracks["A"] == ["t1", "t2"]
    assert tracks["B"] == ["x"]

    playtime = artists.count_playtime(sample)
    assert playtime["A"] == 1000 + 2000 + 3000
    assert playtime["B"] == 500

    assert artists.find_most_played(playtime) == "A"
    assert set(artists.find_favorites(tracks, 2)) == {"A"}

    print("[tests] passed")


def get_streams_for_date():
    """
    REQUIRED:
    - try/except for wrong date(s) entered
    - user types in year -> cast to int
    - if not castable: except + break loop
    """
    # Only April data  is provided, but we wrap it in a year/month structure.
    data = {
        2024: {
            "april": streaming_history.april,
        }
    }

    while True:
        year_in = input("Enter a year (e.g., 2024) or type 'quit': ").strip().lower()
        if year_in == "quit":
            return None

        try:
            year = int(year_in)
        except ValueError:
            print("Year must be an integer. Exiting.")
            return None  # break the loop requirement

        if year not in data:
            print("No data available for that year. Try again.")
            continue

        month_in = input("Enter a month (e.g., april) or type 'quit': ").strip().lower()
        if month_in == "quit":
            return None

        if month_in not in data[year]:
            print("No data available for that month/year. Try again.")
            continue

        return data[year][month_in]


def main():
    run_tests()

    streams = get_streams_for_date()
    if streams is None:
        return

    # Total playtime per artist (uses nesting inside count_playtime)
    playtime_by_artist = artists.count_playtime(streams)
    top_artist = artists.find_most_played(playtime_by_artist)

    print(f"\nYour top artist by playtime was {top_artist}.")

    tracks_by_artist = artists.list_tracks(streams)
    print(f"\nYou listened to these {top_artist} tracks (unique):")
    for track in tracks_by_artist.get(top_artist, []):
        print(f"* {track}")

    print("\nYou're a true fan of these artists (>= 10 unique tracks):")
    for artist in artists.find_favorites(tracks_by_artist, 10):
        print(f"* {artist}")

    #user input using while loop, quit breaks
    while True:
        cmd = input("\nType 'top' (top artist), an artist name (msPlayed), or 'quit': ").strip()
        if cmd.lower() == "quit":
            break
        if cmd.lower() == "top":
            print(f"Top artist: {top_artist} ({playtime_by_artist.get(top_artist, 0)} ms)")
        else:
            ms = playtime_by_artist.get(cmd)
            if ms is None:
                print("Artist not found in this dataset.")
            else:
                print(f"{cmd}: {ms} ms")


if __name__ == "__main__":
    main()
