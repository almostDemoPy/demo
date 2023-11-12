import asyncio
import chess
import discord
import json
import random
import requests
import traceback
from discord import app_commands, ui
from discord.ext import commands
from stockfish import Stockfish

class TextSelectSide(ui.View):
  def __init__(self, user, member, bot):
    super().__init__(
      timeout = None
    )
    self.user = user
    self.member = member
    self.bot = bot
    self.board = None
    self.boardMsg = None
    self.boardThread = None

  async def startGame(self, interaction : discord.Interaction, side : str):
    try:
      with open('json/chessEmojis.json', 'r') as f:
        emojis = json.load(f)
      with open('json/games.json', 'r') as f:
        games = json.load(f)
      players = {
        str(self.user.id): None,
        str(self.member.id): None
      }
      if interaction.user == self.user:
        if side == "white":
          players[str(self.user.id)] = "white"
          players[str(self.member.id)] = "black"
        else:
          players[str(self.member.id)] = "white"
          players[str(self.user.id)] = "black"
      else:
        if side == "white":
          players[str(self.member.id)] = "white"
          players[str(self.user.id)] = "black"
        else:
          players[str(self.user.id)] = "white"
          players[str(self.member.id)] = "black"
      while True:
        if self.board.is_checkmate() or self.board.is_stalemate():
          embed = self.boardMsg.embeds[0].copy()
          if self.board.outcome() is None:
            winner = "It's a draw !"
          elif self.board.outcome() == chess.WHITE:
            winner = "White wins !"
          elif self.board.outcome() == chess.BLACK:
            winner = "Black wins !"
          embed.description = winner
          await self.boardMsg.edit(
            embed = embed
          )
          del games["chess"][str(self.user.id)]
          del games["chess"][str(self.member.id)]
          with open('json/games.json', 'w') as f:
            json.dump(games, f, indent = 2)
          break
        currentTurn = "white" if self.board.turn == chess.WHITE else "black"
        if self.member == self.bot.user and players[str(self.member.id)] == currentTurn:
          boardFen = self.board.board_fen()
          cT = "w" if currentTurn == "white" else "b"
          castlingRights = " "
          if self.board.has_castling_rights(chess.WHITE):
            if self.board.has_kingside_castling_rights(chess.WHITE):
              castlingRights += "K"
            if self.board.has_queenside_castling_rights(chess.WHITE):
              castlingRights += "Q"
          if self.board.has_castling_rights(chess.BLACK):
            if self.board.has_kingside_castling_rights(chess.BLACK):
              castlingRights += "k"
            if self.board.has_queenside_castling_rights(chess.BLACK):
              castlingRights += "q"
          halfmove = self.board.halfmove_clock
          epSquare = chess.square_name(self.board.ep_square) if self.board.ep_square is not None else "-"
          fullmove = self.board.fullmove_number
          fullfen = f"{boardFen} {cT}{castlingRights} {epSquare} {halfmove} {fullmove}"
          result = requests.get(
            url = f"https://stockfish.online/api/stockfish.php",
            params = {
              "fen": fullfen,
              "depth": 13,
              "mode": "bestmove"
            }
          )
          data = result.json()
          msgMove = data["data"].split(" ")[1]
          botMove = True
        else:
          def messageCheck(message):
            if message.author.id in [self.user.id, self.member.id]:
              if message.content.lower() in ["demo.chess.end", "demo.chess.resign"]:
                return True
            return message.author.id in [self.user.id, self.member.id] and players[str(message.author.id)] == currentTurn and message.channel == self.boardThread
          msg = await self.bot.wait_for("message", check = messageCheck)
          if msg.content.lower() in ["demo.chess.end", "demo.chess.resign"]:
            await msg.delete()
            return
          msgMove = msg.content
          botMove = False
          await msg.delete()
        try:
          move = chess.Move.from_uci(msgMove)
          if move not in self.board.legal_moves:
            continue
          self.board.push(move)
          strBoard = ""
          numberIndicatorList = [":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]
          for ind, numberIndicator in enumerate(numberIndicatorList):
            strBoard += numberIndicator + str(self.board).split("\n")[ind]
            strBoard += "\n"
          strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
          strBoard = strBoard.replace(
            " ",
            ""
          )
          strBoard2 = ""
          for ind, number in enumerate(numberIndicatorList):
            strBoard2 += number
            line = strBoard.split("\n")[ind][len(number):]
            for ind2, char in enumerate(line):
              if char == ".":
                if ind % 2 == 0:
                  color = ":white_large_square:" if ind2 % 2 != 0 else ":green_square:"
                else:
                  color = ":white_large_square:" if ind2 % 2 == 0 else ":green_square:"
                strBoard2 += color
                continue
              if ind % 2 == 0:
                if ind2 % 2 == 0:
                  color = "green"
                else:
                  color = "white"
                strBoard2 += str(self.bot.get_emoji(emojis[color][char]))
                continue
              else:
                if ind2 % 2 == 0:
                  color = "white"
                else:
                  color = "green"
                strBoard2 += str(self.bot.get_emoji(emojis[color][char]))
                continue
            strBoard2 += "\n"
          strBoard2 += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
          currentTurn = "White" if self.board.turn == chess.WHITE else "Black"
          embed = discord.Embed(
            title = f"**{currentTurn}**'s turn !",
            description = strBoard2,
            color = 0x2b2d31
          )
          if players[str(self.member.id)] == "white":
            if self.member != self.bot.user:
              embed.set_author(
                name = self.user.display_name + (f" | {msgMove}" if msg.author == self.user else "") + (" | Check" if msg.author == self.member and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.member and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.member and self.board.is_stalemate() else ""),
                icon_url = self.user.display_avatar
              ).set_footer(
                text = self.member.display_name + (f" | {msgMove}" if msg.author == self.member else "") + (" | Check" if msg.author == self.user and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.user and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.user and self.board.is_stalemate() else ""),
                icon_url = self.member.display_avatar
              )
            else:
              if not botMove:
                embed.set_author(
                  name = self.user.display_name + (" | Check" if msg.author == self.member and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.member and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.member and self.board.is_stalemate() else ""),
                  icon_url = self.user.display_avatar
                )
              else:
                embed.set_author(
                  name = self.user.display_name + (" | Check" if self.board.is_check() else "") + (" | Checkmate" if self.board.is_checkmate() else "") + (" | Stalemate" if self.board.is_stalemate() else ""),
                  icon_url = self.user.display_avatar
                )
              embed.set_footer(
                text = self.member.display_name + (f" | {msgMove}" if botMove else "") + (" | Check" if self.board.is_check() else "") + (" | Checkmate" if self.board.is_checkmate() else "") + (" | Stalemate" if self.board.is_stalemate() else ""),
                icon_url = self.member.display_avatar
              )
          elif players[str(self.member.id)] == "black":
            if self.member != self.bot.user:
              embed.set_author(
                name = self.member.display_name + (f" | {msgMove}" if msg.author == self.member else "") + (" | Check" if msg.author == self.user and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.user and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.user and self.board.is_stalemate() else ""),
                icon_url = self.member.display_avatar
              ).set_footer(
                text = self.user.display_name + (f" | {msgMove}" if msg.author == self.user else "") + (" | Check" if msg.author == self.member and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.member and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.member and self.board.is_stalemate() else ""),
                icon_url = self.user.display_avatar
              )
            else:
              embed.set_author(
                name = self.member.display_name + (f" | {msgMove}" if botMove else "") + (" | Check" if self.board.is_check() else "") + (" | Checkmate" if self.board.is_checkmate() else "") + (" | Stalemate" if self.board.is_stalemate() else ""),
                icon_url = self.member.display_avatar
              )
              if not botMove:
                embed.set_footer(
                  text = self.user.display_name + (" | Check" if msg.author == self.member and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.member and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.member and self.board.is_stalemate() else ""),
                  icon_url = self.user.display_avatar
                )
              else:
                embed.set_footer(
                  text = self.user.display_name + (" | Check" if self.board.is_check() else "") + (" | Checkmate" if self.board.is_checkmate() else "") + (" | Stalemate" if self.board.is_stalemate() else ""),
                  icon_url = self.user.display_avatar
                )
          self.boardMsg = await self.boardMsg.edit(
            embed = embed
          )
          continue
        except Exception as error:
          if isinstance(error, chess.InvalidMoveError):
            traceback.print_exc()
          traceback.print_exc()
          continue
    except:
      traceback.print_exc()

  @ui.button(
    label = "White",
    custom_id = "selectWhiteSide",
    style = discord.ButtonStyle.primary
  )
  async def selectWhiteSide(self, interaction : discord.Interaction, button : ui.Button):
    with open('json/chessEmojis.json', 'r') as f:
      emojis = json.load(f)
    response = interaction.response
    await response.defer()
    user = interaction.user
    if interaction.user not in [self.user, self.member]:
      err = discord.Embed(
        description = "You do not own this menu !",
        color = 0xff3131
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    self.board = chess.Board()
    strBoard = ""
    numberIndicatorList = [":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]
    for ind, numberIndicator in enumerate(numberIndicatorList):
      strBoard += numberIndicator + str(self.board).split("\n")[ind].replace(
        ". . . . . . . .",
        ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:" if ind % 2 == 0 else ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:"
      )
      strBoard += "\n"
    strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
    whitePawnWhite = self.bot.get_emoji(1169093436528398417)
    whitePawnGreen = self.bot.get_emoji(1169093434854875187)
    blackPawnWhite = self.bot.get_emoji(1169104510019444796)
    blackPawnGreen = self.bot.get_emoji(1169104506441699410)
    strBoard = strBoard.replace(
      " ",
      ""
    )
    for ind, number in enumerate(numberIndicatorList):
      line = strBoard.split("\n")[ind].replace(
        number,
        ""
      ).replace(
        ":white_large_square:",
        "."
      ).replace(
        ":green_square:",
        "."
      )
      for ind, char in enumerate(line):
        if char == ".":
          continue
        if ind % 2 == 0:
          color = "white" if char.islower() else "green"
          if char in ["p", "P"]:
            color = "green" if char.islower() else "white" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
        else:
          color = "green" if char.islower() else "white"
          if char in ["p", "P"]:
            color = "white" if char.islower() else "green" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
    embed = discord.Embed(
      title = "**White**'s turn !",
      description = strBoard,
      color = 0x2b2d31
    ).set_author(
      name = self.member.display_name,
      icon_url = self.member.display_avatar
    ).set_footer(
      text = self.user.display_name,
      icon_url = self.user.display_avatar
    )
    origRes = await interaction.original_response()
    await origRes.delete()
    self.boardMsg = await interaction.channel.send(
      embed = embed
    )
    self.boardThread = await interaction.channel.create_thread(
      name = f"{self.user.display_name} VS. {self.member.display_name}",
      message = self.boardMsg
    )
    await self.startGame(interaction, "white")

  @ui.button(
    label = "Black",
    custom_id = "selectBlackSide",
    style = discord.ButtonStyle.primary
  )
  async def selectBlackSide(self, interaction : discord.Interaction, button : ui.Button):
    with open('json/chessEmojis.json', 'r') as f:
      emojis = json.load(f)
    response = interaction.response
    user = interaction.user
    await response.defer()
    if interaction.user not in [self.user, self.member]:
      err = discord.Embed(
        description = "You do not own this menu !",
        color = 0xff3131
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    self.board = chess.Board()
    strBoard = ""
    numberIndicatorList = [":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]
    for ind, numberIndicator in enumerate(numberIndicatorList):
      strBoard += numberIndicator + str(self.board).split("\n")[ind].replace(
        ". . . . . . . .",
        ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:" if ind % 2 == 0 else ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:"
      )
      strBoard += "\n"
    strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
    whitePawnWhite = self.bot.get_emoji(1169093436528398417)
    whitePawnGreen = self.bot.get_emoji(1169093434854875187)
    blackPawnWhite = self.bot.get_emoji(1169104510019444796)
    blackPawnGreen = self.bot.get_emoji(1169104506441699410)
    strBoard = strBoard.replace(
      " ",
      ""
    )
    for ind, number in enumerate(numberIndicatorList):
      line = strBoard.split("\n")[ind].replace(
        number,
        ""
      ).replace(
        ":white_large_square:",
        "."
      ).replace(
        ":green_square:",
        "."
      )
      for ind, char in enumerate(line):
        if char == ".":
          continue
        if ind % 2 == 0:
          color = "white" if char.islower() else "green"
          if char in ["p", "P"]:
            color = "green" if char.islower() else "white" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
        else:
          color = "green" if char.islower() else "white"
          if char in ["p", "P"]:
            color = "white" if char.islower() else "green" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
    embed = discord.Embed(
      title = "**White**'s turn !",
      description = strBoard,
      color = 0x2b2d31
    ).set_author(
      name = self.user.display_name,
      icon_url = self.user.display_avatar
    ).set_footer(
      text = self.member.display_name,
      icon_url = self.member.display_avatar
    )
    origRes = await interaction.original_response()
    await origRes.delete()
    self.boardMsg = await interaction.channel.send(
      embed = embed
    )
    self.boardThread = await interaction.channel.create_thread(
      name = f"{self.user.display_name} VS. {self.member.display_name}",
      message = self.boardMsg
    )
    await self.startGame(interaction, "black")
  
  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    err = discord.Embed(
      description = "Something went wrong",
      color = 0xff3131
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await interaction.response.send_message(
      embed = err,
      ephemeral = True
    )

class Chess(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  play = app_commands.Group(name = "play", description = "Play commands")

  @play.command(
    name = "chess",
    description = "Play a game of Chess"
  )
  @app_commands.describe(
    member = "Select your opponent :"
  )
  async def playChess(self, interaction : discord.Interaction, member : discord.Member = None):
    with open('json/chessEmojis.json', 'r') as f:
      chessEmojis = json.load(f)
    with open('json/games.json', 'r') as f:
      games = json.load(f)
    response = interaction.response
    user = interaction.user
    if str(user.id) in games["chess"]:
      opponent = await self.bot.fetch_user(games["chess"][str(user.id)])
      err = discord.Embed(
        description = f"You are currently playing  a game with {opponent.mention} ! You cannot create another game for now",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member is not None and member.bot:
      err = discord.Embed(
        description = "You cannot play with a bot !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member is not None and member == user:
      err = discord.Embed(
        description = "You cannot play against yourself !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member is None:
      description = ""
      rowIndicatorList = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
      for n in range(8):
        description += rowIndicatorList[(n)]
        if n % 2 == 0:
          description += ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:\n"
        else:
          description += ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:\n"
      description += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
      embed = discord.Embed(
        description = description,
        color = 0x2b2d31
      ).set_footer(
        text = "Select  a side :"
      )
      await response.send_message(
        content = f"{user.mention}",
        embed = embed,
        view = TextSelectSide(user, self.bot.user, self.bot)
      )
    else:
      description = ""
      rowIndicatorList = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
      for n in range(8):
        description += rowIndicatorList[(n)]
        if n % 2 == 0:
          description += ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:\n"
        else:
          description += ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:\n"
      description += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
      embed = discord.Embed(
        description = description,
        color = 0x2b2d31
      ).set_footer(
        text = "Select  a side :"
      )
      await response.send_message(
        content = f"{user.mention} | {member.mention}",
        embed = embed,
        view = TextSelectSide(user, member, self.bot)
      )
      newData = {
        str(user.id): member.id,
        str(member.id): user.id
      }
      games["chess"].update(newData)
      with open('json/games.json', 'w') as f:
        json.dump(games, f, indent = 2)

  @playChess.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

  @commands.command(
    name = "chess.end",
    description = "End your current game of Chess"
  )
  async def end(self, ctx):
    with open('json/games.json', 'r') as f:
      games = json.load(f)
    user = ctx.author
    if str(user.id) not in games["chess"]:
      err = discord.Embed(
        description = f"{user.mention}, You aren't playing a game of Chess with anyone !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.send(
        embed = err,
        mention_author = False,
        delete_after = 10
      )
      return
    opponent = await self.bot.fetch_user(games["chess"][str(user.id)])
    boardMsg = None
    if isinstance(ctx.channel, discord.Thread):
      err = discord.Embed(
        description = "This thread is only for chess moves ! You cannot do commands here !",
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.channel.send(
        embed = err,
        delete_after = 10
      )
      return
    else:
      async for message in ctx.channel.history(limit = None):
        if message.author == self.bot.user and len(message.embeds) != 0:
          if message.embeds[0].footer.text is not None and message.embeds[0].author.name is not None and message.embeds[0].title.endswith("turn !"):
            if (message.embeds[0].footer.text.startswith(user.display_name) and message.embeds[0].author.name.startswith(opponent.display_name)) or (message.embeds[0].footer.text.startswith(opponent.display_name) and message.embeds[0].author.name.startswith(user.display_name)):
              boardMsg = message
              break
    if boardMsg is None:
      err = discord.Embed(
        description = f"{user.mention}, You do not have an active game in this channel",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.send(
        embed = err,
        mention_author = False,
        delete_after = 10
      )
      return
    else:
      if boardMsg.embeds[0].title.endswith("ended the game"):
        return
      del games["chess"][str(user.id)]
      del games["chess"][str(opponent.id)]
      with open('json/games.json', 'w') as f:
        json.dump(games, f, indent = 2)
      embed = boardMsg.embeds[0].copy()
      embed.title = f"{user.display_name} ended the game"
      await boardMsg.edit(
        embed = embed
      )
      if isinstance(ctx.channel, discord.Thread):
        await ctx.channel.delete()
      else:
        try:
          boardThread = ctx.channel.get_thread(boardMsg.id)
          await boardThread.delete()
        except:
          pass
        await ctx.send(
          f"Ended **{user.display_name}** and **{opponent.display_name}**'s game",
          mention_author = False,
          delete_after = 10
        )

  @end.error
  async def error(self, ctx, error):
    traceback.print_exc()

  @commands.command(
    name = "chess.resign",
    description = "Resign from your game"
  )
  async def resign(self, ctx):
    with open('json/games.json', 'r') as f:
      games = json.load(f)
    user = ctx.author
    if str(user.id) not in games["chess"]:
      err = discord.Embed(
        description = f"{user.mention}, You aren't playing a game of Chess with anyone !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.send(
        embed = err,
        mention_author = False,
        delete_after = 10
      )
      return
    opponent = await self.bot.fetch_user(games["chess"][str(user.id)])
    boardMsg = None
    if isinstance(ctx.channel, discord.Thread):
      err = discord.Embed(
        description = "This thread is only for chess moves ! You cannot do commands here !",
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.channel.send(
        embed = err,
        delete_after = 10
      )
      return
    else:
      async for message in ctx.channel.history(limit = None):
        if message.author == self.bot.user and len(message.embeds) != 0:
          if message.embeds[0].footer.text is not None and message.embeds[0].author.name is not None and message.embeds[0].title.endswith("turn !"):
            if (message.embeds[0].footer.text.startswith(user.display_name) and message.embeds[0].author.name.startswith(opponent.display_name)) or (message.embeds[0].footer.text.startswith(opponent.display_name) and message.embeds[0].author.name.startswith(user.display_name)):
              boardMsg = message
              break
    if boardMsg is None:
      err = discord.Embed(
        description = f"{user.mention}, You do not have an active game in this channel",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.send(
        embed = err,
        mention_author = False,
        delete_after = 10
      )
      return
    else:
      if boardMsg.embeds[0].title.endswith("won !"):
        return
      del games["chess"][str(user.id)]
      del games["chess"][str(opponent.id)]
      with open('json/games.json', 'w') as f:
        json.dump(games, f, indent = 2)
      embed = boardMsg.embeds[0].copy()
      embed.title = f"{user.display_name} resigned. {opponent.display_name} won !"
      await boardMsg.edit(
        embed = embed
      )
      if isinstance(ctx.channel, discord.Thread):
        await ctx.channel.delete()
      else:
        try:
          boardThread = ctx.channel.get_thread(boardMsg.id)
          await boardThread.delete()
        except:
          pass
        await ctx.send(
          f"Ended **{user.display_name}** and **{opponent.display_name}**'s game with a resign",
          mention_author = False,
          delete_after = 10
        )

  @resign.error
  async def error(self, ctx, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(Chess(bot))