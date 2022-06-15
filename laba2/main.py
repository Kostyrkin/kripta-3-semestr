class BASE:
    def __init__(self, txt):
        self.text = txt
        self.bait_code = ""
        self.cod_text = ""
        self.dict_64 = [
                   ['A', '000000'], ['B', '000001'], ['C', '000010'], ['D', '000011'], ['E', '000100'], ['F', '000101'],
                   ['G', '000110'], ['H', '000111'], ['I', '001000'], ['J', '001001'], ['K', '001010'], ['L', '001011'],
                   ['M', '001100'], ['N', '001101'], ['O', '001110'], ['P', '001111'], ['Q', '010000'], ['R', '010001'],
                   ['S', '010010'], ['T', '010011'], ['U', '010100'], ['V', '010101'], ['W', '010110'], ['X', '010111'],
                   ['Y', '011000'], ['Z', '011001'], ['a', '011010'], ['b', '011011'], ['c', '011100'], ['d', '011101'],
                   ['e', '011110'], ['f', '011111'], ['g', '100000'], ['h', '100001'], ['i', '100010'], ['j', '100011'],
                   ['k', '100100'], ['l', '100101'], ['m', '100110'], ['n', '100111'], ['o', '101000'], ['p', '101001'],
                   ['q', '101010'], ['r', '101011'], ['s', '101100'], ['t', '101101'], ['u', '101110'], ['v', '101111'],
                   ['w', '110000'], ['x', '110001'], ['y', '110010'], ['z', '110011'], ['0', '110100'], ['1', '110101'],
                   ['2', '110110'], ['3', '110111'], ['4', '111000'], ['5', '111001'], ['6', '111010'], ['7', '111011'],
                   ['8', '111100'], ['9', '111101'], ['+', '111110'], ['/', '111111']]
        self.dict_32 = [
                   ['A', '00000'], ['B', '00001'], ['C', '00010'], ['D', '00011'], ['E', '00100'], ['F', '00101'],
                   ['G', '00110'], ['H', '00111'], ['I', '01000'], ['J', '01001'], ['K', '01010'], ['L', '01011'],
                   ['M', '01100'], ['N', '01101'], ['O', '01110'], ['P', '01111'], ['Q', '10000'], ['R', '10001'],
                   ['S', '10010'], ['T', '10011'], ['U', '10100'], ['V', '10101'], ['W', '10110'], ['X', '10111'],
                   ['Y', '11000'], ['Z', '11001'], ['2', '11010'], ['3', '11011'], ['4', '11100'], ['5', '11101'],
                   ['6', '11110'], ['7', '11111']]

    def encode64(self):
        self.ascii_cod()
        fl = 0
        if len(self.bait_code) % 24 != 0:
            if len(self.bait_code) % 24 == 16:
                while True:
                    if len(self.bait_code) % 6 != 0:
                        self.bait_code += "0"
                    else:
                        break
                fl = 1
            else:
                while True:
                    if len(self.bait_code) % 6 != 0:
                        self.bait_code += "0"
                    else:
                        break
                fl = 2
        for i in range(0, len(self.bait_code), 6):
            for j in self.dict_64:
                if j[1] == self.bait_code[i:i+6]:
                    self.cod_text += j[0]
                    break
        self.cod_text += "=" * fl
        self.write_file_encode("BASE64")

    def decode64(self):
        fl = 0
        text_m = self.text
        if self.text[-2:] == "==":
            fl = 2
            self.text = self.text[:-2]
        elif self.text[-1:] == "=":
            fl = 1
            self.text = self.text[:-1]
        for i in range(len(self.text)):
            for j in self.dict_64:
                if j[0] == self.text[i]:
                    self.bait_code += j[1]
                    break
        while True:
            if len(self.bait_code) % 24 != 0:
                self.bait_code += "0"
            else:
                if fl != 0:
                    self.bait_code = self.bait_code[:-8*fl]
                break
        self.text = text_m
        self.ascii_decod()
        self.write_file_decode("BASE64")

    def encode32(self):
        self.ascii_cod()
        fl = 0
        if len(self.bait_code) % 40 != 0:
            if len(self.bait_code) % 5 == 1:
                self.bait_code += "0000"
                fl = 4
            elif len(self.bait_code) % 5 == 2:
                self.bait_code += "000"
                fl = 1
            elif len(self.bait_code) % 5 == 3:
                self.bait_code += "00"
                fl = 6
            elif len(self.bait_code) % 5 == 4:
                self.bait_code += "0"
                fl = 3

        for i in range(0, len(self.bait_code), 5):
            for j in self.dict_32:
                if j[1] == self.bait_code[i:i + 5]:
                    self.cod_text += j[0]
                    break
        self.cod_text += "=" * fl
        self.write_file_encode("BASE32")

    def decode32(self):
        fl = 0
        text_m = self.text
        if self.text[-6:] == "======":
            fl = 2
            self.text = self.text[:-6]
        elif self.text[-4:] == "====":
            fl = 4
            self.text = self.text[:-4]
        elif self.text[-3:] == "===":
            fl = 1
            self.text = self.text[:-3]
        elif self.text[-3:] == "=":
            fl = 3
            self.text = self.text[:-1]
        for i in range(len(self.text)):
            for j in self.dict_32:
                if j[0] == self.text[i]:
                    self.bait_code += j[1]
                    break
        if fl != 0:
            self.bait_code = self.bait_code[:-fl]
        self.text = text_m
        self.ascii_decod()
        self.write_file_decode("BASE32")

    def ascii_cod(self):
        for i in range(len(self.text)):
            a = str(bin(ord(self.text[i])))
            if len(a[2:]) % 8 != 0:
                a = (8 - len(a[2:]))*"0" + a[2:]
            self.bait_code += a

    def ascii_decod(self):
        for j in range(0, len(self.bait_code), 8):
            self.cod_text += str(chr(int(self.bait_code[j:j+8], 2)))

    def write_file_encode(self, bas):
        with open('encript.txt', 'w', encoding='utf-8') as file:
            file.write(f"Закодированное слово {self.text} в {bas}: {self.cod_text}")

    def write_file_decode(self, bas):
        with open('decript.txt', 'w', encoding='utf-8') as file:
            file.write(f"Декадированное слово {self.text} в {bas}: {self.cod_text}")


if __name__ == '__main__':
    flag1 = int(input("Действия:\n1)Кодирование\n2)Декодирование\n"))
    flag2 = int(input("Метод:\n1)BASE64\n2)BASE32\n"))
    flag3 = input("Ввод:\n1)С клавиатуры\n2)С файла\n")
    if flag3 == "1":
        text = input("Текст:")
    else:
        listed = open('file.txt', 'r')
        text = listed.readline()
    if flag1 == 1 and flag2 == 1:
        obj = BASE(text)
        obj.encode64()
    elif flag1 == 1 and flag2 == 2:
        obj = BASE(text)
        obj.encode32()
    elif flag1 == 2 and flag2 == 1:
        obj = BASE(text)
        obj.decode64()
    elif flag1 == 2 and flag2 == 2:
        obj = BASE(text)
        obj.decode32()
