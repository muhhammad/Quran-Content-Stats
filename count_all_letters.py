import sys
from quran_letter_counter import count_all_letters_in_verses


def parse_verses(arg):

    verses = []

    parts = arg.split(",")

    for part in parts:

        if "-" in part:
            start, end = map(int, part.split("-"))
            verses.extend(range(start, end+1))

        else:
            verses.append(int(part))

    return verses


if len(sys.argv) != 3:

    print("Usage:")
    print("python3 count_all_letters.py <surah> <verse_list>")
    print("Example:")
    print("python3 count_all_letters.py 96 1-5")

    sys.exit()


surah = int(sys.argv[1])
verses = parse_verses(sys.argv[2])


plain, uthmani = count_all_letters_in_verses(surah, verses)


print("\nPlain text letter counts\n")

total = 0

for letter in sorted(plain):
    print(letter, ":", plain[letter])
    total += plain[letter]

print("\nTotal letters:", total)


print("\nUthmani text letter counts\n")

total = 0

for letter in sorted(uthmani):
    print(letter, ":", uthmani[letter])
    total += uthmani[letter]

print("\nTotal letters:", total)