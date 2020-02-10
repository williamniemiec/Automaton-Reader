# -*- coding: utf-8 -*-

#==========================================================================
#                           AUTOMATON - MAIN CLASS
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS
#--------------------------------------------------------------------------
import os
from src.Automaton import Automaton
from src.AutomatonFileManager import AutomatonFileManager
from src.AutomatonView import AutomatonView


#--------------------------------------------------------------------------
#    PROMPT CONFIGURATION
#--------------------------------------------------------------------------
os.system('mode con: cols=100 lines=200000')


#--------------------------------------------------------------------------
#    MAIN
#--------------------------------------------------------------------------
class Main:
    @staticmethod
    def run():
        exit_program = False
        init = False
        
        af = Automaton()
        
        while not exit_program:
            AutomatonView.printHeader("Choose an option")
            print("1: Open automaton")
            if init:
                print("2: Show automaton")
                print("3: Check accepted and rejected words")
                print("4: Generate grammar")
                print("5: Convert to minimal automaton")
                print("6: Verify equivalence with another automaton")
            print("0: Exit\n")
            
            AutomatonView.printDiv()
            op = input("Option: ")
            AutomatonView.printDiv()
            if op == '1':
                AutomatonView.printHeader('Open automaton')
                exit_option = False
                
                # Try to open automaton file
                filename = AutomatonFileManager.askFilePath("Open automaton file", "Automaton txt file")
                out = af.txtToAutomaton(filename)
                
                while out == None and exit_option == False:
                    print("Error: Invalid file path")
                    choose = input("Press 0 to exit or any button to try again: ")
                    
                    if choose == '0':
                        exit_option = True
                    else:
                        filename = AutomatonFileManager.askFilePath("Open automaton file", "Automaton txt file")
                        out = af.txtToAutomaton(filename)
                
                if not exit_option:
                    init = True
            elif init:
                if op == '2':
                    af.printAutomaton()
                    AutomatonView.wait()
                elif op == '3':
                    AutomatonView.printHeader('Check accepted and rejected words')
                    exit_option = False
                    filename = AutomatonFileManager.askFilePath("Open words file", "Words txt file")
                    
                    wordList = AutomatonFileManager.csvToWordList(filename)
        
                    while wordList == None and exit_option == False:
                        print("Error: Invalid file path")
                        choose = input("Press 0 to exit or any button to try again: ")
                        
                        if choose == '0':
                            exit_option = True
                        else:
                            filename = AutomatonFileManager.askFilePath("Open words file", "Words txt file")
                            wordList = AutomatonFileManager.csvToWordList(filename)
                    
                    af.checkWords(wordList)
                elif op == '4':
                    AutomatonView.printHeader('Generate grammar')
                    #name = AutomatonFile.askSaveFilePath("Save grammar file")
                    name = input("Enter a name  for the file (or '0' to exit): ")
                    if name:
                        af.generateGrammar(name)
                        AutomatonFileManager.printFileContent(name+'.txt')
                        AutomatonView.wait()
                elif op == '5':
                    print('Converting to minimal automaton...')
                    af = af.minAutomaton()
                    print('Conversion done successfully!')
                    AutomatonView.wait()
                elif op == '6':
                    AutomatonView.printHeader('Verify equivalence with another automaton')
                    af_tmp = Automaton()
                    exit_option = False
                    
                    filename = AutomatonFileManager.askFilePath("Choose the automaton file to be compared", "Automaton txt file")
                    out = af_tmp.txtToAutomaton(filename)
                    
                    while out == None and exit_option == False:
                        print("Error: Invalid file path")
                        choose = input("Press 0 to exit or any button to try again: ")
                        
                        if choose == '0':
                            exit_option = True
                        else:
                            filename = AutomatonFileManager.askFilePath("Choose the automaton file to be compared")
                            out = af_tmp.txtToAutomaton(filename)
        
                    if not exit_option:
                        out = af.checkEquivalence(af_tmp)
                        
                        if out == True:
                            print("The %s and %s automata are equivalent!" % (af.name, af_tmp.name))
                        else:
                            print("The %s and %s automata are not equivalent!" % (af.name, af_tmp.name))
                        af_tmp.destroy()
                        AutomatonView.wait()
            if op == '0':
                exit_program = True
        if init:
            af.destroy()



if __name__ == '__main__':
    Main.run()

