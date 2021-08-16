import math

def binToDec(binNum):
    """Wandelt eine gegebene Binär-Zahl (ggf. -String) in eine Binär-Zahl um."""
    return int(str(binNum), 2)

def decToBin(decNum): 
    """Wandelt eine gegebene Dezimal-Zahl in einen Binär-String um."""
    rest = ''
    while int(decNum) > 0:
        rest += str((decNum % 2))
        decNum = math.floor(decNum/2)
    rest = rest[::-1]
    
    for i in range(10-len(rest)):
        rest = '0' + rest
        
    return rest


def binToKlappen(binNum):
    '''Wandelt einen gegebenen zehnstelligen Binär-String in eine "Klappen-Liste" um.'''
    arr = list(str(binNum))
    for i in range(1, len(arr)+1):
        if not arr[i-1] == '0':
            arr[i-1] = i
        else:
            arr[i-1] = 0
            
    for i in range(arr.count(0)):
        arr.remove(0)
        
    return arr


def klappenToBin(klappen):
    '''Wandelt eine gegebene "Klappen-Liste" in einen zehnstelligen Binär-String um.'''
    arr = []
    for i in range(0, 10):
        arr.append('0')
    
    for i in range(len(klappen)):
        arr[klappen[i]-1] = '1'
    
    return ''.join(arr)
    

def decToKlappen(decNum):
    '''Wandelt eine gegebene Dezimal-Zahl in eine dementsprechende "Klappen-Liste" um.'''
    return binToKlappen(decToBin(decNum))


def klappenToDec(klappen):
    '''Wandelt eine gegebene "Klappen-Liste" in eine dementsprechende Dezimal-Zahl um.'''
    return binToDec(klappenToBin(klappen))