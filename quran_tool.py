import sys
from quran_letter_counter import count_letter_in_surah
from quran_letter_counter import count_all_letters_in_verses


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


def divisible_by_19(n):
    return n % 19 == 0


def usage():

    print("""
Quran CLI Tool

Commands:

1️⃣ Count words
python3 quran_tool.py words <surah> <verse_list>

Example:
python3 quran_tool.py words 96 1-5


2️⃣ Count specific letter
python3 quran_tool.py letters <letter> <surah1> [surah2] ...

Example:
python3 quran_tool.py letters qaf 50
python3 quran_tool.py letters qaf 50 42


3️⃣ Letter frequency in verses
python3 quran_tool.py freq <surah> <verse_list>

Example:
python3 quran_tool.py freq 96 1-5
""")

    sys.exit()


if len(sys.argv) < 2:
    usage()


command = sys.argv[1]


# ------------------------
# LETTER COUNTS
# ------------------------

if command == "letters":

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
    print("Divisible by 19:", divisible_by_19(total_plain))

    print()

    print("Uthmani total :", total_uthmani)
    print("Divisible by 19:", divisible_by_19(total_uthmani))


# ------------------------
# LETTER FREQUENCY
# ------------------------

elif command == "freq":

    if len(sys.argv) != 4:
        usage()

    surah = int(sys.argv[2])
    verses = parse_verses(sys.argv[3])

    plain, uthmani = count_all_letters_in_verses(surah, verses)

    print("\nPlain text letter frequency\n")

    total = 0

    for letter in sorted(plain):
        print(letter, ":", plain[letter])
        total += plain[letter]

    print("\nTotal letters:", total)

    print("\nUthmani text letter frequency\n")

    total = 0

    for letter in sorted(uthmani):
        print(letter, ":", uthmani[letter])
        total += uthmani[letter]

    print("\nTotal letters:", total)


else:
    usage()