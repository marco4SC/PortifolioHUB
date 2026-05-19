import os
from ferramentas import LetrasAcento, printSecretWord, printForca, tratamento, VerifyLetraInWord, printdisplay, dicas


#funcao para verificar se o jogador acertou e marcar seus lst_er e acertos
def game(word, pontos):

  lst_desc = []  # lista de letras corretas
  lst_er = []  # lista de letras erradas

  printdisplay(word, lst_desc, lst_er, pontos)
  while True:
    ltr = input(
        "Digite Uma Letra, obs:Digite Dica para Dicas>:")  # digitar Letra
    if ltr == "Dica":
      dica, pontos = dicas(pontos, word, lst_desc)

      newW = printdisplay(word, lst_desc, lst_er, pontos)
      if dica != "False":
        print("A dica foi:", dica, "\n")
      else:
        print(f"Voce precisa ter no mínimo 5 pontos para ter dicas")

      if newW == word:
        print("voce ganhou :D")
        pontos+=len(word)
        return pontos

      continue
    ltr = tratamento(ltr)

    if ltr == "FALSE!":  # se tratamento retornar a string "FALSE!" ele reinicia o loop
      continue

    if ltr in lst_er or ltr in lst_desc:
      print("Você ja digitou essa letra antes")
      continue

    ltr = LetrasAcento(ltr, word)

    acertou = VerifyLetraInWord(ltr, word, lst_desc, lst_er)

    if len(lst_er) > 5:
      print("Você perdeu a palavra era ", word)
      return pontos

    newW = printdisplay(word, lst_desc, lst_er, pontos)

    if acertou:
      print("voce acertou uma letra :D")
    else:
      print("voce errou :(", "")

    if newW == word:

      print("voce ganhou :D")
      pontos+=len(word)
      return pontos
