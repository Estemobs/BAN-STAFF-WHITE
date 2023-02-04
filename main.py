import discord
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Liste des IDs de grades à vérifier
GRADE_ID = [747710162801786922, 747709432774918186, 541705433069649931, 541705436081160192, 649733488932814863, 823277528759795802]

# Liste des utilisateurs blacklistés
blacklisted_users = []

# Chemin vers le fichier txt
BLACKLIST_FILE = "blacklist.txt"

# Charger la liste des utilisateurs blacklistés à partir du fichier txt
def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        open(BLACKLIST_FILE, "w").close()
    with open(BLACKLIST_FILE, "r") as file:
        for line in file:
            user_id = int(line.strip())
            blacklisted_users.append(user_id)

# Enregistrer la liste des utilisateurs blacklistés dans le fichier txt
def save_blacklist():
    with open(BLACKLIST_FILE, "w") as file:
        for user_id in blacklisted_users:
            file.write(str(user_id) + "\n")

# Vérifier les grades des utilisateurs tous les jours
async def check_grades(guild):
    for member in guild.members:
        for role in member.roles:
            if role.id in GRADE_ID:
                if member.id not in blacklisted_users:
                    blacklisted_users.append(member.id)
                    save_blacklist()

# Ban automatiquement un utilisateur blacklisté s'il rejoint le serveur
async def on_member_join(member):
    if member.id in blacklisted_users:
        await member.send("T ban sale merde")
        await member.ban(reason="Vous êtes sur la liste noire")
        
# Initialisation de Discord
client = discord.Client()

@client.event
async def on_ready():
    print("Le bot est en ligne")
    guild = client.get_guild(541703278967128125) # Id de la guilde
    await check_grades(guild)

@client.event
async def on_member_join(member):
    await on_member_join(member)

# Charger la blacklist à partir du fichier txt
load_blacklist()

# Connexion au bot Discord

client.run("token")
