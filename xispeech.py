from pydub import AudioSegment
from os import path
from base64 import b64encode
from pypinyin import pinyin, Style
from cn2an import an2cn, transform
from opencc import OpenCC
from glob import glob
from re import sub
from random import randint
from math import floor, log2
from exception import ProcessAbortedException


class XiSpeechSynthesizer:
    table = {
        "，": " . ",
        "。": " . ",
        "！": " . ",
        "？": " . ",
        "；": " . ",
        "、": " . ",
        "：": " . ",
        ",": " . ",
        ".": " . ",
        "?": " . ",
        ";": " . ",
        ":": " . ",
        "…": " . ",
        "!": " . ",
        "”": "",
        "“": "",
        "《": "",
        "》": "",
        "‘": "",
        "’": "",
        "'": "",
        "\"": "",
        "%": "个百分点",
        "℃": "摄氏度",
        "℉": "华氏度"
    }
    regex = r'(?<![A-Za-z])((?<!\d)-)?\d+(\.\d*[1-9])?'  # match all numbers, excl. tones
    translation = str.maketrans(table)
    convert_to_simplified = OpenCC('t2s.json')
    files = glob("sounds/*.wav")
    sounds = {}
    loading = 0
    sum = len(files)
    for i in files:
        if loading % 20 == 0:
            print("加载资源 {0}/{1}".format(loading, sum))
        syllable = path.splitext(path.basename(i))[0].split()[0]
        if syllable in sounds:
            sounds[syllable].append(AudioSegment.from_file(i, format="wav"))
        else:
            sounds[syllable] = [AudioSegment.from_file(i, format="wav")]
        loading += 1

    def __init__(self):
        self.current_step = 0
        self.steps_required = 0
        self.progress = 0
        self.result = ""
        self.error = "" # stores non-fatal errors only such as sounds missing. fatal errors will throw exceptions
        self.stop = False

    # recursively split the list of words into half, synthesize them one by one and merge them, just like merge sort
    # motivation: it is faster to merge two audio files with similar lengths
    def _recursive_synthesize(self, x, left, right):
        self.current_step += 1
        self.progress = self.current_step / self.steps_required * 0.9
        if self.stop:
            raise ProcessAbortedException("停止合成")
        if right - left == 1:
            i = x[left]
            if i == ".":
                return AudioSegment.silent(duration=350), []
            else:
                if i in XiSpeechSynthesizer.sounds:
                    l = len(XiSpeechSynthesizer.sounds[i])
                    return XiSpeechSynthesizer.sounds[i][randint(0, l - 1)], []
                elif str.isdigit(i[len(i) - 1]) and i[:len(i) - 1] in XiSpeechSynthesizer.sounds:
                    j = i[:len(i) - 1]
                    l = len(XiSpeechSynthesizer.sounds[j])
                    return XiSpeechSynthesizer.sounds[j][randint(0, l - 1)], []
                else:
                    if str.isdigit(i[len(i) - 1]):
                        return AudioSegment.empty(), ["找不到音节 " + i[:len(i) - 1]]
                    else:
                        return AudioSegment.empty(), ["找不到音节 " + i]
        else:
            mid = (left + right) // 2
            left_audio, left_error = self._recursive_synthesize(x, left, mid)
            right_audio, right_error = self._recursive_synthesize(x, mid, right)
            return left_audio + right_audio, left_error + right_error

    def _get_raw_audio(self, x):
        self.progress = 0.0
        x = XiSpeechSynthesizer.convert_to_simplified.convert(x)  # convert text to simplified chinese
        # MODE 1: convert numbers to chinese characters. can convert decimal and negative numbers correctly.
        x = sub(XiSpeechSynthesizer.regex, lambda m: an2cn(m.group()), x)
        # MODE 2: convert numbers to chinese characters. can convert fractional numbers and dates correctly.
        # x = transform(x, "an2cn")  # convert numbers to chinese characters
        x = x.translate(XiSpeechSynthesizer.translation)  # convert all punctuations to full stops.
        x = x.lower()
        x = pinyin(x, style=Style.TONE3)
        x = XiSpeechSynthesizer.reshape_array(x)
        # audio = AudioSegment.empty()
        length = len(x)
        if length == 0:
            self.progress = 0.9
            return AudioSegment.empty(), []
        self.steps_required = 2 ** (floor(log2(length)) + 1) - 1 + 2 * (length - 2 ** floor(log2(length)))
        self.current_step = 0
        audio, error_message = self._recursive_synthesize(x, 0, length)
        audio += AudioSegment.silent(duration=50)
        self.progress = 0.9
        return audio, error_message

    def create_and_store_encoded_audio(self, x):
        try:
            audio, error = self._get_raw_audio(x)
            self.result = b64encode(audio.export(bitrate="128k").read()).decode('ascii')
            self.error = XiSpeechSynthesizer.list_to_string(error)
        except ProcessAbortedException as e:
            self.result = ""
            self.error = str(e)
        finally:
            self.progress = 1.0

    def create_and_export_audio(self, x):
        try:
            audio, error = self._get_raw_audio(x)
            audio.export("temp.mp3")
        except ProcessAbortedException:
            pass
        finally:
            self.progress = 1.0

    @staticmethod
    def is_number(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    @staticmethod
    def convert_to_number(x):
        try:
            number = float(x)
            if number.is_integer():
                return int(number)
            return number
        except ValueError:
            print("无法将 {0} 转为数字;".format(x))
            return 0

    @staticmethod
    def reshape_array(x):
        result = []
        for i in x:
            result += i[0].split()
        return result

    @staticmethod
    def list_to_string(x):
        return ';'.join(x)
