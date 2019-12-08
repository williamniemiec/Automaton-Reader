#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("src/")
from Automato import *


# In[ ]:


# ARRUMAR AFN


# In[ ]:


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
#    MAIN
#--------------------------------------------------------------------------
af = Automato()
#aEq1 = Automato()
#aEq2 = Automato()
af.txtToAutomato('midia/ex_pptMin.txt')
#af.txtToAutomato('midia/Robo_Catador_AFN.txt')
#aEq1.txtToAutomato('midia/ex_pptMin_1.txt')
#aEq2.txtToAutomato('midia/ex_pptMin_2.txt')
#af.txtToAutomato('midia/afn_ppt_ext.txt')
#af.txtToAutomato('midia/min_simples.txt')
#aEq1.printAutomato()
#aEq2.printAutomato()
#af = af.aMin()
#af = af.aMin()
#af = af.automatoMinimo()
af = af.afnToAfd()
#af.fPrograma.sort()

#af.removeEstadosInalcancaveis()
#af.convertAfdToFpt()
#af = af.automatoMinimo() 
#af = af.automatoMinimo() 
#print(aEq1.verificaEquivalencia2(aEq2))
af.printAutomato()
print('fim')


#input('..')

# In[ ]:




