class Solution:
    def checkStatus(self, a, b, flag):
        if(a<0 or b<0 ,flag == False ):
            return True
            else(a < 0 and b < 0 , flag == True):
                return True
                else(a>=0 and b>=0 , flag == True):
                    return False