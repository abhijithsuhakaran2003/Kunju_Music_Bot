m = await send(f"__**Searching for {query} on YouTube.**__")
    try:
        results = await arq.youtube(query, 1)
        link = f"https://youtube.com{results[0].url_suffix}"
        title = results[0].title
        thumbnail = results[0].thumbnails[0]
        duration = results[0].duration
        views = results[0].views
        if time_to_seconds(duration) >= 1800:
            await m.edit("__**Bruh! Only songs within 30 Mins.**__")
            playing = False
            return
    except Exception as e:
        await m.edit("__**Found No Song Matching Your Query.**__")
        playing = False
        print(str(e))
        return
    await m.edit("__**Processing Thumbnail.**__")
    await generate_cover(requested_by, title, views, duration, thumbnail)
    await m.edit("__**Downloading Music.**__")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    await m.edit("__**Transcoding.**__")
    os.rename(audio_file, "audio.webm")
    transcode("audio.webm")
    await m.delete()
    m = await app.send_photo(
        chat_id=sudo_chat_id,
        caption=f"**Playing** **[{title}]({link})** Via YouTube.",
        photo="final.png",
    )
    os.remove("final.png")
    await asyncio.sleep(int(time_to_seconds(duration)))
    playing = False
    await m.delete()


# Telegram Audio--------------------------------------------------------------------------------


@app.on_message(
    filters.command("telegram") & filters.chat(sudo_chat_id) & ~filters.edited
)
async def tgplay(_, message):
    global playing
    if len(queue) != 0:
        await send("__**You Can Only Play Telegram Files After The Queue Gets Finished.**__")
        return
    if not message.reply_to_message:
        await send("__**Reply to an audio.**__")
        return
    if message.reply_to_message.audio:
        if int(message.reply_to_message.audio.file_size) >= 104857600:
            await send("__**Bruh! Only songs within 100 MB.**__")
            playing = False
            return
        duration = message.reply_to_message.audio.duration
        if not duration:
            await send("__**Only Songs With Duration Are Supported.**__")
            return
        m = await send("__**Downloading.**__")
        song = await message.reply_to_message.download()
        await m.edit("__**Transcoding.**__")
        transcode(song)
        await m.edit(f"**Playing** **{message.reply_to_message.link}.**")
        await asyncio.sleep(duration)
        playing = False
        return
    await send("__**Only Audio Files (Not Document) Are Supported.**__")


async def send(text):
    m = await app.send_message(sudo_chat_id, text=text, disable_web_page_preview=True)
    return m


print("\nBot Starting...\nFor Support Join https://t.me/InfoHubKerala\n")


app.run()




