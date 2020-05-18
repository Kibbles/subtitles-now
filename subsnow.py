#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Subtitles Now is a subtitle downloader for Democracy Now! .mp4 videos.

from sys import argv
from os import remove

import youtube_dl
import webvtt


if __name__ == "__main__":
    if len(argv) > 1:
        video_url = argv[1]
    else:
        video_url = input("Copy and paste a Democracy Now video URL: ")

    video_url = video_url.strip()

    # Match the Democracy Now video filenames (ex. dn2020-0515.mp4)
    video_id = video_url.split("/")
    video_date_month = int(video_id[5])
    video_date_day = int(video_id[6])

    # Pad the day and month with a zero if necessary.
    if video_date_month < 10:
        video_date_month = "0" + video_id[5]
    if video_date_day < 10:
        video_date_day = "0" + video_id[6]
    video_id = "dn", str(video_id[4]), "-", str(video_date_month), str(video_date_day)
    video_id = (''.join(video_id))

    # Options for youtube-dl to download just the subtitles in .vtt format
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'allsubtitles': True,
        'outtmpl': video_id
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Convert the .vtt file to .srt

    vtt_filepath = video_id + ".en.vtt"

    vtt = webvtt.read(vtt_filepath)
    vtt.save_as_srt(video_id + ".srt")

    # Delete the .vtt file
    remove(vtt_filepath)

    print("Subtitle downloaded and converted (" + video_id + ".srt)")
