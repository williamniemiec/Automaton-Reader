import unittest
import sys

sys.path.insert(1, "../src/")

from Automaton import Automaton


class AutomatonTest(unittest.TestCase):
    def testTxtToAutomaton(self):
        automaton = Automaton()
        automaton.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertEqual('EQ1', automaton.name)
        self.assertListEqual(automaton.alphabet, ['0', '1'])
        self.assertListEqual(automaton.states, ['q0', 'q1', 'q2'])
        self.assertEqual(automaton.startState, "q0")
        self.assertListEqual(automaton.finalStates, ['q2'])
        self.assertListEqual(
            automaton.tFunction,   [['q0', '0', 'q0'], 
                                    ['q0', '1', 'q2'], 
                                    ['q2', '0', 'q2'], 
                                    ['q2', '1', 'q1'], 
                                    ['q1', '0', 'q1'], 
                                    ['q1', '1', 'q2']]
        )
    
    
    def testNfaToDfa(self):
        nfa = Automaton()
        nfa.txtToAutomaton("media/automata/nfa.txt")
        dfa = nfa.nfaToDfa()
        
        self.assertEqual('EQ1', dfa.name)
        self.assertListEqual(dfa.alphabet, ['0', '1'])
        self.assertListEqual(dfa.states, ['A', 'A_B', 'A_B_C'])
        self.assertEqual(dfa.startState, "A")
        self.assertListEqual(dfa.finalStates, ['A_B_C'])
        self.assertListEqual(
            dfa.tFunction,  [['A', '0', 'A_B'],
                             ['A', '1', 'A'],
                             ['A_B', '0', 'A_B_C'],
                             ['A_B', '1', 'A'],
                             ['A_B_C', '0', 'A_B_C'],
                             ['A_B_C', '1', 'A']]
        )
        
    def testConvertDFAToTtf(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/noTotal.txt")
        a.convertDFAToTtf()
        
        self.assertEqual('A', a.name)
        self.assertListEqual(a.alphabet, ['a', 'b'])
        self.assertListEqual(a.states, ['q0', 'q1', 'q2', 'qf', '&&'])
        self.assertEqual(a.startState, "q0")
        self.assertListEqual(a.finalStates, ['qf'])
        self.assertListEqual(
            a.tFunction,    [['q0', 'a', 'q1'],
                             ['q0', 'b', 'q0'],
                             ['q1', 'a', 'q2'],
                             ['q1', 'b', '&&'],
                             ['q2', 'a', 'qf'],
                             ['q2', 'b', '&&'],
                             ['qf', 'a', '&&'],
                             ['qf', 'b', '&&'],
                             ['&&', 'a', '&&'],
                             ['&&', 'b', '&&']]
        )
        
    def testReachableStatesDirectly(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertListEqual(['q0', 'q2'], a.reachableStatesDirectly("q0"))
        
    def testReachableStates(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertListEqual(['q0', 'q1', 'q2'], a.reachableStates("q0"))
        
    def testRemoveUnreachableStates(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/uselessState.txt")
        a.removeUnreachableStates()
        
        self.assertEqual('EQ1', a.name)
        self.assertListEqual(a.alphabet, ['0', '1'])
        self.assertListEqual(a.states, ['q0', 'q1', 'q2'])
        self.assertEqual(a.startState, "q0")
        self.assertListEqual(a.finalStates, ['q2'])
        self.assertListEqual(
            a.tFunction,   [['q0', '0', 'q0'], 
                            ['q0', '1', 'q2'], 
                            ['q2', '0', 'q2'], 
                            ['q2', '1', 'q1'], 
                            ['q1', '0', 'q1'], 
                            ['q1', '1', 'q2']]
        )
        
    def testTransitionFunction(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertEqual(["q2"], a.transitionFunction("q0", '1'))
        
    def testReachableSymbols(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertEqual(['0', '1'], a.reachableSymbols("q0"))
    
    def testIsFinal_final(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertTrue(a.isFinal("q2"))
        
    def testIsFinal_noFinal(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        
        self.assertFalse(a.isFinal("q0"))
    
    def testCheckWords(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/eq1.txt")
        wordlist = [
            ["0", "1", "0", "0"],
            ["0"],
            ["0", "1", "0", "1"]
        ]
        
        self.assertDictEqual(
            {'accepted': [['0', '1', '0', '0']], 'rejected': [['0'], ['0', '1', '0', '1']]},
            a.checkWords(wordlist)
        )
        
    def testMinAutomaton(self):
        a = Automaton()
        a.txtToAutomaton("media/automata/minimal/dfa.txt")
        a = a.minAutomaton()
        
        self.assertEqual('EQ1', a.name)
        self.assertListEqual(a.alphabet, ['a', 'b'])
        self.assertListEqual(a.states, ['q0', 'q1', 'q2_q3', 'q4_q5'])
        self.assertEqual(a.startState, "q0")
        self.assertListEqual(a.finalStates, ['q0', 'q4_q5'])
        self.assertListEqual(
            a.tFunction,    [['q0', 'a', 'q2_q3'],
                             ['q0', 'b', 'q1'],
                             ['q1', 'a', 'q1'],
                             ['q1', 'b', 'q0'],
                             ['q2_q3', 'a', 'q4_q5'],
                             ['q2_q3', 'b', 'q4_q5'],
                             ['q4_q5', 'a', 'q2_q3'],
                             ['q4_q5', 'b', 'q2_q3']]
        )
    
    def testCheckEquivalence_equal(self):
        a1 = Automaton()
        a1.txtToAutomaton("media/automata/eq1.txt")
        
        a2 = Automaton()
        a2.txtToAutomaton("media/automata/eq2.txt")
        
        self.assertTrue(a1.checkEquivalence(a2))
    
    def testCheckEquivalence_noEqual(self):
        a1 = Automaton()
        a1.txtToAutomaton("media/automata/eq1.txt")
        
        a2 = Automaton()
        a2.txtToAutomaton("media/automata/nfa.txt")
        
        self.assertFalse(a1.checkEquivalence(a2))    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()