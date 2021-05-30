import random
import discord
import asyncio
import json
import ast
import time
import os
from fuzzywuzzy import fuzz
from discord.ext import commands

os.chdir(r"F:\RotMG bot\New_WinRAR_ZIP_archive\RotMGTriv")


#importing all trives from trivdata
import trivdata
#trivdict is for triv, blitz, duel, freeforall, shopkeepdict is for shoptriv, icontrivdict - icontriv, audiotriv - audiotriv, scramblelist - scramble
trivdict, scramblelist = trivdata.trivdict, trivdata.scramblelist
#getting their lengths for the indicies, hence the -1
trivlen, scramblelen = len(trivdict)-1, len(scramblelist)-1
#getting all of their keys and values as seperate lists
trivkeys, trivvalues = list(trivdict.keys()), list(trivdict.values())


#lists of Replies in case of right, wrong or no/late answers
rightansw, wrongansw, lateansw = trivdata.rightansw, trivdata.wrongansw, trivdata.lateansw
#for scramble
charemojies = trivdata.charemojies

def open_json(jsonfile):
	with open(jsonfile, "r") as fp:
		return json.load(fp)	#openfunc for jsonfiles

def save_json(jsonfile, name):	#savefunc for jsonfiles
	with open(jsonfile, "w") as fp:
		json.dump(name, fp)

def strip_str(text):		#function to remove punctuations, spaces and "the" from string and make it lowercase,
	punctuations = ''' !-;:`'".,/_?'''			# in order to compare bot answers and user replies
	text2 = ""
	for char in text.lower().replace("the ", ""):
		if char not in punctuations:
			text2 = text2 + char
	return text2

def find_correct_answer(dictvalue):			#function to find the correct answer to a triv, used for all triv commands except shoptriv
	if type(dictvalue) == str:
		return dictvalue
	elif type(dictvalue) == tuple:
		return dictvalue[0]
	else:
		return random.choice([z for z in dictvalue if z[0].isupper()])

def calc_time(question, answer):			#Function to calculate time for each question according to its size(for blitz)
	queslen = len(question)
	if type(answer) == str:			#takes the length of the raw answer
		answlen = len(answer)
	else:						#takes the average length of all answers
		answlen = sum(map(len, answer))/len(answer)
	seconds = queslen/12 + answlen/5
	return seconds

class Player():
	def __init__(self, author, ctx):
		self.server, self.channel, self.author = ctx.guild, ctx.channel, author
		self.users = open_json("users.json")
		self.rng = open_json("rngfix.json")
		id = str(self.author.id)
		if id not in self.users.keys():
			self.users[id] = {"fame":10, "items":"[]"}
			save_json("users.json", self.users)
		serv_id = str(self.server.id)
		if serv_id not in self.rng.keys():
			self.rng[serv_id] = {"trivnumbers":"[]", "scramblenumbers":"[]"}
			save_json("rngfix.json", self.rng)
		try:
			self.inventory = ast.literal_eval(self.users[str(author.id)]["items"])
		except KeyError:
			self.inventory = []
		self.saves = (4600 in self.inventory)

	def unique_int_randomizer(self, length, listkey):		#player.unique_int_randomizer used in par with the rngfix.json file to avoid repeating numbers(questions)
		serv_id = str(self.server.id)
		numlist = ast.literal_eval(self.rng[serv_id][listkey])			#convert list string to list
		if len(numlist) > length*7/8:			#if amount of numbers surpass 5/6ths of the total amount delete a chunk of the numbers at the start
			del numlist[:round(length/7)]
			save_json("rngfix.json", self.rng)
		while True:
			n = random.randint(0, length)
			if n not in numlist:		#get a number that isn't already used and append it to the list of numbers in use
				numlist.append(n)
				self.rng[serv_id][listkey] = str(numlist)		#convert list back to string list
				save_json("rngfix.json", self.rng)
				return n

	def compare_strings(self, text, answer):            #function to compare user input and actual answer
		striptext = strip_str(text)        #first we use strip_str on both strings which removes spaces, "the" and unwanted symbols
		if type(answer) == str:
			stripanswer = strip_str(answer)
			ratio = fuzz.ratio(striptext, stripanswer)
		else:                        #if there are multiple answers we pick out the answer that is most similar to the input
			stripanswers = [strip_str(x) for x in answer]
			ratios = []
			for i in stripanswers:            #fill a list with levenshtein ratios
				ratios.append(fuzz.ratio(striptext, i))
			ratio = max(ratios)                #take the max value, its index and the actual string by the index
		if 4852 in self.inventory:        #if user has monkey king bar they get away with more mistakes #rotmg mkb lol
			bool = (ratio > 86)    #change bool to 1 if it's correct
		else:
			bool = (ratio > 97)
		return bool

	def add_fame(self, newfame):        #add fame to users
		id = str(self.author.id)
		multiplier = 1
		if 2200 in self.inventory:
			multiplier += 0.2
		if 2476 in self.inventory:
			multiplier += 0.05
		newfame *= multiplier
		self.users[id]["fame"] = self.users[id]["fame"] + round(newfame)
		save_json("users.json", self.users)
		return round(newfame)

class trives(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief = "A single RotMG related question for a bit of fame.", aliases = ["t"])
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def triv(self, ctx):
		player = Player(ctx.author, ctx)
		trivn = player.unique_int_randomizer(trivlen, "trivnumbers")			#Random number to give a random question
		question, answer = trivkeys[trivn], trivvalues[trivn]
		correctansw = find_correct_answer(answer)
				#Find the correct answer to be displayed incase user gets it wrong
		if type(question) == tuple:			#if the question comes with an image
			await ctx.send(f"**```{question[0]}```**", file=discord.File(f"./trivimages/{question[1]}"))
		else:													#for normal string questions
			await ctx.send(f"**```{question}```**")
		def check(m):
			return m.channel == player.channel and m.author == player.author		#checks if the reply came from the same person in the same channel
		try:
			msg = await self.bot.wait_for("message", check=check, timeout=11)
		except asyncio.TimeoutError:		#If too late
			await ctx.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
		else:
			if player.compare_strings(msg.content, answer):
				g = player.add_fame(24)
				await ctx.send(f"**{random.choice(rightansw)}** you got ``{g}`` fame.")
			else:
				if type(answer) == list:
					await ctx.send(f"**{random.choice(wrongansw)}** One of the possible correct answer was ``{correctansw}``")
				else:
					await ctx.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")

	@commands.command(brief = "Recognize hero names among scrambled letters.", aliases = ["shuffle", "mix"])
	@commands.cooldown(1, 8, commands.BucketType.user)
	async def scramble(self, ctx):
		player = Player(ctx.author, ctx)
		scramblen = player.unique_int_randomizer(scramblelen, "scramblenumbers")			#Random number to give a random question
		correctansw = scramblelist[scramblen]			#the correct answer
		scrambledworde = []			#empty list to .join() emojies onto
		charlist = list(correctansw.lower().replace("'", ""))			#converting string to list
		for char in random.sample(charlist, len(charlist)):		#shuffling the word list and looping through it
			scrambledworde.append(charemojies[char])		#picking up values of charemojies of the lowercase characters
		output = " ".join(scrambledworde)					#joining them to form a string of all emojies to output
		await ctx.send(f"**``Unscramble this name:``**\n{output}")
		def check(m):
			return m.channel == player.channel and m.author == player.author		#checks if the reply came from the same person in the same channel
		try:
			msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(25.ppe))
		except asyncio.TimeoutError:		#If too late
			await ctx.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
		else:
			if player.compare_strings(msg.content, correctansw):
				g = player.add_fame(min(12, len(correctansw))*8)
				await ctx.send(f"**{random.choice(rightansw)}** you got ``{g}`` fame.")
			else:
				await ctx.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")


	@commands.command(brief = "Rapid questions that give more fame but with a risk.")
	@commands.cooldown(1, 52, commands.BucketType.channel)
	async def blitz(self, ctx):
		player = Player(ctx.author, ctx)
		timeout = time.time() + player.shiva(50)		#full time for blitz round
		accumulated_g = 0
		ncorrectansws = 0
		await ctx.send(f"""You have ``{player.shiva(48)}`` seconds for the blitz, don't forget to type in **skip** if you don't know the answer to minimize the fame and time you lose.""")
		time.sleep(3.7)
		while True:
			time.sleep(0.2)
			if time.time() > timeout:			#stop the blitz, add accumulated fame to user.
				g = player.add_fame(ncorrectansws*(accumulated_g+(2*ncorrectansws)-2))		#((2a+d(n-1))/2)n a = 0 d = 4  n = ncorrectanswsers
				await ctx.send(f"**{player.author.display_name}** you got ``{ncorrectansws}`` correct answers and accumulated ``{g}`` fame during the blitz.")
				break
			trivn = player.unique_int_randomizer(trivlen, "trivnumbers")		#Random number to give a random question
			question, answer = trivkeys[trivn], trivvalues[trivn]
			correctansw = find_correct_answer(answer)
			if type(question) == tuple:		#if the question comes with an image
				await ctx.send(f"**```{question[0]}```**", file=discord.File(f"./trivimages/{question[1]}"))
				giventime = player.shiva(calc_time(question[0], answer))
			else:										#for normal string questions
				await ctx.send(f"**```{question}```**")
				giventime = player.shiva(calc_time(question, answer))
			def check(m):
				return m.channel == player.channel and m.author == player.author		#checks if the reply came from the same person in the same channel
			try:
				msg = await self.bot.wait_for("message", check=check, timeout=player.shiva(giventime))
			except asyncio.TimeoutError:			#If too late
				await ctx.send(f"**{random.choice(lateansw)}**, The correct answer was ``{correctansw}``.")
				accumulated_g -= 21
			else:
				if strip_str(msg.content) == "skip":		#if user wants to move onto the next question
					accumulated_g -= 4
					if type(answer) == str or type(answer) == tuple:
						await ctx.send(f"The correct answer was ``{correctansw}``.")
					else:
						await ctx.send(f"One of the possible answers was ``{correctansw}``.")
				elif player.compare_strings(msg.content, answer):		#If there is one correct answer
					accumulated_g += 18
					ncorrectansws += 1
				else:
					accumulated_g -= 12
					if type(answer) == list:
						await ctx.send(f"**{random.choice(wrongansw)}** One of the possible answers was ``{correctansw}``")
					else:
						await ctx.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``.")


	@triv.error
	async def triverror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			users = open_json("users.json")
			if 3500 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
				if error.retry_after < 3:		#if user has mad robe and the remaining time of the cooldown is Less
					await ctx.reinvoke()		#than the time mad robe saves the user just bypasses the cooldownerror
					return
				else:
					await ctx.send("**Triv** is on **cooldown** at the moment. Try again in a few seconds")
			else:
				await ctx.send("**Triv** is on **cooldown** at the moment. You can buy a **Robe of the Mad Scientist** in the bazaar to decrease command cooldowns.")

	@blitz.error
	async def blitzerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send("**Blitz** is on being used in this channel at the moment, wait a bit or play on a different channel.")

	async def cog_command_error(self, ctx, error):
		#Errors to be ignored
		if isinstance(error, (commands.CommandOnCooldown, commands.MissingRequiredArgument, commands.BadArgument)):
			pass
		else:
			raise error

def setup(bot):
	bot.add_cog(trives(bot))
