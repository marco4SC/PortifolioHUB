# Preencha a lista com os números mecanográficos dos autores.
AUTORES = [117462, 117468, 115799]


import random
import os
from game import game




def loadsave():
  try:
    file = open("save.txt","r",encoding='utf-8')
    r = file.read()
    file.close()
    return r
  except:
    file = open("save.txt","w",encoding='utf-8')
    file.close()
    return ""





def save(p):
  file = open("save.txt","w",encoding='utf-8')
  file.write(str(p))
  file.close()
  





def Mymenu():
  print("  █████▒ ▒█████   ██▀███   ▄████▄   ▄▄▄   \n"
        "▓██   ▒ ▒██▒  ██▒▓██ ▒ ██▒▒██▀ ▀█  ▒████▄   \n"
        "▒████ ░ ▒██░  ██▒▓██ ░▄█ ▒▒▓█    ▄ ▒██  ▀█▄   \n"
        "░▓█▒  ░ ▒██   ██░▒██▀▀█▄  ▒▓▓▄ ▄██▒░██▄▄▄▄██  \n"
        "░▒█░    ░ ████▓▒░░██▓ ▒██▒▒ ▓███▀ ░ ▓█   ▓██▒ \n"
        "▒ ░    ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒▒   ▓▒█░ \n"
        "░        ░ ▒ ▒░   ░▒ ░ ▒░  ░  ▒     ▒   ▒▒ ░ \n"
        "░ ░    ░ ░ ░ ▒    ░░   ░ ░          ░   ▒    \n"
        "░ ░     ░     ░ ░            ░  ░ \n"
        "░                  \n")
  
  start = input("1) para iniciar \n2) para fechar \n >:")
  match(start):
      case "1":
          main()
      case "2":
        print("saindo...")
        exit()
      case _:
        print("voce digitou um numero invalido")
          
def main_menu(words1,words2):
  words = words1
  print("  ▓█████   ██████  ▄████▄   ▒█████   ██▓     ██░ ██  ▄▄▄  \n"
    "   ▓█   ▀ ▒██    ▒ ▒██▀ ▀█  ▒██▒  ██▒▓██▒    ▓██░ ██▒▒████▄  \n   "
    "▒███   ░ ▓██▄   ▒▓█    ▄ ▒██░  ██▒▒██░    ▒██▀▀██░▒██  ▀█▄  \n "
    "  ▒▓█  ▄   ▒   ██▒▒▓▓▄ ▄██▒▒██   ██░▒██░    ░▓█ ░██ ░██▄▄▄▄██ \n "
    "  ░▒████▒▒██████▒▒▒ ▓███▀ ░░ ████▓▒░░██████▒░▓█▒░██▓ ▓█   ▓██▒\n "
    "  ░░ ▒░ ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▓  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░\n  "
    "  ░ ░  ░░ ░▒  ░ ░  ░  ▒     ░ ▒ ▒░ ░ ░ ▒  ░ ▒ ░▒░ ░  ▒   ▒▒ ░\n    "
    "  ░   ░  ░  ░  ░        ░ ░ ░ ▒    ░ ░    ░  ░░ ░  ░   ▒   \n    "
    "  ░  ░      ░  ░ ░          ░ ░      ░  ░ ░  ░  ░      ░  ░\n                 "
    "  ░                                           ")

  print("1)palavras sem acentos nem cedilhas \n2)palavras com acentos ou cedilhas. \n3)palavras de ambos os tipos"
  )
  while True:
    i = input(">:")
    match(i):
      case "1":
        words = words1 # palavras sem acentos nem cedilhas.
        break
      case "2":
        words = words2 # palavras com acentos ou cedilhas.
        break
      case  "3":
        words = words1 + words2 # palavras de ambos os tipos
        break
      case _:
        print("Isso não é uma opção")

  return words




def RepeatGame():
  print("Você quer continuar a jogar?\n1)Sim\n2)Não")
  while True:
    i = input(">:")
    match(i):
      case "1":
        return False
        break
      case "2":
        return True
        break
      case _:
        print("Isso não é uma opção")

  return words


#funcao para escolher a biblioteca de palavras com base na resposta do usuario
def main():

  pontos=0
  r = loadsave()
  if  r !="":
    pontos=int(r)
  from wordlist import words1, words2

  while True:
    os.system('clear')

    words = main_menu(words1,words2)

    # Escolhe palavra aleatoriamente
    secret = random.choice(words).upper()
    #print(secret)
    pontos = game(secret,pontos)
    save(pontos)
    if RepeatGame():
      break



if __name__ == "__main__":
  os.system('clear')
  Mymenu()
  
