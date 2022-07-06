from random import choice
import random
import unicodedata

base_de_dados = {"comidas":["chocolate","laranja","lasanha","banana","carne","batata","caju"],"marcas":["apple","amazon","netflix","shopee","rolex"],"lugares":["egito","canada","mexico","brasil","peru","angola"]} #Dicionário 1
rodada_final = {"super-herois":["vespa","thor","flash","batman"],"países":["colombia","espanha","alemanha","coreia","argentina"],"séries":["arrow","you","squidgame","therain"]} #Dicionário 2 
nomeJogadores = {"Ana":0,"Bárbara":0,"Carlos":0} #variável com os jogadores e seus respectivos pontos
jogador1 = "Ana" #variável para determinar o jogador ativo
#algumas variáveis para auxiliarem nas funções 
valorRoleta = 0
palavras = []
palavraFinal = ""
tema = ""
temaFinal = ""
palavrasEscondidas = []
palavraFinalEscondida = ""
letrasChutadas = []
valorRodada = 0
valorTurno = 0

def main():
    """Função principal responsável por executar todas as demais subfunções para o
funcionamento do jogo Roda Roda Jequiti"""
    for i in range(3): #três rodadas para acumular pontos e determinar o vencedor final
        antesDoTurno()
        defineRodada(i + 1)
        jogando()
        inicioTurno(True)
    vencedor()
    rodadaFinal()

def antesDoTurno():
    """Função sub-principal responsável por fazer as primeiras definições do jogo, como
o sorteio do tema, das palavras e transformá-las em underlines."""
    limparAsVariaveis() 
    sorteioTema()
    sorteioDasPalavras()
    tresPalavrasOcultas()

def defineRodada(numero):
    """Função responsável por incrementar 1 ao valorRodada para cada rodada do jogo;
    int --> int"""
    global valorRodada
    valorRodada = numero

def jogando():
    """Função sub-principal responsável por promover a jogabilidade do Roda Roda. Tem como
objetivo executar funções como o contabalizador de turno, o roda roleta, o layout e verificar
quantas letras faltam para que, quando faltarem 3, o jogador1 possa chutar as palavras."""
    while True:
        inicioTurno()
        rodaARoleta()
        layout()

        if not isinstance(valorRoleta, int): #verifica se o jogador nao passou a vez
            valorRoleta()
            continue

        if not faltaZeroLetras() and not pergunta():
            passaVez()
            continue

        definePontuacao(valorRoleta)

        if faltaZeroLetras(): #verifica se todas letras já foram descobertas
            break

        if faltaTresLetras():
            layout()

            if chutarPalavras(): #verifica se o jogador acertou ou não as 3 palavras
                break #Se sim, para. Se não, vai para o próximo jogador
            passaVez()
            continue

def inicioTurno(zerar = False):
    """Função responsável por incrementar 1 no valor turno. No final de cada rodada
ela deve zerar;
    bool --> int"""
    global valorTurno

    if zerar:
        valorTurno = 0
    else:
        valorTurno = valorTurno + 1

def vencedor():
    """Função responsável por contabilizar os pontos feitos pelos jogadores durante os
3 turnos. A função vai analisar o vencedor e encaminhá-lo para a rodada final."""
    jogadorComMaisPontos = sorted(list(nomeJogadores.values()))[2] #boto em ordem crescente de pontos e o vencendor joga a rodada final

    for jogador in nomeJogadores.items():
        if jogador[1] == jogadorComMaisPontos: #Se os pontos da tupla (jogador, pontos) for a com mais pontos
            jogadorGanhador = jogador[0]
            break
    print("O vencedor foi VOCÊ, {}!!!".format(jogadorGanhador))
    print("Parabéns {}, você ganhou {} reais!! Já da pra comprar um lanchinho".format(jogadorGanhador, nomeJogadores[jogadorGanhador]))
    print("{}, você foi selecionado(a) para RODADA FINAL. Nela você pode DOBRAR seus ganhos".format(jogadorGanhador))      

    global jogador1
    jogador1 = jogadorGanhador


def rodadaFinal():
    """Função sub-principal responsável por executar a rodada final. Será sorteado um novo
tema, uma nova palavra, transformando ela em underlines, executará um novo layout (com apenas
o ganhador dos turnos anteriores), pedirá letras para o player, substituindo as acertadas na palavra
oculta e, por fim, dirá se ele ganhou ou não a rodada final."""
    sorteioTemaFinal()
    sorteioPalavraFinal()
    palavraFinalOculta()
    layoutFinal()
    letras = pedirConsoanteVogal()
    substitConsoantVogalPalavFinal(letras)
    layoutFinal()
    if chutarPalavraFinal(): #Se acertar
        print(str.format("PARABÉNS {}!!! Você acertou a palavra final e conseguiu acumular {} REAIS!!",jogador1, nomeJogadores[jogador1]))
    else: #Se errar
        print(str.format("Infelizmente você errou {}, mas ainda saiu com {} reais. A palavra certa era {}",jogador1, nomeJogadores[jogador1], palavraFinal))

def limparAsVariaveis():
    """Função que limpa as variaveis iniciais para começar um novo turno."""
    global palavras
    global palavrasEscondidas
    global letrasChutadas

    palavras = []
    palavrasEscondidas = []
    letrasChutadas = []

def sorteioTema():
    """Função que sorteia o tema a partir do dicionário base de dados."""
    global tema

    tema = random.choice(list(base_de_dados.keys()))

def sorteioDasPalavras():
    """Função que sorteia 3 palavras a partir do tema sorteado anteriormente."""
    global palavras
    
    palavrasSorteada = base_de_dados[tema]
    i = 0
    while i < 3:
        palavraEscolhida1 = random.choice(palavrasSorteada)
        palavraEscolhida2 = random.choice(palavrasSorteada)
        palavraEscolhida3 = random.choice(palavrasSorteada)
        if palavraEscolhida1 != palavraEscolhida2 and palavraEscolhida1 != palavraEscolhida3 and palavraEscolhida2 != palavraEscolhida3: #garanto que as palavras sorteadas não sejam iguais
            palavras = [palavraEscolhida1,palavraEscolhida2,palavraEscolhida3]
            return palavras

def tresPalavrasOcultas():
    """Função que armazena as palavras ocultas em uma lista de palavras escondidas."""
    for letra in palavras:
        list.append(palavrasEscondidas, ocultaPalavra(letra))

def ocultaPalavra(palavra):
    """Função que transforma cada letra da palavra sorteada em underline."""
    return ["_" for letra in palavra]

def rodaARoleta():
    """Função que pega um valor aleatório da roleta."""
    global valorRoleta

    roletaRodada = roleta()
    valorRoleta = random.choice(roletaRodada)

def roleta():
    """Função com os possíveis resultados da roleta."""
    valores = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1000, passaVez, passaVez, perdeuTudo, perdeuTudo]
    return valores

def passaVez():
    """Função que passa a jogada para o próximo jogador da lista."""
    global jogador1
    posicao = list(nomeJogadores.keys()).index(jogador1) + 1

    if posicao < len(nomeJogadores):
        jogador1 = pegaNomeDoDicionario(nomeJogadores, posicao) #pego o próximo
    else:
        jogador1 = pegaNomeDoDicionario(nomeJogadores, 0) #caso seja o último, pego o primeiro

def perdeuTudo():
    """Função que zera os pontos do player que está jogando e passa a vez para o próximo player."""
    nomeJogadores[jogador1] = 0
    passaVez()

def pegaNomeDoDicionario(dicionario, i):
    """Função genérica para auxiliar na função passa vez e layout. Pega a chave do dicionário
dado como parâmetro seu índice;
    dict, int --> str """
    return list(dicionario.keys())[i]

def pegaValorNoDicionario(dicionario, i):
    """Função genérica para auxiliar no layout. Pega o valor correspondente à chave do dicionário
dado como parâmetro o indice da chave;
    dict, int --> list"""
    return dicionario[pegaNomeDoDicionario(dicionario,i)]

def layout():
    """Função responsável por executar o layout do jogo roda roda"""
    print("=================================")
    print(str.format("|RODADA {} - TURNO {}",valorRodada, valorTurno))
    print("=================================")

    for i in range(len(nomeJogadores.keys())):
        print({pegaNomeDoDicionario(nomeJogadores, i)})
        print({pegaValorNoDicionario(nomeJogadores, i)})

    print("=================================")    
    print(str.format("jogador ativo: <{}>", jogador1))
    print(str.format("Pontuação atual: <{}>", nomeJogadores[jogador1]))

    if isinstance(valorRoleta, int): #se o valor da roleta vier um número, o jogador continua jogando
        print(str.format("roleta: <{}>", valorRoleta))
    elif valorRoleta.__name__ == "passaVez":
        print("roleta: Passou a vez! Você não jogará essa rodada! ")
    else:
        print("roleta: Que azar, você PERDEU TUDO! Seu dinheiro foi zerado")

    print(str.format("Nova pontuacao: <{}>", nomeJogadores[jogador1]))
    print("=================================")

    print(str.format("Tema: <{}>", tema))
    print("=================================")

    print(str.format("P1){}", palavrasEscondidas[0]))
    print(str.format("P2){}", palavrasEscondidas[1]))
    print(str.format("P3){}", palavrasEscondidas[2]))
    print(str.format("Tentativa de letras: <{}>", str.join(", ", letrasChutadas)))
    
def faltaLetras():
    """Função que verifica quantas letras faltam para acertar as 3 palavras ocultas"""
    faltaTotal = 0
    for p in palavrasEscondidas:
        faltaTotal = faltaTotal + list.count(p,"_")

    return faltaTotal

def faltaZeroLetras():
    """Função que verifica se todas letras da palavra oculta já foram acertadas"""
    return faltaLetras() == 0

def faltaTresLetras():
    """Função que verifica se faltam apenas 3 letras para acertar todas palavras ocultas"""
    faltaTotal = faltaLetras()
    
    if faltaTotal <= 3 and faltaTotal > 0:
        return True
    return False

def pergunta():
    """Função responsável por perguntar ao player uma letra e, caso ela esteja na palavra
oculta, substituir o underline pela tentativa. Além de marcar a tentativa numa lista com
as letras usadas."""
    while True:
        resposta = input("Vamos lá! Valendo {} reais, escreva uma letra: ".format(valorRoleta))
        respostaSemErros = verificaResposta(resposta)

        if not respostaSemErros[0]:
            print({respostaSemErros[1]}) #Manda a mensagem pro jogador
            continue

        marcaLetrasUsadas(resposta) #adiciona a lista de letras usada
        return revelaLetra(resposta)

def verificaResposta(resposta):
    """Função responsável por verificar e analisar se a tentativa de chute de uma letra,
por parte do jogador, está de acordo com os parâmetros (apenas uma letra, sem aceto, sem
repetição);
    str --> bool"""
    palavra = resposta.strip().upper()

    if len(palavra) > 1:
        return (False, "Hey! nada de tentar burlar o jogo! Você digitou mais de uma letra. Escreva apenas uma.")
    elif palavra in "ÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ": #verifica se tem acento
        return (False, "Não digite uma letra com acento. Escreva outra, sem acento")
    elif palavra in letrasChutadas:
        return (False, "Acho melhor você procurar um tratamento para alzheimer. A letra já foi escrita antes. Tente novamente")
    elif len(palavra) < 1:
        return (False, "Você não digitou nenhuma letra, está nervoso(a)?. Escreva alguma letra.")
    else:
        return (True,)

def marcaLetrasUsadas(letra):
    """Função responsável por armazenar as letras chutadas pelo player em uma lista
chamada letrasChutadas;
    str --> list"""
    list.append(letrasChutadas, letra.upper())

def revelaLetra(letra):
    """Função responsável por verificar se a tentativa de chute de letra, por parte do
player, está presente na palavra oculta. Caso esteja, a letra chutada deve ser substituida
no índice correto;
    str --> bool"""
    letraSemAcento = semAcento(letra)
    letraSemAcento = letraSemAcento.upper()
    acertouLetra = False
    palavrasSemAcento = palavrasSorteadasSemAcento()

    for i in range(len(palavrasSemAcento)):
        if letraSemAcento in palavrasSemAcento[i]:
            acertouLetra = True

            for l in range(len(palavras[i])):
                if letraSemAcento == semAcento(palavras[i][l]).upper():
                    palavrasEscondidas[i] = palavrasEscondidas[i][:l] + [palavras[i][l].upper()] + palavrasEscondidas[i][l + 1:] #para substituir o underline preciso que a palavra vá até o índice da letra e troque pela letra acertada

    return acertouLetra

def definePontuacao(pontuacao):
    """Função responsável por incrementar o valor girado na roleta(pontuacao) na quantidade
de pontos atual do jogador1(valor do dicionário).
    int --> int"""
    nomeJogadores[jogador1] = nomeJogadores[jogador1] + pontuacao

def chutarPalavras():
    """Função responsável por executar uma sequência de ações que façam com que o player
tenha a possibilidade de chutar as 3 palavras ocultas de uma vez. Essa função só será chamada
quando faltarem apenas 3 letras para a descoberta das palavras ocultas."""
    while True:
        resposta = input("Você sabe todas palavras e deseja chutá-las de uma vez só? S ou N? ") #Pergunto pro jogador se ele quer chutar

        if resposta.upper() not in "SN": #Verifico se ele escreveu sim ou não
            print("Nada de indecisão!! Só aceito como resposta S ou N")
            continue
        elif resposta.upper() == "S":
            quantAcertos = 0

            for i in range(3):
                palavra = semAcento(input("Então temos um espertinho(a)... Valendo {} reais, escreva a palavra {}: ".format(nomeJogadores[jogador1] * 2, i + 1))) #dobra os pontos do jogador, caso ele acerte

                if palavra.upper() in palavrasSorteadasSemAcento():
                    quantAcertos = quantAcertos + 1
                else:
                    return False #vai para o próximo, caso o jogador erre.

            if quantAcertos >= 3:
                print("Você acertou todas!!! Você, {}, ganhou {} reais".format(jogador1, nomeJogadores[jogador1]*2))
                definePontuacao(nomeJogadores[jogador1] * 2) #dobra a quant de pontos

            return True
        else: #Caso o jogador não queira arriscar, vai para o próximo
            return False
                
def semAcento(palavra): #feito a partir do módulo unicodedata
    """Função que tira o acento da palavra;
    str --> str"""
    tiraAcento = unicodedata.normalize("NFD", palavra)
    tiraAcento = tiraAcento.encode("ASCII","ignore")
    tiraAcento = tiraAcento.decode("utf-8")
    return tiraAcento

    
def palavrasSorteadasSemAcento():
    """Função que transforma todas letras das palavras sorteadas em maiúsculas, sem acento
e adiciona elas numa lista."""
    palavrasSemAcento = []

    for l in palavras:
        list.append(palavrasSemAcento, semAcento(l).upper())

    return palavrasSemAcento


def sorteioTemaFinal():
    """Função que sorteia o tema final a partir do dicionário rodada_final."""
    global temaFinal

    temaFinal = random.choice(list(rodada_final.keys()))

def sorteioPalavraFinal():
    """Função que sorteia uma palavra final a partir do tema sorteado anteriormente."""
    global palavraFinal

    palavrasSorteadas = rodada_final[temaFinal]

    palavraFinal = random.choice(palavrasSorteadas)

def palavraFinalOculta():
    """Função que transforma todos caracteres da palavra final em underline"""
    global palavraFinalEscondida

    palavraFinalEscondida = ocultaPalavra(palavraFinal)

    
def layoutFinal():
    """Função responsável por executar o layout da rodada final do jogo roda roda"""
    print("=================================")
    print("|RODADA FINAL|")
    print("=================================")
    print(str.format("jogador ativo: <{}>", jogador1))
    print(str.format("Pontuação atual: <{}>", nomeJogadores[jogador1]))
    print(str.format("Nova pontuacao: <{}>", nomeJogadores[jogador1] * 2))
    print("=================================")
    print(str.format("Tema: <{}>", temaFinal))
    print("=================================")
    print(str.format("Palavra Final:{}", palavraFinalEscondida))
    print("=================================")

def pedirConsoanteVogal():
    """Função responsável por pedir 5 consoantes e 1 vogal para o jogador participante
da rodada final."""
    while True:
        letras = input("Rodada muito tensa!!! Digite 5 consoantes e 1 vogal[todas letras minúsculas]: \n")
        letras = letras.strip()

        if not verificaRespostaFinal2(letras): #verifico se o jogador colocou de forma correta
            continue
        if not verificaRespostaFinal1(letras):
            continue
        if not verificaRespostaFinal3(letras):
            continue
        return letras

def verificaRespostaFinal1(letras):
    """Função que verifica se as 6 letras chutadas pelo player na rodada final estão
de acordo com os parâmetros requisitados(apenas 1 vogal e 5 consoantes);
    str --> bool"""
    letrasSeparadas = letras.split()
    letra1 = letrasSeparadas[0][0]
    letra2 = letrasSeparadas[0][1]
    letra3 = letrasSeparadas[0][2]
    letra4 = letrasSeparadas[0][3]
    letra5 = letrasSeparadas[0][4]
    letra6 = letrasSeparadas[0][5]
    qtdVogais = contaVogais(letra1, letra2, letra3, letra4, letra5, letra6) #verifico cada uma das letras para ver se o player colocou mais vogais que consoantes ou vice-versa
    if qtdVogais != 1:
        print("Nada de tentar dar a volta em mim!!! Digite apenas 1 vogal. Escreva novamente")
        return False
    return True

def verificaRespostaFinal2(letras):
    """Função que verifica se as 6 letras chutadas pelo player na rodada final estão
de acordo com os parâmetros requisitados(apenas 6 letras, sem acento);
    str --> bool"""
    if not len(letras) == 6:
        print("Nada de tentar dar a volta em mim!!! Digite apenas 6 letras. Escreva novamente")
        return False
    elif letras in "áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ": #verifica se tem acento
        print("Não digite uma letra com acento. Escreva outra, sem acento")
        return False
    return True

def verificaRespostaFinal3(letras):
    """Função que verifica se as 6 letras chutadas pelo player na rodada final estão
de acordo com os parâmetros requisitados(apenas 1 vogal e 5 consoantes);
    str --> bool"""
    letrasSeparadas = letras.split()
    letra1 = letrasSeparadas[0][0]
    letra2 = letrasSeparadas[0][1]
    letra3 = letrasSeparadas[0][2]
    letra4 = letrasSeparadas[0][3]
    letra5 = letrasSeparadas[0][4]
    letra6 = letrasSeparadas[0][5]
    qtdConsoantes = contaConsoantes(letra1, letra2, letra3, letra4, letra5, letra6) #verifico cada uma das letras para ver se o player colocou mais vogais que consoantes ou vice-versa
    if qtdConsoantes != 5:
        print("Nada de tentar dar a volta em mim!!! Digite apenas 5 consoantes. Escreva novamente")
        return False
    if (letra1 == letra2) or (letra1 == letra3) or (letra1 == letra4) or (letra1 == letra5) or (letra1 == letra6) or (letra2 == letra3) or (letra2 == letra4) or (letra2 == letra5) or (letra2 == letra6) or (letra3 == letra4) or (letra3 == letra5) or (letra3 == letra6) or (letra4 == letra5) or (letra4 == letra5) or (letra5 == letra6):
        print("Nada de tentar dar a volta em mim!!! Digite 5 consoantes diferentes. Escreva novamente")
        return False
    return True

def contaConsoantes(letra1, letra2, letra3, letra4, letra5, letra6):
    """Função que conta a quantidade de consoantes dado 6 letras;
    str, str, str, str, str, str --> int"""
    consoantes = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]
    qtd1 = list.count(consoantes,letra1)
    qtd2 = list.count(consoantes,letra2)
    qtd3 = list.count(consoantes,letra3)
    qtd4 = list.count(consoantes,letra4)
    qtd5 = list.count(consoantes,letra5)
    qtd6 = list.count(consoantes,letra6)
    return qtd1 + qtd2 + qtd3 + qtd4 + qtd5 + qtd6   
    

def contaVogais(letra1, letra2, letra3, letra4, letra5, letra6):
    """Função que conta a quantidade de vogais dado 6 letras;
    str, str, str, str, str, str --> int"""
    vogais = ["a","e","i","o","u"]
    qtd1 = list.count(vogais,letra1)
    qtd2 = list.count(vogais,letra2)
    qtd3 = list.count(vogais,letra3)
    qtd4 = list.count(vogais,letra4)
    qtd5 = list.count(vogais,letra5)
    qtd6 = list.count(vogais,letra6)
    return qtd1 + qtd2 + qtd3 + qtd4 + qtd5 + qtd6
        
def substitConsoantVogalPalavFinal(letras):
    """Função responsável por substituir as letras chutadas, pelo player vencedor, que
estiverem na palavra final;
    str --> list"""
    global palavraFinal
    global palavraFinalEscondida

    palavraFinalSemAcento = semAcento(palavraFinal)
    palavraFinalSemAcento = palavraFinalSemAcento.upper() #transformo todas letras em maiúsculas
    letrasSeparadas = [letra.upper() for letra in letras]

    for i in range(len(palavraFinalSemAcento)):
        indices = []

        for letraSeparadas in letrasSeparadas:
            if palavraFinalSemAcento[i] == letraSeparadas: #Guardo o indice de cada letra que o jogador acertou
                list.append(indices,i)

        for l in indices:
            palavraFinalEscondida = palavraFinalEscondida[:l] + [palavraFinalSemAcento[i]] + palavraFinalEscondida[l + 1:] #para substituir o underline preciso que a palavra vá até o índice da letra e troque pela letra acertada
    
def chutarPalavraFinal():
    """Função responsável por armazenar o chute final do player final e verificar se
foi correto (dobrando o número de pontos) ou não."""
    palavra = semAcento(input("Satisfeito com as letras que você chutou? Valendo {} reais, digite a palavra final: ".format(nomeJogadores[jogador1] * 2)))

    if palavra.upper() == semAcento(palavraFinal).upper():
        definePontuacao(nomeJogadores[jogador1] * 2) #dobro a pontuação, caso o jogador acerte
        return True
    return False

if (__name__ == "__main__"):
    main()
