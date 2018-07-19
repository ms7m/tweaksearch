"""
Created by:

oganessium
exofeel

License: GNU GENERAL PUBLIC LICENSE v3.0
"""

import discord
from discord.ext import commands
import asyncio
import platform
import json
import requests
from bs4 import BeautifulSoup
import re
client = discord.Client()


# You're welcome to remove these if you'd like.
"""
So to add a prohibited repo, just take the repo name as listed in
the website but add a space in the beginning, I could fix that but I'm
too lazy
"""
prohibited_repos = [' RKO1195 repo', ' Team Kodi']

class tweaksearch(object):
	def __init__(self, bot):
		self.bot = bot
	
	# Credit to Yak for doing the hard stuff
	# much love
	@client.event
	async def on_message(self, message):
		
		if "[[" in message.content and "]]" in message.content:
			if message.content.count('[[') > message.content.count(']]'):
				repeat=message.content.count(']]')
			elif message.content.count('[[')==message.content.count(']]'):
				repeat=message.content.count(']]')
				
			else:
				repeat=message.content.count('[[')
			searching_message = await self.bot.send_message(message.channel, "🔄")
			xxx=0
			keywords = []
			while xxx < repeat:
				notregex = message.content.split("[[")[xxx+1]
				notregex = notregex.split("]]")[0]
				keywords.append(notregex)
				xxx+=1
			for aaaa in keywords:
		#main Function
				
				# check for piracy (need to find a better way, most likely
				# going block specific repos but the website should handle it)
				
				# Main Start
				try:
					if keywords == "":
						await self.bot.send_message(message.channel, "No tweak detected.. ``[[Palette]]]``")
					req = requests.get("https://www.ios-repo-updates.com/search/?s={}&section=all&repo=all".format(aaaa))
				except Exception as e:
					await self.bot.say(e)
					await self.bot.say("Please contact exofeel.")
					print(e)

				# Get Link + Search Results and add them to Dictionary
				searchResults = []
				try:
					soup = BeautifulSoup(req.text, 'html.parser')
					for elem in soup.find_all('a', href=re.compile('/pack/')):
						searchResults.append(elem['href'])
					# Grab First Link **To DO: Add feature to make user choose which tweak.
					link = "https://www.ios-repo-updates.com" + searchResults[0]
				except Exception as e:
					await self.bot.send_message(message.channel, "Tweak could not be found.")
					#await self.bot.say(e)
					print(e)
					return

				
				

				# Add Information to Dictionary for later Use
				try:
					req = requests.get(link)
					soup = BeautifulSoup(req.text, 'html.parser')
					sources = []
					#paid_check = ['no']
					for text in soup.find_all('li', {"class": "list-group-item"}):
						try:
							text2 = text.text
							info = text2.split(':')[1]
							sources.append(info)
						except Exception as e:
							pass

				except Exception as e:
					await self.bot.say("Tweak Could not be found")
					#await self.bot.say(e)

				# Check if tweak has been updated (work in progress)
				try:
					updateCheck = soup.find_all('b', text='Updated Date ')
					if len(updateCheck) > 0:
						updated = True
					else:
						updated = False	
				except Exception as e:
					await self.bot.send_message(message.channle, "There has been a critical error. You should never get an error like this. Please contact exofeel or yak\nErrorCode: 979698")			
					print(e)
				
				
				
				# Check for paid package
				try:
					test = soup.find_all('b', text='Paid package')
					test2 = soup.find_all('b', text='Paid package :')
					if len(test) > 0:
						paid = "Yes"
					else:
						if len(test2) > 0:
							paid = "Yes"
						else:

							paid = "No"
				except Exception as e:
					await self.bot.send_message(message.content, e)



				try:
					if "No package found" in sources:
						await self.bot.say(message.channel, "Tweak could not be found.")
						return
					else:
						pass
				except Exception:
					pass
				


				# Check for Depiction and Grab the Depiction (Simple)
				try:
					depictionCheck = soup.find(text="Depiction")
					if depictionCheck == "Depiction":
						depictionActive = True
						LinkRaw = soup.find('a', {'class' : 'btn btn-default btn-xs'})
						link2 = LinkRaw['href']
					else:
						depictionActive = False
						link2 = 'cydia.com'
				except Exception as e:
					#await self.bot.send_message(message.channel, "Unknown error has occured. Please contact exofeel")
					linkCheck = False
					#await self.bot.say(e)

			
				#grab repo
				try:
					if depictionActive == False:
						repo = soup.find('a', {'rel' : 'nofollow'}).text
						if repo == "":
							repoLink = "No link found."
						else:
							repoLink = repo
					else:
						pass
				except Exception as e:
					print(e)



				# Grab Description
				try:
					tweakDescription = soup.find('p', {'class', 'text-center'}).text
					if tweakDescription == "":
						tweakDescriptionFinal = "N/A"
					else:
						tweakDescriptionFinal = tweakDescription
				except Exception as e:
					tweakDescription = "Unknown"
					#await self.bot.say(e)
					pass

				
				# Grab Title
				try:
					title = soup.find('span', {'itemprop' : 'headline'}).text
				except Exception as e:
					title = "Unknown"
					#await self.bot.say(e)
					pass
				



				# Check if prohibted Repo
				try:
					for x in sources:
						if x in prohibited_repos:
							return
						else:
							pass
				except Exception as e:
					print(e)


				# Embed the info now

				# Basically distinguish between the categories Yak Style
				if " Tweaks" in sources:
					embed = discord.Embed(colour=discord.Colour(0xf8d21c))
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/465952129815805962/465978476168609802/unknown.png")
					embed.add_field(name="Tweak Name", value=title)

				elif " Themes" in sources:
					embed = discord.Embed(colour=discord.Colour(0x1c85ff))
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/465952129815805962/465980222869864468/unknown.png")
					embed.add_field(name="Theme Name", value=title)

				elif " System" in sources:
					embed = discord.Embed(colour=discord.Colour(0xff4848))
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/465952129815805962/465981400172986378/unknown.png")
					embed.add_field(name="Tweak Name", value=title)

				else:
					embed = discord.Embed(colour=discord.Colour(0x969696))
					embed.add_field(name="Tweak Name", value=title)

				embed.set_footer(text="Cydia Search")

				embed.add_field(name="Identifier", value=sources[0])
				embed.add_field(name="Description", value=tweakDescriptionFinal)
				embed.add_field(name="Version", value=sources[9], inline=True)
				
				embed.add_field(name="Paid Package", value=paid, inline=True)

				
				if " BigBoss" in sources:
					embed.add_field(name="Depiction", value="Default Repo", inline=True)
				else:
					if depictionActive == True:
						embed.add_field(name="Depiction", value="[Depiction]({})".format(link2), inline=True)
					else:
						embed.add_field(name="Repo", value=repoLink, inline=True)

				await self.bot.delete_message(searching_message)
				await self.bot.send_message(message.channel, embed=embed)


def setup(bot):
    bot.add_cog(tweaksearch(bot))