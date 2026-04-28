---
name: twitter-video-download
description: >
  Download videos from Twitter/X using yt-dlp, verify with ffprobe, and deliver to Telegram.
  Use whenever the user shares a Twitter/X video URL (x.com/.../video/1).
category: media
---

# Twitter/X Video Download Workflow

## File Paths (CRITICAL - Updated 2026-04-27)
All downloaded videos go to `/Users/jiang/Desktop/hermes/media/` — NOT `~/.hermes/media/`

## Download Command
```bash
yt-dlp --no-playlist -f "bestvideo+bestaudio" "https://x.com/USERNAME/status/VIDEO_ID/video/1?s=XX" -o "/Users/jiang/Desktop/hermes/media/%(title)s.%(ext)s"
```
**Note:** yt-dlp on Twitter often fails with SSL errors (`EOF occurred in violation of protocol`) or HTTP 404 — use the Browser Console Extraction method below instead.

## Verification (ffprobe)
Always verify the downloaded video has a video stream and audio:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height -of csv=p=0 "PATH_TO_VIDEO.mp4"
```
Expected output: `h264,1280,720` or similar — confirms video has both video and audio streams.

Also check duration and completeness:
```bash
ffprobe -v error -show_entries format=duration,size "PATH_TO_VIDEO.mp4"
```

## Telegram Delivery
1. Send a text preview with video info (account name, title, resolution, size)
2. Send the video file using `MEDIA:/path/to/file.mp4`

Target Telegram chat: `telegram:1111860238` (dou bao)

## Daily News Briefing PDF Delivery
When sending daily news briefings, ALWAYS include:
1. Text summary (already done)
2. PDF file via `MEDIA:/Users/jiang/Desktop/hermes/news/YYYYMMDD_每日新闻简报.pdf`

Both must be sent separately — text first, then PDF file.

## Fallback: Browser Console Extraction (when yt-dlp SSL fails)

When yt-dlp fails with SSL/EOF errors on Twitter (common error: `HTTP Error 404` or `EOF occurred in violation of protocol`):

1. **Navigate to tweet in browser**
   ```
   browser_navigate → https://x.com/USERNAME/status/POST_ID
   ```

2. **Extract video URLs via browser console**
   ```
   browser_console → (() => { const html = document.documentElement.innerHTML; const matches = html.match(/https:\/\/video\.twimg\.com\/[^\"\\s]+/g); return JSON.stringify([...new Set(matches || [])]); })()
   ```
   Returns all video.twimg.com URLs found in the page — multiple resolutions (360p, 480p, 720p, 1080p) — de-duplicated.

3. **Check which resolutions are actually available**
   ```bash
   # Use HEAD request to check content-length without downloading
   curl -sI --max-time 15 "VIDEO_URL" | grep -i content-length
   ```
   - content-length > 0 = available
   - content-length: 0 = not available (try another resolution)
   - 360p: ~100MB for 1hr video
   - 480p: ~50MB for 1hr video
   - 720p: often unavailable (returns 0)
   - 1080p: ~460MB for 1hr video, download may timeout

4. **Download with curl (background for large files)**
   ```bash
   # Foreground for small files (<50MB)
   curl -sL --max-time 120 -L -o "OUTPUT.mp4" "VIDEO_URL"

   # Background for large files (use background=true with notify_on_complete)
   curl -sL --max-time 2400 -C - -L -o "OUTPUT.mp4" "VIDEO_URL"
   ```
   - `-C -` enables resume of interrupted downloads
   - `-L` follows redirects

5. **Monitor progress of background downloads**
   ```bash
   ls -lh "OUTPUT.mp4"  # check current size
   ```
   Twitter connection drops frequently; background download with resume (-C) makes incremental progress.

6. **Verify with ffprobe** (same as above)

## Common Patterns
- `x.com/.../video/1` — single video, use `--no-playlist`
- `x.com/.../status/...` — may contain multiple videos, `1` selects first video
- Title often contains Chinese/emoji characters, path must handle Unicode
- Twitter videos are hosted at `video.twimg.com/amplify_video/` with `vid/avc1/RESOLUTION/` subpaths
