#==========================================================================
#                           AUTÔMATO - DEFINIÇÕES
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS
#--------------------------------------------------------------------------
import re
import pprint


#--------------------------------------------------------------------------
#    FUNÇÕES AUXILIARES
#--------------------------------------------------------------------------
# Converte um arquivo csv em uma lista (util para wordList)
def csvToWordList(filename):
    wordList = []
    tmp = []
    erro = False
        
    try:
        file = open(filename, 'r')
    except IOError:
        erro = True
    
    if erro:
        return None
    
    content = file.readlines()
    file.close()  
    
    
    # Lê cada linha do arquivo e coloca na wordList
    for line in content:
        tmp = []
        tmp.extend(re.findall('[A-Za-z]+[^"\n\s]*', line)) # Lê linha tirando aspas e quebras de linha
        if tmp:
            wordList.append(tmp)
    
    return wordList


# Remove elementos repetidos de uma lista
def removeDuplicates(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 


# Dada uma lista, retorna aquela que possui maior tamanho
def listaMaiorTamanho(lista):
    indexMaior = 0
    tamMaior = 0
    
    for i in range(len(lista)):
        if len(lista[i]) > tamMaior:
            indexMaior = i
            tamMaior = len(lista[i])
    return lista[indexMaior]


# Retorna lista de maior tamanho sem elem que ja foram visitados (se todas listas tiverem elementos visitados, retorna None)
# Se todas as listas forem de tamanho 1, retorna None e atualiza pilha de estados a serem processados
def listaMaiorTamanho_NãoVisitado(lista, visitados, pilhaProc):
    if not lista:
        return None
    
    indexMaior = 0
    tamMaior = 0
    
    for i in range(len(lista)):
        igual = False
        s = ''
        
        if len(lista[i]) > tamMaior:
            for item in lista[i]:
                s += item
            if visitados.get(s) != None:
                igual = True
                
            if not igual:
                indexMaior = i
                tamMaior = len(lista[i])
        
        elif len(lista[i]) == tamMaior:
            s = ''
            for item in lista[i]:
                s += item
                
            if visitados.get(s) != None:
                igual = True
            if not igual:
                indexMaior = i
                tamMaior = len(lista[i])

    if tamMaior == 1:
        for item in lista:
            if item:
                item = item[0]
                if pilhaProc.count(item) == 0 and visitados.get(item) == None: # Se elem n ta na pilha e nao foi processado, coloca ele
                    pilhaProc.append(item)
        return None
    elif tamMaior == 0:
        return None
    else:
        return lista[indexMaior]
    

def printDiv():
    print('------------------------------------------------------------------------------------')
    

def printHeader(str):
    print('====================================================================================')
    print("\t%s" % str)
    print('====================================================================================')


def printFileContent(filename):
    file = open(filename, 'r')
    content = file.readlines()
    file.close()
    printHeader('Conteúdo do arquivo %s' % filename)
    pprint.pprint(content)

def wait():
  input("Tecle enter para continuar . . .")
  

#--------------------------------------------------------------------------
#    OBJETO AUTÔMATO
#--------------------------------------------------------------------------
class Automato:
    def __init__(self):
        self.nome = ''
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = ''
        self.estadosFinais = []
        self.fPrograma = [] # matriz com colunas sendo estado, simbolo e prox estado
    
    # Converte um arquivo txt com formato específico em um autômato
    def txtToAutomato(self, filename):
        erro = False

        # Tenta abrir o arquivo. Se não conseguir, gera um erro
        try:
            file = open(filename, 'r')
        except IOError:
            erro = True

        if erro:
            return None

        content = file.readlines()
        file.close()

        # Contrução da matriz que armazena funcao programa
        i = len(content) - 2
        self.fPrograma = [[0 for x in range(3)] for y in range(i)]

        # Pega definição do automato
        tmp = re.split("=", content[0])
        self.nome = tmp[0] #pega nome do automato
        defAutomato = re.findall('({[A-Za-z0-9,]+})',tmp[1])

        # Pega estados, alfabeto e estados finais do autômato
        self.estados = re.findall('[A-Za-z0-9]+', defAutomato[0]) 
        self.alfabeto = re.findall('[A-Za-z0-9]+', defAutomato[1])
        self.estadosFinais = re.findall('[A-Za-z0-9]+', defAutomato[2])

        # Pega estado inicial do autômato
        tmp2 = re.findall('(},[A-Za-z0-9]+,{)',tmp[1])
        self.estadoInicial = re.findall('([A-Za-z0-9]+)',tmp2[0])
        self.estadoInicial = self.estadoInicial[0]

        # Pega função programa do autômato
        i = 0
        for c in range(2, len(content)): #comeca em 2 pq a linha 1 é 'prog'
            tmp = re.split('=', content[c])
            tmp2 = re.findall('([A-Za-z0-9]{1,})', tmp[0]) # Pega (q,s)

            self.fPrograma[i][0] = tmp2[0]          # Pega estado lido
            self.fPrograma[i][1] = tmp2[1]          # Pega simbolo lido
            tmp2 = re.findall('[^\\n]+', tmp[1])  # Pega prox estado (removendo \n)
            self.fPrograma[i][2] = tmp2[0]

            i += 1
        return True


    # Printa autômato
    def printAutomato(self):
        printHeader('Autômato %s' % self.nome)
        print('Alfabeto: ', self.alfabeto)
        print('Estados: ', self.estados)
        print('Estado inicial: ', self.estadoInicial)
        print('Estados finais: ', self.estadosFinais)
        print('Função programa:')
        pprint.pprint(self.fPrograma)
        printDiv()
    
    # Converte autômato não deterministico em deterministico
    def afnToAfd(self):
        afd = Automato()
        afd.nome = self.nome
        afd.alfabeto = self.alfabeto
        afd.estadoInicial = self.estadoInicial
        afd.fPrograma = [['', '', '']]
        mudou = False
        
        actualStates = [afd.estadoInicial] # Armazena estados atuais que estão sendo analisados
        indice = 0 # Indice atual da fPrograma
        visitados = {}
        estadosUnificados = {}
        filaEstados = [] # Fila de estados a serem processados
        larg = len(afd.alfabeto) + 1
        alt = 1
        tabelaAFN = [[[] for x in range(larg)] for y in range(alt)]
        
        ## Criação da tabela afn

        i = 0
        # Executa enquanto houverem estados a serem processados
        while (actualStates or filaEstados):
            aux = []
            
            if actualStates == None: # Se actualStates estiver vazio, coloca um estado a ser processado nele
                if not filaEstados: # Se a fila de estados for vazia, acaba
                    break
                    
                actualStates = []
                actualStates.append(filaEstados.pop(0))
            
            tabelaAFN[i][0].extend(actualStates)

            j = 1 # j começa em 1 porque 0 estao os actual states
            for symbol in afd.alfabeto:
                s = ''
                aux2 = []
                for state in actualStates:
                    s += state # unifica estados
                    fP = self.funcaoPrograma(state, symbol)

                    if fP[0] == '&':
                        continue

                    tabelaAFN[i][j].extend(fP)
                    aux2.extend(fP)
                
                tabelaAFN[i][j] = removeDuplicates(tabelaAFN[i][j])
                aux2 = removeDuplicates(aux2)
                
                j += 1
                visitados[s] = True # marca estado unificado como visitado
                aux.append(aux2)
            
            # Prepara a próxima iteração
            i += 1
            tabelaAFN.append([[] for x in range(larg)])
            actualStates = listaMaiorTamanho_NãoVisitado(aux, visitados, filaEstados) # se tds campos em aux tiverem msm tam, retorna fila deles em filaEstados

        tabelaAFN.pop() # Remove final, que será vazio
        
        # Exibe tabela afn
        '''
        # Printa tabela afn
        print('\t', afd.alfabeto)
        for k in tabelaAFN:
            for e in k:
                print(e, ",\t", end='')
            print("\n")
        '''  
        
        ## Geração do afd

        # Percorre toda a tabela afn
        k = 0
        for i in range(len(tabelaAFN)):
            estado = ''
            final = False
            
            # Unifica estados de actualstates
            tabelaAFN[i][0].sort()
            for state in tabelaAFN[i][0]:
                estado += state + '_'

                # Se estado for final, estado unificado deverá ser final também
                if self.isFinal(state):
                    final = True
            
            estado = estado[:-1:] # Remove '_' do final da string
            
            # Atualiza fPrograma
            for j in range(1, len(afd.alfabeto)+1):
                ####
                tabelaAFN[i][j].sort()

                if tabelaAFN[i][j]: # Verifica se a célula da tabela afn não é vazia
                    afd.fPrograma[k][0] = estado
                    afd.fPrograma[k][1] = afd.alfabeto[j-1]
                    
                    # Une lista de uma célula em uma única string
                    for s in tabelaAFN[i][j]:
                        afd.fPrograma[k][2] += s + '_'
                    
                    afd.fPrograma[k][2] = afd.fPrograma[k][2][:-1:] # Remove '_' do final da string
                    k += 1
                    afd.fPrograma.append(['', '', ''])
            
            # Atualiza estados
            afd.estados.append(estado)
            
            # Atualiza estados finais, se necessário
            if final:
                afd.estadosFinais.append(estado)
        
        # Retira ultima posição da função programa (excesso)
        afd.fPrograma.pop()

        ####
        # Deixa automato ordenado para evitar inconsistências
        #afd.fPrograma.sort()
        afd.estados.sort()
        afd.estadosFinais.sort()
        
        return afd           
    

    # Converte um afd em um afd com função programa total
    #FPT : Função Programa Total
    def convertAfdToFpt(self):
        d = '&&' #representa o 'd' do ppt da aula (não da para um automato ter esse simbolo no input do arquivo)
        naoTotal = False
        i = 0
        fProgramaAux = []
        
        # Transforma função programa em função programa total
        for state in self.estados:
            for symbol in self.alfabeto:
                fp = self.funcaoPrograma(state, symbol)

                # Se encontrar uma indefinição, coloca transição para d
                if fp[0] == '&':
                    naoTotal = True
                    self.fPrograma.insert(i, [state, symbol, d])
                i += 1
    
        self.fPrograma.sort()
        
        # Se afd não possuia função total, acrescenta o simbolo '&&' nos estados do afd
        if naoTotal:
            self.estados.append(d)
            for symbol in self.alfabeto:
                self.fPrograma.append([d, symbol, d])
        
        
    # Função que retorna lista de estados que é possivel ir diretamente a partir de um (se nao achar, retorna None)
    def estadosAtingiveis(self, estado):
        estAtingiveis = []
        
        for i in range(len(self.fPrograma)):
            if self.fPrograma[i][0] == estado:
                estAtingiveis.append(self.fPrograma[i][2])
                
        if not estAtingiveis:
            estAtingiveis = None
        else:
            estAtingiveis = removeDuplicates(estAtingiveis)
            
        return estAtingiveis
    
    
    #retorna todos os estados alcançaveis a partir de um
    def estadosAlcancaveis(self, estado):
        estAlcancaveis = []
        pilha = []
        visitados = {}
        pilha.append(estado)
        
        # Executa enquanto houver estados a serem percorridos
        while pilha:
            est = pilha.pop()
            
            # Busca na função programa estados que sejam alcançaveis a partir do estado fornecido
            for i in range(len(self.fPrograma)):
                if self.fPrograma[i][0] == est and visitados.get(est) == None:
                    estAlcancaveis.append(self.fPrograma[i][2])
                    pilha.append(self.fPrograma[i][2]) # Coloca na pilha para analisar todos os estados alcançaveis
            visitados[est] = True
                
        if not estAlcancaveis:
            estAlcancaveis = None
        else:
            estAlcancaveis = removeDuplicates(estAlcancaveis)
            estAlcancaveis.sort()
            
        return estAlcancaveis
        
        
    #Remove todos os estados inalcancaveis a partir do estado inicial
    def removeEstadosInalcancaveis(self):
        #converter para dicionacio
        estAting = self.estadosAlcancaveis(self.estadoInicial)
        estAting.append(self.estadoInicial)
        
        i = 0
        # Percorre toda a função programa
        while i < len(self.fPrograma):
            # Se o i-esimo estado não é atingivel a partir do estado inicial, remove
            # ele e todas as suas ocorrências da função programa
            if estAting.count(self.fPrograma[i][0]) == 0:
                self.fPrograma.pop(i)
                i -= 1
            
            if estAting.count(self.fPrograma[i][2]) == 0:
                self.fPrograma.pop(i)
                i -= 1
            i += 1
        
        # Remove estados inatingiveis a partir do estafo inicial da lista de estados
        i = 0
        # Percorre todos os estados
        while i < len(self.estados):
            if estAting.count(self.estados[i]) == 0:
                self.estados.pop(i)
                i -= 1
            i += 1

    # Função que simula a função programa do autômato
    def funcaoPrograma(self, estado, simbolo):
        i = 0
        achou = False
        retorno = []
        
        # Busca uma transição dado estado atual e o simbolo lido
        while (not achou) and (i < len(self.fPrograma)):
            if (self.fPrograma[i][0] == estado) and (self.fPrograma[i][1] == simbolo):
                achou = True
                
                while i < len(self.fPrograma):
                    if (self.fPrograma[i][0] == estado) and (self.fPrograma[i][1] == simbolo):
                        retorno.append(self.fPrograma[i][2])    #Pega todos os estados de transição
                    i += 1 
            i += 1
        
        if not achou: # Se não achou, retorna palavra vazia
            retorno.append('&')
        
        return retorno
    
    
    # Retorna se um estado é final
    def isFinal(self, estado):
        i = 0
        ret = True
        
        while i < len(self.estadosFinais):
            if self.estadosFinais[i] == estado:
                return True
            i += 1
        return False
    

    def verificaPalavras(self, wordList):
        i = 1
        tam = len(self.fPrograma)
        resultado = {'aceitas':[], 'rejeitadas':[]}

        # Percorre todas as palavras da lista
        for word in wordList:
            aceita = False
            i = 1
            estadoAtual = []    # Variável que armazena estado que está sendo analisado
            estadoAtual.append(self.estadoInicial) 

            # Percorre todos o alfabeto das palavras
            for symbol in word:
                # Percorre todos os estados que estão sendo analisados no momento
                for s in estadoAtual:
                    tmp = self.funcaoPrograma(s, symbol) # Função programa para estado atual
                    if tmp[0] != '&':       # Se não for palavra vazia, coloca na lista estadoAtual
                        estadoAtual.extend(tmp) 
                        estadoAtual.pop(0)  # Elimina estado que acabou de ser analisado
                estadoAtual = removeDuplicates(estadoAtual) # Remove possiveis estados duplicados dos estados a serem analisados
                
                # Percorre todos os estados que estão sendo analisados no momento e verifica se algum é final
                for estado in estadoAtual:
                    if self.isFinal(estado) and i == len(word): #se for estado final e for ultima letra da palavra, aceita
                        resultado['aceitas'].append(word)
                        aceita = True
                i += 1      
            
            # Se a palavra não for aceita, coloca na lista de rejeitadas
            if aceita == False:
                resultado['rejeitadas'].append(word)
        
        # Exibe palavras aceitas e rejeitadas        
        printHeader('Palavras aceitas')
        pprint.pprint(resultado['aceitas'])
        printDiv()
        printHeader('Palavras Rejeitadas')
        pprint.pprint(resultado['rejeitadas'])
        printDiv()
        
        return resultado
    
    
    # Dado um AFD M, gerar a GR equivalente
    def geraGR(self, fileOutputName):
        fProducao = [[]] # Contém símbolo variável e próximo símbolo

        # Cria o arquivo de saída
        fileOutput = open(fileOutputName+'.txt', 'w')
        
        # Verifica se há um estado inicial
        if self.estadoInicial != '':
            tam = len(self.fPrograma) + len(self.estadosFinais) + 1
            fProducao = [[0 for x in range(2)] for y in range(tam)]  #fProducao[tam][2]
            
            # Coloca na fProdução a transição S -> simbolo_inicial
            fProducao[0][0] = 'S'
            fProducao[0][1] = self.estadoInicial
            
            # Para todos estados finais, gera GR produzindo palavra vazia
            for i in range(0, len(self.estadosFinais)):
                fProducao[i+1][0] = self.estadosFinais[i]
                fProducao[i+1][1] = '&'
            
            i += 2
            # Percorre toda função programa e converte em função de produção
            for j in range(len(self.fPrograma)):
                fProducao[i][0] = self.fPrograma[j][0]
                fProducao[i][1] = '"' + self.fPrograma[j][1] + '"' + self.fPrograma[j][2]
                i += 1
            
            # Escreve definição da gramatica
            print("G=({", end='', file=fileOutput)
            
            # Coloca estados na definição
            for i in range(len(self.estados)):
                print(self.estados[i], end='', file=fileOutput)
                
                if(i+1 < (len(self.estados))):
                    print(",", end='', file=fileOutput)
            
            print("},{", end='', file=fileOutput)
            
            # Coloca alfabeto na definição
            for i in range(len(self.alfabeto)):
                print('"'+self.alfabeto[i]+'"', end='', file=fileOutput)
                
                if(i+1 < len(self.alfabeto)):
                    print(", ", end='', file=fileOutput)
            
            print("},S,P)", file=fileOutput)
            print("P", file=fileOutput)
            
            # Escreve função de produção no arquivo
            for k in range(len(fProducao)):
                fileOutput.write("%s -> %s\n" % (fProducao[k][0], fProducao[k][1]))

        fileOutput.close()
        print("Gramática gerada com sucesso!")
    
    
    # Gera autômato mínimo, garantindo que autômato enviado cumpra os requisitos
    def aMin(self):
        self = self.afnToAfd()          # Converte ele para afd
        self.removeEstadosInalcancaveis()   # Remove seus estados inalcançaveis
        self.convertAfdToFpt()          # Deixa ele com função programa total
        
        return self.automatoMinimo()        # Converte em autômato mínimo
    

    #Dado um AFN M, construir o seu equivalente autômato mínimo Mmin;
    def automatoMinimo(self):
        afm = Automato()
        pilha = []
        firstTime = True
        d = '&&'
        
        afm.nome = self.nome
        afm.estados = self.estados
        afm.estadoInicial = self.estadoInicial
        afm.fPrograma = self.fPrograma
        afm.alfabeto = self.alfabeto
        afm.estadosFinais = self.estadosFinais
        
        ## Cria tabela de distinções
        larg = len(self.estados)
        alt = larg
        tabDistincoes = [['-' for x in range(larg)] for y in range(alt)] #+1 para ser inclusivo no intervalo
        
        listaDependencias = {}
        
        # Preenche matriz coluna 0 com estados
        for l in range(alt-1):
            tabDistincoes[l][0] = self.estados[l+1]
        l += 1 # Armazena indice da última linha da tabela

        # Preenche ultima linha matriz com estados
        for a in range(1, larg):
            tabDistincoes[l][a] = self.estados[a-1]
        
        ## Marca pares estados finais com não finais com true e o resto com false
        for i in range(0, l):
            for j in range(1, i+2): # j vai de 1 até i+1 (incluindo)
                if (self.isFinal(tabDistincoes[i][0])) and (not self.isFinal(tabDistincoes[l][j])):
                    tabDistincoes[i][j] = True
                elif (self.isFinal(tabDistincoes[l][j])) and (not self.isFinal(tabDistincoes[i][0])):
                    tabDistincoes[i][j] = True
                else:
                    tabDistincoes[i][j] = False
        
        ## Percorre pares não marcados no passo anterior
        for i in range(0, l):
            for j in range(1, i+2):
                if tabDistincoes[i][j] == False:
                    p = tabDistincoes[i][0]
                    q = tabDistincoes[l][j]
                    
                    # Para cada simbolo s do alfabeto, testar suas funções programa
                    for letter in self.alfabeto:
                        pR = self.funcaoPrograma(p, letter) # pResultante
                        qR = self.funcaoPrograma(q, letter) # qResultante
                        pR = pR[0]
                        qR = qR[0]
                        
                        if pR == qR:
                            continue
                        
                        # Buscar indice do pR
                        ipR = 0
                        achou = False
                        
                        while not achou and ipR < l:
                            if tabDistincoes[ipR][0] == pR:
                                achou = True
                            else:
                                ipR += 1
                        if not achou:
                            continue
                        
                        # Buscar indice do qR
                        iqR = 1
                        achou = False
                        k = 0
                        while not achou and iqR < larg:
                            if tabDistincoes[l][iqR] == qR:
                                achou = True
                            else:
                                iqR += 1
                        if not achou:
                            continue

                        # Se ipR ou iqR passarem dos limites, 'inverter' eles
                        if tabDistincoes[ipR][iqR] == '-':
                            tmp = ipR
                            ipR = iqR - 2
                            iqR = tmp + 2
                            
                            tmp = pR
                            pR = qR
                            qR = tmp
                            
                        # "Se r e s não estão marcados, criar lista de dep com p e q encabeçados por r e s"
                        if tabDistincoes[ipR][iqR] == False: 
                            listaDependencias[pR+','+qR] = []
                            listaDependencias[pR+','+qR].append([p,q,i,j]) # Guarda p, q e o indice onde esta p,q
                        else:
                            tabDistincoes[i][j] = True
                            
                            # Verifica se p,q possuem lista de dependencia, marcar tds estados dessa lista e
                            # Verifica se cada estado marcado possui uma lista de dependencia (se sim, marcar tds)
                            # e assim recursivamente
                            # Pilha: guarda estados q foram marcados para verificar se possuem lista de dependencia
                            firstTime = True
                            while pilha or firstTime:
                                firstTime = False
                                    
                                if pilha:
                                    elem = pilha.pop()
                                    p1 = elem[0]
                                    q1 = elem[1]
                                else:
                                    p1 = p
                                    q1 = q
                            
                                if (listaDependencias.get(p+','+q) != None) or (listaDependencias.get(q+','+p) != None):
                                    # Se p,q possuem lista de dependencia, marcar todos estados dessa lista
                                    # e guardar estados marcados em uma pilha para verificar se possuem lista de dependência também
                                    if listaDependencias.get(p1+','+q1) != None:
                                        for listaEstados in listaDependencias[p1+','+q1]:
                                            tabDistincoes[listaEstados[2]][listaEstados[3]] = True
                                            pilha.append([listaEstados[0], listaEstados[1]]) # Guarda estado marcado

                                            listaDependencias[p1+','+q1] = None

                                    if listaDependencias.get(q1+','+p1) != None:
                                        for listaEstados in listaDependencias[q1+','+p1]:
                                            tabDistincoes[listaEstados[2]][listaEstados[3]] = True
                                            pilha.append([listaEstados[0], listaEstados[1]])

                                        listaDependencias[q1+','+p1] = None     

        ## Percorre tds estados não marcados e unifica eles
        for i in range(0, l):
            for j in range(1, i+2):
                if tabDistincoes[i][j] == False:
                    if tabDistincoes[i][0] == '&&' or tabDistincoes[l][j] == '&&':
                        continue
                    # Concatena dois estados q1 e q2 e forma um novo 'q1_q2'
                    if tabDistincoes[i][0] < tabDistincoes[l][j]:
                        estadoU = tabDistincoes[i][0] +'_'+ tabDistincoes[l][j]
                    else:
                        estadoU = tabDistincoes[l][j] +'_'+ tabDistincoes[i][0]

                    k = 0
                    # Substitui todas transições que gerem q1 ou q2 por q1_q2
                    while k < len(afm.fPrograma):
                        # Atualiza função programa
                        if afm.fPrograma[k][0] == tabDistincoes[i][0]:
                            afm.fPrograma[k][0] = estadoU
                        
                        # Se havia uma transição para esse estado, muda para ela ir para o estado unificado
                        if afm.fPrograma[k][2] == tabDistincoes[i][0]:
                            afm.fPrograma[k][2] = estadoU
                                               
                        # Exclui o outro estado (já que foi unificado)
                        if afm.fPrograma[k][0] == tabDistincoes[l][j]:
                            afm.fPrograma[k][0] = estadoU
                        
                        # Se havia uma transição para esse estado, muda para ela ir para o estado unificado
                        if afm.fPrograma[k][2] == tabDistincoes[l][j]:
                            afm.fPrograma[k][2] = estadoU

                        if afm.fPrograma[k][2] == '&&':
                            afm.fPrograma.pop(k)
                            k -= 1
                        
                        k += 1
                    
                    k = 0
                    # Atualiza estados com o estado unificado
                    while k < len(afm.estados):
                        if afm.estados[k] == tabDistincoes[i][0] or afm.estados[k] == tabDistincoes[l][j]:
                            afm.estados[k] = estadoU 
                        k += 1
                    
                    k = 0
                    # Atualiza estados finais com o estado unificado (se necessário)
                    while k < len(afm.estadosFinais):
                        if afm.estadosFinais[k] == tabDistincoes[i][0] or afm.estadosFinais[k] == tabDistincoes[l][j]:
                            afm.estadosFinais[k] = estadoU
                            
                        k += 1
                    
                    # Atualiza estado inicial com o estado unificado (se necessário)
                    if afm.estadoInicial == tabDistincoes[i][0]:
                        afm.estadoInicial = estadoU
                    
                    if afm.estadoInicial == tabDistincoes[l][j]:
                        afm.estadoInicial = estadoU
        
        
        ## Exclusão de estados inúteis
        visitado = {}
        pilha = []

        # Marca todos os estados como não visitados
        for state in afm.estados:
            visitado[state] = False
        
        pilha.append(afm.estadoInicial)
        
        # Executa enquanto houver estados a serem analisados
        while pilha:
            est = pilha.pop()
            visitado[est] = True
            est_fp = afm.estadosAtingiveis(est)
            
            # Se não há estados atingíveis a partir do estado atual
            if est_fp == None:
                if not afm.isFinal(est): # Se estado nao é final, achou estado inútil
                    i = 0
                    # Elimina esse estado da função programa
                    while i < len(afm.fPrograma):
                        if afm.fPrograma[i][0] == est or afm.fPrograma[i][2] == est:
                            afm.fPrograma.pop(i)
                            i -= 1
                        i += 1

                    i = 0
                    # Elimina esse estado dos estados do autômato
                    while i < len(afm.estados):
                        if afm.estados[i] == est:
                            afm.estados.pop(i)
                            i -= 1
                        i += 1
            else:   # Se há estados atingíveis a partir do estado atual
                # Se estado atingido nao atinge um estado final, elimina ele
                if len(est_fp) == 1 and est_fp[0] == est and not afm.isFinal(est):
                    i = 0
                    # Elimina esse estado da função programa
                    while i < len(afm.fPrograma):
                        if afm.fPrograma[i][0] == est or afm.fPrograma[i][2] == est:
                            afm.fPrograma.pop(i)
                            i -= 1
                        i += 1
                        
                    i = 0
                    # Elimina esse estado dos estados do autômato
                    while i < len(afm.estados):
                        if afm.estados[i] == est:
                            afm.estados.pop(i)
                            i -= 1
                        i += 1
                else:   # Se estado atingido atinge um estado final, verifica outros estados não visitados
                    for state in est_fp:
                        if visitado.get(state) == None:
                            pilha.append(state)
            
            
        # Printa tabela de distinções
        '''
        for k in tabDistincoes:
            for e in k:
                print(e, ",\t", end='')
            print("\n")
        for m in afm.fPrograma:
            print(m)
        '''
        afm.estados = removeDuplicates(afm.estados)
        afm.fPrograma = removeDuplicates(afm.fPrograma)
        
        ####
        afm.estadosFinais = removeDuplicates(afm.estadosFinais)
        afm.fPrograma.sort()
        afm.estados.sort(reverse=True)
        afm.estadosFinais.sort()
        q = afm.estados.pop() #Elimina estado &&
        if q != '&&':
            afm.estados.append(q)
            afm.estados.sort()
        return afm
    
    # Dados dois AFD M1 e M2, decidir se ACEITA(M1) = ACEITA(M2)
    def verificaEquivalencia(self, m2):
        minM1 = self.aMin()
        minM2 = m2.aMin()

        # Verifica se cada estado do minM1 gera as mesmas transições que minM2
        #if  (len(minM1.estados) != len(minM2.estados)) or (len(minM1.alfabeto) != len(minM2.alfabeto)) or (len(minM1.estadosFinais) != len(minM2.estadosFinais)):
        #        return False
        #else:
        pilha = [] #[est_antigo, novo estado]
        index = 0
        minM1.fPrograma.sort()
        minM2.fPrograma.sort()

        # Renomeia estados da função programa de M1
        i = 0
        lastState = minM1.fPrograma[i][0]

        # Percorre toda fPrograma de M1
        while i < len(minM1.fPrograma):
            pilha.append([minM1.fPrograma[i][0], '_Q' + str(index)])

            # Verifica se o ultimo estado renomeado é igual ao estado que está sendo analisado
            if minM1.fPrograma[i][0] == lastState: # Se for, não incrementa o index
                lastState = minM1.fPrograma[i][0]
                minM1.fPrograma[i][0] = '_Q' + str(index)

            else:
                lastState = minM1.fPrograma[i][0]
                index += 1
                minM1.fPrograma[i][0] = '_Q' + str(index)
            i += 1

        # Percorre toda fPrograma de M1 e atualiza prox_est
        # Renomeia estados restantes de M1
        while pilha:
            tmp = pilha.pop()
            est_ant = tmp[0]
            est_renom = tmp[1]

            for i in range(len(minM1.fPrograma)):
                if minM1.fPrograma[i][2] == est_ant:
                    minM1.fPrograma[i][2] = est_renom

            if minM1.estadoInicial == est_ant:
                minM1.estadoInicial = est_renom

        # Renomeia estados da função programa de M2
        pilha = []
        index = 0

        # Renomeia estados restantes de M2
        i = 0
        lastState = minM2.fPrograma[i][0]

        while i < len(minM2.fPrograma):
            pilha.append([minM2.fPrograma[i][0], '_Q' + str(index)])

            if minM2.fPrograma[i][0] == lastState:
                lastState = minM2.fPrograma[i][0]
                minM2.fPrograma[i][0] = '_Q' + str(index)

            else:
                lastState = minM2.fPrograma[i][0]
                index += 1
                minM2.fPrograma[i][0] = '_Q' + str(index)
            i += 1

        while pilha:
            tmp = pilha.pop()
            est_ant = tmp[0]
            est_renom = tmp[1]

            for i in range(len(minM2.fPrograma)):
                if minM2.fPrograma[i][2] == est_ant:
                    minM2.fPrograma[i][2] = est_renom

            if minM2.estadoInicial == est_ant:
                minM2.estadoInicial = est_renom

        # Verifica se sao equivalentes
        for i in range(len(minM1.fPrograma)):
            if minM1.fPrograma[i][0] != minM2.fPrograma[i][0] or minM1.fPrograma[i][1] != minM2.fPrograma[i][1] or minM1.fPrograma[i][2] != minM2.fPrograma[i][2]:
                return False

        return True
      
    # Dados dois AFD M1 e M2, decidir se ACEITA(M1) = ACEITA(M2)
    def destroi(self):
        del self
        return None