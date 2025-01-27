import discord
from main import getAllProb
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up Intents
intents = discord.Intents.default()
intents.message_content = True

# Create the Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# 全局变量，控制是否喂过 Bot
font_size_increased = False


def format_output(text):
    """
    根据 font_size_increased 状态格式化输出文字。
    如果 Bot 被喂过（font_size_increased = True），输出加粗和大写。
    """
    global font_size_increased
    if font_size_increased:
        return f"**{text.upper()}**"  # 加粗并转为大写
    return text  # 原样输出


@bot.event
async def on_ready():
    """Triggered when the bot is connected to Discord."""
    print(f"Logged in as {bot.user}")


def parse_input(content: str):
    """
    Parse user input into two lists of integers.

    :param content: Input string in the format "37 15 20, 3 1 2"
    :return: Two lists of integers (deck_nums, want_nums)
    """
    try:
        left_str, right_str = content.split(",")
        deck_nums = [int(x) for x in left_str.strip().split()]
        want_nums = [int(x) for x in right_str.strip().split()]
        return deck_nums, want_nums
    except ValueError:
        raise ValueError(
            format_output("Invalid input. Ensure the input is two groups of integers separated by a comma. "
            "Example: `!prob 37 15 20, 3 1 2`")
        )


def validate_input(deck_nums, want_nums):
    """
    Validate the parsed input.

    :param deck_nums: List of deck composition integers.
    :param want_nums: List of desired draw integers.
    :return: None if valid, raises ValueError otherwise.
    """
    if sum(deck_nums) > 99:
        raise ValueError(format_output("The sum of the first group (deck composition) cannot exceed 99."))
    if sum(want_nums) > 7:
        raise ValueError(format_output("The sum of the second group (desired draws) cannot exceed 7."))


@bot.command(name="helpme")
async def help_command(ctx):
    """
    Provides guidance on how to use the bot's commands.
    """
    if font_size_increased:
        help_text = "Kill the duck."
    else:
        help_text = (
            "This duck calculates the probability of drawing specific cards in a MTG commander game.\n\n"
            "### Example\n"
            "`!prob 37 15 20, 3 1 2`\n"
            "This calculates, if your deck has **37** lands, **15** creatures, and **20** instants, "
            "what's the probability of drawing AT LEAST **3** lands, **1** creature, and **2** instants in your 7-card opening hand.\n\n"
            "### Rules\n"
            "- The first group describes your deck composition (e.g., 37 lands, 15 creatures, etc.).\n"
            "- The second group describes how many cards from each category you want to draw, 0 if you don't care.\n"
            "- The first group must sum to 99 or less.\n"
            "- The second group must sum to 7 or less.\n"
            "- DO NOT feed the duck.\n\n"
            "**Commands**\n"
            "`!prob`: Returns the probability in short form.\n"
            "`!detail`: Returns detailed results."
    )
    await ctx.send(help_text)


async def handle_calculation(ctx, content, detailed=False):
    """
    Handle probability calculation for both `!prob` and `!detail` commands.

    :param ctx: Discord context.
    :param content: User input string.
    :param detailed: Whether to return detailed results.
    """
    try:
        # Parse and validate input
        deck_nums, want_nums = parse_input(content)
        validate_input(deck_nums, want_nums)

        # Add 99 and 7 as first elements for total cards and total draw cards
        deck_nums.insert(0, 99)
        want_nums.insert(0, 7)

        # Calculate probabilities
        full_res, simp_res = getAllProb(deck_nums, want_nums)

        # Return results
        if detailed:
            max_length = 2000
            if len(full_res) <= max_length:
                await ctx.send(format_output(full_res))
            else:
                # Send detailed results in chunks
                for i in range(0, len(full_res), max_length):
                    await ctx.send(format_output(full_res[i:i + max_length]))
        else:
            await ctx.send(format_output(f"The probability of given data is: {simp_res}"))

    except ValueError as ve:
        await ctx.send(format_output(str(ve)))
    except Exception as e:
        await ctx.send(format_output(f"An unexpected error occurred: {e}"))


@bot.command(name="feed")
async def feed_command(ctx):
    """
    Simulates feeding the bot. Increases font size.
    """
    global font_size_increased
    if not font_size_increased:
        font_size_increased = True
        await ctx.send("...Didn't I tell you not to feed the duck?")
    else:
        await ctx.send(format_output("Thank you but duck is full <3"))


@bot.command(name="kill")
async def kill_command(ctx):
    """
    Simulates killing the bot. Resets font size.
    """
    global font_size_increased
    if font_size_increased:
        font_size_increased = False
        await ctx.send("The duck has been killed. No more big fonts.\n"
                       "Here's a new duck. Learn your lesson.")
    else:
        await ctx.send("NO you freaking monster.")


@bot.command()
async def prob(ctx, *, content: str):
    """
    Calculates the probability in short form.
    Usage: !prob 37 15 20, 3 1 2
    """
    await handle_calculation(ctx, content, detailed=False)


@bot.command()
async def detail(ctx, *, content: str):
    """
    Calculates the probability with detailed results.
    Usage: !detail 37 15 20, 3 1 2
    """
    await handle_calculation(ctx, content, detailed=True)


# Run the bot
bot.run(TOKEN)

