from collections import Counter

# Correct Muqattaʿat sequences
muqattaat = {
2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
38:"ص",40:"حم",41:"حم",42:"حم عسق",43:"حم",44:"حم",45:"حم",
46:"حم",50:"ق",68:"ن"
}

# Arabic → English names
letter_names = {
"ا":"alif","ب":"ba","ت":"ta","ث":"tha","ج":"jeem","ح":"ha","خ":"kha",
"د":"dal","ذ":"dhal","ر":"ra","ز":"zay","س":"seen","ش":"sheen",
"ص":"sad","ض":"dad","ط":"ta","ظ":"za","ع":"ain","غ":"ghain",
"ف":"fa","ق":"qaf","ك":"kaf","ل":"lam","م":"meem","ن":"nun",
"ه":"ha","و":"waw","ي":"ya"
}

counter = Counter()

for seq in muqattaat.values():

    seq = seq.replace(" ","")

    for letter in seq:
        counter[letter] += 1


print("Muqattaʿat Letters Total\n")

grand_total = 0

for letter,count in sorted(counter.items()):
    name = letter_names.get(letter,"unknown")
    print(f"{letter} ({name}) : {count}")
    grand_total += count

print("\nGrand Total:", grand_total)