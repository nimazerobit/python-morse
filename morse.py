import numpy as np
import simpleaudio as sa

class Morse:
    codes = {
        "A": ".-",    "B": "-...",  "C": "-.-.", "D": "-..",   "E": ".",
        "F": "..-.",  "G": "--.",   "H": "....", "I": "..",    "J": ".---",
        "K": "-.-",   "L": ".-..",  "M": "--",   "N": "-.",    "O": "---",
        "P": ".--.",  "Q": "--.-",  "R": ".-.",  "S": "...",   "T": "-",
        "U": "..-",   "V": "...-",  "W": ".--",  "X": "-..-",  "Y": "-.--",
        "Z": "--..",  "0": "-----", "1": ".----", "2": "..---", "3": "...--",
        "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..",
        "9": "----.", ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
        "!": "-.-.--", "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...",
        ":": "---...", ";": "-.-.-.", "=": "-...-", "+": ".-.-.",
        "-": "-....-", "_": "..--.-", "\"": ".-..-.", "$": "...-..-", "@": ".--.-.",
        "\n": ".-.-", "\x01": "-.-.-", "\x04": "...-.-"
    }
    reverse = {v: k for k, v in codes.items()}

class MorsePlayer:
    def __init__(self, wpm=20, tone=600, word_spacing=1, character_spacing=1):
        self.wpm = wpm
        self.tone = tone
        self.word_spacing = word_spacing
        self.character_spacing = character_spacing
        self.sample_rate = 44100

    @staticmethod
    def to_morse(text):
        result = []
        for char in text.upper():
            if char == ' ':
                result.append(' / ')
            else:
                result.append(Morse.codes.get(char, ''))
        return ' '.join(result).replace('  /  ', ' / ')

    def play(self, text):
        buffer = self.create_tone_buffer(text.upper())
        sa.play_buffer(buffer, 1, 2, self.sample_rate).wait_done()

    def create_tone_buffer(self, text):
        unit_duration_ms = 1200 / self.wpm
        unit = int(self.sample_rate * (unit_duration_ms / 1000))
        sequence = []

        for char in text:
            if char == ' ':
                sequence.append((0, 7 * self.word_spacing * unit))
            else:
                morse = Morse.codes.get(char, '')
                for i, symbol in enumerate(morse):
                    duration = unit if symbol == '.' else 3 * unit
                    sequence.append((1, duration))
                    if i < len(morse) - 1:
                        sequence.append((0, unit))
                sequence.append((0, 3 * self.character_spacing * unit))

        total_length = sum(duration for _, duration in sequence)
        audio = np.zeros(total_length, dtype=np.float32)
        pos = 0

        for is_tone, duration in sequence:
            if is_tone:
                t = np.linspace(0, duration / self.sample_rate, duration, endpoint=False)
                wave = 0.5 * np.sin(2 * np.pi * self.tone * t)
                fade_length = min(int(self.sample_rate * 0.004), duration)
                wave[-fade_length:] *= np.linspace(1, 0, fade_length)
                audio[pos:pos + duration] = wave
            pos += duration

        audio_int16 = np.int16(audio * 32767)
        return audio_int16.tobytes()