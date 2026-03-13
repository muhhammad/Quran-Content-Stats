import sys
from quran_letter_counter import count_letter_in_surah


def count_letter_in_verses(surah, letter_name, verses):

    letter_name = letter_name.lower()

    if letter_name not in letter_map:
        raise ValueError("Unknown letter")

    letter = letter_map[letter_name]

    start = sum(ayah_counts[:surah-1])

    count_plain = 0
    count_uthmani = 0

    with open("quran-simple-plain.txt", encoding="utf-8") as f:
        lines = f.readlines()

    for v in verses:
        text = normalize(lines[start + v - 1])
        count_plain += text.count(letter)

    with open("quran-uthmani.txt", encoding="utf-8") as f:
        lines = f.readlines()

    for v in verses:
        text = normalize(lines[start + v - 1])
        count_uthmani += text.count(letter)

    return count_plain, count_uthmani


def check_19(n):

    if n % 19 == 0:
        return f"YES ({n//19} × 19)"
    else:
        return f"NO (remainder {n%19})"


if len(sys.argv) < 3:
    print("Usage:")
    print("python3 check_19.py <letter> <surah1> [surah2] ...")
    print("Example:")
    print("python3 check_19.py qaf 50 42")
    sys.exit()


letter = sys.argv[1]
surah_numbers = [int(s) for s in sys.argv[2:]]

total_plain = 0
total_uthmani = 0

print("\nLetter:", letter)
print("Surahs:", surah_numbers)
print()

for surah in surah_numbers:

    plain, uthmani = count_letter_in_surah(surah, letter)

    total_plain += plain
    total_uthmani += uthmani

    print(f"Surah {surah}")
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