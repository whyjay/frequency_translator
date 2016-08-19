__author__ = 'whyjay'


class Converter:
    def convert(self, dic):
        base_dir = "./output"

        result = ""
        save_type = ""

        if dic["type"] == "s2p":
            result = self.dic2mdif(dic)
            save_type = "mdif"
        elif dic["type"] == "mdif":
            result = self.dic2s2p(dic)
            save_type = "s2p"

        save_dir = "{}/{}.{}".format(base_dir, dic["name"], save_type)
        with open(save_dir, "w") as fp:
            fp.write(result)

    def dic2mdif(self, dic):
        result = "REM MDIF format file containing S parameter data (Real and Imag)\r\n"

        for i in range(len(dic["data"])):

            hdr = dic["data"][i]["header"]
            hdr_str = "REM\r\n"
            hdr_str += "REM Id = {} mA\r\n".format(hdr["ids"])
            hdr_str += "REM Ig = {} mA\r\n".format(hdr["igs"])
            hdr_str += "VAR Vgs = {}\r\n".format(hdr["vgs"])
            hdr_str += "VAR Vds = {}\r\n".format(hdr["vds"])
            hdr_str += "BEGIN ACDATA\r\n"

            opt = hdr["option"][:2] + hdr["option"][2].upper() + hdr["option"][3:]
            hdr_str += "# ( {} )\r\n".format(opt)
            hdr_str += "% F n11x n11y n21x n21y n12x n12y n22x n22y\r\n"

            body = dic["data"][i]["body"]
            body_str = ""

            for row in body:
                body_str += "{} {} {} {} {} {} {} {} {}\r\n".format(*row)

            result += hdr_str + body_str + "END\r\n"

        return result[:-2]

    def dic2s2p(self, dic):
        result = ""

        for i in range(len(dic["data"])):

            hdr = dic["data"][i]["header"]
            hdr_str = "BEGIN ACDATA\r\n"
            hdr_str += "!# (VmA)\tVgs\tIgs\tVds\tIds\r\n"
            hdr_str += "!#\t{}\t{}\t{}\t{}\r\n".format(hdr["vgs"], hdr["igs"], hdr["vds"], hdr["ids"])
            hdr_str += "# {}\r\n".format(hdr["option"])

            body = dic["data"][i]["body"]
            body_str = ""

            for row in body:
                body_str += "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\r\n".format(*row)

            result += hdr_str + body_str + "END ACDATA\r\n"

        return result[:-2]


# example code
if __name__ == "__main__":

    parser = imp.load_source('parser', 'parser.py').Parser()
    converter = imp.load_source('converter', 'converter.py').Converter()

    fname = "sample.s2p"
    d = parser.parse(fname)
    converter.convert(d)

    fname = "sample.mdif"
    d = parser.parse(fname)
    converter.convert(d)
