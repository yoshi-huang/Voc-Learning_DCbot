import pytz
from random import choice
from csv import reader as csv_reader

import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, date

from W2V_Relative import load_google_word2vec, vocList
from W2V_Relative import similar_above_threshold as resemb

# ------------------------------------------
# initialization
# ------------------------------------------

# TOKEN = ""
# CHANNEL_IDS = []  # CHANNEL ID 

TIMEZONE = pytz.timezone("Asia/Taipei")
TARGET_DATE = date(2026, 1, 17)  # target

global SCHEDULE, LEVELS, COUNTS
SCHEDULE = [7, 12, 23]
LEVELS = [1,2,3,3,3,4,4,4,4,5,5,6,6]
COUNTS = 3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

VOCLST = vocList()
with open('voc7000.csv', 'r', newline='', encoding='utf-8') as voc6000:
    vocs = csv_reader(voc6000, delimiter=',')
    for voc in vocs:
        VOCLST.append(Level=voc[0], voc=voc[1], part_of_speech=voc[2], translate=voc[3])

wv = load_google_word2vec(path="GoogleNews-vectors-negative300.bin")
print("len of vocabulary list:", len(VOCLST.voc))

# ------------------------------------------
# find resemble word function
# ------------------------------------------

def find_resemble_word(target_word, threshold_value:int = 0.6):

    top_words = resemb(target_word, VOCLST.voc, threshold=threshold_value, wv=wv)
    result=[]

    for w, score in top_words:
        word = VOCLST.get(VOCLST.voc.index(w))

        if word['vocabulary'] != target_word :
            vocabulary = (word['Level'], word['vocabulary'], word['translate'], word['part_of_speech'], score)
            if not vocabulary in result : result.append(vocabulary)
    
    return sorted(result, key=lambda word: word[0])
    # print(f"【 Words similar to '{target_word}' 】")
    # for word in result: print(f"LEVEL {word[0]}  {word[1]: <15} {word[3]: <5} {word[2]: <8}\t {word[-1]:.4f}")

def days_until_target():
    today = date.today()
    delta = TARGET_DATE - today
    return delta.days

# ------------------------------------------
# send daily message
# ------------------------------------------

async def send_daily_message():

    days_left = days_until_target()
    Time = datetime.now().hour
    lines = "### 本次的隨機 7000 單：\n"

    for i in range(COUNTS):
        level = choice(LEVELS) 
        wordTODAY = VOCLST.random_by_level(level)
        resemble_word = find_resemble_word(wordTODAY['vocabulary'])

        r = ""
        for word in resemble_word:
            r += f"\n**{word[1]: <15}** {word[3]: <5} {word[2]: <8}\tLEVEL {word[0]}"

        lines += f"### {i+1}：\t**{wordTODAY['vocabulary']: <15}** {wordTODAY['part_of_speech']: <5} {wordTODAY['translate']: <8}\tLEVEL {wordTODAY['Level']}\n"
        lines += f"### 其他近似的單字：{r}" if r else ""

    if 4 <= Time <= 10:
        TITLE = f"早安！ 距離 `學測` 還有 **{days_left}** 天 "
    elif 10 < Time <= 19:
        TITLE = f"午安！ 距離 `學測` 還有 **{days_left}** 天 "
    else:
        TITLE = f"晚安！ 距離 `學測` 還有 **{days_left}** 天 "

    embed = discord.Embed(
        title=TITLE,
        description=lines,
        color=discord.Color.blue()
    )

    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)

@bot.command(name='callVOC')
async def callTest(ctx):
    days_left = days_until_target()
    Time = datetime.now().hour
    lines = "### 本次的隨機 7000 單：\n"

    for i in range(COUNTS):
        level = choice(LEVELS) 
        wordTODAY = VOCLST.random_by_level(level)
        resemble_word = find_resemble_word(wordTODAY['vocabulary'])

        r = ""
        for word in resemble_word:
            r += f"\n**{word[1]: <15}** {word[3]: <5} {word[2]: <8}\tLEVEL {word[0]}"

        lines += f"### {i+1}：\t**{wordTODAY['vocabulary']: <15}** {wordTODAY['part_of_speech']: <5} {wordTODAY['translate']: <8}\tLEVEL {wordTODAY['Level']}\n"
        lines += f"### 其他近似的單字：{r}" if r else ""

    if 4 <= Time <= 10:
        TITLE = f"早安！ 距離 `學測` 還有 **{days_left}** 天 "
    elif 10 < Time <= 19:
        TITLE = f"午安！ 距離 `學測` 還有 **{days_left}** 天 "
    else:
        TITLE = f"晚安！ 距離 `學測` 還有 **{days_left}** 天 "

    embed = discord.Embed(
        title=TITLE,
        description=lines,
        color=discord.Color.blue()
    )

    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)

@bot.command(name='scheude')
async def SCHEDULE_setting(ctx, scheude: str = None):
    SCHEDULE = [ int(i) for i in scheude.split(",")]

@bot.command(name='voclevels')
async def SCHEDULE_setting(ctx, levels: str = None):
    LEVELS = [ int(i) for i in levels.split(",")]

@bot.command(name='counts')
async def SCHEDULE_setting(ctx, counts: str = None):
    COUNTS = [ int(i) for i in counts.split(",")]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    for T in SCHEDULE:
        scheduler.add_job(send_daily_message, "cron", hour=T, minute=0)
    scheduler.start()

bot.run(TOKEN)