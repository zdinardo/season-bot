import os
from datetime import date, datetime

import interactions
from interactions import SlashContext, slash_command

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

def get_season(now):
  Y = 2000  # dummy leap year to allow input XXXX-02-29 (leap day)
  seasons = [('❄️winter', (date(Y, 1, 1), date(Y, 3, 20))),
             ('🌷spring', (date(Y, 3, 21), date(Y, 6, 20))),
             ('🌞summer', (date(Y, 6, 21), date(Y, 9, 22))),
             ('🍂fall', (date(Y, 9, 23), date(Y, 12, 20))),
             ('❄️winter', (date(Y, 12, 21), date(Y, 12, 31)))]
  if isinstance(now, datetime):
    now = now.date()
  now = now.replace(year=Y)
  return next(season for season, (start, end) in seasons
              if start <= now <= end)

@slash_command(name="season-wtf",
               description="Update channel name to current season.")
async def season_wtf(ctx: SlashContext):
  await ctx.defer()

  season = get_season(date.today())
  new_name = '{}-{}-wtf'.format(season, date.today().year)
  await ctx.channel.edit(name=new_name)
  await ctx.send('The new channel name is \"{}\"'.format(new_name))

print('starting bot...')
bot = interactions.Client(token=DISCORD_BOT_TOKEN,
                          intents=interactions.Intents.MESSAGES)
bot.start()