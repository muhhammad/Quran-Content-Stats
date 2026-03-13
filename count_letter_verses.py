import sys
from quran_letter_counter import count_letter_in_verses


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


if len(sys.argv) != 4:

    print("Usage:")
    print("python3 count_letter_verses.py <letter> <surah> <verse_list>")
    print("Example:")
    print("python3 count_letter_verses.py qaf 50 1-10")

    sys.exit()


letter = sys.argv[1]
surah = int(sys.argv[2])
verses = parse_verses(sys.argv[3])


plain, uthmani = count_letter_in_verses(surah, letter, verses)


print("\nLetter:", letter)
print("Surah:", surah)
print("Verses:", verses)

print("\nPlain text count :", plain)
print("Uthmani text count :", uthmani)