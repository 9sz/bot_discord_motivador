import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

mensagens_tristes = ["triste", "to bad", "vida merda", "pra baixo", "to sad", "depre", "feels", ":(", "to mal", "não aguento mais", "Sad", "Triste", "Depre", "estou triste", "estou bad", "estou mal", "mto sad", "muito sad", "mto bad", "muito bad"]

starter_encouragements = [
  "Se entregar ao desânimo ou enfrentá-lo é a diferença mais notável entre vencer e ser vencido.",
  "Relaxa e goza.",
  "Tua hora de brilhar.",
  "Os momentos difíceis, é necessário e bom ultrapassá-los. É deles que tiramos o que é realmente valoroso para cada um de nós.",
  "Tudo o que vc precisa fazer é transformar teus demônios em poder e seguir em frente.",
  "Você alcançará seus objetivos quando deixar de andar acompanhado pelo desânimo.",
  "Tudo vai melhorar.",
  "Maior que a tristeza de não haver vencido é a vergonha de não ter lutado.",
  "Vai fumar uma maconha.",
  "Respira e dá uma sentada.",
  "Quem quica não chora",
  "Desânimo nenhum pode ser maior que a vontade de ser feliz e vencer!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('~inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in mensagens_tristes):
      await message.channel.send(random.choice(options))

  if msg.startswith("~new"):
    encouraging_message = msg.split("~new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("~del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("~del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("~list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("~responding"):
    value = msg.split("~responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))
