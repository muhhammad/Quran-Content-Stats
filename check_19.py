import sys
from quran_letter_counter import count_letter_in_surah


def divisible_by_19(n):
    return n % 19 == 0


if len(sys.argv) < 3:
    print("Usage: python3 check_19.py <letter> <surah1> [surah2] [surah3] ...")
    sys.exit()

letter = sys.argv[1]
surah_numbers = [int(s) for s in sys.argv[2:]]

total_plain = 0
total_uthmani = 0

print("Letter:", letter)
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
print("Divisible by 19:", divisible_by_19(total_plain))

print()

print("Uthmani total :", total_uthmani)
print("Divisible by 19:", divisible_by_19(total_uthmani))