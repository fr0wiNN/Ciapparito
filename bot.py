import asyncio
import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz

TOKEN = ""

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    wakeup_queue = asyncio.Queue()

    ## WAKEUP

    async def process_wakeup_queue():
        while True:
            user, ctx = await wakeup_queue.get()
            try:
                await handle_wakeup(user, ctx)
            finally:
                wakeup_queue.task_done()

    async def handle_wakeup(user, ctx):
        current_channel_id = '1064987439954939986'  # ekipa
        temp_channel_id = '1046864992990941184'  # klasyczek

        current_channel = ctx.guild.get_channel(int(current_channel_id))
        temp_channel = ctx.guild.get_channel(int(temp_channel_id))

        if temp_channel is not None and current_channel is not None:
            try:
                for i in range(3):
                    await user.move_to(temp_channel)
                    await asyncio.sleep(1)
                    await user.move_to(current_channel)
                await ctx.send(f'{user.display_name} has been woken up!')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to move {user.display_name}. Error: {e}')
        else:
            await ctx.send('Channel not found.')

    @bot.command()
    async def wakeup(ctx, user: discord.Member):
        await wakeup_queue.put((user, ctx))
        await ctx.send(f'{user.display_name} added to the wakeup queue!')

    @bot.event
    async def on_ready():
        print(f'Logged in as: {bot.user} (ID: {bot.user.id})')
        bot.loop.create_task(process_wakeup_queue())
        check_time.start()

    ## SLIDE

    @bot.command()
    async def slide(ctx, user: discord.Member):
        await ctx.send(f'Sliding {user.display_name}!')
        await handle_slide(user, ctx)

    async def handle_slide(user, ctx):
        channel_1_id = '1064987439954939986' # ekipa
        channel_2_id = '1051525618195497082' # geje
        channel_3_id = '1046864992990941184' # klasyczek
        channel_4_id = '906594462619303936' # dla debili
        channel_5_id = '965280880476180522' # cs
        channel_6_id = '879703228881711164' # fortnite
        channel_7_id = '1051537345087803422' # mine campf

        channel_1 = ctx.guild.get_channel(int(channel_1_id))
        channel_2 = ctx.guild.get_channel(int(channel_2_id))
        channel_3 = ctx.guild.get_channel(int(channel_3_id))
        channel_4 = ctx.guild.get_channel(int(channel_4_id))
        channel_5 = ctx.guild.get_channel(int(channel_5_id))
        channel_6 = ctx.guild.get_channel(int(channel_6_id))
        channel_7 = ctx.guild.get_channel(int(channel_7_id))

        if channel_1 is not None and channel_2 is not None:
            try:
                sleep_time = 1
                # sliding down
                await user.move_to(channel_2)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_3)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_4)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_5)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_6)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_7)
                await asyncio.sleep(sleep_time)
                # sliding up
                await user.move_to(channel_6)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_5)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_4)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_3)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_2)
                await asyncio.sleep(sleep_time)
                await user.move_to(channel_1)
                await ctx.send(f'{user.display_name} has been slided!')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to move {user.display_name}. Error: {e}')
        else:
            await ctx.send('Channel not found.')

    ## BARKA

    barka_normal_path = 'mp3/barka_normal.mp3'
    barka_drill_path = 'mp3/barka_drill.mp3'

    @bot.command()
    async def barka(ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()

            audio_source = discord.FFmpegPCMAudio(barka_normal_path)
            if not vc.is_playing():
                vc.play(audio_source, after=lambda e: print(f'Finished playing {e}'))

            while vc.is_playing():
                await asyncio.sleep(1)

            await vc.disconnect()
        else:
            await ctx.send("You need to be in a voice channel to use this command.")

    ## AUTOMATIC JOIN

    target_voice_channel_id = '1064987439954939986'  # Replace with your target voice channel ID

    @tasks.loop(seconds=60)  # Check every minute
    async def check_time():
        tz = pytz.timezone('Europe/Warsaw')  # Use the correct timezone for your location
        now = datetime.now(tz)
        print('------------------- LOG ----------------------')
        print(f"logging time: {now}")
        print(f"hour: {now.hour}")
        print(f"minute: {now.minute}")
        print(f"second: {now.second}")
        if now.hour == 21 and now.minute == 37:
            guild = bot.guilds[0]  # Assumes the bot is only in one guild
            voice_channel = guild.get_channel(int(target_voice_channel_id))
            if voice_channel:
                vc = await voice_channel.connect()
                audio_source = discord.FFmpegPCMAudio(barka_drill_path)
                if not vc.is_playing():
                    vc.play(audio_source, after=lambda e: print(f'Finished playing {e}'))

                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()

    bot.run(TOKEN, root_logger=True)

if __name__ == "__main__":
    print("Booting up the bot...")
    token_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ciapparito_token.txt')
    with open(token_file_path, 'r') as file:
        TOKEN = file.read().strip()
    run()
