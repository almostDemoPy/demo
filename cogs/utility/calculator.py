import ast
import discord
import numexpr
import traceback
from discord import app_commands, ui
from discord.ext import commands
from math import *

class CalculatorFunctionView(ui.View):
  def __init__(self, equation = "", answer = ""):
    super().__init__(
      timeout = None
    )
    self.numList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    self.symList = ["(", ")", "+", "-", "*", "/"]
    self.equation = equation
    self.answer = answer

  async def addVar(self, interaction, button):
    response = interaction.response
    user = interaction.user
    if button.label in ["(", ")"]:
      if len(self.equation) == 0:
        self.equation += button.label
      else:
        if self.equation[-1] in ["(", ")"]:
          self.equation += button.label
        else:
          self.equation += f" {button.label}"
    elif button.label == "DEL":
      if self.equation == "" or len(self.equation) == 1:
        self.equation = ""
      else:
        if self.equation[-2] == " ":
          self.equation = self.equation[:-2]
        else:
          if len(self.equation) >= 4 and (self.equation.endswith("sin(") or self.equation.endswith("log(") or self.equation.endswith("cos(") or self.equation.endswith("fac(") or self.equation.endswith("sqr(") or self.equation.endswith("tan(") or self.equation.endswith("exp(")):
            if len(self.equation) >= 5:
              if self.equation[-5] == " ":
                self.equation = self.equation[:-5]
              else:
                self.equation = self.equation[:-4]
            else:
              self.equation = self.equation[:-4]
          elif len(self.equation) >= 3 and (self.equation.endswith("ln(") or self.equation.endswith("ANS")):
            if len(self.equation) >= 4:
              if self.equation[-4] == " ":
                self.equation = self.equation[:-4]
              else:
                self.equation = self.equation[:-3]
            else:
              self.equation = self.equation[:-3]
          else:
            self.equation = self.equation[:-1]
    elif button.label == "A/C":
      self.equation = ""
    elif button.label in ["sin", "log", "cos", "fac", "sqr", "tan", "exp"]:
      if len(self.equation) == 0:
        self.equation += f"{button.label}("
      else:
        self.equation += f" {button.label}("
    elif button.label == "π":
      if len(self.equation) == 0:
        self.equation += button.label
      else:
        self.equation += " π"
    elif button.label == "e":
      if len(self.equation) == 0:
        self.equation += button.label
      else:
        self.equation += " e"
    elif button.label == "ANS":
      if len(self.equation) in [0, 1]:
        if self.equation in self.symList:
          self.equation += f" ANS"
        else:
          self.equation += "ANS"
      else:
        self.equation += " ANS"
    elif button.label == "=":
      try:
        self.answer = str(eval(self.equation.replace("ANS", self.answer).replace("π", "3.14").replace("fac(", "factorial(").replace("sqr(", "sqrt(")))
        if self.answer.endswith(".0"):
          self.answer = self.answer[:-2]
        button.label = "SEND"
      except:
        traceback.print_exc()
        self.answer = ""
        err = interaction.message.embeds[0].copy()
        err.color = 0xff3131
        err.clear_fields()
        err.add_field(
          name = "Output :",
          value = "```\nMath Error\n```",
          inline = False
        )
        await response.edit_message(
          embed = err,
          view = self
        )
        return
    elif button.label == "SEND":
      embedCalculatorPrompt = interaction.message.embeds[0].copy()
      embedCalculatorPrompt.set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await interaction.channel.send(
        embed = embedCalculatorPrompt
      )
      button.label = "="
    if button.label not in ["SEND", "="]:
      if self.children[19].label != "=":
        self.children[19].label = "="
    embedCopy = interaction.message.embeds[0].copy()
    embedCopy.color = 0x2b2d31
    embedCopy.description = f"```\n{self.equation}\n```"
    embedCopy.clear_fields()
    embedCopy.add_field(
      name = "Output :",
      value = f"```\n{self.answer}\n```",
      inline = False
    )
    await response.edit_message(
      embed = embedCopy,
      view = self
    )

  @ui.button(
    label = "("
  )
  async def openingParenthesis(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = ")"
  )
  async def closingParenthesis(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "​",
    disabled = True
  )
  async def emptySlotThree(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "DEL",
    style = discord.ButtonStyle.primary
  )
  async def delete(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "A/C",
    style = discord.ButtonStyle.primary
  )
  async def allClear(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "sin"
  )
  async def sine(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "log"
  )
  async def logarithmBaseTen(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "π"
  )
  async def pi(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "​",
    disabled = True,
    style = discord.ButtonStyle.primary
  )
  async def emptySlotNine(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "​",
    disabled = True,
    style = discord.ButtonStyle.primary
  )
  async def emptySlotTen(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "cos"
  )
  async def cosine(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "e"
  )
  async def euler(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "fac"
  )
  async def factorial(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "sqr",
    style = discord.ButtonStyle.primary
  )
  async def squareRoot(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "​",
    disabled = True,
    style = discord.ButtonStyle.primary
  )
  async def emptySlotFifteen(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "tan"
  )
  async def tangent(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "exp",
    style = discord.ButtonStyle.primary
  )
  async def exponentialEuler(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "​",
    disabled = True,
    style = discord.ButtonStyle.primary
  )
  async def emptySlotEighteen(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "ANS",
    style = discord.ButtonStyle.primary
  )
  async def answer(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "=",
    style = discord.ButtonStyle.green
  )
  async def equals(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.select(
    placeholder = "Select a section :",
    min_values = 1,
    max_values = 1,
    options = [
      discord.SelectOption(
        label = "Nums"
      )
    ]
  )
  async def functionsSelect(self, interaction, select):
    response = interaction.response
    user = interaction.user
    if select.values[0] == "Nums":
      await response.edit_message(
        view = CalculatorView(self.equation, self.answer)
      )

  async def on_error(self, interaction, error):
    traceback.print_exc()

class CalculatorView(ui.View):
  def __init__(self, equation = "", answer = ""):
    super().__init__(
      timeout = None
    )
    self.numList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    self.symList = ["(", ")", "+", "-", "*", "/"]
    self.equation = equation
    self.answer = answer

  async def addVar(self, interaction, button):
    response = interaction.response
    user = interaction.user
    if button.label in self.numList or button.label == ".":
      if self.equation == "" or self.equation[-1] in self.numList or self.equation[-1] == ".":
        self.equation += button.label
      else:
        self.equation += f" {button.label}"
    elif button.label == "A/C":
      self.equation = ""
    elif button.label == "DEL":
      if self.equation == "" or len(self.equation) == 1:
        self.equation = ""
      else:
        if self.equation[-2] == " ":
          self.equation = self.equation[:-2]
        else:
          if len(self.equation) >= 4 and (self.equation.endswith("sin(") or self.equation.endswith("log(") or self.equation.endswith("cos(") or self.equation.endswith("fac(") or self.equation.endswith("sqr(") or self.equation.endswith("tan(") or self.equation.endswith("exp(")):
            if len(self.equation) >= 5:
              if self.equation[-5] == " ":
                self.equation = self.equation[:-5]
              else:
                self.equation = self.equation[:-4]
            else:
              self.equation = self.equation[:-4]
          elif len(self.equation) >= 3 and (self.equation.endswith("ln(") or self.equation.endswith("ANS")):
            if len(self.equation) >= 4:
              if self.equation[-4] == " ":
                self.equation = self.equation[:-4]
              else:
                self.equation = self.equation[:-3]
            else:
              self.equation = self.equation[:-3]
          else:
            self.equation = self.equation[:-1]
    elif button.label == ".":
      if len(self.equation) in [0, 1]:
        if self.equation in self.symList:
          self.equation += " ."
        else:
          self.equation += "."
      else:
        if self.equation[-1] in self.symList:
          self.equation += " ."
        else:
          self.equation += "."
    elif button.label == "00":
      if len(self.equation) in [0, 1]:
        if self.equation in self.symList:
          self.equation += " 00"
        else:
          self.equation += "00"
      else:
        if self.equation[-1] in self.symList:
          self.equation += " 00"
        else:
          self.equation += "00"
    elif button.label == "×" or button.label == "÷" or button.label in self.symList:
      if self.equation == "" or self.equation[-1] in ["*", "/"]:
        self.equation += f"{button.label}".replace("×", "*").replace("÷", "/")
      else:
        self.equation += f" {button.label}".replace("×", "*").replace("÷", "/")
    elif button.label == "ANS":
      if len(self.equation) in [0, 1]:
        if self.equation in self.symList:
          self.equation += f" ANS"
        else:
          self.equation += "ANS"
      else:
        self.equation += " ANS"
    elif button.label == "=":
      try:
        self.answer = str(eval(self.equation.replace("ANS", self.answer).replace("π", "3.14").replace("fac(", "factorial(").replace("sqr(", "sqrt(")))
        if self.answer.endswith(".0"):
          self.answer = self.answer[:-2]
        button.label = "SEND"
      except:
        traceback.print_exc()
        self.answer = ""
        err = interaction.message.embeds[0].copy()
        err.color = 0xff3131
        err.clear_fields()
        err.add_field(
          name = "Output :",
          value = "```\nMath Error\n```",
          inline = False
        )
        await response.edit_message(
          embed = err,
          view = self
        )
        return
    elif button.label == "SEND":
      embedCalculatorPrompt = interaction.message.embeds[0].copy()
      embedCalculatorPrompt.set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await interaction.channel.send(
        embed = embedCalculatorPrompt
      )
      button.label = "="
    if button.label not in ["SEND", "="]:
      if self.children[19].label != "=":
        self.children[19].label = "="
    embedCopy = interaction.message.embeds[0].copy()
    embedCopy.color = 0x2b2d31
    embedCopy.description = f"```\n{self.equation}\n```"
    embedCopy.clear_fields()
    embedCopy.add_field(
      name = "Output :",
      value = f"```\n{self.answer}\n```",
      inline = False
    )
    await response.edit_message(
      embed = embedCopy,
      view = self
    )

  @ui.button(
    label = "7"
  )
  async def seven(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "8"
  )
  async def eight(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "9"
  )
  async def nine(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "DEL",
    style = discord.ButtonStyle.primary
  )
  async def delete(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "A/C",
    style = discord.ButtonStyle.primary
  )
  async def allClear(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "4"
  )
  async def four(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "5"
  )
  async def five(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "6"
  )
  async def six(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "×",
    style = discord.ButtonStyle.primary
  )
  async def multiply(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "÷",
    style = discord.ButtonStyle.primary
  )
  async def divide(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "1"
  )
  async def one(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "2"
  )
  async def two(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "3"
  )
  async def three(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "+",
    style = discord.ButtonStyle.primary
  )
  async def add(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "-",
    style = discord.ButtonStyle.primary
  )
  async def subtract(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "0"
  )
  async def zero(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = ".",
    style = discord.ButtonStyle.primary
  )
  async def decimal(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "00",
    style = discord.ButtonStyle.primary
  )
  async def zeroHundred(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "ANS",
    style = discord.ButtonStyle.primary
  )
  async def answer(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.button(
    label = "=",
    style = discord.ButtonStyle.green
  )
  async def equals(self, interaction, button):
    await self.addVar(interaction, button)

  @ui.select(
    placeholder = "Select a section :",
    min_values = 1,
    max_values = 1,
    options = [
      discord.SelectOption(
        label = "Functions"
      )
    ]
  )
  async def numSelect(self, interaction, select : str):
    response = interaction.response
    user = interaction.user
    if select.values[0] == "Functions":
      await response.edit_message(
        view = CalculatorFunctionView(self.equation, self.answer)
      )

  async def on_error(self, interaction, error):
    traceback.print_exc()

class Calculator(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command\t\t: /calculator")

  @app_commands.command(
    name = "calculator",
    description = "Use a calculator"
  )
  async def calculator(self, interaction : discord.Interaction):
    response = interaction.response
    user = interaction.user
    embed = discord.Embed(
      description = "```\n\n```",
      color = 0x2b2d31
    ).add_field(
      name = "Output :",
      value = "```\n\n```",
      inline = False
    )
    await response.send_message(
      embed = embed,
      view = CalculatorView(),
      ephemeral = True
    )

  @calculator.error
  async def error(self, interaction, error):
    traceback.print_exc()
  
async def setup(bot):
  await bot.add_cog(Calculator(bot))