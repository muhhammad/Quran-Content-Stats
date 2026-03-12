import json
import re


class QuranWordCounter:

    def __init__(self, quran_file):

        with open(quran_file, "r", encoding="utf-8") as f:
            raw_quran = json.load(f)

        self.quran = {}

        for surah, ayahs in raw_quran.items():

            cleaned_ayahs = []

            for i, ayah in enumerate(ayahs):

                # normalize first
                normalized = self._normalize_arabic(ayah)

                # remove Bismillah prefix (except Surah 1)
                if i == 0 and surah != "1":
                    if normalized.startswith("بسم الله الرحمن الرحيم"):
                        normalized = normalized.replace("بسم الله الرحمن الرحيم", "").strip()

                cleaned_ayahs.append(normalized)

            self.quran[surah] = cleaned_ayahs


    def _clean_text(self, text):

        # remove Arabic diacritics
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

        # remove Quran annotation marks
        text = re.sub(r'[\u06D6-\u06ED]', '', text)

        # normalize hamzat-wasl
        text = text.replace("ٱ", "ا")

        # remove tatweel
        text = text.replace("ـ", "")

        # normalize spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()


    def _normalize_arabic(self, text):

        # remove diacritics
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

        # remove Quranic marks
        text = re.sub(r'[\u06D6-\u06ED]', '', text)

        # normalize hamza forms
        text = text.replace("ٱ", "ا")

        # remove tatweel
        text = text.replace("ـ", "")

        # normalize spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()


    def _count_words(self, text):

        text = self._clean_text(text)

        words = text.split()

        # remove Bismillah
        if words[:4] == ["بسم", "الله", "الرحمن", "الرحيم"] or \
        words[:4] == ["بسم", "الله", "الرحمٰن", "الرحيم"]:
            words = words[4:]

        print(words)   # debug AFTER cleanup

        return len(words)


    def count_words_in_ayah(self, surah, ayah):

        text = self.quran[str(surah)][ayah - 1]
        return self._count_words(text)


    def count_words_first_n_ayahs(self, surah, n):

        total = 0

        for ayah in self.quran[str(surah)][:n]:
            total += self._count_words(ayah)

        return total


    def count_words_in_surah(self, surah):

        total = 0

        for ayah in self.quran[str(surah)]:
            total += self._count_words(ayah)

        return total


    def count_words_range(self, surah, start_ayah, end_ayah):

        total = 0

        for ayah in self.quran[str(surah)][start_ayah-1:end_ayah]:
            total += len(ayah.split())

        return total