import sys
from quran_letter_counter import count_letter_in_surah


def divisible_by_19(n):
    return n % 19 == 0


if len(sys.argv)!=3:
    print("Usage: python3 check_19.py <surah> <letter>")
    sys.exit()

surah=int(sys.argv[1])
letter=sys.argv[2]

plain,uthmani=count_letter_in_surah(surah,letter)

print("Surah:",surah)
print("Letter:",letter)

print("\nPlain count:",plain)
print("Divisible by 19:",divisible_by_19(plain))

print("\nUthmani count:",uthmani)
print("Divisible by 19:",divisible_by_19(uthmani))