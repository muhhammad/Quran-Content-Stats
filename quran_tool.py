import sys

from quran_letter_counter import count_letter_in_surah
from quran_letter_counter import count_all_letters_in_verses
from quran_letter_counter import letter_map
from quran_letter_counter import ayah_counts

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

    if len(sys.argv) not in (3,4):
        usage()

    surah = int(sys.argv[2])

    surah = int(sys.argv[2])

    if len(sys.argv) == 4:
        verses = parse_verses(sys.argv[3])
    else:
        verses = list(range(1, ayah_counts[surah-1] + 1))

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

    from quran_letter_counter import ayah_counts

    if len(sys.argv) not in (3,4):
        usage()

    surah = int(sys.argv[2])

    # If verses specified
    if len(sys.argv) == 4:
        verses = parse_verses(sys.argv[3])

    # Otherwise use entire surah
    else:
        verses = list(range(1, ayah_counts[surah-1] + 1))


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
# LETTER FREQUENCY ALL SURAHS
# -------------------------

elif command == "freq_all":

    from quran_letter_counter import ayah_counts

    print("\nLetter frequency across all surahs\n")

    grand_total_plain = 0
    grand_total_uthmani = 0

    for surah in range(1,115):

        verses = list(range(1, ayah_counts[surah-1] + 1))

        plain, uthmani = count_all_letters_in_verses(surah, verses)

        total_plain = sum(plain.values())
        total_uthmani = sum(uthmani.values())

        grand_total_plain += total_plain
        grand_total_uthmani += total_uthmani

        print(
            f"Surah {surah:3}  "
            f"Plain:{total_plain:6} "
            f"Uthmani:{total_uthmani:6}"
        )

    print("\n----------------------------------")
    print("TOTAL LETTERS IN QURAN")
    print("----------------------------------")

    print("Plain total   :", grand_total_plain)
    print("Divisible by 19:", check_19(grand_total_plain))

    print()

    print("Uthmani total :", grand_total_uthmani)
    print("Divisible by 19:", check_19(grand_total_uthmani))


# -------------------------
# LETTER COUNT PER VERSE
# -------------------------

elif command == "letter_verses":

    from quran_letter_counter import ayah_counts, normalize, letter_map

    if len(sys.argv) != 4:
        usage()

    letter_name = sys.argv[2].lower()
    surah = int(sys.argv[3])

    if letter_name not in letter_map:
        print("Unknown letter")
        sys.exit()

    letter = letter_map[letter_name]

    start = sum(ayah_counts[:surah-1])

    with open("quran-simple-plain.txt", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"\nLetter '{letter}' ({letter_name}) in Surah {surah}\n")

    total = 0

    for ayah in range(1, ayah_counts[surah-1] + 1):

        text = normalize(lines[start + ayah - 1])

        count = text.count(letter)

        total += count

        print(f"{surah}:{ayah:3}  {count}")

    print("\n----------------------------------")

    print("TOTAL:", total)
    print("Divisible by 19:", check_19(total))


# -------------------------
# VISUAL LETTER MAP
# -------------------------

elif command == "letter_map":

    from quran_letter_counter import ayah_counts, normalize, letter_map

    if len(sys.argv) != 4:
        usage()

    letter_name = sys.argv[2].lower()
    surah = int(sys.argv[3])

    if letter_name not in letter_map:
        print("Unknown letter")
        sys.exit()

    letter = letter_map[letter_name]

    start = sum(ayah_counts[:surah-1])

    with open("quran-simple-plain.txt", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"\nLetter '{letter}' ({letter_name}) visual map in Surah {surah}\n")

    total = 0

    for ayah in range(1, ayah_counts[surah-1] + 1):

        text = normalize(lines[start + ayah - 1])

        count = text.count(letter)

        total += count

        bar = "█" * count

        print(f"{surah}:{ayah:3}  {bar}")

    print("\n----------------------------------")

    print("TOTAL:", total)
    print("Divisible by 19:", check_19(total))

    
# -------------------------
# TOTAL OCCURRENCES OF A LETTER IN QURAN
# -------------------------

elif command == "letter_total":

    from quran_letter_counter import ayah_counts

    if len(sys.argv) != 3:
        usage()

    letter = sys.argv[2]

    total_plain = 0
    total_uthmani = 0

    print(f"\nCounting letter '{letter}' across the entire Quran\n")

    for surah in range(1,115):

        plain, uthmani = count_letter_in_surah(surah, letter)

        total_plain += plain
        total_uthmani += uthmani

    print("TOTAL OCCURRENCES")
    print("----------------------")

    print("Plain text   :", total_plain)
    print("Divisible by 19:", check_19(total_plain))

    print()

    print("Uthmani text :", total_uthmani)
    print("Divisible by 19:", check_19(total_uthmani))


# -------------------------
# COUNT WORD IN QURAN
# -------------------------

elif command == "count_word":

    import re

    if len(sys.argv) != 3:
        usage()

    word = sys.argv[2]

    counter = QuranWordCounter("quran.json")

    total = 0

    print(f"\nSearching for word: {word}\n")

    for surah in range(1,115):

        ayahs = counter.quran[str(surah)]

        for i, ayah in enumerate(ayahs, start=1):

            occurrences = len(re.findall(rf'\b{word}\b', ayah))

            if occurrences > 0:

                print(f"{surah}:{i}  ({occurrences})  {ayah}")

                total += occurrences

    print("\n----------------------------------")
    print("TOTAL OCCURRENCES:", total)
    print("Divisible by 19:", check_19(total))


# -------------------------
# ROOT SEARCH
# -------------------------

elif command == "root":

    import re

    if len(sys.argv) != 3:
        usage()

    root = sys.argv[2]

    counter = QuranWordCounter("quran.json")

    total = 0

    print(f"\nSearching for root letters: {root}\n")

    pattern = re.compile(rf"[ء-ي]*{root}[ء-ي]*")

    for surah in range(1,115):

        ayahs = counter.quran[str(surah)]

        for i, ayah in enumerate(ayahs, start=1):

            matches = pattern.findall(ayah)

            if matches:

                print(f"{surah}:{i}  {matches}")

                total += len(matches)

    print("\n----------------------------------")
    print("TOTAL MATCHES:", total)
    print("Divisible by 19:", check_19(total))


# -------------------------
# VERSE ANALYSIS
# -------------------------

elif command == "verse":

    import re

    if len(sys.argv) != 3:
        usage()

    ref = sys.argv[2]

    if ":" not in ref:
        print("Format must be surah:ayah (example 96:1)")
        sys.exit()

    surah, ayah = map(int, ref.split(":"))

    counter = QuranWordCounter("quran.json")

    raw_text = counter.quran[str(surah)][ayah-1]

    # clean verse exactly like the word counter
    clean_text = counter._clean_text(raw_text)

    words = clean_text.split()

    # remove Bismillah (same logic used in _count_words)
    if words[:4] == ["بسم", "الله", "الرحمن", "الرحيم"] or \
       words[:4] == ["بسم", "الله", "الرحمٰن", "الرحيم"]:
        words = words[4:]

    verse_text = " ".join(words)

    word_count = len(words)

    letters = re.findall(r"[ء-ي]", verse_text)
    letter_count = len(letters)

    freq = {}

    for l in letters:
        freq[l] = freq.get(l, 0) + 1


    print("\nVerse:", ref)
    print("----------------------------------")
    print(verse_text)

    print("\nWord count:", word_count)
    print("Divisible by 19:", check_19(word_count))

    print("\nLetter count:", letter_count)
    print("Divisible by 19:", check_19(letter_count))

    print("\nLetter frequency\n")

    for k in sorted(freq):
        print(k, ":", freq[k])


# -------------------------
# VERSE SCAN (WHOLE SURAH)
# -------------------------

elif command == "verse_scan":

    import re
    from quran_letter_counter import ayah_counts

    if len(sys.argv) != 3:
        usage()

    surah = int(sys.argv[2])

    counter = QuranWordCounter("quran.json")

    total_words = 0
    total_letters = 0

    print(f"\nVerse scan for Surah {surah}\n")

    for ayah in range(1, ayah_counts[surah-1] + 1):

        raw_text = counter.quran[str(surah)][ayah-1]

        clean_text = counter._clean_text(raw_text)

        words = clean_text.split()

        # remove Bismillah if present
        if words[:4] == ["بسم","الله","الرحمن","الرحيم"] or \
           words[:4] == ["بسم","الله","الرحمٰن","الرحيم"]:
            words = words[4:]

        verse_text = " ".join(words)

        word_count = len(words)

        letters = re.findall(r"[ء-ي]", verse_text)
        letter_count = len(letters)

        total_words += word_count
        total_letters += letter_count

        print(
            f"{surah}:{ayah:3}  "
            f"Words:{word_count:3}  "
            f"Letters:{letter_count:3}"
        )

    print("\n----------------------------------")

    print("TOTAL WORDS:", total_words)
    print("Divisible by 19:", check_19(total_words))

    print()

    print("TOTAL LETTERS:", total_letters)
    print("Divisible by 19:", check_19(total_letters))


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