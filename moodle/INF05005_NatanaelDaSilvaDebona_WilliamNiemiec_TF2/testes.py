#==========================================================================
#                             AUTÔMATO - TESTES
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS
#--------------------------------------------------------------------------
import sys
sys.path.append("src/")
from Automato import *


#--------------------------------------------------------------------------
#    TESTES
#--------------------------------------------------------------------------
###########################################################################
#   Teste principal
###########################################################################
printHeader('Teste principal')
# Inicialização
af = Automato()
af.txtToAutomato("midia/Robo_Catador_AFN.txt")
af.printAutomato()

# Palavras aceitas e rejeitadas
wordList = csvToWordList("midia/palavras.txt")
af.verificaPalavras(wordList)

# Gramatica equivalente
printHeader('Gramática equivalente')
af.geraGR('gramaticaEquivalente')
printFileContent('gramaticaEquivalente.txt')

# Autômato mínimo
printHeader('Autômato mínimo')
am = af.aMin()
am.printAutomato()

# Teste de palavras no autômato mínimo gerado
wordList = csvToWordList("midia/palavras.txt")
res = am.verificaPalavras(wordList)

# Deixa no formato funcao programa total
'''
printHeader('Deixa no formato funcao programa total')
af.convertAfdToFpt()
af.printAutomato()
'''
# Remoção estados inalcançaveis
'''
printHeader('Remoção estados inalcançaveis')
af.removeEstadosInalcancaveis()
af.printAutomato()
'''
'''
# Conversão afn -> afd
printHeader('Conversão afn -> afd')
af2 = af.afnToAfd()
af2.printAutomato()
'''

###########################################################################
#   Teste equivalência
###########################################################################
printHeader('Teste equivalência')
af = Automato()
af.alfabeto = ['0', '1']
af.estados = ['q0', 'q1']
af.estadoInicial = 'q0'
af.estadosFinais = ['q1']
af.fPrograma = [['q0', '0', 'q0'],
                 ['q0', '1', 'q1'],
                 ['q1', '0', 'q1'],
                 ['q1', '1', 'q0']]

af3 = Automato()
af3.alfabeto = ['0', '1']
af3.estados = ['q0', 'q1', 'q2']
af3.estadoInicial = 'q0'
af3.estadosFinais = ['q2']
af3.fPrograma = [['q0', '0', 'q0'],
                 ['q0', '1', 'q2'],
                 ['q2', '0', 'q2'],
                 ['q2', '1', 'q1'],
                 ['q1', '0', 'q1'],
                 ['q1', '1', 'q2']]

print('True') if af.verificaEquivalencia(af3) else print("False")


###########################################################################
#   Teste autômato mínimo com mesmo exemplo do ppt de minimização
###########################################################################
printHeader('Teste autômato mínimo com mesmo exemplo do ppt de minimização')
af2 = Automato()
af2.alfabeto = ['a', 'b']
af2.estados = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
af2.estadoInicial = 'q0'
af2.estadosFinais = ['q0', 'q4', 'q5']
af2.fPrograma = [['q0', 'a', 'q2'],
                 ['q0', 'b', 'q1'],
                 ['q1', 'a', 'q1'],
                 ['q1', 'b', 'q0'],
                 ['q2', 'a', 'q4'],
                 ['q2', 'b', 'q5'],
                 ['q3', 'a', 'q5'],
                 ['q3', 'b', 'q4'],
                 ['q4', 'a', 'q3'],
                 ['q4', 'b', 'q2'],
                 ['q5', 'a', 'q2'],
                 ['q5', 'b', 'q3']]
t = af2.aMin()
t.nome = 'ppt minimização'
t.printAutomato()


input('Tecle enter para sair . . . ')