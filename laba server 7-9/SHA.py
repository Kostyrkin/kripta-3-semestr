class SHA:
    def __init__(self):
        self.K_256 = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        self.H_256 = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
        self.K_512 = [
            0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
            0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
            0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
            0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
            0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
            0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
            0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
            0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
            0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
            0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
            0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
            0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
            0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
            0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
            0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
            0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
            0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
            0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
            0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
            0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
        ]
        self.H_512 = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
                      0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]

    def SHA_function(self, Mes, flag):
        if flag == "1":
            return self.SHA_512(Mes)
        elif flag == "2":
            return self.SHA_256(Mes)

    def SHA_256(self, M):
        M_512 = []
        M_32 = []
        if len(M) > pow(2, 64):
            return "Сообщение больше допустимого значения. Введите другое сообщение"
        for i in range(0, len(M), 512):
            if len(M) - i < 512:
                M_512.append(
                    M[i:] + "1" + "0" * (pow((448 - len(M[i:]) - 1), 1, 512)) + "0" * (64 - len(bin(len(M))[2:])) + bin(
                        len(M))[2:])
                if len(M) - i > 447:
                    M_512.append(M_512[-1][512:])
                    M_512[-2] = M_512[-2][:512]
            else:
                M_512.append(M[i:i + 512])
        for i in M_512:
            vm = []
            for j in range(0, 512, 32):
                vm.append(i[j:j + 32])
            M_32.append(vm)
        for i in M_32:
            W_t = []
            # 1 этап
            for j in i:
                W_t.append(j)
            for j in range(16, 64):
                q_1 = self.Q_1_256(W_t[j - 2]) + int(str(W_t[j - 7]), 2) + self.Q_0_256(W_t[j - 15]) + int(
                    str(W_t[j - 16]), 2)
                q_1 = bin(pow(q_1, 1, pow(2, 32)))[2:].zfill(32)
                W_t.append(q_1)
            for j in range(len(W_t)):
                W_t[j] = int(W_t[j], 2)
            # 2 этап
            a = self.H_256[0]
            b = self.H_256[1]
            c = self.H_256[2]
            d = self.H_256[3]
            e = self.H_256[4]
            f = self.H_256[5]
            g = self.H_256[6]
            h = self.H_256[7]

            # 3 этап
            for t in range(64):
                T_1 = h + self.Z_1_256(bin(e)[2:].zfill(32)) + self.Ch(bin(e)[2:].zfill(32), bin(f)[2:].zfill(32),
                                                                       bin(g)[2:].zfill(32)) + self.K_256[t] + W_t[t]
                T_1 = pow(T_1, 1, pow(2, 32))
                T_2 = self.Z_0_256(bin(a)[2:].zfill(32)) + self.Maj(bin(a)[2:].zfill(32), bin(b)[2:].zfill(32),
                                                                    bin(c)[2:].zfill(32))
                T_2 = pow(T_2, 1, pow(2, 32))
                h = g
                g = f
                f = e
                e = pow(d + T_1, 1, pow(2, 32))
                d = c
                c = b
                b = a
                a = pow(T_1 + T_2, 1, pow(2, 32))
            # 4 этап
            self.H_256[0] = pow(a + self.H_256[0], 1, pow(2, 32))
            self.H_256[1] = pow(b + self.H_256[1], 1, pow(2, 32))
            self.H_256[2] = pow(c + self.H_256[2], 1, pow(2, 32))
            self.H_256[3] = pow(d + self.H_256[3], 1, pow(2, 32))
            self.H_256[4] = pow(e + self.H_256[4], 1, pow(2, 32))
            self.H_256[5] = pow(f + self.H_256[5], 1, pow(2, 32))
            self.H_256[6] = pow(g + self.H_256[6], 1, pow(2, 32))
            self.H_256[7] = pow(h + self.H_256[7], 1, pow(2, 32))
        H = ""
        H_i = ""
        for i in self.H_256:
            H = H + hex(i)[2:].zfill(8)
        for i in range(len(H)):
            H_i = H_i + bin(int(H[i], 16))[2:].zfill(4)
        return H_i


    def SHA_512(self, M):
        M_1024 = []
        M_64 = []
        if len(M) > pow(2, 128):
            return "Сообщение больше допустимого значения. Введите другое сообщение"
        for i in range(0, len(M), 1024):
            if len(M) - i < 1024:
                M_1024.append(
                    M[i:] + "1" + "0" * (pow((896-len(M[i:])-1), 1, 1024)) + "0" * (128 - len(bin(len(M))[2:])) + bin(len(M))[2:])
                if len(M) - i > 895:
                    M_1024.append(M_1024[-1][1024:])
                    M_1024[-2] = M_1024[-2][:1024]
            else:
                M_1024.append(M[i:i + 1024])
        for i in M_1024:
            vm = []
            for j in range(0, 1024, 64):
                vm.append(i[j:j + 64])
            M_64.append(vm)
        for i in M_64:
            W_t = []
            # 1 этап
            for j in i:
                W_t.append(j)
            for j in range(16, 80):
                q_1 = self.Q_1_512(W_t[j - 2]) + int(str(W_t[j - 7]), 2) + self.Q_0_512(W_t[j - 15]) + int(
                    str(W_t[j - 16]), 2)
                q_1 = bin(pow(q_1, 1, pow(2, 64)))[2:].zfill(64)
                W_t.append(q_1)
            for j in range(len(W_t)):
                W_t[j] = int(W_t[j], 2)
            # 2 этап
            a = self.H_512[0]
            b = self.H_512[1]
            c = self.H_512[2]
            d = self.H_512[3]
            e = self.H_512[4]
            f = self.H_512[5]
            g = self.H_512[6]
            h = self.H_512[7]
            # 3 этап
            for t in range(80):
                T_1 = h + self.Z_1_512(bin(e)[2:].zfill(64)) + self.Ch(bin(e)[2:].zfill(64), bin(f)[2:].zfill(64),
                                                                       bin(g)[2:].zfill(64)) + self.K_512[t] + W_t[t]
                T_1 = pow(T_1, 1, pow(2, 64))
                T_2 = self.Z_0_512(bin(a)[2:].zfill(64)) + self.Maj(bin(a)[2:].zfill(64), bin(b)[2:].zfill(64),
                                                                    bin(c)[2:].zfill(64))
                T_2 = pow(T_2, 1, pow(2, 64))
                h = g
                g = f
                f = e
                e = pow(d + T_1, 1, pow(2, 64))
                d = c
                c = b
                b = a
                a = pow(T_1 + T_2, 1, pow(2, 64))
            # 4 этап
            self.H_512[0] = pow(a + self.H_512[0], 1, pow(2, 64))
            self.H_512[1] = pow(b + self.H_512[1], 1, pow(2, 64))
            self.H_512[2] = pow(c + self.H_512[2], 1, pow(2, 64))
            self.H_512[3] = pow(d + self.H_512[3], 1, pow(2, 64))
            self.H_512[4] = pow(e + self.H_512[4], 1, pow(2, 64))
            self.H_512[5] = pow(f + self.H_512[5], 1, pow(2, 64))
            self.H_512[6] = pow(g + self.H_512[6], 1, pow(2, 64))
            self.H_512[7] = pow(h + self.H_512[7], 1, pow(2, 64))
        H = ""
        H_i = ""
        for i in self.H_512:
            H = H + hex(i)[2:].zfill(16)
        for i in range(len(H)):
            H_i = H_i + bin(int(H[i], 16))[2:].zfill(4)
        return H_i

    def Ch(self, x, y, z):
        x_o = ""
        ch = ""
        x = str(x)
        y = str(y)
        z = str(z)
        for i in range(len(x)):
            if x[i] == "1":
                x_o += "0"
            else:
                x_o += "1"
        for i in range(len(x)):
            x_y = int(x[i]) * int(y[i])
            x_o_z = int(x_o[i]) * int(z[i])
            ch += str(x_y ^ x_o_z)
        return int(ch, 2)

    def Maj(self, x, y, z):
        maj = ""
        x = str(x)
        y = str(y)
        z = str(z)
        for i in range(len(x)):
            x_y = int(x[i]) * int(y[i])
            x_z = int(x[i]) * int(z[i])
            y_z = int(y[i]) * int(z[i])
            maj += str(x_y ^ x_z ^ y_z)
        return int(maj, 2)

    def Z_0_256(self, x):
        z = ""
        x = str(x)
        a = x[-2:] + x[:-2]
        b = x[-13:] + x[:-13]
        c = x[-22:] + x[:-22]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Z_1_256(self, x):
        z = ""
        x = str(x)
        a = x[-6:] + x[:-6]
        b = x[-11:] + x[:-11]
        c = x[-25:] + x[:-25]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Q_0_256(self, x):
        z = ""
        x = str(x)
        a = x[-7:] + x[:-7]
        b = x[-18:] + x[:-18]
        c = "0" * 3 + x[:-3]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Q_1_256(self, x):
        z = ""
        x = str(x)
        a = x[-17:] + x[:-17]
        b = x[-19:] + x[:-19]
        c = "0" * 10 + x[:-10]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Z_0_512(self, x):
        z = ""
        x = str(x)
        a = x[-28:] + x[:-28]
        b = x[-34:] + x[:-34]
        c = x[-39:] + x[:-39]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Z_1_512(self, x):
        z = ""
        x = str(x)
        a = x[-14:] + x[:-14]
        b = x[-18:] + x[:-18]
        c = x[-41:] + x[:-41]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Q_0_512(self, x):
        z = ""
        x = str(x)
        a = x[-1:] + x[:-1]
        b = x[-8:] + x[:-8]
        c = "0"*7 + x[:-7]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)

    def Q_1_512(self, x):
        z = ""
        x = str(x)
        a = x[-19:] + x[:-19]
        b = x[-61:] + x[:-61]
        c = "0" * 6 + x[:-6]
        for i in range(len(a)):
            z += str(int(a[i]) ^ int(b[i]) ^ int(c[i]))
        return int(z, 2)