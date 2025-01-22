import discord, ast
from Algorithm import getCombos, factCalc
from main import initiateDate, getSingleProb, getAllProb
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 1. Set up Intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content (requires enabling in Developer Portal)

# 2. Create the Bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """
    This event is called when the bot has finished connecting to Discord.
    """
    print(f"Logged in as {bot.user}")


# Example function for probability or any custom calculation
def calculate_probability(list1, list2):
    return getAllProb(list1, list2)


@bot.command(name="helpme")
async def help_command(ctx):
    """
    A custom 'helpme' command to guide users on how to use other commands.
    """
    help_text = (
        "This bot is used to calculate the probability of drawing specific cards in an MTG (Magic: The Gathering) game. "
        "For example, if your deck has 37 lands, 15 creatures, and 20 instants, and you want to see the probability of drawing "
        "at least 3 lands, 1 creature, and 2 instants in your 7-card opening hand, this bot can compute it. "
        "Currently, it supports calculations for three categories and will be expanded to more in the future.\n\n"

        "Please enter two groups of numbers:\n"
        "1. The first list describes the composition of your deck (e.g., 37 for lands, 15 for creatures, etc.).\n"
        "2. The second list specifies how many cards from each category you want to draw in your opening 7 cards. "
        "   The elements in the second list can be zero if you don't care of a given category.\n\n"
        
        "To calculate your probability, you can use command !prob:\n"
        "**!prob 37 15 20, 3 1 2**\n"
        "For more detailed results, use command !detail:\n"
        "!detail 37 15 20, 3 1 2\n\n"

        "More features will be added later."
    )
    await ctx.send(help_text)


@bot.command()
async def prob(ctx, *, content: str):
    """
    Usage:
      !prob 37 15 20, 3 1 2

    This command:
      1) Splits the user's input on a comma to separate two groups of numbers.
      2) Parses the first group (e.g., '37 15 20') into a deck composition list.
      3) Parses the second group (e.g., '3 1 2') into the desired-draw list.
      4) Checks sums against 99 (for deck) and 7 (for opening hand).
      5) (For demonstration) sends the parsed results back to the channel.
         - Replace this part with your probability calculation logic if needed.
    """
    try:
        # Example: content = "37 15 20, 3 1 2"
        # Split at the comma
        left_str, right_str = content.split(",")

        # Strip whitespace
        left_str = left_str.strip()
        right_str = right_str.strip()

        # Parse each side into lists of integers
        deck_nums = [int(x) for x in left_str.split()]  # e.g., [37, 15, 20]
        want_nums = [int(x) for x in right_str.split()]  # e.g., [3, 1, 2]

        # Optional checks
        if sum(deck_nums) > 99:
            await ctx.send("Error: The sum of the first group cannot exceed 99.")
            return
        if sum(want_nums) > 7:
            await ctx.send("Error: The sum of the second group cannot exceed 7.")
            return

        deck_nums.insert(0, 99)
        want_nums.insert(0, 7)

        # 4. Call your custom calculation function
        fullRes, simpRes = calculate_probability(deck_nums, want_nums)

        # Replace the following with your real probability calculations
        await ctx.send(
             f"The probability of given data is: {simpRes}"
        )

    except ValueError:
        await ctx.send(
            "Please make sure your input includes valid integers separated by spaces, "
            "and a comma to split the two groups. "
            "Example: `!prob 37 15 20, 3 1 2`"
        )
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


@bot.command()
async def detail(ctx, *, content: str):
    """
    Usage:
      !prob 37 15 20, 3 1 2

    This command:
      1) Splits the user's input on a comma to separate two groups of numbers.
      2) Parses the first group (e.g., '37 15 20') into a deck composition list.
      3) Parses the second group (e.g., '3 1 2') into the desired-draw list.
      4) Checks sums against 99 (for deck) and 7 (for opening hand).
      5) (For demonstration) sends the parsed results back to the channel.
         - Replace this part with your probability calculation logic if needed.
    """
    try:
        # Example: content = "37 15 20, 3 1 2"
        # Split at the comma
        left_str, right_str = content.split(",")

        # Strip whitespace
        left_str = left_str.strip()
        right_str = right_str.strip()

        # Parse each side into lists of integers
        deck_nums = [int(x) for x in left_str.split()]  # e.g., [37, 15, 20]
        want_nums = [int(x) for x in right_str.split()]  # e.g., [3, 1, 2]

        # Optional checks
        if sum(deck_nums) > 99:
            await ctx.send("Error: The sum of the first group cannot exceed 99.")
            return
        if sum(want_nums) > 7:
            await ctx.send("Error: The sum of the second group cannot exceed 7.")
            return

        deck_nums.insert(0, 99)
        want_nums.insert(0, 7)

        # 4. Call your custom calculation function
        fullRes, simpRes = calculate_probability(deck_nums, want_nums)

        max_length = 2000

        if len(fullRes) <= max_length:
            await ctx.send(
                f"The probability of given data is: {fullRes}"
            )
        else:
            # Otherwise, send in chunks
            for i in range(0, len(fullRes), max_length):
                chunk = fullRes[i: i + max_length]
                await ctx.send(chunk)

    except ValueError:
        await ctx.send(
            "Please make sure your input includes valid integers separated by spaces, "
            "and a comma to split the two groups. "
            "Example: `!prob 37 15 20, 3 1 2`"
        )
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


# 6. Run the bot with your token
bot.run(TOKEN)
