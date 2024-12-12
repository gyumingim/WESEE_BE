import hbcvt

class BrailleService:
    @staticmethod
    def letter_to_braille(result):
        dot_letters = []
        for letter in hbcvt.h2b.text(result):
            for consonant in letter[1]:
                dot_letter = 0
                ord_value = 64
                for dot in consonant[1][0]:
                    dot_letter += int(dot) * ord_value
                    ord_value /= 2
                dot_letters.append(int(dot_letter))
        return dot_letters

    @staticmethod
    def decimal_to_braille_binary(dot_letters):
        return [list(map(int, format(decimal_dot, '06b')))[:6] for decimal_dot in dot_letters]