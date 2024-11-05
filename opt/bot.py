import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import arxiv
from transformers import pipeline
import asyncio
from pytz import timezone


translator = pipeline('translation', model='facebook/mbart-large-50-one-to-many-mmt', src_lang='en_XX', tgt_lang='ja_XX')

intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

scheduler = AsyncIOScheduler(timezone=timezone('Asia/Tokyo'))

@scheduler.scheduled_job('cron', hour=7, minute=30)
async def scheduled_paper_post():
    channel = bot.get_channel(1303097125340446801)
    await fetch_and_send_paper(channel)

async def fetch_and_send_paper(channel):
    search_terms = [
    ('image processing', '画像処理'),
    ('security', 'セキュリティ'),
    ('Image Generation', '画像生成')
    ]
    for query, jp_query in search_terms:
        search = arxiv.Search(
            query=query,
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for result in search.results():
            title_translation = translator(result.title, max_length=400)[0]['translation_text']
            summary_translation = translator(result.summary, max_length=1000)[0]['translation_text']
            message = (
                f"**Title:** {title_translation}\n"
                f"**Authors:** {', '.join(author.name for author in result.authors)}\n"
                f"**Summary:** {summary_translation}\n"
                f"**PDF Link:** {result.pdf_url}\n"
                f"----------------------------------\n"
            )
            await channel.send(message)

@bot.event
async def on_ready():
    print("Hello!")
    print(f'Logged in as {bot.user}')
    scheduler.start() 

@bot.event
async def on_message(message: discord.Message):
    # メッセージ送信者がBot(自分を含む)だった場合は無視する
    if message.author.bot:
        return

    # メッセージが"hello"だった場合、"Hello!"と返信する
    if message.content.lower() == 'hello':  # 小文字で比較
        await message.reply("Hello!")

    # コマンド処理を行う
    await bot.process_commands(message)

@bot.command(name='ronbun')
async def fetch_paper(ctx):
    search_terms = [
        ('image processing', '画像処理'),
        ('security', 'セキュリティ'),
        ('Image Generation', '画像生成')
    ]

    for query, jp_query in search_terms:
        search = arxiv.Search(
            query=query,
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for result in search.results():
            title_translation = translator(result.title, max_length=400)[0]['translation_text']
            summary_translation = translator(result.summary, max_length=1000)[0]['translation_text']
            message = (
                f"**Title:** {title_translation}\n"
                f"**Authors:** {', '.join(author.name for author in result.authors)}\n"
                f"**Summary:** {summary_translation}\n"
                f"**PDF Link:** {result.pdf_url}\n"
                f"----------------------------------\n"
            )
            await ctx.send(message)


TOKEN = 'your_token'
bot.run(TOKEN)