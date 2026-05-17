import csv
import sys
from pathlib import Path

MUSICLIST = [
    "My Spotify Library.CSV",
    "My YouTubeMediaConnect Library.CSV",
]


def read_music_csv(file_name: str) -> list[dict]:
    """Read one CSV file and return its rows as dictionaries."""
    path = Path(file_name)
    with path.open(mode="r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def read_all_music_lists(file_list: list[str]) -> dict[str, list[dict]]:
    """Read all CSV files listed in file_list."""
    data: dict[str, list[dict]] = {}
    for file_name in file_list:
        data[file_name] = read_music_csv(file_name)
    return data


def infer_artist_name(row: dict) -> str:
    """Return artist name, inferring from track title when CSV artist is empty."""
    artist = (row.get("Artist name") or "").strip()
    if artist:
        return artist

    track_name = (row.get("Track name") or "").strip()
    for separator in (" - ", " \u00b7 ", " | "):
        if separator in track_name:
            return track_name.split(separator, 1)[0].strip()
    return ""


def get_unique_overview(all_data: dict[str, list[dict]]) -> tuple[list[str], list[str]]:
    """Build sorted unique artist and playlist lists from all source rows."""
    unique_artists: set[str] = set()
    unique_playlists: set[str] = set()

    for rows in all_data.values():
        for row in rows:
            artist_name = infer_artist_name(row)
            playlist_name = (row.get("Playlist name") or "").strip()

            if artist_name:
                unique_artists.add(artist_name)
            if playlist_name:
                unique_playlists.add(playlist_name)

    return sorted(unique_artists, key=str.casefold), sorted(unique_playlists, key=str.casefold)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        # Avoid UnicodeEncodeError in Windows terminals.
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    loaded_data = read_all_music_lists(MUSICLIST)
    for name, rows in loaded_data.items():
        print(f"Loaded {len(rows)} rows from {name}")

    artists, playlists = get_unique_overview(loaded_data)

    print("\nUnique Artist name values (combined):")
    for artist in artists:
        print(f"- {artist}")

    print("\nUnique Playlist name values (combined):")
    for playlist in playlists:
        print(f"- {playlist}")
