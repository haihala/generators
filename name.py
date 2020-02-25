import random, sys, argparse

# Y is in both because sometimes it acts like a consonant
letters = ["aeiou", "bcdfghjklmnpqrstvwxyz"]

LEN_MEAN = 6
LEN_STD = 2
MIN_LEN = 3
CHUNK_LEN_BIAS = -0.2
CHUNK_LEN_CONSONANT_BIAS = -0.2
APOSTROPHE_CHANCE = 0.2
RARE_LETTERS = "xqz"

def generate():
    for _ in range(50):
        size = max(MIN_LEN, random.normalvariate(LEN_MEAN, LEN_STD))
        bit_type = bool(round(random.random()))
        name = ""
        while size>0:
            bit_type = not bit_type
            bit_len = 1+max(0, min(1, round(random.random()+CHUNK_LEN_BIAS+CHUNK_LEN_CONSONANT_BIAS*int(bit_type))))
            size -= bit_len
            
            for _ in range(bit_len):
                letter = random.choice(letters[int(bit_type)])
                if letter in RARE_LETTERS:
                    letter = random.choice(letters[int(bit_type)])
                name += letter

            if bit_type and bit_len>1 and random.random() < APOSTROPHE_CHANCE:
                end = name[-1]
                name = name[:-1]
                name += "'"+end

        print(name)


if __name__ == "__main__":
    generate()