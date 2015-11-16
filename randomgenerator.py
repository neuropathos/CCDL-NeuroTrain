        #for i in range(0 721)
from random import randrange
import numpy as np
a = open('DEFAULT_CONTROL.csv', 'w')




for j in range(1,5):
    ratio = 0
    a.write('0.5\n')
    while ratio < .48 or ratio > .52:
        sectionlength = 0
        section = []
        while sectionlength < 1200:
            sectionvalue = randrange(1,100)
            if sectionvalue < 50: sectionvalue = 0
            else: sectionvalue = 1
            length = randrange(2, 16)
            sectionlength = sectionlength + length
            for i in range(1,length + 1):
                section.append(sectionvalue)
        ratio = np.mean(section)
    for item in section:
     a.write("%s," % item)
    a.write('\n')
a.close
    
            
    
                

