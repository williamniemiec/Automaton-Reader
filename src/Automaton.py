# -*- coding: utf-8 -*-

#==========================================================================
#                         AUTOMATON - AUTOMATON CLASS
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS
#--------------------------------------------------------------------------
import pprint
import re

from src.AutomatonView import AutomatonView
from src.AutomatonListHelper import AutomatonListHelper


#--------------------------------------------------------------------------
#    AUTOMATON OBJECT
#--------------------------------------------------------------------------
class Automaton:
    def __init__(self):
        self.name = ''
        self.alphabet = []
        self.states = []
        self.startState = ''
        self.finalStates = []
        
        '''
        ' Transition function
        '
        ' matrix with columns being state, symbol and next state
        '''
        self.tFunction = [] 
    
    
    '''
    ' Convert a txt file to automaton format
    ' 
    ' @param string filename Automaton file name
    '
    ' @return boolean | None
    '''
    def txtToAutomaton(self, filename):
        erro = False

        # Try to open the file. If it can't, return none
        try:
            file = open(filename, 'r')
        except IOError:
            erro = True

        if erro:
            return None

        content = file.readlines()
        file.close()

        # Make the matrix that will be responsible for the transition function
        i = len(content) - 2
        self.tFunction = [[0 for x in range(3)] for y in range(i)]
        
        # Get automaton definition
        tmp = re.split("=", content[0])
        self.name = tmp[0]      #Take automaton name
        defAutomato = re.findall('({[A-Za-z0-9,]+})',tmp[1])

        # Get states, alphabet and final states of the automaton
        self.states = re.findall('[A-Za-z0-9]+', defAutomato[0]) 
        self.alphabet = re.findall('[A-Za-z0-9]+', defAutomato[1])
        self.finalStates = re.findall('[A-Za-z0-9]+', defAutomato[2])

        # Get final state of the automaton
        tmp2 = re.findall('(},[A-Za-z0-9]+,{)',tmp[1])
        self.startState = re.findall('([A-Za-z0-9]+)',tmp2[0])
        self.startState = self.startState[0]

        # Get transition function of the automaton
        i = 0
        for c in range(2, len(content)): # Starts in 2 because the first line is 'prog'
            tmp = re.split('=', content[c])
            tmp2 = re.findall('([A-Za-z0-9]{1,})', tmp[0]) # Get (q,s)

            self.tFunction[i][0] = tmp2[0]          # Get read state
            self.tFunction[i][1] = tmp2[1]          # Get read symbol
            
            # Get next state (removing '\n')
            tmp2 = re.findall('[^\\n]+', tmp[1])    
            self.tFunction[i][2] = tmp2[0]

            i += 1
        return True


    '''
    ' Show automaton data
    '''
    def printAutomaton(self):
        AutomatonView.printHeader('Automaton %s' % self.name)
        print('Alphabet: ', self.alphabet)
        print('States: ', self.states)
        print('Start state: ', self.startState)
        print('Final states: ', self.finalStates)
        print('Transition function:')
        pprint.pprint(self.tFunction)
        AutomatonView.printDiv()
    

    '''
    ' Converts an NFA in DFA
    '
    ' @return Automaton
    '''
    def nfaToDfa(self):
        dfa = Automaton()
        dfa.name = self.name
        dfa.alphabet = self.alphabet
        dfa.startState = self.startState
        dfa.tFunction = [['', '', '']]
        changed = False
        
        currentStates = [dfa.startState]    # Stores states that are being analyzed
        index = 0                           # Current tFunction index
        visited = {}
        unifiedStates = {}
        statesQueue = []                    # Queue of states to be processed
        length = len(dfa.alphabet) + 1
        height = 1
        nfaTable = [[[] for x in range(length)] for y in range(height)]
        
        ## Creation of NFA table
        i = 0
        
        # Runs as long as there are states to be processed
        while (currentStates or statesQueue):
            aux = []                        # Auxiliary variable
            
            if currentStates == None:       # If currentStates is empty, puts a state to be processed in it
                if not statesQueue:         # If there are not states to be processed, ends
                    break
                    
                currentStates = []
                currentStates.append(statesQueue.pop(0))
            
            nfaTable[i][0].extend(currentStates)

            j = 1               # j starts in 1 because in 0 are the actual states
            for symbol in dfa.alphabet:
                s = ''
                aux2 = []
                for state in currentStates:
                    s += state  # Unifies states
                    fP = self.transitionFunction(state, symbol)

                    if fP[0] == '&':
                        continue

                    nfaTable[i][j].extend(fP)
                    aux2.extend(fP)
                
                nfaTable[i][j] = AutomatonListHelper.removeDuplicates(nfaTable[i][j])
                aux2 = AutomatonListHelper.removeDuplicates(aux2)
                
                j += 1
                visited[s] = True     # Mark unified state as visited
                aux.append(aux2)
            
            # Prepares the next iteration
            i += 1
            nfaTable.append([[] for x in range(length)])
            currentStates = AutomatonListHelper.largerSizeList_NotVisited(aux, visited, statesQueue) 
            # If all fields in aux have the same size, it will return a queue of these states in 'statesQueue'

        nfaTable.pop()     # Removes final row because it will be empty
        
        '''    --{ DEBUG }--
        # Show NFA table
        print('\t', dfa.alphabet)
        for k in nfaTable:
            for e in k:
                print(e, ",\t", end='')
            print("\n")
        '''  
        
        ## NFA generation
        # Iterate over the NFA table
        k = 0
        for i in range(len(nfaTable)):
            state = ''
            final = False
            
            # Unify states in currentStates
            nfaTable[i][0].sort()
            for s in nfaTable[i][0]:
                state += s + '_'

                # If the state is final, the unified state must also be final
                if self.isFinal(s):
                    final = True
            
            state = state[:-1:] # Removes '_' of the end
            
            # Updates transition function
            for j in range(1, len(dfa.alphabet)+1):
                nfaTable[i][j].sort()

                if nfaTable[i][j]:     # Checks if the cell of the NFA table is not empty
                    dfa.tFunction[k][0] = state
                    dfa.tFunction[k][1] = dfa.alphabet[j-1]
                    
                    # Join a cell list into a single string
                    for s in nfaTable[i][j]:
                        dfa.tFunction[k][2] += s + '_'
                    
                    dfa.tFunction[k][2] = dfa.tFunction[k][2][:-1:] # Removes '_' of the end
                    k += 1
                    dfa.tFunction.append(['', '', ''])
            
            # Update states
            dfa.states.append(state)
            
            # Updates final states (if necessary)
            if final:
                dfa.finalStates.append(state)
        
        # Take out the last tFunction row (it is empty)
        dfa.tFunction.pop()
        dfa.states.sort()
        dfa.finalStates.sort()
        
        return dfa           
    
    
    '''
    ' Converts a DFA in a DFA with total transition function (ttf) (all transitions defined)
    '''
    def convertDFAToTtf(self):
        d = '&&'    # Artificial state
        noTotal = False
        i = 0
        tFunctionAux = []
        
        # Transforms transition function into total transition function
        for state in self.states:
            for symbol in self.alphabet:
                fp = self.transitionFunction(state, symbol)

                # If it founds an indefiniteness, put a transition to 'd'
                if fp[0] == '&':
                    noTotal = True
                    self.tFunction.insert(i, [state, symbol, d])
                i += 1
    
        self.tFunction.sort()
        
        # If DFA did not have total transition function, put 'd' in DFA states 
        if noTotal:
            self.states.append(d)
            for symbol in self.alphabet:
                self.tFunction.append([d, symbol, d])
        
    
    '''
    ' Returns a list of states that are directly reachable from one (if there are not states, returns none)
    '
    ' @param string state Origin state 
    '
    ' @return list
    '''
    def reachableStatesDirectly(self, state):
        reachableStates = []
        
        for i in range(len(self.tFunction)):
            if self.tFunction[i][0] == state:
                reachableStates.append(self.tFunction[i][2])
                
        if not reachableStates:
            reachableStates = None
        else:
            reachableStates = AutomatonListHelper.removeDuplicates(reachableStates)
            
        return reachableStates
    
    
    '''
    ' Returns a list of states that are reachable from one (if there are not states, returns none)
    '
    ' @param string state Origin state 
    '
    ' @return list
    '''
    def reachableStates(self, state):
        rStates = []
        stack = []
        visited = {}
        stack.append(state)
        
        # Runs as long as are states to be visited
        while stack:
            s = stack.pop()
            
            # Search in the transition function states that can be reached from the given state 
            for i in range(len(self.tFunction)):
                if self.tFunction[i][0] == s and visited.get(s) == None:
                    rStates.append(self.tFunction[i][2])
                    stack.append(self.tFunction[i][2])  # Put in the stack to analyze all reachable states
            visited[s] = True
                
        if not rStates:
            rStates = None
        else:
            rStates = AutomatonListHelper.removeDuplicates(rStates)
            rStates.sort()
            
        return rStates
        
    
    '''
    ' Removes all unreachable states from the automaton
    '''
    def removeUnreachableStates(self):
        reachableStates = self.reachableStates(self.startState)
        reachableStates.append(self.startState)
        
        i = 0

        # Iterate over the transition function
        while i < len(self.tFunction):
            # If the i-th state is not reachable starting from start state, removes it
            # and all its occurrences of the transition function
            if reachableStates.count(self.tFunction[i][0]) == 0:
                self.tFunction.pop(i)
                i -= 1
            
            if reachableStates.count(self.tFunction[i][2]) == 0:
                self.tFunction.pop(i)
                i -= 1
            i += 1
        
        # Removes unreachable states from automaton states
        i = 0
        while i < len(self.states):
            if reachableStates.count(self.states[i]) == 0:
                self.states.pop(i)
                i -= 1
            i += 1


    '''
    ' Transition function of the automaton
    '
    ' @param string state Read state
    ' @param string symbol Read symbol
    '
    ' @return list
    '''
    def transitionFunction(self, state, symbol):
        i = 0
        found = False
        response = []
        
        # Search for a transition given state read and symbol read
        while (not found) and (i < len(self.tFunction)):
            if (self.tFunction[i][0] == state) and (self.tFunction[i][1] == symbol):
                found = True
                
                while i < len(self.tFunction):
                    # If the transition exists
                    if (self.tFunction[i][0] == state) and (self.tFunction[i][1] == symbol):
                        response.append(self.tFunction[i][2])       # Get all transition states
                    i += 1 
            i += 1
        
        if not found: # if not found, returns 'empty word'
            response.append('&')
        
        return response

    '''
    ' Returns all directly reachable symbols from the given state
    '
    ' @param string state Origin state
    '
    ' @return list
    '''
    def reachableSymbols(self, state):
        i = 0
        found = False
        response = []
        
        # Search reachable symbols from the given state
        while i < len(self.tFunction):
            if (self.tFunction[i][0] == state) and (response.count(self.tFunction[i][1]) == 0):
                found = True
                response.append(self.tFunction[i][1])
            i += 1
        
        if not found: 
            return None
        
        return response
    
    '''
    ' Checks if a state is final
    '
    ' @param string state Read state
    '
    ' @return boolean
    '''
    def isFinal(self, state):
        i = 0
        
        while i < len(self.finalStates):
            if self.finalStates[i] == state:
                return True
            i += 1
        return False
    
    '''
    ' Given a word list, returns a dictionary with accepted and rejected words
    '
    ' @param list wordList List of words
    '
    ' @return dictionary
    '''
    def checkWords(self, wordList):
        i = 1
        response = {'accepted':[], 'rejected':[]}

        # Iterate over all words in the list
        for word in wordList:
            accept = False
            i = 1
            currentState = []    # Stores the state that is being analyzed
            currentState.append(self.startState) 

            # Iterate over all word characters
            for symbol in word:
                # Iterate over all states that are currently being analyzed
                # "Walk the transitional graph in each actual state"
                for s in currentState:
                    tmp = self.transitionFunction(s, symbol)    # Transitional function of the current state
                    
                    # If next state exists, put in the current states list
                    if tmp[0] != '&':       
                        currentState.extend(tmp) 
                        currentState.pop(0)     # Removes state that has just been analyzed
                currentState = AutomatonListHelper.removeDuplicates(currentState) # Remove possible duplicate statess from the states to be analyzed
                
                
                # Iterate over all states that are currently being analyzed and checks if any are final
                for state in currentState:
                    # If it is the final state and the last letter of the word, accept
                    if self.isFinal(state) and i == len(word): 
                        response['accepted'].append(word)
                        accept = True
                i += 1      
            
            # If the word is not accept, put it on the rejected list
            if accept == False:
                response['rejected'].append(word)
        
        # Show accepted and rejected words       
        AutomatonView.printHeader('Acepted words')
        pprint.pprint(response['accepted'])
        AutomatonView.printDiv()
        AutomatonView.printHeader('Rejected words')
        pprint.pprint(response['rejected'])
        AutomatonView.printDiv()
        
        return response
    
    
    '''
    ' Generates a grammar of the automaton (must be DFA)
    '
    ' @param string outputFilename Name of the output file
    '''
    def generateGrammar(self, outputFilename):
        '''
        ' Production function
        '
        ' Contains variable and next symbol
        '''
        pFunction = [[]]

        # Generate output file
        fileOutput = open(outputFilename+'.txt', 'w')
        
        # Check if there is a start state
        if self.startState != '':
            length = len(self.tFunction) + len(self.finalStates) + 1
            pFunction = [[0 for x in range(2)] for y in range(length)]  # pFunction[length][2]
            
            # Put in pFunction the transition: S -> start symbol
            pFunction[0][0] = 'S'
            pFunction[0][1] = self.startState
            
            # For every final state, generate the production of this state for the empty word
            for i in range(0, len(self.finalStates)):
                pFunction[i+1][0] = self.finalStates[i]
                pFunction[i+1][1] = '&'
            
            i += 2
            # Iterates over the transition function and convert it to a production function
            for j in range(len(self.tFunction)):
                pFunction[i][0] = self.tFunction[j][0]
                pFunction[i][1] = '"' + self.tFunction[j][1] + '"' + self.tFunction[j][2]
                i += 1
            
            # Put the grammar definition in the output file
            print("G=({", end='', file=fileOutput)
            
            # Put the states in this definition
            for i in range(len(self.states)):
                print(self.states[i], end='', file=fileOutput)
                
                if(i+1 < (len(self.states))):
                    print(",", end='', file=fileOutput)
            
            print("},{", end='', file=fileOutput)
            
            # Put the alphabet in this definition
            for i in range(len(self.alphabet)):
                print('"'+self.alphabet[i]+'"', end='', file=fileOutput)
                
                if(i+1 < len(self.alphabet)):
                    print(", ", end='', file=fileOutput)
            
            print("},S,P)", file=fileOutput)
            print("P", file=fileOutput)
            
            # Put production function in the output file
            for k in range(len(pFunction)):
                fileOutput.write("%s -> %s\n" % (pFunction[k][0], pFunction[k][1]))

        fileOutput.close()
        print("Successfully generated grammar!")
    
    
    '''
    ' Generates minimal automaton, ensuring that it meets the requirements of the algorithm
    '
    ' @return Automaton
    '''
    def minAutomaton(self):
        self = self.nfaToDfa()              # Convert it to DFA
        
        self.printAutomaton()
        print("\n\n")
        
        self.removeUnreachableStates()      # Remove its unreachable states
        self.convertDFAToTtf()              # Convert its transitional function to total transitional function
        
        return self._MinimalAutomaton()       # Convert it to a minimal automaton
    
    
    '''
    ' Generates minimal automaton
    '
    ' @return Automaton
    '''
    def _MinimalAutomaton(self):
        dfa = Automaton()
        stack = []
        firstTime = True
        d = '&&'
        
        dfa.name = self.name
        dfa.states = self.states
        dfa.startState = self.startState
        dfa.tFunction = self.tFunction
        dfa.alphabet = self.alphabet
        dfa.finalStates = self.finalStates
        
        ## Generates the distinction table
        width = len(self.states)
        height = width
        distinctionTable = [['-' for x in range(width)] for y in range(height)] # +1 to be inclusive in the range
        
        dependenciesList = {}
        
        # Fill the column 0 of the matrix with the states
        for l in range(height-1):
            distinctionTable[l][0] = self.states[l+1]
        l += 1  # Stores the last row index of the matrix

        # Fill this last row with the states
        for a in range(1, width):
            distinctionTable[l][a] = self.states[a-1]
        
        ## Marks the pairs of final and non-final states with true and the rest with false
        for i in range(0, l):
            for j in range(1, i+2): # j goes from 1 to i+1
                if (self.isFinal(distinctionTable[i][0])) and (not self.isFinal(distinctionTable[l][j])):
                    distinctionTable[i][j] = True
                elif (self.isFinal(distinctionTable[l][j])) and (not self.isFinal(distinctionTable[i][0])):
                    distinctionTable[i][j] = True
                else:
                    distinctionTable[i][j] = False
        
        ## Check unmarked pairs in the previous step
        for i in range(0, l):
            for j in range(1, i+2):
                if distinctionTable[i][j] == False:
                    p = distinctionTable[i][0]
                    q = distinctionTable[l][j]
                    
                    # For each symbol s of the alphabet, test its transition function
                    for letter in self.alphabet:
                        pR = self.transitionFunction(p, letter) # pResultant
                        qR = self.transitionFunction(q, letter) # qResultant
                        pR = pR[0]
                        qR = qR[0]
                        
                        if pR == qR:
                            continue
                        
                        # Search pR index
                        ipR = 0
                        achou = False
                        
                        while not achou and ipR < l:
                            if distinctionTable[ipR][0] == pR:
                                achou = True
                            else:
                                ipR += 1
                        if not achou:
                            continue
                        
                        # Search qR index
                        iqR = 1
                        achou = False
                        k = 0
                        while not achou and iqR < width:
                            if distinctionTable[l][iqR] == qR:
                                achou = True
                            else:
                                iqR += 1
                        if not achou:
                            continue

                        # If ipR or iqR 
                        # If ipR or iqR exceeds the limits of the table, invert them
                        if distinctionTable[ipR][iqR] == '-':
                            tmp = ipR
                            ipR = iqR - 2
                            iqR = tmp + 2
                            
                            tmp = pR
                            pR = qR
                            qR = tmp
                        
                        # If r and s are not marked, create a dependency list with p and q headed by r and s 
                        if distinctionTable[ipR][iqR] == False: 
                            dependenciesList[pR+','+qR] = []
                            dependenciesList[pR+','+qR].append([p,q,i,j])   # Stores p, q and the index where p and q are
                        else:
                            distinctionTable[i][j] = True
                            
                            # Checks if p,q have a dependency list, mark all states on that list and
                            # checks if each checked state has a dependency list (if yes, check all)
                            # and so recursively
                            # stack: Stores states that have been marked to see if they have a dependency list
                            firstTime = True
                            while stack or firstTime:
                                firstTime = False
                                    
                                if stack:
                                    elem = stack.pop()
                                    p1 = elem[0]
                                    q1 = elem[1]
                                else:
                                    p1 = p
                                    q1 = q
                            
                                if (dependenciesList.get(p+','+q) != None) or (dependenciesList.get(q+','+p) != None):
                                    # If p, q have a dependency list, mark all states on that list
                                    # and store marked states in the stack to see if they have a dependency list as well
                                    if dependenciesList.get(p1+','+q1) != None:
                                        for listaEstados in dependenciesList[p1+','+q1]:
                                            distinctionTable[listaEstados[2]][listaEstados[3]] = True
                                            stack.append([listaEstados[0], listaEstados[1]]) # Stores marked state

                                            dependenciesList[p1+','+q1] = None

                                    if dependenciesList.get(q1+','+p1) != None:
                                        for listaEstados in dependenciesList[q1+','+p1]:
                                            distinctionTable[listaEstados[2]][listaEstados[3]] = True
                                            stack.append([listaEstados[0], listaEstados[1]])

                                        dependenciesList[q1+','+p1] = None     

        ## Iterates over all unmarked states and unifies them
        for i in range(0, l):
            for j in range(1, i+2):
                if distinctionTable[i][j] == False:
                    if distinctionTable[i][0] == '&&' or distinctionTable[l][j] == '&&':
                        continue
                    # Concatenates two states q1 and q2 and forms a new state 'q1_q2'
                    if distinctionTable[i][0] < distinctionTable[l][j]:
                        unifiedState = distinctionTable[i][0] +'_'+ distinctionTable[l][j]
                    else:
                        unifiedState = distinctionTable[l][j] +'_'+ distinctionTable[i][0]

                    k = 0
                    # Replaces all transitions that generate q1 or q2 with q1_q2
                    while k < len(dfa.tFunction):
                        # Updates transition function
                        if dfa.tFunction[k][0] == distinctionTable[i][0]:
                            dfa.tFunction[k][0] = unifiedState
                        
                        # If there was a transition to that state, it changes to go to the unified state
                        if dfa.tFunction[k][2] == distinctionTable[i][0]:
                            dfa.tFunction[k][2] = unifiedState
                                               
                        # Excludes the other state (since it has been unified)
                        if dfa.tFunction[k][0] == distinctionTable[l][j]:
                            dfa.tFunction[k][0] = unifiedState
                        
                        # If there was a transition to that state, it changes to go to the unified state
                        if dfa.tFunction[k][2] == distinctionTable[l][j]:
                            dfa.tFunction[k][2] = unifiedState

                        if dfa.tFunction[k][2] == '&&':
                            dfa.tFunction.pop(k)
                            k -= 1
                        
                        k += 1
                    
                    k = 0
                    # Updates states with the unified state
                    while k < len(dfa.states):
                        if dfa.states[k] == distinctionTable[i][0] or dfa.states[k] == distinctionTable[l][j]:
                            dfa.states[k] = unifiedState 
                        k += 1
                    
                    k = 0
                    # Updates final states with the unified state (if necessary)
                    while k < len(dfa.finalStates):
                        if dfa.finalStates[k] == distinctionTable[i][0] or dfa.finalStates[k] == distinctionTable[l][j]:
                            dfa.finalStates[k] = unifiedState
                            
                        k += 1
                    
                    # Updates start state with unified state (if necessary)
                    if dfa.startState == distinctionTable[i][0]:
                        dfa.startState = unifiedState
                    
                    if dfa.startState == distinctionTable[l][j]:
                        dfa.startState = unifiedState
        
        
        ## Exclusion of useless states
        visited = {}
        stack = []

        # Marks all states as not visited
        for state in dfa.states:
            visited[state] = False
        
        stack.append(dfa.startState)
        
        # Runs as long as there are states to be analyzed
        while stack:
            est = stack.pop()
            visited[est] = True
            est_fp = dfa.reachableStatesDirectly(est)
            
            # If there are no reachable states from the current state
            if est_fp == None:
                if not dfa.isFinal(est):    # If current state is not final, found state useless
                    i = 0
                    # Eliminates this state of the transition function
                    while i < len(dfa.tFunction):
                        if dfa.tFunction[i][0] == est or dfa.tFunction[i][2] == est:
                            dfa.tFunction.pop(i)
                            i -= 1
                        i += 1

                    i = 0
                    # Eliminates this state from the states of the automaton
                    while i < len(dfa.states):
                        if dfa.states[i] == est:
                            dfa.states.pop(i)
                            i -= 1
                        i += 1
            else:   # If there are reachable states from the current state
                # If reached state does not reach a final state, eliminate it
                if len(est_fp) == 1 and est_fp[0] == est and not dfa.isFinal(est):
                    i = 0
                    # Eliminates this state of the transition function
                    while i < len(dfa.tFunction):
                        if dfa.tFunction[i][0] == est or dfa.tFunction[i][2] == est:
                            dfa.tFunction.pop(i)
                            i -= 1
                        i += 1
                        
                    i = 0
                    # Eliminates this state from the states of the automaton
                    while i < len(dfa.states):
                        if dfa.states[i] == est:
                            dfa.states.pop(i)
                            i -= 1
                        i += 1
                else:   # If reached state reaches a final state, check other unvisited states
                    for state in est_fp:
                        if visited.get(state) == None:
                            stack.append(state)

        
        # Eliminate state d from automaton (if it have it)
        try:
            indice = dfa.states.index('&&')
            dfa.states.pop(indice)
        except:
            pass

        # Eliminates transitions to states that have been eliminated from the automation states
        i = 0
        tam = len(dfa.tFunction)
        while i < tam:
            if dfa.states.count(dfa.tFunction[i][0]) == 0 or dfa.states.count(dfa.tFunction[i][2]) == 0:
                dfa.tFunction.pop(i)
                tam -= 1
                i -= 1
            i += 1
            
        
        '''    --{ DEBUG }--
        # Print distinction table
        for k in distinctionTable:
            for e in k:
                print(e, ",\t", end='')
            print("\n")
        for m in dfa.tFunction:
            print(m)
        '''
        dfa.states = AutomatonListHelper.removeDuplicates(dfa.states)
        dfa.tFunction = AutomatonListHelper.removeDuplicates(dfa.tFunction)
        
        dfa.finalStates = AutomatonListHelper.removeDuplicates(dfa.finalStates)
        dfa.tFunction.sort()
        dfa.finalStates.sort()
        
        return dfa
    
    '''
    ' Given another DFA, checks if this automaton is equal to the given automaton
    '
    ' @param Automaton m2 Automaton to be checked equality
    '
    ' @return boolean
    '''
    def checkEquivalence(self, m2):        
        stack_states1 = []
        stack_states2 = []
        visited1 = {}
        visited2 = {}

        minM1 = self.minAutomaton()
        minM2 = m2.minAutomaton()

        stack_states1.insert(0, minM1.startState)
        stack_states2.insert(0, minM2.startState)

        # Runs as long as there are states to be processed in M1 and M2
        while stack_states1 and stack_states2:
            queue_next_states1 = []
            queue_next_states2 = []
            list_simb1 = []
            list_simb2 = []
            totFinal1 = 0
            totFinal2 = 0

            # Take symbols reachable by M1
            for state in stack_states1:
                tmp = minM1.reachableSymbols(state)
                if tmp != None:
                    list_simb1.extend(tmp)
                visited1[state] = True
                
                if minM1.isFinal(state):
                    totFinal1 += 1

            # Take symbols reachable by M1
            for state in stack_states2:
                tmp = minM2.reachableSymbols(state)

                if tmp != None:
                    list_simb2.extend(tmp)
                visited2[state] = True

                if minM2.isFinal(state):
                    totFinal2 += 1

            # If the list of symbols reached by M1 is different from M2 or
            # if there are final states reached by the current states that are
            # in one automaton and not in another, rejects
            if (set(list_simb1) != set(list_simb2)) or (totFinal1 != totFinal2):
                return False

            # Prepares the next iteration
            # Get all states reached by the states that are in the M1 queue
            for state in stack_states1:
                queue_next_states1.extend(minM1.reachableStatesDirectly(state))

            # Get all states reached by the states that are in the M2 queue
            for state in stack_states2:
                queue_next_states2.extend(minM2.reachableStatesDirectly(state))

            # Eliminates states that have already been visited by M1
            i = 0
            length = len(queue_next_states1)

            while i < length:
                if visited1.get(queue_next_states1[i]) != None:
                    queue_next_states1.pop(i)
                    length -= 1
                    i -= 1
                i += 1

            # Eliminates states that have already been visited by M2
            i = 0
            length = len(queue_next_states2)

            while i < length:
                if visited2.get(queue_next_states2[i]) != None:
                    queue_next_states2.pop(i)
                    length -= 1
                    i -= 1 # Decreases i because it will be incremented shortly thereafter, and since an item has been removed, prevents it from skipping items
                i += 1

            # Place the next unvisited states in the queue of states to be processed
            stack_states1 = queue_next_states1
            stack_states2 = queue_next_states2

        # If in the end there are unprocessed states in M1 or M2, it is because they are not the same
        if stack_states1 or stack_states2:
            return False

        return True

    '''
    ' Remove automaton and deallocate occupied memory
    '
    ' @return None
    '''
    def destroy(self):
        del self
        return None
