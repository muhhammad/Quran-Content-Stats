import sys

from quran_letter_counter import count_letter_in_surah
from quran_letter_counter import count_all_letters_in_verses
from quran_letter_counter import letter_map

from quran_word_counter import QuranWordCounter


# -------------------------
# Helpers
# -------------------------

def parse_verses(arg):

    verses = []

    parts = arg.split(",")

    for part in parts:

        if "-" in part:
            start, end = map(int, part.split("-"))
            verses.extend(range(start, end + 1))

        else:
            verses.append(int(part))

    return verses


def check_19(n):

    if n % 19 == 0:
        return f"YES ({n//19} × 19)"
    else:
        return f"NO (remainder {n%19})"


def usage():

    print("""
Quran CLI Tool

Commands:

words        count words in verses
letters      count specific letter
freq         letter frequency
stats        full statistics
scan         scan a letter across Quran
muqattaat_scan  analyze Muqattaat surahs

Examples:

python3 quran_tool.py words 96 1-5
python3 quran_tool.py letters qaf 50 42
python3 quran_tool.py freq 96 1-5
python3 quran_tool.py stats 96 1-5
python3 quran_tool.py scan qaf
python3 quran_tool.py muqattaat_scan
""")

    sys.exit()


if len(sys.argv) < 2:
    usage()


command = sys.argv[1]


# -------------------------
# WORD COUNTS
# -------------------------

if command == "words":

    if len(sys.argv) != 4:
        usage()

    surah = int(sys.argv[2])
    verses = parse_verses(sys.argv[3])

    counter = QuranWordCounter("quran.json")

    total = 0

    print()

    for v in verses:

        count = counter.count_words_in_ayah(surah, v)

        print(f"{surah}:{v} -> {count} words")

        total += count

    print("\nTotal words:", total)
    print("Divisible by 19:", check_19(total))


# -------------------------
# LETTER COUNTS
# -------------------------

elif command == "letters":

    if len(sys.argv) < 4:
        usage()

    letter = sys.argv[2]
    surahs = [int(x) for x in sys.argv[3:]]

    total_plain = 0
    total_uthmani = 0

    print("\nLetter:", letter)
    print("Surahs:", surahs)
    print()

    for s in surahs:

        plain, uthmani = count_letter_in_surah(s, letter)

        total_plain += plain
        total_uthmani += uthmani

        print(f"Surah {s}")
        print("  Plain count   :", plain)
        print("  Uthmani count :", uthmani)
        print()

    print("TOTAL COUNTS")
    print("-------------------")

    print("Plain total   :", total_plain)
    print("Divisible by 19:", check_19(total_plain))

    print()

    print("Uthmani total :", total_uthmani)
    print("Divisible by 19:", check_19(total_uthmani))


# -------------------------
# LETTER FREQUENCY
# -------------------------

elif command == "freq":

    if len(sys.argv) != 4:
        usage()

    surah = int(sys.argv[2])
    verses = parse_verses(sys.argv[3])

    plain, uthmani = count_all_letters_in_verses(surah, verses)

    print("\nPlain text frequency\n")

    total = 0

    for letter in sorted(plain):
        print(letter, ":", plain[letter])
        total += plain[letter]

    print("\nTotal letters:", total)
    print("Divisible by 19:", check_19(total))

    print("\nUthmani frequency\n")

    total = 0

    for letter in sorted(uthmani):
        print(letter, ":", uthmani[letter])
        total += uthmani[letter]

    print("\nTotal letters:", total)
    print("Divisible by 19:", check_19(total))


# -------------------------
# FULL STATS
# -------------------------

elif command == "stats":

    if len(sys.argv) != 4:
        usage()

    surah = int(sys.argv[2])
    verses = parse_verses(sys.argv[3])

    counter = QuranWordCounter("quran.json")

    word_total = 0

    for v in verses:
        word_total += counter.count_words_in_ayah(surah, v)

    plain, uthmani = count_all_letters_in_verses(surah, verses)

    letter_total_plain = sum(plain.values())
    letter_total_uthmani = sum(uthmani.values())

    print("\nSTATISTICS\n")

    print("Words:", word_total)
    print("Divisible by 19:", check_19(word_total))

    print("\nPlain letters:", letter_total_plain)
    print("Divisible by 19:", check_19(letter_total_plain))

    print("\nUthmani letters:", letter_total_uthmani)
    print("Divisible by 19:", check_19(letter_total_uthmani))


# -------------------------
# SCAN LETTER ACROSS QURAN
# -------------------------

elif command == "scan":

    if len(sys.argv) != 3:
        usage()

    letter = sys.argv[2]

    print(f"\nScanning letter: {letter}\n")

    for surah in range(1, 115):

        plain, uthmani = count_letter_in_surah(surah, letter)

        mark_plain = f"(19×{plain//19})" if plain % 19 == 0 and plain != 0 else ""
        mark_uthmani = f"(19×{uthmani//19})" if uthmani % 19 == 0 and uthmani != 0 else ""

        print(
            f"Surah {surah:3}  "
            f"Plain: {plain:4} {mark_plain}   "
            f"Uthmani: {uthmani:4} {mark_uthmani}"
        )


# -------------------------
# MUQATTAAT SCAN
# -------------------------

elif command == "muqattaat_scan":

    reverse_letter_map = {v: k for k, v in letter_map.items()}

    muqattaat = {
        2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
        14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
        28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
        38:"ص",40:"حم",41:"حم",42:"حم عسق",43:"حم",44:"حم",
        45:"حم",46:"حم",50:"ق",68:"ن"
    }

    print("\nMuqattaat Surah Analysis\n")

    for surah, letters in muqattaat.items():

        print(f"Surah {surah}  Opening letters: {letters}")

        letters = letters.replace(" ", "")

        for letter in letters:

            name = reverse_letter_map.get(letter)

            if not name:
                continue

            plain, uthmani = count_letter_in_surah(surah, name)

            mark_plain = f"(19×{plain//19})" if plain % 19 == 0 else f"(rem {plain%19})"
            mark_uthmani = f"(19×{uthmani//19})" if uthmani % 19 == 0 else f"(rem {uthmani%19})"

            print(
                f"   {letter} ({name})"
                f"  Plain:{plain:4} {mark_plain}"
                f"  Uthmani:{uthmani:4} {mark_uthmani}"
            )

        print()


# -------------------------
# MUQATTAAT MATRIX
# -------------------------

elif command == "matrix":

    muqattaat = {
        2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
        14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
        28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
        38:"ص",40:"حم",41:"حم",42:"حم عسق",43:"حم",44:"حم",
        45:"حم",46:"حم",50:"ق",68:"ن"
    }

    reverse_letter_map = {v:k for k,v in letter_map.items()}

    letters = [
        "alif","lam","meem","sad","ra",
        "kaf","ha","ya","ain",
        "ta","seen","qaf","nun"
    ]

    print("\nMuqattaat Letter Matrix\n")

    header = "Surah ".ljust(6)

    for l in letters:
        header += l[:3].rjust(6)

    print(header)
    print("-"*len(header))

    for surah,opening in muqattaat.items():

        row = str(surah).ljust(6)

        opening_letters = opening.replace(" ","")

        for l in letters:

            arabic_letter = letter_map[l]

            if arabic_letter in opening_letters:

                plain,_ = count_letter_in_surah(surah,l)

                row += str(plain).rjust(6)

            else:
                row += " ".rjust(6)

        print(row)


# -------------------------
# VERIFY MUQATTAAT CLAIMS
# -------------------------

elif command == "verify":

    muqattaat = {
        2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",
        14:"الر",15:"الر",19:"كهيعص",20:"طه",26:"طسم",27:"طس",
        28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",
        38:"ص",40:"حم",41:"حم",42:"حم عسق",43:"حم",44:"حم",
        45:"حم",46:"حم",50:"ق",68:"ن"
    }

    reverse_letter_map = {v:k for k,v in letter_map.items()}

    print("\nMuqattaat Verification Report\n")

    failures = []

    for surah, opening in muqattaat.items():

        letters = opening.replace(" ","")

        print(f"Surah {surah}  Opening: {opening}")

        for letter in letters:

            name = reverse_letter_map.get(letter)

            if not name:
                continue

            plain, uthmani = count_letter_in_surah(surah, name)

            ok_plain = plain % 19 == 0
            ok_uthmani = uthmani % 19 == 0

            status = "PASS" if ok_plain and ok_uthmani else "FAIL"

            print(
                f"   {letter} ({name}) "
                f"Plain:{plain} "
                f"Uthmani:{uthmani} "
                f"{status}"
            )

            if status == "FAIL":
                failures.append((surah, letter, plain, uthmani))

        print()

    print("SUMMARY")
    print("--------------------")

    if not failures:
        print("All checks passed.")
    else:

        print("Failures detected:\n")

        for s,l,p,u in failures:

            print(
                f"Surah {s} Letter {l} "
                f"Plain:{p} "
                f"Uthmani:{u}"
            )

            
else:
    usage()