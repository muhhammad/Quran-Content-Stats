import json
import re


class QuranWordCounter:
    def __init__(self, quran_file):
        with open(quran_file, "r", encoding="utf-8") as f:
            self.quran = json.load(f)

    def _clean_text(self, text):
        """
        Remove punctuation and extra spaces
        """
        text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
        return text.strip()

    def _count_words(self, text):
        text = self._clean_text(text)
        return len(text.split())

    def count_words_in_ayah(self, surah, ayah):
        """
        Count words in a specific ayah
        """
        ayah_text = self.quran[str(surah)][ayah - 1]
        return self._count_words(ayah_text)

    def count_words_in_surah(self, surah):
        """
        Count words in entire surah
        """
        total = 0
        for ayah in self.quran[str(surah)]:
            total += self._count_words(ayah)
        return total

    def count_words_first_n_ayahs(self, surah, n):
        """
        Count words in first N ayahs of a surah
        """
        total = 0
        ayahs = self.quran[str(surah)][:n]

        for ayah in ayahs:
            total += self._count_words(ayah)

        return total

    def count_words_range(self, surah, start_ayah, end_ayah):
        """
        Count words in a range of ayahs
        """
        total = 0
        ayahs = self.quran[str(surah)][start_ayah - 1:end_ayah]

        for ayah in ayahs:
            total += self._count_words(ayah)

        return total