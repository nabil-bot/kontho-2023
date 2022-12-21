from pydub import AudioSegment
from pydub.silence import split_on_silence
import os


from pydub import AudioSegment
sound1 = AudioSegment.from_mp3(".//audio_chunks//sentChunck0.mp3")

duration_in_milliseconds = len(sound1)

toCutlast = 500

# print(duration_in_milliseconds)

firstpart = sound1[:(duration_in_milliseconds - toCutlast)]
firstpart = firstpart +7
firstpart.export(".//audio_chunks//splitedExport3.mp3", format ="mp3")  