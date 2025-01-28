import base64

letters = "abcdefghijklmnopqrstuvwxyz"
letters_list = []

for letter in letters:
    letters_list.append(letter)


def decrypt_char(char, num):
    glob_offset = 2
    if char not in letters_list:
        return char

    char_num = letters_list.index(char)

    offset = (char_num - (num + glob_offset)) % len(letters_list)
    out = letters_list[offset]

    return out


def decrypt(inp):
    decoded_inp = base64.b64decode(inp).decode()
    response = ""

    for word in decoded_inp.split():
        for num, char in enumerate(word):
            response += decrypt_char(char, num)
        response += " "

    return response.strip()
