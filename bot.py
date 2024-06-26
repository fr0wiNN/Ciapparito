import asyncio
import os
import discord
from discord.ext import commands

TOKEN = ""

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    wakeup_queue = asyncio.Queue()

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

    @bot.event
    async def on_ready():
        print(f'Logged in as: {bot.user} (ID: {bot.user.id})')
        bot.loop.create_task(process_wakeup_queue())

    @bot.command()
    async def wakeup(ctx, user: discord.Member):
        await wakeup_queue.put((user, ctx))
        await ctx.send(f'{user.display_name} added to the wakeup queue!')

    bot.run(TOKEN, root_logger=True)

if __name__ == "__main__":
    print("Booting up the bot...")
    token_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ciapparito_token.txt')
    with open(token_file_path, 'r') as file:
        TOKEN = file.read().strip()
    run()
