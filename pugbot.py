import discord  # Import the original discord.py module
from discord.ext import commands  # Import the discord.py extension "commands"
import discord_slash  # Import the third-party extension discord_slash module
import sqlite3
import asyncio
import random

bot = commands.Bot(command_prefix='!')
slash = discord_slash.SlashCommand(bot, sync_commands=True)  # sync_commands is for doing synchronization for
# every command you add, remove or update in your
# code

conn = sqlite3.connect("pugbotdb.db")
c = conn.cursor()

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

    # print(modnameparsed)

    c.execute(
        "SELECT playername FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + server + "' AND channel = '" + channel + "'")

    response = c.fetchall()

    b = [i[0] for i in response]
    i = 0

    playerlist = ''

    while i < len(b):
        c.execute(
            "SELECT (julianday('now') - julianday(time)) * 24 * 60 * 60 FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + server + "' AND channel = '" + channel + "' AND playername = '"+b[i]+"'")
        timetest = c.fetchall()
        t = [i[0] for i in timetest]
        timediff = str(time_elapsed(t[0]))
        timediff = timediff.replace("'", '')


        playertime = (b[i] + ' ' + timediff + ':small_orange_diamond:')

        playerlist = playertime + playerlist

        i = i + 1
    size = len(playerlist)
    playerlist = playerlist[:size -22]

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

    # print(playerlimit)

    parsedplayerlimit = str(playerlimit)
    parsedplayerlimit = parsedplayerlimit.replace('[', "")
    parsedplayerlimit = parsedplayerlimit.replace('', "")
    parsedplayerlimit = parsedplayerlimit.replace('(', "/")
    parsedplayerlimit = parsedplayerlimit.replace(')', "")
    parsedplayerlimit = parsedplayerlimit.replace(',', "")

    # print(parsedplayerlimit)

    parsedresponse = '**__' + modnameparsed + ': [' + parsedplayernum + parsedplayerlimit + '__**' + ' \n ' + \
                     playerlist

    ###await ctx.channel.send(f'{parsedresponse} ')

    return (parsedresponse)


########

######## Lists players to pick
def listpicks(gametype):
    modnameparsed = 'temp'

    # print(modnameparsed)

    c.execute("SELECT rowid, playername FROM " + modnameparsed + " WHERE pickorder is NULL")

    response = c.fetchall()
    response1 = str(response[0])
    # print('test: ' + response1)

    # print(response)

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

    # print(parsedresponse)

    parsedresponse = '**__' + gametype + ':__**' + ' \n ' + \
                     parsedresponse

    ###await ctx.channel.send(f'{parsedresponse} ')

    return (parsedresponse)


######## Lists players on team
def listteampicks(gametype, team):
    modnameparsed = 'temp'

    # print(modnameparsed)

    c.execute("SELECT playername FROM " + modnameparsed + " WHERE team = '" + team + "' ORDER BY pickorder")

    response = c.fetchall()
    response1 = str(response[0])
    # print('test: ' + response1)

    # print(response)

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

    # print(parsedresponse)

    ###await ctx.channel.send(f'{parsedresponse} ')

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
    # print(z)

    random_id1 = random.randint(0, numplayers)
    random_id2 = random.choice([ele for ele in temp_list if ele != random_id1])

    modnameparsed = str(gametype)

    modnameparsed = modnameparsed.replace('(', '')
    modnameparsed = modnameparsed.replace(')', '')
    modnameparsed = modnameparsed.replace(',', '')

    c.execute(
        "SELECT players FROM playerlist WHERE mod = '" + modnameparsed + "' AND serverid = '" + str(server) + "' AND channelid = '" + str(channel) + "' ;")

    players = c.fetchall()
    print(players)
    print(random_id1)
    print(random_id2)
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

    await asyncio.sleep(10)

    c.execute(
        "DELETE FROM playerlist WHERE server = '" + server + "' AND channel = '" + channelname +
        "' AND mod = '" + gametype + "' AND playername = ('" + str(name) + "');")
    conn.commit()

    print("TIMED OUT")
    await chan.send(name + ' has timed out of ' + gametype)

#### Begins countdown timer for random captains

async def countdown(time, chan, chanid, server, modname):

    print(time)
    print(chan)
    print(server)
    print(modname)

    for x in range(1, time):
        if x == 1:
            message = await chan.send(f'{modname} has been filled \n Choosing Random Captains in ' + str(time))
            await asyncio.sleep(1)
            time = time - 1

        await message.edit(content=f'{modname} has been filled \n Choosing Random Captains in ' + str(time))
        await asyncio.sleep(1)
        time = time - 1

    c.execute(
        "SELECT playerlimit FROM modsettings WHERE mod='" + modname + "' AND serverid = '" + str(server) + "' AND channelid = '" + str(chanid) + "'")
    playerlimit = c.fetchall()

    captains = randcapt(modname, playerlimit[0], server, chanid)
    print(captains)
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

    ####### Assign captains 0 pick order
    c.execute("UPDATE temp SET pickorder = 0 WHERE playername = '" + xparsed1 + "'")
    conn.commit()
    c.execute("UPDATE temp SET pickorder = 0 WHERE playername = '" + xparsed2 + "'")
    conn.commit()

    ####### Assign team to captains
    c.execute("UPDATE temp SET team = 'red' WHERE playername = '" + xparsed1 + "'")
    conn.commit()
    c.execute("UPDATE temp SET team = 'blue' WHERE playername = '" + xparsed2 + "'")
    conn.commit()

#get pick orders
#!#!#!# This sucks. Figure out how to generate
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

@slash.slash(name="addmod", description="Add a gametype",  # Adding a new slash command with our slash variable
             options=[
                 discord_slash.manage_commands.create_option(
                     name="gametype",
                     description="enter gametype name",
                     option_type=3,
                     required=True),
                 discord_slash.manage_commands.create_option(
                     name="playernum",
                     description="enter number of players",
                     option_type=3,
                     required=True),
                 discord_slash.manage_commands.create_option(
                     name="pickorder",
                     description="enter pick order (1,2,3)",
                     option_type=3,
                     required=True),
             ])
async def addmod(ctx: discord_slash.SlashContext, gametype, playernum, pickorder):
    modname = str(gametype)

    c.execute("INSERT INTO modsettings (server, serverid, channel, channelid, mod, playerlimit, pickorder) VALUES ("
              "'" + ctx.guild.name +
              "','" + str(ctx.guild.id) +
              "','" + ctx.channel.name +
              "','" + str(ctx.channel.id) +
              "', '" + modname +
              "', '" + playernum +
              "','" + pickorder + "');")

    conn.commit()

    await ctx.send(f'{modname} has been added with {playernum} players')


###################################################################################################################

### REMOVE A GAMETYPE
###################################################################################################################

@slash.slash(name="delmod", description="Remove a gametype",
             options=[
                 discord_slash.manage_commands.create_option(
                     name="gametype",
                     description="enter gametype name",
                     option_type=3,
                     required=True)])
async def delmod(ctx: discord_slash.SlashContext, gametype):
    c.execute(
        "DELETE FROM modsettings WHERE mod = '" + gametype + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "' ;")
    conn.commit()

    c.execute(
        "DELETE FROM playerlist WHERE mod = '" + gametype + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "' ;")
    conn.commit()

    await ctx.send(f'{gametype} has been removed')



###################################################################################################################

### JOIN PUG
###################################################################################################################

@slash.slash(name="j", description="Join a pug",  # Adding a new slash command with our slash variable
             options=[discord_slash.manage_commands.create_option(
                 name="gametype",
                 description="enter the pug to join",
                 option_type=3,
                 required=True)])
async def join(ctx: discord_slash.SlashContext, gametype):
    author = ctx.author.id
    displayname = ctx.author.name
    name = str(author)
    playername = str(displayname)
    modname = gametype

    c.execute(
        "SELECT players FROM playerlist WHERE server = '" + ctx.guild.name +
        "' AND channel = '" + ctx.channel.name +
        "' AND mod = '" + gametype +
        "' AND players = '" + name + "'")

    isplayer = c.fetchall()
    isplayerparsed = str(isplayer)

    if isplayerparsed == '[]':
        isplayerin = 0
    else:
        isplayerin = 1

    if isplayerin != 0:
        await ctx.send(f'{displayname} is already in the {modname} pug')
    else:
        c.execute("INSERT INTO playerlist (server, serverid, channel, channelid, mod, players, playername, time) "
                  "VALUES('" + ctx.guild.name +
                  "', '" + str(ctx.guild.id) +
                  "', '" + ctx.channel.name +
                  "', '" + str(ctx.channel.id) +
                  "', '" + gametype +
                  "', '" + name +
                  "', '" + playername +
                  "', CURRENT_TIMESTAMP);")
        conn.commit()

        ####### Checks if full

        c.execute(
            "SELECT COUNT(*) FROM playerlist WHERE players is not null AND mod = '" + gametype + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
        playernum = c.fetchall()

        c.execute(
            "SELECT playerlimit FROM modsettings WHERE mod='" + gametype + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
        playerlimit = c.fetchall()

        ####### Begin picks
        if playernum == playerlimit:

            ##### creates countdown task where random captains are chosen if finishes
            chan = bot.get_channel(int(ctx.channel.id))
            asyncio.create_task(
                countdown(3, chan, ctx.channel.id, ctx.guild.id, gametype),
                name=str('countdown'+str(ctx.guild.id)) + str(ctx.channel.id) + gametype)

            ####### Copy player list to temp table
            c.execute(
                "INSERT INTO temp(server, channel, players, playername) SELECT server, channel, players, playername "
                "FROM playerlist WHERE mod = '" + gametype + "' AND server = '"
                + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
            conn.commit()

            ####### Fill gametype with mod
            c.execute("UPDATE temp SET gametype = IFNULL(gametype, '" + modname + "')")
            conn.commit()

            ### Wait for countdown
            await asyncio.sleep(5)

            ### List available picks
            await ctx.channel.send(f'{listpicks(gametype)} ')

        else:

            parsedresponse = listplayers(gametype, ctx.guild.name, ctx.channel.name)
            await ctx.send(f'{parsedresponse} ')

            ### remove players in for > 2 hours
            chan = bot.get_channel(int(ctx.channel.id))

            task = asyncio.create_task(
                playertimer(ctx.guild.name, chan, ctx.channel.name, gametype, playername), name=str(ctx.guild.id)+str(ctx.channel.id)+gametype+str(ctx.author.id))
            runninglist.append(task)

            print(runninglist)

### LEAVE PUG
###################################################################################################################


@slash.slash(name="l", description="Leave a pug",
             options=[discord_slash.manage_commands.create_option(
                 name="gametype",
                 description="leaves a pug",
                 option_type=3,
                 required=True)])
async def leave(ctx: discord_slash.SlashContext, gametype):
    name = ctx.author.id
    displayname = ctx.author.name
    modname = gametype

    c.execute("SELECT players FROM playerlist WHERE players = '" + str(
        name) + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")

    isplayer = c.fetchall()
    isplayerparsed = str(isplayer)

    ###CHECKS IF PUG WAS FULL. DELETE TEMP IF SO

    c.execute(
        "SELECT COUNT(*) FROM playerlist WHERE mod ='" + gametype + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
    playernum = c.fetchall()

    c.execute(
        "SELECT playerlimit FROM modsettings WHERE mod='" + modname + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
    playerlimit = c.fetchall()

    if playernum == playerlimit:
        c.execute(
            "DELETE FROM temp WHERE gametype='" + modname + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
        conn.commit()
        await ctx.channel.send(f'Picking aborted')
    #####

    if isplayerparsed == '[]':
        isplayerin = 0
    else:
        isplayerin = 1

    if isplayerin != 1:
        await ctx.send(f'{displayname} is not in the {modname} pug')
    else:
        c.execute("DELETE FROM playerlist WHERE server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name +
                  "' AND mod = '" + gametype + "' AND players = ('" + str(name) + "');")
        conn.commit()

        await ctx.send(f'{displayname} has left the {modname} pug')


    ### remove timeout task
    task, = [task for task in asyncio.all_tasks() if task.get_name() == (str(ctx.guild.id)+str(ctx.channel.id)+gametype+str(ctx.author.id))]
    task.cancel()

###################################################################################################################

### LIST PUGS
###################################################################################################################


@slash.slash(name="list", description="List a pug",
             options=[discord_slash.manage_commands.create_option(
                 name="gametype",
                 description="enter the pug to list",
                 option_type=3,
                 required=False)])
async def list(ctx: discord_slash.SlashContext, gametype=None):
    if gametype:

        parsedresponse = listplayers(gametype, ctx.guild.name, ctx.channel.name)

        await ctx.send(f'{parsedresponse} ')

    else:

        c.execute(
            "SELECT DISTINCT mod FROM modsettings WHERE server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")

        modlist = c.fetchall()
        print(modlist)

        response = ''

        for x in modlist:
            xparsed = str(x).replace('(', '')
            xparsed = xparsed.replace(')', '')
            xparsed = xparsed.replace("'", '')
            xparsed = xparsed.replace(',', '')

            c.execute(
                "SELECT playerlimit FROM modsettings WHERE mod='" + xparsed + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
            playerlimit = c.fetchall()

            parsedplayerlimit = str(playerlimit)
            parsedplayerlimit = parsedplayerlimit.replace('[', "")
            parsedplayerlimit = parsedplayerlimit.replace(']', "")
            parsedplayerlimit = parsedplayerlimit.replace('', "")
            parsedplayerlimit = parsedplayerlimit.replace(')', "")
            parsedplayerlimit = parsedplayerlimit.replace('(', "")
            parsedplayerlimit = parsedplayerlimit.replace(',', "")

            c.execute(
                "SELECT COUNT(*) FROM playerlist WHERE mod = '" + xparsed + "' AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")

            playernum = c.fetchall()

            parsedplayernum = str(playernum).replace('[', '')
            parsedplayernum = parsedplayernum.replace(']', '')
            parsedplayernum = parsedplayernum.replace(')', '')
            parsedplayernum = parsedplayernum.replace('(', '')
            parsedplayernum = parsedplayernum.replace(',', '')

            together = '**' + xparsed + ': **' + "[" + parsedplayernum + '/' + parsedplayerlimit + "] "

            response = "\n" + response + together

        await ctx.send(f'{response} ')


###################################################################################################################

### PICKING
###################################################################################################################

# !#!#!#!#! CHECK FOR CAPTAIN STATUS SOMEHOW!

@slash.slash(name="p", description="pick a player",
             options=[discord_slash.manage_commands.create_option(
                 name="pickedplayer",
                 description="enter player to pick",
                 option_type=3,
                 required=True)])
async def pick(ctx: discord_slash.SlashContext, pickedplayer):
    name = ctx.author.id
    displayname = ctx.author.name

    c.execute("SELECT gametype FROM temp WHERE players = " + str(name) +
              " AND server = '" + ctx.guild.name + "' AND channel = '" + ctx.channel.name + "'")
    gametype = c.fetchall()
    modname = gametype

    parsedmodname = str(modname[0]).replace('(', '')
    parsedmodname = parsedmodname.replace(')', '')
    parsedmodname = parsedmodname.replace(",", '')
    parsedmodname = parsedmodname.replace("'", '')
    parsedmodname = parsedmodname.replace(']', '')
    parsedmodname = parsedmodname.replace('[', '')

    # !#!#!#! check for captain and pick order

    # !#!#!#!

    # CHECK FOR IF ALREADY PICKED
    c.execute("SELECT pickorder FROM temp WHERE ROWID = " + pickedplayer + "")
    hasteam = c.fetchone()
    hasteamint = hasteam[0]

    if hasteamint:
        await ctx.send('player already picked')
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
        print(highpick)
        # print(highpick)

        parsedhighpick = str(highpick[0]).replace('(', '')
        parsedhighpick = parsedhighpick.replace(')', '')
        parsedhighpick = parsedhighpick.replace(",", '')
        parsedhighpick = parsedhighpick.replace(']', '')
        parsedhighpick = parsedhighpick.replace('[', '')

        # print(parsedhighpick)

        highpick = int(parsedhighpick) + 1

        # print(highpick)

        c.execute("UPDATE temp SET pickorder = '" + str(highpick) + "' WHERE players = '" + parsedpickedplayer + "'")
        conn.commit()

        ##### Retrive pick orders #!#!#! Still need to generate somehow

        c.execute("SELECT playerlimit FROM modsettings WHERE channelid = '" + str(ctx.channel.id) + "' AND serverid = '" + str(ctx.guild.id) + "' AND mod= '"+parsedmodname+"'")
        playerlimit = c.fetchone()
        c.execute("SELECT pickorder FROM modsettings WHERE channelid = '" + str(ctx.channel.id) + "' AND serverid = '" + str(ctx.guild.id) + "' AND mod= '"+parsedmodname+"'")
        pickorder = c.fetchone()

        redorder, blueorder = await getpickorders(playerlimit[0], pickorder)
        print(redorder)
        print(blueorder)

        if highpick in redorder:
            c.execute("UPDATE temp SET team = 'red' WHERE players = '" + parsedpickedplayer + "'")
            conn.commit()
        elif highpick in blueorder:
            c.execute("UPDATE temp SET team = 'blue' WHERE players = '" + parsedpickedplayer + "'")
            conn.commit()

        if highpick == (playerlimit[0]-3):
            print("assigning last player")

            c.execute("SELECT COUNT(*) FROM temp WHERE team = 'red' ")
            redtotal = c.fetchone()
            c.execute("SELECT COUNT(*) FROM temp WHERE team = 'blue' ")
            bluetotal = c.fetchone()

            if redtotal[0] < bluetotal[0]:
                lessteam = 'red'
            else:
                lessteam = 'blue'

            c.execute("UPDATE temp SET team = '" + lessteam + "' WHERE team is NULL")
            conn.commit()
            c.execute("UPDATE temp SET pickorder = '" + str(highpick + 1) + "' WHERE pickorder is NULL")
            conn.commit()

            redpicks = listteampicks(parsedmodname, 'red')
            bluepicks = listteampicks(parsedmodname, 'blue')
            await ctx.send(f' Teams have been chosen \n **Red Team: ** {redpicks} \n **Blue Team: ** {bluepicks} ')

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

            c.execute("DELETE from temp WHERE gametype = '" + parsedmodname +
                      "' AND server = '" + ctx.guild.name +
                      "' AND channel = '" + ctx.channel.name + "'")
            conn.commit()

            return

        # List remaining players
        remaining = listpicks(parsedmodname)

        redpicks = listteampicks(parsedmodname, 'red')
        bluepicks = listteampicks(parsedmodname, 'blue')

        # print(redpicks)

        await ctx.send(f'{remaining} \n **Red Team: ** {redpicks} \n **Blue Team: ** {bluepicks} \n @____ TO PICK ')

        ### remove timeout task for players in filled pug
        # !#!#! Consider moving to completed picking
        # !#!#! May be broken. need to test with real players
        c.execute(
            "SELECT players FROM playerlist WHERE mod='" + gametype + "' AND serverid = '" + str(
                ctx.guild.id) + "' AND channelid = '" + str(ctx.channel.id) + "'")
        playerids = c.fetchall()
        print(playerids)

        playeridlist = [i[0] for i in playerids]
        print(playeridlist)

        for x in range(0, len(playeridlist)):
            print(playeridlist[x])
            task, = [task for task in asyncio.all_tasks() if
                     task.get_name() == (str(ctx.guild.id) + str(ctx.channel.id) + gametype + str(playeridlist[x]))]
            task.cancel()


###################################################################################################################

bot.run('OTE4OTg4MzQyNzg2NDA0NDIz.YbPQlg.yqYFx-Pm12sic3HpzJFCIRBdIBg')
