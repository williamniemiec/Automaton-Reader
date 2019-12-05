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
#af.txtToAutomato('midia/ex_pptMin_min.txt')
af.txtToAutomato('midia/Robo_Catador_AFN.txt')
#af.txtToAutomato('midia/afn.txt')
af.printAutomato()
#af = af.aMin()
af = af.aMin()
#af = af.automatoMinimo()
#af = af.afnToAfd()
#af.fPrograma.sort()

#af.removeEstadosInalcancaveis()
#af.convertAfdToFpt()
#af = af.automatoMinimo() 
#af = af.automatoMinimo() 

af.printAutomato()

input('..')

# In[ ]:




