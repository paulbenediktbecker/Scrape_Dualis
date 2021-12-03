import pickle 
loaded_obj = None 
with open('mypickle.pickle',"rb") as f:
    loaded_obj = pickle.load(f)


print("hi")
Noten = []
for semester in loaded_obj:
    for modul in semester: 
        len_model = len(modul)
        stuff = modul[5:(len_model -5)]
        Noten.append(stuff)

Noten_2 = []
for semester in loaded_obj:
    for modul in semester: 
        len_model = len(modul)
        stuff = modul[5:(len_model -5)]
        Noten_2.append(stuff)

for x,y in zip(Noten,Noten_2):
    print(x ==y)


