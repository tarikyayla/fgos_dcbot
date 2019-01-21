import discord
from freegamesonsteam_bot import Vt,Config,updater
from time import sleep

client = discord.Client()
channel = discord.Object(id=Config.channel_id)

async def background_loop():
    await client.wait_until_ready()
    while not client.is_closed:
        await updater()
        for post in Vt.get_items():
            await client.send_message(channel,"{}\n{}".format(post[2],post[1]))
            Vt.update_item(post)
            sleep(10)
        await sleep(60*60)


client.loop.create_task(background_loop())
client.run(Config.bot_token)
