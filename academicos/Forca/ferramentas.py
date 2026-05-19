import os
import random


#funcao para verificar as letras acentuadas
#Letra digitada, palavra a ser descoberta
def LetrasAcento(ltr, word):
  mapLetra = {
      "A": ["Á", "Ã", "Â"],
      "E": ["Ê", "É"],
      "I": ["Í"],
      "O": ["Ó", "Õ", "Ô"],
      "U": ["Ú"],
      "C": ["Ç"]
  }
  lst = [ltr]  #lista com as letras
  if not (ltr in mapLetra):
    return lst
  for i in mapLetra[ltr]:
    if i in word:
      lst.append(i)

  return lst


#funcao para imprimir as letras descobertas os erros
#palavra a ser descoberta, lista de letras descobertas, letras erradas descobertas
def printSecretWord(word, lst_desc, lst_er):

  alfabeto = ",A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z"

  print("Nº DE ERROS:", len(lst_er))

  newWord = ""

  for i in word:
    if i in lst_desc:
      newWord += i
    else:
      newWord += " _ "

  for i in (lst_er + lst_desc):
    if i in alfabeto:
      alfabeto = alfabeto.replace("," + i, "")

  print("Letras que eu errei:", ",".join(lst_er))
  print("Letras disponiveis:", alfabeto[1:])

  return newWord


#funcao de desenho da forca
#palavra a ser descoberta, lista de letras descobertas, letras erradas descobertas
def printForca(word, lst_desc, lst_er):

  anim = [
      "------- \n !     | \n       |\n       |\n       |\n       |\n=========",  #sem erros 
      "------- \n !     | \n O     |\n       |\n       |\n       |\n=========",  #1 erros
      "------- \n !     | \n O     |\n |     |\n       |\n       |\n=========",  #2 erros
      "------- \n !     | \n O     |\n/|     |\n       |\n       |\n=========",  #3 erros
      "------- \n !     | \n O     |\n/|\    |\n       |\n       |\n=========",  #4 erros
      "------- \n !     | \n O     |\n/|\    |\n/      |\n       |\n=========",  #5 erros
      "------- \n !     | \n O     |\n/|\    |\n/ \    |\n       |\n========="  #6 erros 
  ]

  print(anim[lst_er])

  print("")


#funcao para verificar se o usuario digitou apenas uma letra e se colocou algum caracter invalido
def tratamento(ltr):
  if len(ltr) > 1:
    print("escreva apenas 1 letra por vez")
    return "FALSE!"
  if not (ltr.isalpha()):
    print("Isso não é um caracter valido")
    return "FALSE!"

  ltr = ltr.upper()
  return ltr


#funcao para verificar se a letra esta na palavra
#letra digitada, palavra a ser descoberta, lista de letras descobertas, letras erradas descobertas
def VerifyLetraInWord(ltr, word, descobertas, erros):
  acerT = False
  for ltrI in ltr:
    if ltrI in word:
      descobertas.append(ltrI)
      acerT = True
    else:
      erros.append(ltrI)
  return acerT


def printdisplay(word, lst_desc, lst_er, pontos):
  os.system('clear')
  printForca(word, lst_desc, len(lst_er))
  newW = printSecretWord(word, lst_desc, lst_er)
  print(newW)
  print("")

  print("")
  print("Meus pontos:", pontos, "\n")
  return newW


def dicas(pontos, word, lst_desc):

  if pontos >= 5:
    pontos -= 5
    while True:
      new = random.choice(list(word))
      if not (new in lst_desc):
        lst_desc.append(new)

        return new, pontos
  else:
    return "False", pontos
