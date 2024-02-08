import os
import random
import time
import msvcrt

saldo_eur = 1000  # valor inicial do saldo em euros
fichas = 0  # valor inicial das fichas

# Definindo os naipes e valores das cartas
NAIPES = ['Copas', 'Ouros', 'Paus', 'Espadas']
VALORES = ['Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove', 'Dez', 'Valete', 'Dama', 'Rei', 'Ás']

# Função para criar um baralho
def criar_baralho():
    baralho = [{'Naipe': naipe, 'Valor': valor} for naipe in NAIPES for valor in VALORES]
    random.shuffle(baralho)
    return baralho

# Função para exibir as cartas na mão de um jogador
def exibir_mao(jogador, mao, revelar=True):
    print(f"\nMão do {jogador}:")
    for i, carta in enumerate(mao):
        if revelar or jogador != 'Utilizador':
            print(f" {carta['Valor']} de {carta['Naipe']} \n")
        else:
            print(f"Carta {i + 1}: Virada para baixo")

# Função para realizar uma rodada de apostas
def fazer_aposta(jogadores, apostas, fichas_cpus, apostas_totais):
    global fichas
    aposta_minima = max(apostas.values()) if apostas else 0

    # Inicializar a aposta do Utilizador
    apostas['Utilizador'] = apostas.get('Utilizador', 0)

    for jogador in jogadores:
        if jogador != 'Utilizador':
            aposta_aleatoria = random.randint(0, fichas_cpus[jogador] // 2)  # Exemplo de aposta aleatória
            apostas[jogador] = aposta_aleatoria
            fichas_cpus[jogador] -= aposta_aleatoria
            print(f" {jogador} apostou {aposta_aleatoria} fichas.")
            apostas_totais[jogador] = apostas_totais.get(jogador, 0) + aposta_aleatoria

    while True:
        try:
            nova_aposta = int(input("Utilizador, faça sua aposta (ou 0 para manter): "))
            if 0 <= nova_aposta <= fichas:
                apostas['Utilizador'] += nova_aposta
                fichas -= nova_aposta
                apostas_totais['Utilizador'] = apostas_totais.get('Utilizador', 0) + nova_aposta
                break
            else:
                print("A aposta não pode exceder o saldo. Tente novamente.")
        except ValueError:
            print("Por favor, insira um valor numérico válido.")

    # Exibir saldo do Utilizador
    print(f"Total de fichas do Utilizador: {fichas} fichas.")

    return apostas, fichas_cpus, apostas_totais

def avaliar_mao(mao, cartas_mesa):
    todas_as_cartas = mao + cartas_mesa
    valores = [carta['Valor'] for carta in todas_as_cartas]
    naipes = [carta['Naipe'] for carta in todas_as_cartas]

    valores_numericos = {'Dois': 2, 'Três': 3, 'Quatro': 4, 'Cinco': 5, 'Seis': 6, 'Sete': 7, 'Oito': 8, 'Nove': 9,
                         'Dez': 10, 'Valete': 11, 'Dama': 12, 'Rei': 13, 'Ás': 14}

    valores_ordenados = sorted([valores_numericos[valor] for valor in valores], reverse=True)

    # Verifica se é uma sequência
    sequencia = all(x - 1 == valores_ordenados[i + 1] for i, x in enumerate(valores_ordenados[:-1]))

    # Verifica se todos os naipes são iguais
    mesmo_naipe = len(set(naipes)) == 1

    # Verifica se é um flush (cinco cartas do mesmo naipe)
    flush = mesmo_naipe

    # Verifica se é uma sequência (straight flush)
    straight_flush = sequencia and flush

    # Verifica pares, trincas, quadras e full house
    contagem_valores = {valores.count(valor): valor for valor in set(valores)}

    # Verifica se há um par
    par = 2 in contagem_valores

    # Verifica se há uma trinca
    trinca = 3 in contagem_valores

    # Verifica se há uma quadra
    quadra = 4 in contagem_valores

    # Verifica se há um full house (trinca e um par)
    full_house = trinca and par

    # Verifica se é um straight
    straight = sequencia

    if straight_flush:
        return 'Straight Flush'
    elif quadra:
        return 'Quadra'
    elif full_house:
        return 'Full House'
    elif flush:
        return 'Flush'
    elif straight:
        return 'Straight'
    elif trinca:
        return 'Trinca'
    elif par == 2:
        return 'Dois Pares'
    elif par == 1:
        return 'Um Par'
    else:
        return 'Carta Alta'

def mostrar_resultado(maos, cartas_mesa, apostas_totais):
    print("\n--- Resultado Final ---")

    # Exibir mãos finais
    for jogador, mao in maos.items():
        exibir_mao(jogador, mao)

    # Determinar vencedor
    vencedor = determinar_vencedor(maos, cartas_mesa)
    print(f"\nVencedor: {vencedor}")

# Função para determinar o vencedor
def determinar_vencedor(maos, cartas_mesa):
    melhores_maos = {}

    for jogador, mao in maos.items():
        melhor_mao = avaliar_mao(mao, cartas_mesa)
        melhores_maos[jogador] = melhor_mao

    vencedor = max(melhores_maos, key=melhores_maos.get)

    return vencedor

def espera_tecla_esc():
    if os.name == 'nt':
        return msvcrt.kbhit() and msvcrt.getch() == b'\x1b'
    else:
        return False

def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


saldo_eur = 1000  # valor inicial do saldo em euros
fichas = 0  # valor inicial das fichas

def mostrar_menu():
    clear()
    print("################################")
    print("#                              #")
    print("#      Bem-vindo ao Casino     #")
    print("#        Python Royale         #")
    print("#                              #")
    print("################################")
    print("# Opções:                      #")
    print("# 1. Slot Machine              #")
    print("# 2. Blackjack                 #")
    print("# 3. Roleta                    #")
    print("# 4. Poker                     #")
    print("# 5. Dados                     #")
    print("# 6. Deposito de Fichas        #")
    print("# 7. Levantamento de Fichas    #")
    print("# 8. Consultar Saldo           #")
    print("# 9. Sair                      #")
    print("################################")

def jogar_slot():
    global fichas

    print("\n=== Bem-vindo à Máquina de Slots ===")

    # Variáveis da máquina de slots
    jackpot = 0
    chance_multiplicacao = 0.1  # 10%
    multiplicador = 1  # Valor padrão do multiplicador
    valor_aposta = 0

    def girar_slots():
        # Inicializar as posições dos números
        linhas = [[random.choice(['♠', '♘', '⍫', '☬', '♅', '♆', '𝟟', '✵', '☣']) for _ in range(5)] for _ in range(4)]
        posicoes = [[0, 0, 0] for _ in range(4)]

        # Exibir mensagem enquanto os slots giram
        print("\nA girar os slots...")

        # Animar o giro dos números
        for _ in range(7):
            for i in range(4):
                posicoes[i] = [random.choice(['♠', '♘', '⍫', '☬', '♅', '♆', '𝟟', '✵', '☣']) for _ in range(5)]
                print(" ".join(map(str, posicoes[i])))
                time.sleep(0.1)

                # Limpar a tela a cada três linhas
                if i == 2:
                    time.sleep(0.2)  # Atraso adicional para visualização
                    clear()

        # Limpar a mensagem "Girando os slots" após a animação
        clear()

        # Exibir os resultados finais
        print("\nResultados finais:")
        for i in range(4):
            print(" ".join(map(str, linhas[i])))
        return linhas

    def calcular_ganhos(resultados):
        ganho = 0

        # Verificar número total de símbolos iguais
        total_simbolos_iguais = sum(linha.count(simbolo) for linha in resultados for simbolo in linha)

        if total_simbolos_iguais == 8:
            print(f"Parabéns! Oito símbolos iguais no total. Recebeu o Triplo do Valor Apostado.")
            ganho += valor_aposta * 3 * multiplicador
        elif total_simbolos_iguais == 7:
            print(f"Parabéns! Sete símbolos iguais no total. Recebeu o Dobro do Valor Apostado.")
            ganho += valor_aposta * 2 * multiplicador
        elif total_simbolos_iguais == 6:
            print(f"Parabéns! Seis símbolos iguais no total. Recebeu o Valor Apostado.")
            ganho += valor_aposta * multiplicador
        elif total_simbolos_iguais == 5:
            print(f"Parabéns! Cinco símbolos iguais no total. Recebeu Metade do Valor Apostado.")
            ganho += valor_aposta / 2 * multiplicador

        # Verificar combinações nas linhas
        for linha in resultados:
            for simbolo in set(linha):
                if linha.count(simbolo) == 5:
                    print(f"Parabéns! Cinco símbolos {simbolo} na mesma linha. Recebeu o Quádruplo do Valor Apostado.")
                    ganho += valor_aposta * 4 * multiplicador
                elif linha.count(simbolo) == 4:
                    print(f"Parabéns! Quatro símbolos {simbolo} na mesma linha. Recebeu o Triplo do Valor Apostado.")
                    ganho += valor_aposta * 3 * multiplicador
                elif linha.count(simbolo) == 3:
                    print(f"Parabéns! Três símbolos {simbolo} na mesma linha. Recebeu 0.25 do Valor Apostado.")
                    ganho += valor_aposta / 4 * multiplicador

        # Verificar combinações em colunas
        for coluna in range(5):
            for simbolo in set(resultados[i][coluna] for i in range(4)):
                if resultados[0].count(simbolo) == 4:
                    print(f"Parabéns! Quatro símbolos {simbolo} na mesma coluna. Recebeu o Quádruplo do Valor Apostado.")
                    ganho += valor_aposta * 4 * multiplicador
                elif resultados[0].count(simbolo) == 3:
                    print(f"Parabéns! Três símbolos {simbolo} na mesma coluna. Recebeu o Triplo do Valor Apostado.")
                    ganho += valor_aposta * 3 * multiplicador

        # Verificar combinações nas diagonais
        for simbolo in set(resultados[i][i] for i in range(4)):
            if all(resultados[i][i] == simbolo for i in range(4)):
                print(f"Parabéns! Quatro símbolos {simbolo} na diagonal. Recebeu o Quádruplo do Valor Apostado.")
                ganho += valor_aposta * 4 * multiplicador
        for simbolo in set(resultados[i][4 - i] for i in range(4)):
            if all(resultados[i][4 - i] == simbolo for i in range(4)):
                print(f"Parabéns! Quatro símbolos {simbolo} na diagonal. Recebeu o Quádruplo do Valor Apostado.")
                ganho += valor_aposta * 4 * multiplicador

        # Verificar jackpot
        if resultados[0].count('𝟟') == 5:
            print("Parabéns! Cinco símbolos 𝟟 em linha. Jackpot!")
            ganho += jackpot

        if ganho == 0:
            print("Não ganhou dinheiro. Tente novamente.")

        return ganho


    while True:
        clear()  # Limpar o ecrã antes da entrada do dinheiro
        print(f"Fichas disponíveis: {fichas}")
        print(f"Jackpot atual: {jackpot}€")
        print(f"Chance de Multiplicação Atual: {chance_multiplicacao * 100}%")
        print(f"Multiplicador Atual: {multiplicador}x")

        try:
            while True:
                fichas_apostadas = int(input("Introduza a Quantia de Fichas que Deseja Apostar (0 para sair): "))
                if fichas_apostadas == 0:
                    print("Obrigado por jogar!")
                    return
                elif fichas_apostadas > 0 and fichas_apostadas <= fichas:
                    break
                else:
                    print("Quantidade de fichas inválida. Tente novamente.")
        except ValueError:
            print("Por favor, insira um valor numérico válido.")

        # Aumentar o jackpot ao fazer um único spin
        jackpot += fichas_apostadas / 2

        escolha_spins = input("Quantos spins deseja fazer? (Digite '1' para um único spin, 'auto' para spins automáticos): ").lower()

        if escolha_spins == '1':
            num_spins = 1
        elif escolha_spins == 'auto':
            while True:
                try:
                    num_spins = int(input("Quantos spins automáticos deseja fazer? (1 ou mais): "))
                    if num_spins >= 1:
                        break
                    else:
                        print("Número de spins inválido. Tente novamente.")
                except ValueError:
                    print("Por favor, insira um valor numérico válido.")
        else:
            print("Escolha inválida. Tente novamente.")
            continue

        valor_aposta = fichas_apostadas // max(1, num_spins)
        saldo_final_total = 0
        total_ganhos = 0
        total_perdas = 0

        # Inicializar o jackpot com o valor apostado multiplicado por 100
        jackpot = fichas_apostadas * 100

        # Adicione a variável de controle
        sair_spins_automaticos = False

        spin_num = 1
        while spin_num <= num_spins:
            resultados = girar_slots()
            ganho = calcular_ganhos(resultados)
            jackpot += fichas_apostadas // num_spins // 2  # Adicionar metade da aposta naquele spin ao jackpot quando se perde
            fichas -= valor_aposta  # Retirar a aposta
            fichas += ganho # Adicionar o ganho

            print(f"\nSpin: {spin_num}")
            print(f"Fichas ganhas no spin: {ganho}")
            print(f"Jackpot atualizado: {jackpot}€")
            print(f"Fichas disponíveis: {fichas}")

            if ganho > 0:
                total_ganhos += ganho
                # Aplicar chance de multiplicação
                if random.random() < chance_multiplicacao:
                    multiplicador *= 2
                    print(f"Você teve sorte! Multiplicador agora é {multiplicador}x")
            else:
                total_perdas += valor_aposta

            if spin_num < num_spins:
                print("Pressione Esc para parar ou aguarde para continuar...")
                time.sleep(2.5)
                # Adicione a lógica para verificar a tecla "Esc"
                if espera_tecla_esc():
                    print("Saindo dos spins automáticos.")
                    time.sleep(1)
                    break

                time.sleep(2)  # Intervalo de 2 segundos entre spins

            spin_num += 1

        print(f"\nFichas ganhas total após spins: {total_ganhos} fichas")
        print(f"Fichas perdidas total após spins: {total_perdas} fichas")
        print("Total de ganhos: ", total_ganhos - total_perdas)
        input("Pressione Enter para continuar...")

def jogar_blackjack():
    global fichas
    while True:
        clear()
        print("Bem-vindo ao Blackjack!\n")

        # Verificar saldo
        print(f"Saldo atual: {fichas:.2f} fichas")

        # Perguntar pela aposta
        while True:
            try:
                aposta = int(input("Digite o valor da aposta (ou 0 para cancelar): "))
                if 0 < aposta <= fichas:
                    break
                elif aposta == 0:
                    print("Aposta cancelada.")
                    time.sleep(2)
                    return
                else:
                    print("A aposta não pode exceder o saldo.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        # Reduzir a aposta do saldo
        fichas -= aposta

        # Inicializar baralho
        baralho = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # As cartas de 2 a 10 valem seu valor, 10 para cartas de imagem, 11 para As

        # Inicializar mãos do jogador e do dealer
        mao_jogador = [random.choice(baralho), random.choice(baralho)]
        mao_dealer = [random.choice(baralho), random.choice(baralho)]

        def calcular_pontuacao(mao):
            """Calcula a pontuação de uma mão, tratando os As de forma especial."""
            pontuacao = sum(mao)
            if 11 in mao and pontuacao > 21:
                mao.remove(11)
                mao.append(1)
                pontuacao = sum(mao)
            return pontuacao

        def mostrar_maos(jogador, dealer, mostra_tudo=False):
            """Mostra as mãos do jogador e do dealer."""
            print(f" Sua mão: {jogador}, Pontuação: {calcular_pontuacao(jogador)}")
            time.sleep(2)
            if mostra_tudo:
                print(f" Mão do dealer: {dealer}, Pontuação: {calcular_pontuacao(dealer)}")
            else:
                print(f" Mão do dealer: {dealer[0]}, ?")

        def verificar_vitoria(jogador, dealer):
            """Verifica as condições de vitória."""
            pontuacao_jogador = calcular_pontuacao(jogador)
            pontuacao_dealer = calcular_pontuacao(dealer)

            if pontuacao_jogador == 21:
                return("Blackjack! Você venceu!")
            elif pontuacao_dealer == 21:
                return("Dealer tem Blackjack. Você perdeu.")
            elif pontuacao_jogador > 21:
                return("Você ultrapassou 21. Você perdeu.")
            elif pontuacao_dealer > 21:
                return("Dealer ultrapassou 21. Você venceu!")
            elif pontuacao_jogador > pontuacao_dealer:
                return("Você venceu!")
            elif pontuacao_jogador < pontuacao_dealer:
                return("Você perdeu.")
            else:
                return("Empate!")

        # Mostrar mãos iniciais
        mostrar_maos(mao_jogador, mao_dealer)

        # Verificar Blackjack
        if calcular_pontuacao(mao_jogador) == 21 or calcular_pontuacao(mao_dealer) == 21:
            print(verificar_vitoria(mao_jogador, mao_dealer))
            break

        # Rodada do jogador
        while calcular_pontuacao(mao_jogador) < 21:
            escolha = input("Digite 'h' para pedir uma carta, 's' para parar: ").lower()
            if escolha == 'h':
                mao_jogador.append(random.choice(baralho))
                mostrar_maos(mao_jogador, mao_dealer)
            elif escolha == 's':
                break
            else:
                print("Escolha inválida. Digite 'h' ou 's'.")

        time.sleep(2)

        # Rodada do dealer
        while calcular_pontuacao(mao_dealer) < 17:
            mao_dealer.append(random.choice(baralho))
            mostrar_maos(mao_jogador, mao_dealer)

        time.sleep(2.5)  # Pausa antes de mostrar o resultado final

        # Mostrar mãos finais
        mostrar_maos(mao_jogador, mao_dealer, mostra_tudo=True)

        # Verificar vencedor
        resultado = verificar_vitoria(mao_jogador, mao_dealer)
        print(resultado)

        # Atualizar o saldo com base no resultado
        if "venceu" in resultado.lower():
            fichas += 2 * aposta  # Ganha o dobro da aposta
        elif "perdeu" in resultado.lower():
            # Nada a fazer, já que a aposta já foi retirada do saldo
            pass
        else:
            fichas += aposta  # Recupera a aposta em caso de empate

        # Perguntar se quer jogar novamente
        jogar_novamente = input("Deseja jogar outra mão? (Digite 's' para sim, 'n' para não): ").lower()
        if jogar_novamente != 's':
            break        

def jogar_roleta():
    print("Você escolheu jogar Roleta. Boa sorte!")
    global fichas

    numeros_vermelhos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    numeros_pretos = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    # Perguntar pelo tipo de aposta
    while True:
        clear()
        print("Bem-vindo à Roleta!\n")
        print(f"Saldo atual: {fichas:.2f} fichas")

        # Perguntar pela aposta
        while True:
            try:
                aposta = int(input("Digite o valor da aposta (ou 0 para cancelar): "))
                if 0 < aposta <= fichas:
                    break
                elif aposta == 0:
                    print("Aposta cancelada.")
                    time.sleep(2)
                    return
                else:
                    print("A aposta não pode exceder o saldo.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        # Reduzir a aposta do saldo
        fichas -= aposta

        # Exibir os números vermelhos e pretos
        print("\nNúmeros Vermelhos:", ", ".join(map(str, numeros_vermelhos)))
        print("Números Pretos:", ", ".join(map(str, numeros_pretos)))

        print("Opções de Aposta:")
        print("1. Números de 1 a 18")
        print("2. Números de 19 a 36")
        print("3. Vermelho")
        print("4. Preto")
        print("5. Verde (0)")
        print("6. Par")
        print("7. Ímpar")
        print("8. Escolher número específico")

        while True:
            try:
                escolha_aposta = int(input("Escolha o tipo de aposta (1-8): "))
                if 1 <= escolha_aposta <= 8:
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        # Rodar a roleta (números de 0 a 36, onde 0 é verde)
        numero_sorteado = random.randint(0, 36)

        # Determinar a cor
        if numero_sorteado == 0:
            cor = "verde"
        elif numero_sorteado in numeros_vermelhos:
            cor = "vermelho"
        elif numero_sorteado in numeros_pretos:
            cor = "preto"

        # Verificar resultados e atualizar o saldo
        if escolha_aposta == 1 and 1 <= numero_sorteado <= 18:
            print("Apostou em 1-18. Ganhou!")
        elif escolha_aposta == 2 and 19 <= numero_sorteado <= 36:
            print("Apostou em 19-36. Ganhou!")
        elif escolha_aposta == 3 and cor == "vermelho":
            print("Apostou no vermelho. Ganhou!")
        elif escolha_aposta == 4 and cor == "preto":
            print("Apostou no preto. Ganhou!")
        elif escolha_aposta == 5 and cor == "verde":
            print("Apostou no verde (0). Ganhou!")
        elif escolha_aposta == 6 and numero_sorteado % 2 == 0:
            print("Apostou no par. Ganhou!")
        elif escolha_aposta == 7 and numero_sorteado % 2 == 1:
            print("Apostou no ímpar. Ganhou!")
        elif escolha_aposta == 8:
            numero_escolhido = int(input("Escolha um número de 0 a 36: "))
            if numero_escolhido == numero_sorteado:
                print(f"Escolheu o número certo! Ganhou!")
            else:
                print(f"Escolheu o número errado. Perdeu.")
        else:
            print("Perdeu.")

        # Apresentar o número sorteado depois de verificar os resultados
        print(f"O número sorteado é: {numero_sorteado} ({cor})")

        # Perguntar se quer jogar novamente
        jogar_novamente = input("Deseja jogar outra vez? (Digite 's' para sim, 'n' para não): ").lower()
        if jogar_novamente != 's':
            break

def jogar_poker():
    global fichas
    jogadores = ['CPU1', 'CPU2', 'CPU3', 'Utilizador']
    fichas_cpus = {jogador: random.randint(50, 150) for jogador in jogadores if jogador != 'Utilizador'}
    apostas_totais = {}

    # Inicializar baralho e mão dos jogadores
    baralho = criar_baralho()
    maos = {jogador: [baralho.pop(), baralho.pop()] for jogador in jogadores}

    # Mostrar a mão do Utilizador
    exibir_mao('Utilizador', maos['Utilizador'], revelar=True)

    # Solicitar aposta inicial
    while True:
        try:
            print("\nApostas dos CPUs:")
            for jogador, aposta_cpu in fichas_cpus.items():
                print(f"{jogador}: {aposta_cpu} fichas")
            nova_aposta = int(input("\nUtilizador, faça sua aposta (ou -1 para sair): "))
            if nova_aposta == -1:
                print("Saindo do jogo...")
                vencedor = determinar_vencedor(maos, [])
                print(f"O vencedor é: {vencedor}")
                time.sleep(2)
                return  # Sair da função
            elif nova_aposta == 0:
                print("Apostando 0 fichas. Mantendo a aposta.")
                break
            elif 1 <= nova_aposta <= fichas:
                apostas = {'Utilizador': nova_aposta}
                fichas -= nova_aposta
                apostas_totais['Utilizador'] = nova_aposta
                break
            else:
                print("A aposta deve ser maior que zero e menor ou igual ao saldo. Tente novamente.")
        except ValueError:
            print("Por favor, insira um valor numérico válido.")

    print("\nAntes de começar, vamos mostrar sua mão.")
    exibir_mao('Utilizador', maos['Utilizador'], revelar=True)
    print("Agora, vamos fazer a aposta inicial.")

    # Revelar 3 cartas na mesa
    cartas_mesa = [baralho.pop() for _ in range(3)]
    print("\nCartas na mesa após a primeira rodada de apostas:")
    for carta in cartas_mesa:
        print(f" {carta['Valor']} de {carta['Naipe']}")

    exibir_mao('Utilizador', maos['Utilizador'], revelar=True)

    # Permitir apostas para esta fase
    apostas, fichas_cpus, apostas_totais = fazer_aposta(jogadores, apostas, fichas_cpus, apostas_totais)

    # Verificar se o jogador optou por desistir após cada rodada de apostas
    if -1 in apostas.values():
        print("O jogador optou por desistir. Determinando o vencedor...")
        vencedor = determinar_vencedor(maos, cartas_mesa)
        print(f"O vencedor é: {vencedor}")
        return

    # Revelar mais 1 carta na mesa
    cartas_mesa.append(baralho.pop())
    print("\nCartas na mesa após a segunda rodada de apostas:")
    for carta in cartas_mesa:
        print(f"{carta['Valor']} de {carta['Naipe']}")

    exibir_mao('Utilizador', maos['Utilizador'], revelar=True)

    # Permitir apostas para esta fase
    apostas, fichas_cpus, apostas_totais = fazer_aposta(jogadores, apostas, fichas_cpus, apostas_totais)

    # Verificar se o jogador optou por desistir após cada rodada de apostas
    if -1 in apostas.values():
        print("O jogador optou por desistir. Determinando o vencedor...")
        vencedor = determinar_vencedor(maos, cartas_mesa)
        print(f"O vencedor é: {vencedor}")
        return

    # Revelar a última carta na mesa
    cartas_mesa.append(baralho.pop())
    print("\nCartas na mesa após a terceira rodada de apostas:")
    for carta in cartas_mesa:
        print(f"{carta['Valor']} de {carta['Naipe']}")

    exibir_mao('Utilizador', maos['Utilizador'], revelar=True)

    # Permitir apostas para esta fase
    apostas, fichas_cpus, apostas_totais = fazer_aposta(jogadores, apostas, fichas_cpus, apostas_totais)

    # Verificar se o jogador optou por desistir após cada rodada de apostas
    if -1 in apostas.values():
        print("O jogador optou por desistir. Determinando o vencedor...")
        vencedor = determinar_vencedor(maos, cartas_mesa)
        print(f"O vencedor é: {vencedor}")
        return

    # Exibir mãos finais
    for jogador, mao in maos.items():
        exibir_mao(jogador, mao, revelar=True)

    # Avaliar mãos e determinar o vencedor
    exibir_mao('Utilizador', maos['Utilizador'], revelar=True)  # Revelar as cartas do Utilizador
    mostrar_resultado(maos, cartas_mesa, apostas_totais)

    # Exibir apostas totais
    print("\nApostas totais:")
    for jogador, aposta_total in apostas_totais.items():
        print(f" {jogador}: {aposta_total} fichas")

    # Esperar antes de avançar para a próxima rodada
    input("Pressione Enter para continuar...")

def jogar_dados():
    print("Você escolheu jogar Dados. Boa sorte!")
    global fichas

    while True:
        # Verificar saldo
        print(f"Saldo atual: {fichas:.2f} fichas")

        # Perguntar pela aposta
        while True:
            try:
                aposta = int(input("Digite o valor da aposta (ou 0 para cancelar): "))
                if 0 < aposta <= fichas:
                    break
                elif aposta == 0:
                    print("Aposta cancelada.")
                    time.sleep(2)
                    return
                else:
                    print("A aposta não pode exceder o saldo.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")

        # Reduzir a aposta do saldo
        fichas -= aposta

        input("Pressiona Enter para lançar os dados...")

        # Simula o lançamento de dois dados
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)

        # O jogador escolhe se o total será maior, menor ou igual a 6
        escolha = input("Acha que o total será maior, menor ou igual a 6? (maior/menor/igual): ").lower()

        print(f"\nResultado do dado 1: {dado1}")
        print(f"Resultado do dado 2: {dado2}")

        total = dado1 + dado2
        print(f"Total: {total}")

        # Verifica se o jogador acertou
        if (escolha == 'maior' and total > 6) or (escolha == 'menor' and total < 6) or (escolha == 'igual' and total == 6):
            print("Parabéns! Ganhou!")
            fichas += 2 * aposta  # Ganha o dobro da aposta
        else:
            print("Perdeu. Tente novamente!")

        jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
        if jogar_novamente != 's':
            break

def deposito():
    global saldo_eur
    global fichas
    
    print(f'------------------Casino Python Royale------------------\n')
    print(f'Seu saldo em euros é: €{saldo_eur}')
    print(f'Seu saldo de fichas é: {fichas} fichas\n')

    while True:
        try:
            fichas_depositar = int(input(' Introduza a Quantidade de Fichas que Deseja Depositar (ou 0 para cancelar): '))
            if fichas_depositar == 0:
                print("Depósito cancelado.")
                time.sleep(2)
                break
            elif fichas_depositar > 0 and fichas_depositar <= saldo_eur:
                saldo_eur -= fichas_depositar
                fichas += fichas_depositar
                break
            elif fichas_depositar > saldo_eur:
                print("Não é possível depositar mais fichas do que o saldo em euros.")
            else:
                print("O valor deve ser maior ou igual a zero. Tente novamente.")
                time.sleep(2)
        except ValueError:
            print("Por favor, insira um valor numérico válido.")

    print(f'--------------------------------------------------------\n')
    if fichas_depositar != 0:
        print(f"Você depositou {fichas_depositar} em fichas. Saldo total em euros: €{saldo_eur}. Saldo total de fichas: {fichas} fichas")
        time.sleep(4)

def levantamento():
    global saldo_eur
    global fichas

    print(f'------------------Casino Python Royale------------------\n')
    print(f'Seu saldo em euros é: €{saldo_eur}')
    print(f'Seu saldo de fichas é: {fichas} fichas\n')

    while True:
        try:
            fichas_levantar = int(input(' Introduza a Quantidade de Fichas que Deseja Levantar (ou 0 para cancelar): '))
            if fichas_levantar == 0:
                print("Levantamento cancelado.")
                time.sleep(2)
                break
            elif fichas_levantar > 0 and fichas_levantar <= fichas:
                taxa = fichas_levantar * 0.05  # taxa de 5% para lucro do casino
                total_levantado = fichas_levantar - taxa
                fichas -= fichas_levantar
                saldo_eur += total_levantado
                break
            elif fichas_levantar > fichas:
                print("Não é possível levantar mais fichas do que você tem.")
            else:
                print("O valor deve ser maior ou igual a zero. Tente novamente.")
                time.sleep(2)
        except ValueError:
            print("Por favor, insira um valor numérico válido.")

    print(f' Será aplicada uma taxa de 5% no levantamento.')
    print(f' Valor a levantar (após taxa): €{total_levantado:.2f}. Saldo total em euros: €{saldo_eur}. Saldo total de fichas: {fichas} fichas')
    time.sleep(5)


def consultar_saldo():
    global saldo_eur
    while True:
        clear()
        print(f'------------------Casino Python Royale------------------\n')
        print(f'Seu saldo em euros é: €{saldo_eur}\n')
        print(f'Seu saldo de fichas é: {fichas} fichas\n')
        print("Opções:")
        print("1. Voltar para o menu inicial")
        print("2. Recarregar saldo")
        
        opcao = input("Escolha uma opção (1-2): ")
        
        if opcao == '1':
            break
        elif opcao == '2':
            saldo_eur += 1000
            print(f'Saldo recarregado com sucesso!')
            time.sleep(2)
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(2)

while True:
    clear()
    mostrar_menu()

    escolha = input("Escolha uma opção (1-9): ")

    if escolha == '1':
        clear()
        jogar_slot()
    elif escolha == '2':
        clear()
        jogar_blackjack()
    elif escolha == '3':
        clear()
        jogar_roleta()
    elif escolha == '4':
        clear()
        jogar_poker()
    elif escolha == '5':
        clear()
        jogar_dados()
    elif escolha == '6':
        clear()
        deposito()
    elif escolha == '7':
        clear()
        levantamento()
    elif escolha == '8':
        clear()
        consultar_saldo()
    elif escolha == '9':
        print("Obrigado por jogar. Até mais!")
        break
    else:
        print("Opção inválida. Tente novamente.")
