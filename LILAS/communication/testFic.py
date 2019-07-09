#
fic = open("communication/tickets_comm.csv", 'r')
fic2 = open("communication/tickets_comm__.csv", 'r')

t = fic.readlines()
t2 = fic2.readlines()

fic.close()
fic2.close()

for i in range(len(t)): #On parcourt tous les tickets ----- len(t)
    t[i] = t[i].split(",")#On sépare les champs du ticket
    
for i in range(len(t2)): #On parcourt tous les tickets ----- len(t)
    t2[i] = t2[i].split(",")#On sépare les champs du ticket
    
texteDate = t[0][23]
texteDate2 = t2[0][23]

print(texteDate)
print(t[0][22])
print(texteDate2)