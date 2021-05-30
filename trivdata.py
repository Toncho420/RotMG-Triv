#The dictionary of questions: the keys are the questions and the values are answers, if the question has one answer the value is a string or a tuple if the same answer can be answered in multiple ways
#the answer is a list if the question has multiple right answers. Image questions are presented as tuples where the first item is the question and the second is the image location
#When the user has the wrong answer the correct answer is presented as 1)if string it is the string; 2)if it's a tuple the first answer gets displayed; 3)if it's a list a randomly selected answer that begins with a capital letter is displayed
trivdict = {"How many classes are there in RotMG?":"17", "How many dungeons are in the Court of Oryx?":"5", "Which boss is immune to Armor Brake?":["Void Entity","Oryx 3","void","o3"], "How many items can make the player Invulnerable?":"5",
"How many shots does the Staff of Extreme Prejudice shoots?":"10", "Which weapon in the game is the only one to do flat damage?":("Ray katana","ray"), "How many pet families are there in the game?":"14",
"How many rooms are there between the starting room and dungeon boss room in The Nest?":"5", "Who is the advisor of Oryx the Mad God?":"Shaitan", "Which Court of Oryx dungeon doesn't have a Skin in it's loot table?":("Lair of Shaitan", "shaitan"),
"Which Event Boss doesn't drop a Shield Rune?":["Avatar", "Dwarf Miner", "miner", "Lost Sentry", "sentry", "nest"], "Which Event Boss can spawn multiple times per realm?":["Cube God", "cube", "Pentaract", "pent", "penta", "Skull Shrine", "shrine", "skull"],
"Which God in the Godlands had it's sprite changed 2 times?":"Leviathan", "How many UTs are there in The Machine?":"26", "Which God in the Godlands was the last one to receieve a dungeon?":"Beholder", "Which class has 75 attack and 75 dexterity stat cap?":("Wizard", "wiz"),
"Which ring allows the user to become invisible?":["Crystallised Mist", "mist"], "How much Feed Power does a legendary egg has?":"3000", "Is King Alexander alive?":"He lives and reigns and conquers the world.",
"How many items can inflict the debuff Dazed on an enemy?":"3", "Which UT item can petrify the player?":"Karma Orb", "Who turned the Master Rat into a rodent?":"Dr.Terrible", "Which key was received by leveling a Ninja to 20 on Kongregate?":["Treasure Map","tcave"],
"Which dungeon's mark is seen in both Standard and Mighty quests?":["Mountain Temple", "mt", "Third Dimension", "3d"], "Which Epic quest mark is seen in the Mighty quests?":"Nest", "Which Cloak allows the Rogue to teleport to cursor location?":["Planewalker", "plane"],
"Which weapon has the highest base damage in the game?":"Blade of Ages", "How much Forgefire do you get per day?":"300", "How many pet abilities are there in the game?":"9", "Which armor gives the highest amount of defense?":["candycoated", "cc"],
"How is the Magical Lodestone often referred as?":"potato", "Which UT item has the highest feed power?":("Omnipotence Ring","omni"), "What is the lowest tier in the game?":"0", "In what year was The Shatters added to the game?":"2013",
"Which dungeon has a limit of 1 player?":("Santa's Workshop","workshop"), "In what bag the Wine Cellar Incantations used to drop from?":"white", "Which Robe class doesn't have a Wisdom Modifer?":["Wizard", "wiz", "Bard", "Summoner"],
"How many Cultists do you fight in the Cultist Hideout?":"5", "How many Event Whites are in the game?":"15", "In what bag does the Ring of Decades drop?":"Red", "In the dungeons Fungal Cavern and Crystal Cavern, how many Cavern Crystals must be destroyed to power up the drill to 100%?":"25",
"Which weapon has the most range in the game?":("B.O.W", "bow"), "How many rooms are there between the starting room and dungeon boss room in the Ocean Trench?":"11", "Which ability has the highest MP cost?":("Scholar's Seal", "scholar", "sseal"),
"What is the player limit of the Heroic dungeons?":"15", "How many abilities can inflict Armor Brake?":"3", "Which poison has the longest duration?":("Plague poison", "plague"), "What is the highest weapon tier you can find in a Purple Bag?":"9",
"What year held the first Month of the Mad God?":"2014", "Which Pet Food item can be found in the Toxic Sewers dungeon?":("Power pizza", "pizza"), "How much Fame did it cost to enter The Arena?":"250", "How many Drake Eggs are there in the game?":"6",
"How many UT items does the boss Crystal Entity drops?":"5", "Which Class has the least amount of UT abilities?":"Bard", "Which Class has the most amount of UT abilities?":"Archer"}

print(f"Amount of triv questions: {len(trivdict)}")

alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

#The dictioanry to call emojies
charemojies = {'a': ':regional_indicator_a:', 'b': ':regional_indicator_b:', 'c': ':regional_indicator_c:', 'd': ':regional_indicator_d:', 'e': ':regional_indicator_e:', 'f': ':regional_indicator_f:', 'g': ':regional_indicator_g:', 'h': ':regional_indicator_h:', 'i': ':regional_indicator_i:', 'j':
':regional_indicator_j:', 'k': ':regional_indicator_k:', 'l': ':regional_indicator_l:', 'm': ':regional_indicator_m:', 'n': ':regional_indicator_n:', 'o': ':regional_indicator_o:', 'p': ':regional_indicator_p:', 'q': ':regional_indicator_q:', 'r': ':regional_indicator_r:', 's': ':regional_indicator_s:',
't': ':regional_indicator_t:', 'u': ':regional_indicator_u:', 'v': ':regional_indicator_v:', 'w': ':regional_indicator_w:', 'x': ':regional_indicator_x:', 'y': ':regional_indicator_y:', 'z': ':regional_indicator_z:', ' ': ':blue_square:'}

#The list of words to scramble using scramble
scramblelist = ()

#lists of Replies in case of right, wrong or no/late answers
rightansw = ("That is correct!", "That's correct.", "Correct answer!", "You're right!", "Your answer is correct!", "Nice one.", "That answer is correct!", "Spot on!", "Right on!", "Nicely done.", "Well done.", "Good job!", "Correct!", "That's true!", "Right answer!")
wrongansw = ("That's not quite right.", "That's not right...", "Your answer isn't correct.", "You're mistaken.", "Not correct...", "Not quite it...", "From the Ghastly Eyrie I can see to the ends of the world, and from this vantage point I declare with utter certainty that your answer is wrong.", "YOU GET NOTHING, GOOD DAY SIR!", "At least you tried...")
lateansw = ("You ran out of time.", "Too late.", "You didn't answer in time.", "Be quicker next time...", "You're out of time.", "Out of time.", "Time grinds even questions to dust.", "You took too much time.", "Time is the cruelest cut.", "Time's up.", "Don't wait too long...")

#Detailed command infos for ppe help command
command_dinfos = {}

#The bazaar system:
bazaar_items = {"Robe of the Mad Scientist":3500}
bazaar_descriptions = {"Robe of the Mad Scientist":"Lower cooldowns for commands by 25%."}
