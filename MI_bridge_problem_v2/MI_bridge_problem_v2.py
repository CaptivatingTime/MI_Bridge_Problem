import copy
from itertools import combinations 

# Katra civlēka klase
class Person:

    def __init__(self,speed,name):
        self.speed = speed
        self.name = name

    def getName(self):
        return self.name

    def getSpeed(self):
        return self.speed

# Lāpas klase
class Torch:

    def __init__(self,amount, symbol):
       self.amount = amount
       self.name = symbol

    def decreseAmount(self, spent):
       self.amount = self.amount - spent

    def amountLeft(self):
        return self.amount

    def getName(self):
        return self.name

# Vieta, kur saglabāt pabeigtās un apstrādes procesā esošās virsotnes
class Database:

    def __init__(self):
        self.completed = []
        self.usable = []
        self.selectedNode = []

# Virsotnes klase
class Node:

    def __init__(self):
        self.P1 = []
        self.P2 = []
        self.status = "In progress"
        self.depth = 0

    def addItem1(self, obj):
        self.P1.append(obj)

    def addItem2(self, obj):
        self.P2.append(obj)

    def removeItem1(self, obj):
        self.P1.remove(obj)

    def removeItem2(self, obj):
        self.P2.remove(obj)

    def setStatus(self,status):
        self.status = status

    def getStatus(self):
        return self.status

    def setDepth(self, depth):
        self.depth = depth

    def getDepth(self):
        return self.depth

# Samazina lāpas atlikušo laiku
def decreseTorch(person1Speed, person2Speed, direction): 

    
    def minimum(a, b):
      
        if a <= b:
            return a
        else:
            return b

    def maximum(a, b):
      
        if a >= b:
            return a
        else:
            return b


    if direction == "begin":
        
        if person1Speed > person2Speed:
            spent = person1Speed
        else:
            spent = person2Speed
    elif direction == "forward":       
        spent = maximum(person1Speed,person2Speed)
    elif direction == "backV1":     
        spent = minimum(person1Speed,person2Speed)
    elif direction == "backV2":
        spent = maximum(person1Speed,person2Speed)
    
    return spent

def generatePaths(db):

    db = Database()
    db.completed.append(Node())

    comb = combinations([1, 2, 3],2)
    possibleStarts = []

    # Izveido sarakstu ar visiem iespējamiem sākuma gājieniem
    for i in list(comb):
        possibleStarts.append(i)
    
    # Izveido cilvēkus
    A = Person(1, "A")
    B = Person(3, "B")
    C = Person(5, "C")

    T = Torch(12, "T")

    # Pievieno sākuma virsotni
    db.completed[0].addItem1(T)
    db.completed[0].addItem1(A)
    db.completed[0].addItem1(B)
    db.completed[0].addItem1(C)
    
    # Izvēlas virsotni priekš tālākas apstrādes
    db.selectedNode.append(copy.deepcopy(db.completed[0]))

    active = 0

    NotLastNode = True

    # Pirmie divi civlēki pāriet pāri tiltam
    def crossBridge_leve1(person1, person2): 

        if db.selectedNode[active].P1[0].amountLeft() >= db.selectedNode[active].P1[person1].getSpeed() or  db.selectedNode[active].P1[0].aamountLeft() >= db.selectedNode[active].P1[person2].getSpeed():
            
            # Mainīgajiem piešķir lāpas un civlēku objektus
            torch = db.selectedNode[active].P1[0]
            pers1 = db.selectedNode[active].P1[person1]
            pers2 = db.selectedNode[active].P1[person2]

            # Cilvēki dodas pāri ar lāpu
            db.selectedNode[active].addItem2(torch)
            db.selectedNode[active].addItem2(pers1)
            db.selectedNode[active].addItem2(pers2)

            # Cilvēki, kuri pārgāji, tiek noņemti no tilta sākuma
            db.selectedNode[active].removeItem1(torch)
            db.selectedNode[active].removeItem1(pers1)
            db.selectedNode[active].removeItem1(pers2)         

            # Samazina lāpas derīgumu
            db.selectedNode[active].P2[0].decreseAmount(decreseTorch(pers1.speed, pers2.speed, "begin"))

            # Atzīmē cik dziļi sazarojumā virsotne atrodas
            db.selectedNode[active].setDepth(1)


            db.selectedNode.append(copy.deepcopy(db.selectedNode[active]))
            
            # Saglabā apstrādāto virsotni
            db.completed.append(copy.deepcopy(db.selectedNode[active]))
             
            # Izņem no saraksta apstrādāto virsotni
            db.selectedNode.pop(0)

            # Izņem no saraksta izmantoto sākšanas kombināciju
            possibleStarts.pop(0)

    # Viens aiziet atpakaļ un, ja iespējams, šķērso tiltu ar atlikušo cilvēku
    def crossBridge_leve2(person1, person2):   
           
           # Saglabā virsotni, lai vēlāk ģenerētu citu sazarojumu
           db.usable.append(copy.deepcopy(db.selectedNode[0]))
           

           torch = db.selectedNode[active].P2[0]
           pers1 = db.selectedNode[active].P2[person1]
           pers2 = db.selectedNode[active].P2[person2]

           # Saglabā cilvēku, kurš ir palicis tilta sākumā
           temp = db.selectedNode[active].P1.pop(0)

           # Viens cilvēks ar lāpu atgriežas atpakaļ pie palikušā cilvēka sākumā
           db.selectedNode[active].addItem1(torch)
           db.selectedNode[active].addItem1(pers1)
           db.selectedNode[active].addItem1(temp) 

           # Pārbauda kuru no sazarojumiem ģenerēt
           if person1 == 1:
               db.selectedNode[active].P2[0].decreseAmount(decreseTorch(pers1.speed, pers2.speed, "backV1")) 
               db.selectedNode[active].removeItem2(torch)
               db.selectedNode[active].removeItem2(pers1)
           else:
               db.selectedNode[active].P2[0].decreseAmount(decreseTorch(pers1.speed, pers2.speed, "backV2"))
               db.selectedNode[active].removeItem2(torch)
               db.selectedNode[active].removeItem2(pers1)
           
           #Saglabā cik dziļi sazarojumā virsotne atrodāš 
           db.selectedNode[active].setDepth(2)

           #Pārbauda vai pietiks atlikusī lāpa, lai tiktu atpakaļ ar atlikušo cilvēku
           if db.selectedNode[active].P1[0].amountLeft() < db.selectedNode[active].P1[1].getSpeed() or  db.selectedNode[active].P1[0].amountLeft() < db.selectedNode[active].P1[2].getSpeed():
               
               # Atjauno statusu, ka lāpas derīgums nav pietiekams un visi nav tikuši pāri
               db.selectedNode[active].setStatus("Failed")
           db.completed.append(copy.deepcopy(db.selectedNode[active]))
           pers3 = db.selectedNode[active].P1[2]

           #Pārbauda vai pietiks atlikusī lāpa, lai tiktu atpakaļ ar atlikušo cilvēku un to paveic, ja iespējams
           if db.selectedNode[active].P1[0].amountLeft() >= db.selectedNode[active].P1[1].getSpeed() and  db.selectedNode[active].P1[0].amountLeft() >= db.selectedNode[active].P1[2].getSpeed(): ##Sis japavirza augstak

               #Saglabā cilvēķu, kuurš viens gaida tilta otrā pusē
               temp = db.selectedNode[active].P2.pop(0)

               # Atlikušie cilvēki un lāpa dodas pāri tiltam, kur visi veiksmīgi ir tikuši galā
               db.selectedNode[active].addItem2(torch)
               db.selectedNode[active].addItem2(pers1)
               db.selectedNode[active].addItem2(pers2)
               db.selectedNode[active].addItem2(pers3)

               # Izdzēš no tilta sākuma esošos cilvēkus
               db.selectedNode[active].removeItem1(torch)
               db.selectedNode[active].removeItem1(pers1)
               db.selectedNode[active].removeItem1(pers3)
                
               # Samazina lāpas derīgumu
               db.selectedNode[active].P2[0].decreseAmount(decreseTorch(pers1.speed, pers3.speed, "forward"))

               # Atjauno statusu, ka viss veiksmīgi
               db.selectedNode[active].setStatus("Successful")


               db.selectedNode[active].setDepth(3)
               db.completed.append(copy.deepcopy(db.selectedNode[active]))
               db.selectedNode.pop(0)
               db.selectedNode.append(copy.deepcopy(db.usable[0])) 
               db.usable.pop(0)
           else:
              db.usable.pop(0)
              


           # Pārbauda vai ir sasneigtas beigas
           if len(possibleStarts) == 0:

               # Iestata paša sākuma virsotnes statusu
               db.completed[0].setStatus("Beginning")
               return False
           else: return True

    while NotLastNode: 

       if len (db.selectedNode[active].P2) == 3:
    
          crossBridge_leve2(1,2)  
          NotLastNode = crossBridge_leve2(2,1)
          db.selectedNode.pop(0)
          db.selectedNode.append(copy.deepcopy(db.completed[0]))
       else:
           crossBridge_leve1(possibleStarts[0][0], possibleStarts[0][1]) 

    return db

# Izvada uz ekrāna ģenerētos ceļus
def printPaths(results):
    needSetSide = True
    database = results

     # Formatejuma mainīgie
    depth1 = "              "         
    depth2 = "           |                "             
    depth3 = "           |                               " 
            
    for node in database.completed:

        # Pārbauda vai ir sākums
        if node.getDepth() == 0:
            for i in range(len(node.P1)):
                # Pārbauda vai ir jaizveido Tilta viena puse(P1) un savada vērtbas pa vietām
                if needSetSide:
                    print("  |P1| ", end = '' )
                    needSetSide = False
                    print(node.P1[i].getName() +"(" + str(node.P1[i].amountLeft()) + ")", end = '')
                else:
                   print(node.P1[i].getName(), end = '')
                   if i == len(node.P1) - 1:
                       print("\n _|      ||" + "                                                 Status: " + node.getStatus())

            needSetSide = True

            if len(node.P2) == 0:
                print ("| |P2| ", end = '' )

            for i in range(len(node.P2)):
                # Pārbauda vai jāizveido tilta otra puse(P1) un savada vērtības pa vietām
                if needSetSide:
                    print ("\n|P2| ", end = '' )
                    needSetSide = False
                    print(node.P2[i].getName(), end = '')

            needSetSide = True
        # Pārbauda sazarojumu
        elif node.getDepth() == 1:
            for i in range (len(node.P1)):
                if needSetSide:       
                    print("\n" + "|" + depth1 + "|P1| ", end = '')
                    needSetSide = False
                    print(node.P1[i].getName(), end = '')
                    print("\n" + "|______________"+  "|    ||")
                else:
                   print(node.P1[i].getName(), end = '')


            needSetSide = True

            for i in range(len(node.P2)):
                if needSetSide:
                    print ("|" + "           |  " + "|P2| ", end = '' )
                    needSetSide = False
                    print(node.P2[i].getName() +"(" + str(node.P2[i].amountLeft()) + ")", end = '')
                else:
                   print(node.P2[i].getName(), end = '')


            needSetSide = True
        # Pārbauda sazarojumu
        elif node.getDepth() == 2:
            for i in range (len(node.P1)):
                if needSetSide:     
                    print("\n" + "|" +  depth2 + "|P1| ", end = '')
                    needSetSide = False
                    print(node.P1[i].getName() +"(" + str(node.P1[i].amountLeft()) + ")", end = '')         
                else:
                   print(node.P1[i].getName(), end = '')
                   if i == len(node.P1) - 1:
                       print("\n" + "|" +  "           |________________" + "|      ||" + "                     Status: " + node.getStatus())

            needSetSide = True

            for i in range(len(node.P2)):
                if needSetSide:
                    print ("|" + "           |             |  " + "| |P2| ", end = '' )
                    needSetSide = False
                    print(node.P2[i].getName(), end = '')
                else:
                   print(node.P2[i].getName(), end = '')

            needSetSide = True
        # Pārbauda vai ir jaizvada beigu virsotne
        elif node.getDepth() == 3:
            if len(node.P1) == 0:              
                print ("\n"+"|" +  "           |             |                 " + "|P1| ")
                print("|" + "           |             |_________________" + "|     ||"  + "        Status: " + node.getStatus())

            for i in range(len(node.P2)):
                if needSetSide:
                    print ("|" + depth3 + "|P2| ", end = '' )
                    needSetSide = False
                    print(node.P2[i].getName() +"(" + str(node.P2[i].amountLeft()) + ")", end = '')
                else:
                   print(node.P2[i].getName(), end = '')

            needSetSide = True
    # Izvada kopējo virsotņu skaitu
    print("\n\n                                                            Node Count: " + str(len(database.completed)))

def main():

    generated = []
    generated = generatePaths(generated)

    printPaths(generated)

    
    input()
    

if __name__ == "__main__":
    main()

