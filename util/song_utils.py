from yt_dlp import YoutubeDL
from classes.Song import Song

async def determineMessageType(songElement):
  if (songElement.__contains__("https://www.youtube.com/") or songElement.__contains__("https://youtu.be/")): # dealing with an youtube URL
    submittedSong = await fetchFromYoutubeURL(songElement)
  else:
    submittedSong = await getURLFromTitle(songElement)
  return submittedSong

async def getURLFromTitle(title):
  with YoutubeDL({
    "quiet": True,
    "skip_download": True,
    "noplaylist": True,  # ensure it's treated as a single video
    "format": "bestaudio/best"
  }) as ydl:
    try:
      search_result = ydl.extract_info(f"ytsearch1:{title}", download=False)
      if "entries" in search_result and search_result["entries"]:
        return await fetchFromYoutubeURL(search_result["entries"][0]["webpage_url"])
    except Exception as e:
      print("Search failed: ", e)

async def fetchFromYoutubeURL(url):
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
  return Song(video_info.get("title", "Unknown Title"), f"<{url}>", video_info["url"])