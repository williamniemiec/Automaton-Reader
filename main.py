#--------------------------------------------------------------------------
#    IMPORTS
#--------------------------------------------------------------------------
import sys
sys.path.append("src/")
from Automato import *


#--------------------------------------------------------------------------
#    MAIN
#--------------------------------------------------------------------------
sair = False
init = False

af = Automato()

while not sair:
    printHeader("Escolha uma opção")
    print("1: Abrir autômato")
    if init:
        print("2: Exibir autômato")
        print("3: Palavras aceitas e rejeitadas")
        print("4: Gerar gramática equivalente")
        print("5: Converter em autômato mínimo")
        print("6: Verificar equivalência com outro autômato")
    print("0: Sair\n")
    
    printDiv()
    op = input("Opção: ")
    printDiv()
    if op == '1':
        printHeader('Abrir autômato')
        desistir = False
        filename = input("Insira o nome do arquivo: ")
        out = af.txtToAutomato(filename)
        
        while out == None and desistir == False:
            print("Erro: Arquivo não encontrado")
            filename = input("Insira o nome do arquivo (ou '0' para sair): ")
            if filename == '0':
                desistir = True
            else:
                out = af.txtToAutomato(filename)
        
        if not desistir:
            init = True
    elif init:
        if op == '2':
            af.printAutomato()
            wait()
        elif op == '3':
            printHeader('Palavras aceitas e rejeitadas')
            desistir = False
            filename = input("Insira o nome do arquivo de palavras: ")
            wordList = csvToWordList(filename)

            while wordList == None and desistir == False:
                print("Erro: Arquivo não encontrado")
                filename = input("Insira o nome do arquivo (ou '0' para sair): ")
                if filename == '0':
                    desistir = True
                else:
                    wordList = csvToWordList(filename)
            
            af.verificaPalavras(wordList)
        elif op == '4':
            printHeader('Gramática equivalente')
            name = input("Insira o nome do arquivo (ou '0' para sair): ")
            if name != '0':
                af.geraGR(name)
                printFileContent(name+'.txt')
                wait()
        elif op == '5':
            print('Convertendo para autômato mínimo...')
            af = af.aMin()
            print('Conversão feita com sucesso!')
            wait()
        elif op == '6':
            printHeader('Verificação de equivalência com outro autômato')
            af_tmp = Automato()
            desistir = False
            
            filename = input("Insira o nome do arquivo (ou '0' para sair): ")
            out = af_tmp.txtToAutomato(filename)
            
            while out == None and desistir == False:
                print("Erro: Arquivo não encontrado")
                filename = input("Insira o nome do arquivo (ou '0' para sair): ")
                if filename == '0':
                    desistir = True
                else:
                    out = af_tmp.txtToAutomato(filename)

            if not desistir:
                out = af.verificaEquivalencia(af_tmp)
                if out == True:
                    print("Os autômatos %s e %s são equivalentes!" % (af.nome, af_tmp.nome))
                else:
                    print("Os autômatos %s e %s não são equivalentes!" % (af.nome, af_tmp.nome))
                af_tmp.destroi()
                wait()
    if op == '0':
        sair = True
if init:
    af.destroi()
