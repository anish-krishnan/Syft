def getForgotten(speech, text):
    speechList = speech.split(" ")
    textList = text.split(" ")
    
    forgotList = []
    
    for elem in textList:
        
        if(elem not in speechList):
            print("uh oh")
            forgotList.append(elem.upper())
        else:
            forgotList.append(elem)
            
            
    return " ".join(forgotList);
            
def getExtra(speech, text):
    speechList = speech.split(" ")
    textList = text.split(" ")
    
    extraList = []
    
    for elem in speechList:
        
        if(elem not in textList):
            print("uh oh")
            extraList.append(elem.upper())
        else:
            extraList.append(elem)
            
            
    return " ".join(extraList);
    
def countUmLike(text):
    textList = text.split(" ");
    count = 0
    
    for elem in textList:
        if(elem == "um" or elem == "like"):
            count += 1
            
    return count
    
