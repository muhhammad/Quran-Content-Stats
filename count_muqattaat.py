from quran_letter_counter import count_letter_in_surah

# muqattaat sequences
muqattaat = {
2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
38:"ص",40:"حم",41:"حم",42:"حم",43:"حم",44:"حم",45:"حم",
46:"حم",50:"ق",68:"ن"
}

# collect unique letters
letters=set()
for seq in muqattaat.values():
    for l in seq:
        letters.add(l)

# Arabic → english mapping used by library
arabic_to_name={
"ا":"alif","ب":"ba","ت":"ta","ث":"tha","ج":"jeem","ح":"ha","خ":"kha",
"د":"dal","ذ":"dhal","ر":"ra","ز":"zay","س":"seen","ش":"sheen",
"ص":"sad","ض":"dad","ط":"ta2","ظ":"za","ع":"ain","غ":"ghain",
"ف":"fa","ق":"qaf","ك":"kaf","ل":"lam","م":"meem","ن":"nun",
"ه":"ha2","و":"waw","ي":"ya"
}

print("Muqattaʿat Letter Counts Across All Relevant Surahs\n")

for letter in sorted(letters):

    name=arabic_to_name[letter]

    total_plain=0
    total_uthmani=0

    for surah,seq in muqattaat.items():

        if letter in seq:

            plain,uthmani=count_letter_in_surah(surah,name)

            total_plain+=plain
            total_uthmani+=uthmani

    print(f"{letter} ({name})")
    print("  Plain text total   :",total_plain)
    print("  Uthmani text total :",total_uthmani)
    print()