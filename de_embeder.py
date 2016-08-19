__author__ = 'whyjay'
import numpy as np
from numpy.linalg import inv

z0 = 50/50

class DeEmbeder:
    # pad_in, s2p, pad_out are all dictionary
    def de_embed(self, pad_in, s2p, pad_out):

        left_mat = pad_in["data"][0]["body"]
        right_mat = pad_out["data"][0]["body"]

        for sec_idx in range(len(s2p["data"])):

            section = s2p["data"][sec_idx]

            for i in range(len(section["body"])):

                left = map(float, left_mat[i][1:])
                l_abcd = self.get_ABCD(left)

                center = map(float, section["body"][i][1:])
                c_abcd = self.get_ABCD(center)

                right = map(float, right_mat[i][1:])
                r_abcd = self.get_ABCD(right)

                [[A, B], [C, D]] = inv(l_abcd).dot(c_abcd).dot(inv(r_abcd))
                [s11, s21, s12, s22] = self.abcd2s(A, B, C, D)
                section["body"][i][1:] = \
                    [s11.real, s11.imag, s21.real, s21.imag, s12.real, s12.imag, s22.real, s22.imag]

        return s2p

    def get_ABCD(self, row):
        s11 = np.complex(*row[0:2])
        s21 = np.complex(*row[2:4])
        s12 = np.complex(*row[4:6])
        s22 = np.complex(*row[6:8])

        A = ((1+s11)*(1-s22) + s12 * s21)/(2 * s21)
        B = z0*((1+s11)*(1+s22) - s12 * s21)/(2 * s21)
        C = 1/z0*((1-s11)*(1-s22) - s12 * s21)/(2 * s21)
        D = ((1-s11)*(1+s22) + s12 * s21)/(2 * s21)

        return [[A, B], [C, D]]

    def abcd2s(self, A, B, C, D):
        denominator = A + B/z0 + C*z0 + D
        s11 = (A + B/z0 - C*z0 - D)/denominator
        s21 = 2/denominator
        s12 = 2*(A*D - B*C)/denominator
        s22 = (-A + B/z0 - C*z0 + D)/denominator
        return [s11, s21, s12, s22]

# example code
if __name__ == "__main__":

    parser = imp.load_source('parser', 'parser.py').Parser()
    converter = imp.load_source('converter', 'converter.py').Converter()
    de_embeder = imp.load_source('de_embeder', 'de_embeder.py').DeEmbeder()

    fname = "Pad_in.csv"
    pad_in = parser.parse(fname)

    fname = "data_in.s2p"
    sample = parser.parse(fname)

    fname = "Pad_out.csv"
    pad_out = parser.parse(fname)

    result_dic = de_embeder.de_embed(pad_in, sample, pad_out)
    result_str = converter.dic2s2p(result_dic)

    with open("./output/example.s2p", "w") as fp:
        fp.write(result_str)
