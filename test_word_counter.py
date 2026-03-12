from quran_word_counter import QuranWordCounter

quran = QuranWordCounter("quran.json")

# Words in Surah 96 Ayah 1
print("Words in Surah 96 Ayah 1:")
print(quran.count_words_in_ayah(96, 1))

# Words in entire Surah 96
print("Words in Surah 96:")
print(quran.count_words_in_surah(96))

# Words in first 5 ayahs of Surah 96
print("Words in Surah 96 (Ayah 1-5):")
print(quran.count_words_first_n_ayahs(96, 5))

# Words in range
print("Words in Surah 2 Ayah 1-10:")
print(quran.count_words_range(2, 1, 10))