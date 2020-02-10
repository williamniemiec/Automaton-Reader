import os
import pprint
import re
from tkinter import filedialog

from src.AutomatonView import AutomatonView
import tkinter as tk


class AutomatonFileManager:
    '''
    ' Open window to user choose a file
    '
    ' @param string windowTitle Title of the window
    ' @param string typeName Title of the file type (always is for the extension '.txt')
    '
    ' @return string
    '''
    @staticmethod
    def askFilePath(windowTitle, typeName):
        root = tk.Tk()
        
        path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title=windowTitle,
            filetypes=((typeName, "*.txt"), )
        )
        root.destroy()
        
        return path
    
    
    @staticmethod
    def askSaveFilePath(windowTitle):
        root = tk.Tk()
        
        path = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title=windowTitle
        )
        
        root.destroy()
        
        return path
    
    
    '''
    ' Convert a csv file into a word list
    '
    ' @param string filename File path of a csv file
    '
    ' @return list | None
    '''
    @staticmethod
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
        
        # Reads each line of the file and puts it in a list of words
        for line in content:
            tmp = []
            
            # Reads line without quotation marks and line breaks
            tmp.extend(re.findall('[A-Za-z]+[^"\'\n\s,]*', line))
            if tmp:
                wordList.append(tmp)
        
        return wordList
    
    
    '''
    ' Show the content of a txt file
    '
    ' @param string filename File path of a txt file
    '''
    @staticmethod
    def printFileContent(filename):
        file = open(filename, 'r')
        content = file.readlines()
        file.close()
        AutomatonView.printHeader('File content %s' % filename)
        pprint.pprint(content)