import discord
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
# List of grade  to check
GRADE_ID = [747710162801786922, 747709432774918186, 541705433069649931, 541705436081160192, 649733488932814863, 823277528759795802]

# List of blacklisted users
blacklisted_users = []

# Path to txt file
BLACKLIST_FILE = "blacklist.txt"

# Load list of blacklisted users from txt file
def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        open(BLACKLIST_FILE, "w").close()
    with open(BLACKLIST_FILE, "r") as file:
        for line in file:
            user_id = int(line.strip())
            blacklisted_users.append(user_id)

# Save list of blacklisted users to txt file
def save_blacklist():
    with open(BLACKLIST_FILE, "w") as file:
        for user_id in blacklisted_users:
            file.write(str(user_id) + "\n")

# Check user ranks daily
async def check_grades(guild):
    for member in guild.members:
        for role in member.roles:
            if role.id in GRADE_ID:
                if member.id not in blacklisted_users:
                    blacklisted_users.append(member.id)
                    save_blacklist()

# Automatically ban a blacklisted user if they join the server
async def on_member_join(member):
    if member.id in blacklisted_users:
        await member.send("T ban sale merde")
        await member.ban(reason="Vous êtes sur la liste noire")
        
# Discord initialization
client = discord.Client()

@client.event
async def on_ready():
    print("Le bot est en ligne")
    guild = client.get_guild(541703278967128125) # Id de la guilde
    await check_grades(guild)

@client.event
async def on_member_join(member):
    await on_member_join(member)

# Load blacklist from txt file
load_blacklist()

# Discord bot token

client.run("token")
