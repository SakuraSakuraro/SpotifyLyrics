import requests
import sys

# Function for formating time to [mm:ss.SS]
def format_time(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    hundredths = (ms % 1000) // 10
    return f"[{minutes:02}:{seconds:02}.{hundredths:02}]"

# Check flags
debug_mode = "-debug" in sys.argv
track_id = None
track_name = None

# Parsing command line arguments
for i, arg in enumerate(sys.argv):
    if arg == "-id" and i + 1 < len(sys.argv):
        track_id = sys.argv[i + 1]
    elif arg == "-filename" and i + 1 < len(sys.argv):
        track_name = sys.argv[i + 1]

# Request track ID if not specified
if not track_id:
    track_id = input("Enter track ID: ").strip()

# Request file name if not specified
if not track_name:
    track_name = input("Enter track name for save file (e.g, MySong): ").strip()

# URL for GET
url = f"https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}/image/spotify%3Aimage%3Aab67616d0000b273fb8beba0a84eb86fad899b2d?format=json&vocalRemoval=false&market=from_token"

# Request headers
headers = {
    "Host": "spclient.wg.spotify.com",
    "Connection": "keep-alive",
    "Origin": "https://xpui.app.spotify.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.87 Spotify/1.2.5.1006 Safari/537.36",
    "accept": "application/json",
    "accept-language": "ja",
    "app-platform": "Win32",
    "authorization": "set your authorization token",
    "client-token": "set your client token",
    "sec-ch-ua": "\"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "spotify-app-version": "1.2.43",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://xpui.app.spotify.com/",
    "Accept-Encoding": "gzip, deflate, br",
}

# Send request
response = requests.get(url, headers=headers)

# Check response status code
if response.status_code == 200:
    # Save the original response for debugging if debug mode is enabled
    if debug_mode:
        with open("reply.txt", "w", encoding="utf-8") as file:
            file.write(response.text)

    # Process data
    data = response.json()
    lyrics = data.get("lyrics", {}).get("lines", [])
    sync_type = data.get("lyrics", {}).get("syncType", "UNSYNCED")

    # Transform data
    formatted_lyrics = []
    for line in lyrics:
        text = line["words"]
        if sync_type == "LINE_SYNCED":
            start_time_ms = int(line["startTimeMs"])
            time_formatted = format_time(start_time_ms)
            formatted_lyrics.append(f"{time_formatted}{text}")
        elif sync_type == "UNSYNCED":
            formatted_lyrics.append(text)

    # Save processed data to .lrc file
    output_file = f"{track_name}.lrc"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(formatted_lyrics))

    print(f"Data successfully transformed and written to {output_file}")
else:
    print(f"Error: failed to execute request (code {response.status_code})")
