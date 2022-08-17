import discord  # Import the original discord.py module
# from discord.ext import commands  # Import the discord.py extension "commands"
# import discord_slash  # Import the third-party extension discord_slash module
from disnake.ext import commands
from discord.ui import button, Button, View
from discord.interactions import Interaction
import sqlite3
import asyncio
import random

bot = commands.Bot(
    command_prefix='!',
    test_guilds=[482012169911664640, 192460940409700352],
    sync_commands_debug=True
)
conn = sqlite3.connect("pugbotdb.db")
c = conn.cursor()

with open('token.txt', 'r') as t:
    discordtoken = t.read()

print(discordtoken)

runninglist = []


### Tell me bot is running
###################################################################################################################

@bot.event
async def on_ready():
    print("Bot is online")  # Make sure it's on


###################################################################################################################


########
############## Functions
########

######## Lists players in a gametype
def listplayers(gametype, server, channel):
    modnameparsed = str(gametype)

    modnameparsed = modnameparsed.replace('(', '')
    modnameparsed = modnameparsed.replace(')', '')
    modnameparsed = modnameparsed.replace(',', '')

    c.execute(
        "SELECT playername FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + server + "' AND channel = '" + channel + "'")

    response = c.fetchall()

    b = [i[0] for i in response]
    i = 0

    playerlist = ''

    while i < len(b):
        c.execute(
            "SELECT (julianday('now') - julianday(time)) * 24 * 60 * 60 FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + server + "' AND channel = '" + channel + "' AND playername = '" +
            b[i] + "'")
        timetest = c.fetchall()
        t = [i[0] for i in timetest]
        timediff = str(time_elapsed(t[0]))
        timediff = timediff.replace("'", '')

        playertime = (b[i] + ' ' + timediff + ':small_orange_diamond:')

        playerlist = playertime + playerlist

        i = i + 1
    size = len(playerlist)
    playerlist = playerlist[:size - 22]

    # gets number of players in mod
    c.execute(
        "SELECT COUNT(*) FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + server + "' AND channel = '" + channel + "'")

    playernum = c.fetchall()

    parsedplayernum = str(playernum).replace('[', '')
    parsedplayernum = parsedplayernum.replace(']', '')
    parsedplayernum = parsedplayernum.replace(')', '')
    parsedplayernum = parsedplayernum.replace('(', '')
    parsedplayernum = parsedplayernum.replace(',', '')

    # (parsedplayernum)

    c.execute(
        "SELECT playerlimit FROM modsettings WHERE mod='" + gametype + "' AND server = '" + server + "' AND channel = '" + channel + "'")
    playerlimit = c.fetchall()

    parsedplayerlimit = str(playerlimit)
    parsedplayerlimit = parsedplayerlimit.replace('[', "")
    parsedplayerlimit = parsedplayerlimit.replace('', "")
    parsedplayerlimit = parsedplayerlimit.replace('(', "/")
    parsedplayerlimit = parsedplayerlimit.replace(')', "")
    parsedplayerlimit = parsedplayerlimit.replace(',', "")

    parsedresponse = '**__' + modnameparsed + ': [' + parsedplayernum + parsedplayerlimit + '__**' + ' \n ' + \
                     playerlist

    ###await ctx.channel.send(f'{parsedresponse} ')

    return (parsedresponse)


########

######## Lists players to pick
def listpicks(gametype):
    modnameparsed = 'temp'

    #!#!#!#!#!#!#!#!#! ROW ID NEEDS TO BE AN ACTUAL PICK INDEX VARIABLE IN COLUMN  #!#!#!#!#!#!#!#!

    c.execute("SELECT rowid, playername FROM " + modnameparsed + " WHERE pickorder is 0 AND captain IS NULL")

    response = c.fetchall()

    c.execute("SELECT rowid FROM " + modnameparsed + " WHERE pickorder is 0 AND captain IS NULL")
    pickindex = c.fetchall()
    final_result = [i[0] for i in pickindex]

    ###
    ### MAKE THIS A FUNCTION EVENTUALLY
    ###

    parsedresponse = str(response).replace('(', '**')
    parsedresponse = parsedresponse.replace(')', '')
    parsedresponse = parsedresponse.replace(", '", ')** ')
    parsedresponse = parsedresponse.replace("'", '')
    parsedresponse = parsedresponse.replace(', ', ':small_orange_diamond:')
    parsedresponse = parsedresponse.replace(',', '')
    parsedresponse = parsedresponse.replace(']', '')
    parsedresponse = parsedresponse.replace('[', '')

    parsedresponse = '**__' + gametype + ':__**' + ' \n ' + \
                     parsedresponse

    ###await ctx.channel.send(f'{parsedresponse} ')

    return (parsedresponse, final_result)


######## Lists players on team
def listteampicks(gametype, team):
    modnameparsed = 'temp'

    c.execute("SELECT playername FROM " + modnameparsed + " WHERE team = '" + team + "' ORDER BY pickorder")

    response = c.fetchall()

    ###
    ### MAKE THIS A FUNCTION EVENTUALLY
    ###

    # !#!#!#! Every other comes out bold. fix it | UPDATE: FIXED. SHITTILY

    parsedresponse = str(response).replace('(', '**')
    parsedresponse = parsedresponse.replace(')', '')
    parsedresponse = parsedresponse.replace(", '", ')** ')
    parsedresponse = parsedresponse.replace("'", '')
    parsedresponse = parsedresponse.replace(', ', ':small_orange_diamond:')
    parsedresponse = parsedresponse.replace(',', '')
    parsedresponse = parsedresponse.replace(']', '')
    parsedresponse = parsedresponse.replace('[', '')
    parsedresponse = parsedresponse.replace("**", '')

    return (parsedresponse)


########


######## Randomly Selects Captains removes from current list

def randcapt(gametype, numplayers, server, channel):
    # !#!#!#!#!#! GENERATE LIST BASED ON numplayers!
    ####temp_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # !#!#!#!#!#! GENERATE LIST BASED ON numplayers!

    numplayers = numplayers[0]

    x = numplayers

    z = []
    for i in range(x):
        i = i * 1
        z.append(i)

    temp_list = z

    random_id1 = random.randint(0, numplayers-1)
    random_id2 = random.choice([ele for ele in temp_list if ele != random_id1])

    modnameparsed = str(gametype)

    modnameparsed = modnameparsed.replace('(', '')
    modnameparsed = modnameparsed.replace(')', '')
    modnameparsed = modnameparsed.replace(',', '')

    c.execute(
        "SELECT players FROM playerlist WHERE mod = '" + modnameparsed + "' AND serverid = '" + str(
            server) + "' AND channelid = '" + str(channel) + "' ;")

    players = c.fetchall()

    print('players: ' + str(players))
    print('rand1: ' + str(random_id1))
    print('rand2: ' + str(random_id2))

    playerstr1 = str(players[random_id1])
    playerstr2 = str(players[random_id2])

    return (playerstr1, playerstr2)


########

######## Rounds time to minutes / hours

def time_elapsed(seconds):
    if seconds > 3600:
        a = str(int(seconds // 3600))
        d = ["{}h".format(a)]
    else:
        b = str(int((seconds % 3600) // 60))
        d = ["{}m".format(b)]

    return d


#### Begins timer to remove idle player

async def playertimer(server, chan, channelname, gametype, name):
    await asyncio.sleep(7200)

    c.execute(
        "DELETE FROM playerlist WHERE server = '" + server + "' AND channel = '" + channelname +
        "' AND mod = '" + gametype + "' AND playername = ('" + str(name) + "');")
    conn.commit()

    print("TIMED OUT")
    await chan.send(name + ' has timed out of ' + gametype)


#### Begins countdown timer for random captains

async def countdown(time, chan, chanid, server, modname):

    for x in range(1, time):
        if x == 1:
            message = await chan.send(f'{modname} has been filled \n Choosing Random Captains in ' + str(time))
            await asyncio.sleep(1)
            time = time - 1

        await message.edit(content=f'{modname} has been filled \n Choosing Random Captains in ' + str(time))
        await asyncio.sleep(1)
        time = time - 1

    c.execute(
        "SELECT playerlimit FROM modsettings WHERE mod='" + modname + "' AND serverid = '" + str(
            server) + "' AND channelid = '" + str(chanid) + "'")
    playerlimit = c.fetchall()

    captains = randcapt(modname, playerlimit[0], server, chanid)

    red_captain = captains[0]
    blue_captain = captains[1]

    xparsed1 = str(red_captain).replace('(', '')
    xparsed1 = xparsed1.replace(')', '')
    xparsed1 = xparsed1.replace("'", '')
    xparsed1 = xparsed1.replace(',', '')

    xparsed2 = str(blue_captain).replace('(', '')
    xparsed2 = xparsed2.replace(')', '')
    xparsed2 = xparsed2.replace("'", '')
    xparsed2 = xparsed2.replace(',', '')

    await message.edit(
        content=f'**Random captains selected** \n Red Team: <@{xparsed1}> \n Blue Team: <@{xparsed2}>'
                f' \n <@{xparsed1}> to pick')

    ####### Assign captains 1 or 2
    c.execute("UPDATE temp SET captain = 1 WHERE players = '" + xparsed1 + "'")
    conn.commit()
    c.execute("UPDATE temp SET captain = 2 WHERE players = '" + xparsed2 + "'")
    conn.commit()

    ####### Assign team to captains
    c.execute("UPDATE temp SET team = 'red' WHERE players = '" + xparsed1 + "'")
    conn.commit()
    c.execute("UPDATE temp SET team = 'blue' WHERE players = '" + xparsed2 + "'")
    conn.commit()

    remaining_indexes = listpicks(modname)[1]

    reactionpool = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    for i in range(0, len(remaining_indexes)):
        await message.add_reaction(reactionpool[remaining_indexes[i]])

    ### remove timeout task for players in filled pug
    # !#!#! Consider moving to completed picking
    # !#!#! May be broken. need to test with real players
    c.execute(
        "SELECT players FROM playerlist WHERE mod='" + str(modname) + "' AND serverid = '" + str(
            server) + "' AND channelid = '" + str(chanid) + "'")
    playerids = c.fetchall()

    playeridlist = [i[0] for i in playerids]

    for x in range(0, len(playeridlist)):
        task, = [task for task in asyncio.all_tasks() if
                 task.get_name() == (str(server) + str(chanid) + str(modname) + str(playeridlist[x]))]
        task.cancel()

# get pick orders
# !#!#!# Figure out how to generate
async def getpickorders(playerlimit, pickorder):
    redorder = []
    blueorder = []

    if playerlimit == 2:
        redorder = []
        blueorder = []
    elif playerlimit == 4:
        redorder = [1]
        blueorder = []
    elif playerlimit == 6:
        redorder = [1]
        blueorder = [2, 3]
    elif playerlimit == 8:
        redorder = [1, 4, 5]
        blueorder = [2, 3]
    elif playerlimit == 10:
        redorder = [1, 4, 5]
        blueorder = [2, 3, 6, 7]
    elif playerlimit == 12:
        redorder = [1, 4, 5, 8, 9]
        blueorder = [2, 3, 6, 7]

    return (redorder, blueorder)


###################################################################################################################

########
############## Slash Commands
########

### ADD A GAMETYPE
###################################################################################################################

@bot.slash_command(description="Add a gametype")
async def addmod(inter, gametype: str, playernum: str, pickorder: str):
    modname = str(gametype)

    c.execute("INSERT INTO modsettings (server, serverid, channel, channelid, mod, playerlimit, pickorder) VALUES ("
              "'" + inter.guild.name +
              "','" + str(inter.guild.id) +
              "','" + inter.channel.name +
              "','" + str(inter.channel.id) +
              "', '" + modname +
              "', '" + playernum +
              "','" + pickorder + "');")

    conn.commit()

    await inter.send(f'{modname} has been added with {playernum} players')


##################################################################################################################

## REMOVE A GAMETYPE
##################################################################################################################

@bot.slash_command(description="Remove a gametype")
async def delmod(inter, gametype: str):
    c.execute(
        "DELETE FROM modsettings WHERE mod = '" + gametype + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "' ;")
    conn.commit()

    c.execute(
        "DELETE FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "' ;")
    conn.commit()

    await inter.send(f'{gametype} has been removed')


###################################################################################################################

### JOIN PUG
###################################################################################################################

@bot.slash_command(description="Join a pug")
async def join(inter, gametype: str):
    author = inter.author.id
    displayname = inter.author.name
    name = str(author)
    playername = str(displayname)
    modname = gametype

    c.execute(
        "SELECT players FROM playerlist WHERE server = '" + inter.guild.name +
        "' AND channel = '" + inter.channel.name +
        "' AND mod = '" + gametype +
        "' AND players = '" + name + "'")

    isplayer = c.fetchall()
    isplayerparsed = str(isplayer)

    if isplayerparsed == '[]':
        isplayerin = 0
    else:
        isplayerin = 1

    if isplayerin != 0:
        await inter.send(f'{displayname} is already in the {modname} pug')
    else:
        c.execute("INSERT INTO playerlist (server, serverid, channel, channelid, mod, players, playername, time) "
                  "VALUES('" + inter.guild.name +
                  "', '" + str(inter.guild.id) +
                  "', '" + inter.channel.name +
                  "', '" + str(inter.channel.id) +
                  "', '" + gametype +
                  "', '" + name +
                  "', '" + playername +
                  "', CURRENT_TIMESTAMP);")
        conn.commit()

        ####### Checks if full

        c.execute(
            "SELECT COUNT(*) FROM playerlist WHERE players is not null AND mod = '" + gametype + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
        playernum = c.fetchall()

        c.execute(
            "SELECT playerlimit FROM modsettings WHERE mod='" + gametype + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
        playerlimit = c.fetchall()

        ####### Begin picks
        if playernum == playerlimit:

            ##### creates countdown task where random captains are chosen if finishes
            chan = bot.get_channel(int(inter.channel.id))
            asyncio.create_task(
                countdown(3, chan, inter.channel.id, inter.guild.id, gametype),
                name=str('countdown' + str(inter.guild.id)) + str(inter.channel.id) + gametype)

            ####### Copy player list to temp table
            c.execute(
                "INSERT INTO temp(server, serverid, channel, channelid, players, playername) SELECT server, serverid, channel, channelid, players, playername "
                "FROM playerlist WHERE mod = '" + gametype + "' AND server = '"
                + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
            conn.commit()

            ####### Fill gametype with mod
            c.execute("UPDATE temp SET gametype = IFNULL(gametype, '" + modname + "')")
            conn.commit()

            ####### Fill team with 0
            c.execute("UPDATE temp SET team = IFNULL(team, '0')")
            conn.commit()

            ####### Set pick orders to 0
            c.execute("UPDATE temp SET pickorder = IFNULL(pickorder, '0')")
            conn.commit()

            ### Wait for countdown
            await asyncio.sleep(5)

            ### List available picks
            await inter.channel.send(f'{listpicks(gametype)[0]} ')

        else:

            parsedresponse = listplayers(gametype, inter.guild.name, inter.channel.name)
            await inter.send(f'{parsedresponse}')

            ### remove players in for > 2 hours
            chan = bot.get_channel(int(inter.channel.id))

            task = asyncio.create_task(
                playertimer(inter.guild.name, chan, inter.channel.name, gametype, playername),
                name=str(inter.guild.id) + str(inter.channel.id) + gametype + str(inter.author.id))
            runninglist.append(task)

            print(runninglist)


### LEAVE PUG
###################################################################################################################


@bot.slash_command(description="Leave a gametype")
async def leave(inter, gametype: str):
    name = inter.author.id
    displayname = inter.author.name
    modname = gametype

    c.execute("SELECT players FROM playerlist WHERE players = '" + str(
        name) + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")

    isplayer = c.fetchall()
    isplayerparsed = str(isplayer)

    ###CHECKS IF PUG WAS FULL. DELETE TEMP IF SO

    c.execute(
        "SELECT COUNT(*) FROM playerlist WHERE mod ='" + gametype + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
    playernum = c.fetchall()

    c.execute(
        "SELECT playerlimit FROM modsettings WHERE mod='" + modname + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
    playerlimit = c.fetchall()

    if playernum == playerlimit:
        c.execute(
            "DELETE FROM temp WHERE gametype='" + modname + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
        conn.commit()
        await inter.channel.send(f'Picking aborted')
    #####

    if isplayerparsed == '[]':
        isplayerin = 0
    else:
        isplayerin = 1

    if isplayerin != 1:
        await inter.send(f'{displayname} is not in the {modname} pug')
    else:
        c.execute(
            "DELETE FROM playerlist WHERE server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name +
            "' AND mod = '" + gametype + "' AND players = ('" + str(name) + "');")
        conn.commit()

        await inter.send(f'{displayname} has left the {modname} pug')

    ### remove timeout task
    task, = [task for task in asyncio.all_tasks() if
             task.get_name() == (str(inter.guild.id) + str(inter.channel.id) + gametype + str(inter.author.id))]
    task.cancel()


###################################################################################################################

### LIST PUGS
###################################################################################################################


@bot.slash_command(description="List pugs")
async def list(inter, gametype: str = None):
    if gametype:

        parsedresponse = listplayers(gametype, inter.guild.name, inter.channel.name)

        await inter.send(f'{parsedresponse} ')

    else:

        c.execute(
            "SELECT DISTINCT mod FROM modsettings WHERE server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")

        modlist = c.fetchall()

        response = ''

        for x in modlist:
            xparsed = str(x).replace('(', '')
            xparsed = xparsed.replace(')', '')
            xparsed = xparsed.replace("'", '')
            xparsed = xparsed.replace(',', '')

            c.execute(
                "SELECT playerlimit FROM modsettings WHERE mod='" + xparsed + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")
            playerlimit = c.fetchall()

            parsedplayerlimit = str(playerlimit)
            parsedplayerlimit = parsedplayerlimit.replace('[', "")
            parsedplayerlimit = parsedplayerlimit.replace(']', "")
            parsedplayerlimit = parsedplayerlimit.replace('', "")
            parsedplayerlimit = parsedplayerlimit.replace(')', "")
            parsedplayerlimit = parsedplayerlimit.replace('(', "")
            parsedplayerlimit = parsedplayerlimit.replace(',', "")

            c.execute(
                "SELECT COUNT(*) FROM playerlist WHERE mod = '" + xparsed + "' AND server = '" + inter.guild.name + "' AND channel = '" + inter.channel.name + "'")

            playernum = c.fetchall()

            parsedplayernum = str(playernum).replace('[', '')
            parsedplayernum = parsedplayernum.replace(']', '')
            parsedplayernum = parsedplayernum.replace(')', '')
            parsedplayernum = parsedplayernum.replace('(', '')
            parsedplayernum = parsedplayernum.replace(',', '')

            together = '**' + xparsed + ': **' + "[" + parsedplayernum + '/' + parsedplayerlimit + "] "

            response = "\n" + response + together

        await inter.send(f'{response} ')


###################################################################################################################

### PICKING AS FUNCTION
###################################################################################################################

async def pickplayer(pickedplayer, name, server, serverid, channel, channelid):

    global currentcaptain

    print('NAME: ' + (str(name)))

    # Gets current captains
    c.execute("SELECT players FROM temp WHERE captain = 1")
    currentRcaptain = c.fetchall()
    currentRcaptain = [i[0] for i in currentRcaptain]
    print('CURRENT R CAPTAIN: ' + (str(currentRcaptain[0])))

    c.execute("SELECT players FROM temp WHERE captain = 2")
    currentBcaptain = c.fetchall()
    currentBcaptain = [i[0] for i in currentBcaptain]
    print('CURRENT B CAPTAIN: ' + (str(currentBcaptain[0])))

    # Gets current highest pick order
    c.execute("SELECT MAX(pickorder) from temp")
    highpick1 = c.fetchall()
    highpick1 = [i[0] for i in highpick1]

    # Gets mod name, needed to determine player limit
    c.execute("SELECT gametype FROM temp WHERE players = " + str(name) +
              " AND serverid = '" + str(serverid) + "' AND channelid = '" + str(channelid) + "'")

    gametype = c.fetchall()

    modname = gametype

    parsedmodname = str(modname[0]).replace('(', '')
    parsedmodname = parsedmodname.replace(')', '')
    parsedmodname = parsedmodname.replace(",", '')
    parsedmodname = parsedmodname.replace("'", '')
    parsedmodname = parsedmodname.replace(']', '')
    parsedmodname = parsedmodname.replace('[', '')

    # Gets player limit (needed to determine appropriate captain)
    c.execute("SELECT playerlimit FROM modsettings WHERE channelid = '" + str(
        channelid) + "' AND serverid = '" + str(serverid) + "' AND mod= '" + parsedmodname + "'")
    playerlimit = c.fetchall()
    playerlimit = [i[0] for i in playerlimit]
    print(playerlimit[0])

    # Get pick order for gametype and channel etc
    c.execute(
        "SELECT pickorder FROM modsettings WHERE channelid = '" + str(channelid) + "' AND serverid = '" + str(
            serverid) + "' AND mod= '" + parsedmodname + "'")
    pickorder = c.fetchone()
    redorder, blueorder = await getpickorders(playerlimit[0], pickorder)
    print(redorder)
    print(blueorder)

    # Gets whos allowed pick
    if (highpick1[0] + 1) in redorder:
        c.execute("SELECT players FROM temp WHERE captain = 1 AND team = 'red'")
        allowedcaptain = c.fetchall()
        allowedcaptain = [i[0] for i in allowedcaptain]
        print('ALLOWED to pick:')
        print(allowedcaptain)

    elif (highpick1[0] + 1) in blueorder:
        c.execute("SELECT players FROM temp WHERE captain = 2 AND team = 'blue'")
        allowedcaptain = c.fetchall()
        allowedcaptain = [i[0] for i in allowedcaptain]
        print('ALLOWED to pick:')
        print(allowedcaptain)
    else:
        c.execute("SELECT players FROM temp WHERE captain = 2 AND team = 'red'")
        allowedcaptain = c.fetchall()
        allowedcaptain = [i[0] for i in allowedcaptain]

    # check if picking person is captain

    print(name)
    print(allowedcaptain[0])

    if str(name) != str(allowedcaptain[0]):
        print("NOT ALLOWED CAPTAIN")
        return()


    # !#!#!#! check for captain and pick order

    # !#!#!#!

    # CHECK FOR IF ALREADY PICKED
    c.execute("SELECT pickorder FROM temp WHERE ROWID = " + pickedplayer + "")
    hasteam = c.fetchone()
    hasteamint = hasteam[0]

    if hasteamint:
        await channel.send('player already picked')
    else:
        c.execute("SELECT players FROM temp WHERE ROWID = " + pickedplayer + "")
        pickedplayer = c.fetchall()

        parsedpickedplayer = str(pickedplayer[0]).replace('(', '')
        parsedpickedplayer = parsedpickedplayer.replace(')', '')
        parsedpickedplayer = parsedpickedplayer.replace(",", '')
        parsedpickedplayer = parsedpickedplayer.replace("'", '')
        parsedpickedplayer = parsedpickedplayer.replace(']', '')
        parsedpickedplayer = parsedpickedplayer.replace('[', '')

        # !#!#!#! Add WHERE GAMETYPE WHERE SERVER WHERE CHANNEL ====
        c.execute("SELECT MAX(pickorder) from temp")
        highpick = c.fetchall()



        parsedhighpick = str(highpick[0]).replace('(', '')
        parsedhighpick = parsedhighpick.replace(')', '')
        parsedhighpick = parsedhighpick.replace(",", '')
        parsedhighpick = parsedhighpick.replace(']', '')
        parsedhighpick = parsedhighpick.replace('[', '')

        highpick = int(parsedhighpick) + 1

        c.execute("UPDATE temp SET pickorder = '" + str(highpick) + "' WHERE players = '" + parsedpickedplayer + "'")
        conn.commit()

        ##### Retrive pick orders #!#!#! Still need to generate somehow

        c.execute("SELECT playerlimit FROM modsettings WHERE channelid = '" + str(
            channelid) + "' AND serverid = '" + str(serverid) + "' AND mod= '" + parsedmodname + "'")
        playerlimit = c.fetchone()

        c.execute(
            "SELECT pickorder FROM modsettings WHERE channelid = '" + str(channelid) + "' AND serverid = '" + str(
                serverid) + "' AND mod= '" + parsedmodname + "'")
        pickorder = c.fetchone()

        redorder, blueorder = await getpickorders(playerlimit[0], pickorder)

        if highpick in redorder:
            c.execute("UPDATE temp SET team = 'red' WHERE players = '" + parsedpickedplayer + "'")
            conn.commit()

        elif highpick in blueorder:
            c.execute("UPDATE temp SET team = 'blue' WHERE players = '" + parsedpickedplayer + "'")
            conn.commit()

        if highpick == (playerlimit[0] - 3):
            print("assigning last player")

            c.execute("SELECT COUNT(*) FROM temp WHERE team = 'red' ")
            redtotal = c.fetchone()
            c.execute("SELECT COUNT(*) FROM temp WHERE team = 'blue' ")
            bluetotal = c.fetchone()

            if redtotal[0] < bluetotal[0]:
                lessteam = 'red'
            else:
                lessteam = 'blue'

            c.execute("UPDATE temp SET team = '" + lessteam + "' WHERE team = '0'")
            conn.commit()
            c.execute("UPDATE temp SET pickorder = '" + str(highpick + 1) + "' WHERE pickorder is '0'")
            conn.commit()

            redpicks = listteampicks(parsedmodname, 'red')
            bluepicks = listteampicks(parsedmodname, 'blue')
            await channel.send(f' Teams have been chosen \n **Red Team: ** {redpicks} \n **Blue Team: ** {bluepicks} ')

            # Send to history

            c.execute(
                "INSERT INTO history (server, channel, gametype, team, players, playername, pickorder) "
                "SELECT server, channel, gametype, team, players, playername, pickorder FROM temp "
                "WHERE gametype = '" + parsedmodname + "'"
            )
            conn.commit()

            # Fill in timestamp in history

            c.execute("UPDATE history SET time = CURRENT_TIMESTAMP WHERE time is NULL")
            conn.commit()

            # Delete from global playerlist table

            c.execute(
                "DELETE from playerlist WHERE EXISTS (SELECT * FROM temp WHERE temp.players = playerlist.players)")
            conn.commit()

            # Delete from temp picking table

            c.execute("DELETE from temp WHERE gametype = '" + str(parsedmodname) +
                      "' AND serverid = '" + str(serverid) +
                      "' AND channelid = '" + str(channelid) + "'")
            conn.commit()

            return

        # List remaining players
        remaining = listpicks(parsedmodname)[0]
        print("remaining: " + remaining)

        redpicks = listteampicks(parsedmodname, 'red')
        bluepicks = listteampicks(parsedmodname, 'blue')

        if (highpick-1) in redorder:
            c.execute("SELECT playername FROM temp WHERE captain = 2 AND team = 'blue'")

            currentcaptain = c.fetchone()
            print(currentcaptain)

        elif (highpick-1) in blueorder:
            c.execute("SELECT playername FROM temp WHERE captain = 1 AND team = 'red'")

            currentcaptain = c.fetchone()
            print(currentcaptain)
        else:
            c.execute("SELECT playername FROM temp WHERE captain = 2 AND team = 'blue'")

            currentcaptain = c.fetchone()

        message = await channel.send(f'{remaining} \n **Red Team: ** {redpicks} \n **Blue Team: ** {bluepicks} \n @' + currentcaptain[
            0] + ' TO PICK ')

        remaining_indexes = listpicks(parsedmodname)[1]

        reactionpool = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣','🔟']

        for i in range(0,len(remaining_indexes)):
            await message.add_reaction(reactionpool[remaining_indexes[i]])

    return()

###################################################################################################################

### PICKING
###################################################################################################################

# !#!#!#!#! CHECK FOR CAPTAIN STATUS SOMEHOW!

@bot.slash_command(description="Pick a player")
async def pick(inter, pickedplayer: str):

    name = inter.author.id

    channelid = inter.channel.id
    channel = bot.get_channel(channelid)

    await pickplayer(pickedplayer, name, inter.guild.name, inter.guild.id, channel, channelid)

##################################################################################################################

@bot.event
async def on_reaction_add(reaction, user):

    channelid = reaction.message.channel.id
    channel = bot.get_channel(channelid)

    if user != bot.user:
        if str(reaction.emoji) == '1️⃣':
            await pickplayer('1', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '2️⃣':
            await pickplayer('2', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '3️⃣':
            await pickplayer('3', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '4️⃣':
            await pickplayer('4', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '5️⃣':
            await pickplayer('5', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '6️⃣':
            await pickplayer('6', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '7️⃣':
            await pickplayer('7', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '8️⃣':
            await pickplayer('8', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '9️⃣':
            await pickplayer('9', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        elif str(reaction.emoji) == '🔟':
            await pickplayer('10', user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)
        # elif str(reaction.emoji) == '❌':
        #     await reset_function(user.id, reaction.message.guild.name, reaction.message.guild.id, channel, channelid)


# async def reset_function(name, server, serverid, channel, channelid):
#
#     chan = bot.get_channel(int(channelid))
#     c.execute("SELECT gametype FROM temp WHERE players = " + str(name) +
#               " AND serverid = '" + str(serverid) + "' AND channelid = '" + str(channelid) + "'")
#
#     gametype = c.fetchall()
#     #!#!#! Need to specifcy channel name and mod
#
#     # remove captain status and teams
#     c.execute("UPDATE temp SET team = 0 WHERE team is NOT 0")
#     conn.commit()
#
#     # remove previously assigned teams
#     c.execute("UPDATE temp SET captain = NULL")
#     conn.commit()
#
#     # start new countdown
#     asyncio.create_task(
#         countdown(3, chan, channelid, serverid, gametype),
#         name=str('countdown' + str(serverid)) + str(channelid) + str(gametype)[0])
#
#     ### Wait for countdown
#     await asyncio.sleep(5)
#     await channel.send(f'{listpicks(gametype)[0]} ')

@bot.slash_command(description="Reset a pug")
async def reset(inter, gametype: str):

    chan = bot.get_channel(int(inter.channel.id))

    #!#!#! Need to specifcy channel name and mod

    # remove captain status and teams
    c.execute("UPDATE temp SET team = 0 WHERE team is NOT 0")
    conn.commit()

    # remove previously assigned teams
    c.execute("UPDATE temp SET captain = NULL")
    conn.commit()

    # start new countdown
    asyncio.create_task(
        countdown(3, chan, inter.channel.id, inter.guild.id, gametype),
        name=str('countdown' + str(inter.guild.id)) + str(inter.channel.id) + gametype)

    ### Wait for countdown
    await asyncio.sleep(5)
    await inter.channel.send(f'{listpicks(gametype)[0]} ')

bot.run(str(discordtoken))
