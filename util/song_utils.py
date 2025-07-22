from yt_dlp import YoutubeDL
from classes.Song import Song

async def determine_message_type(songElement):
  if (songElement.__contains__("https://www.youtube.com/") or songElement.__contains__("https://youtu.be/")): # dealing with an youtube URL
    submittedSong = await fetch_from_youtube_URL(songElement)
  else:
    submittedSong = await get_URL_from_title(songElement)
  if (submittedSong == None):
    await print(f"Could not find a suitable URL for the given title.")
  return submittedSong

async def get_URL_from_title(title):
  with YoutubeDL({
    "quiet": True,
    "skip_download": True,
    "noplaylist": True,  # ensure it's treated as a single video
    "format": "bestaudio/best"
  }) as ydl:
    try:
      search_result = ydl.extract_info(f"ytsearch1:{title}", download=False)
      if "entries" in search_result and search_result["entries"]:
        return await fetch_from_youtube_URL(search_result["entries"][0]["webpage_url"])
    except Exception as e:
      print("Search failed: ", e)

async def fetch_from_youtube_URL(url):
  try:
    with YoutubeDL({
      "quiet": True,
      "skip_download": True,
      "noplaylist": True,  # ensure it's treated as a single video
      "format": "bestaudio/best"
    }) as ydl:
      video_info = ydl.extract_info(url, download=False)
    if (url.__contains__("&list")):
      url = url[:url.index("&")]
  except Exception as e:
    print("Error extracting title:", e)
    return
  return Song(video_info.get("title", "Unknown Title"), f"{url}", video_info["url"])