class AutomatonListHelper:
    '''
    ' Removes repeated elements from a list
    '
    ' @param list array List that will be iterate
    ' 
    ' @return list
    '''
    @staticmethod
    def removeDuplicates(array): 
        final_list = [] 
        for num in array: 
            if num not in final_list: 
                final_list.append(num) 
        return final_list 
    
    
    '''
    ' Returns list of largest size without elements that have already been visited 
    ' (if all lists have elements visited, returns None)
    ' If all lists are of size 1, return None and update stack of states to be processed
    '
    ' @param list array List to be iterate
    ' @param dictionary visited Elements to be ignored
    ' @param list stackProcess Stack that will be filled if all lists are of size 1
    '
    ' @return list | None
    '''
    @staticmethod
    def largerSizeList_NotVisited(array, visited, stackProcess):
        if not array:
            return None
        
        highestIndex = 0
        highestLength = 0
        
        for i in range(len(array)):
            equals = False
            s = ''
            
            if len(array[i]) > highestLength:
                for item in array[i]:
                    s += item
                if visited.get(s) != None:
                    equals = True
                    
                if not equals:
                    highestIndex = i
                    highestLength = len(array[i])
            
            elif len(array[i]) == highestLength:
                s = ''
                for item in array[i]:
                    s += item
                    
                if visited.get(s) != None:
                    equals = True
                if not equals:
                    highestIndex = i
                    highestLength = len(array[i])
    
        if highestLength == 1:
            for item in array:
                if item:
                    item = item[0]
                    
                    # If the element is not in the stack and has not been processed, put it in
                    if stackProcess.count(item) == 0 and visited.get(item) == None: 
                        stackProcess.append(item)
            return None
        elif highestLength == 0:
            return None
        else:
            return array[highestIndex]