import string
# from Levenshtein import distance
from weighted_levenshtein import damerau_levenshtein
from signals import *


if __name__ == '__main__':

    s = string.ascii_uppercase + string.ascii_lowercase + "_{}1234567890'\",!?"

    all_letters_dict = {}
    for letter in s:
        all_letters_dict[letter] = "{0:08b}".format(ord(letter))

    index = 0
    word_arr = []
    for arr in second_enc:
        counter = {}
        for letter in all_letters_dict:
            counter[letter] = 0
        for letter, letter_binary in all_letters_dict.items():
            for sub_arr in arr:
                if len(sub_arr) >= 4:
                    counter[letter] += damerau_levenshtein(letter_binary, "".join(map(str, sub_arr)))
                    # counter[letter] += distance(letter_binary, "".join(map(str, sub_arr))[::-1])

        # print({k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)})
        rev = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1])}
        # print(rev)
        min_c = float('inf')
        word_arr.append([])
        for letter, v in rev.items():
            if v <= min_c:
                word_arr[index].append(letter)
                min_c = v
                print(index, letter)
        index += 1
        print()
        print()
    print(word_arr)
