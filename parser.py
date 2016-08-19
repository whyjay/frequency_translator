__author__ = 'whyjay'
import imp
import codecs


class Parser:

    def parse(self, fname):
        base_dir = "./input"
        file_dir = "{}/{}".format(base_dir, fname)

        with codecs.open(file_dir, encoding='utf-8', mode='r') as fp:
            raw = fp.read()

        [name, type] = fname.split("/")[-1].split(".")
        dic = dict()
        dic["name"] = name
        dic["type"] = type

        if type == "s2p":
            dic["data"] = self.parse_s2p(raw)
        # csv-formatted s2p file for embedding
        elif type == "csv":
            dic["data"] = self.parse_csv(raw)
        elif type == "mdif":
            dic["data"] = self.parse_mdif(raw)
        else:
            print "Not proper file type"
            return None

        return dic

    def parse_s2p(self, raw):
        dics = []
        i = -1

        for line in raw.split("\r\n"):
            if (line == "") or ("END" in line) or ("Vgs" in line):
                continue
            elif "BEGIN" in line:    # section begin
                i += 1
                dics.append({"header":
                                 {"vgs": None,
                                  "igs": None,
                                  "vds": None,
                                  "ids": None,
                                  "option": None}, # GHz S RI R 50
                             "body": []})
            elif line[:3] == "!#\t":
                hdr = line.split("\t")[1:]

                dics[i]["header"]["vgs"] = hdr[0]
                dics[i]["header"]["igs"] = hdr[1]
                dics[i]["header"]["vds"] = hdr[2]
                dics[i]["header"]["ids"] = hdr[3]

            elif line[:2] == "# ":
                dics[i]["header"]["option"] = line[2:]

            else:
                # dics[i]["body"].append(map(float, line.split("\t")))
                dics[i]["body"].append(line.split("\t"))

        return dics

    def parse_csv(self, raw):
        dics = []

        dics.append({"header": None, "body": []})

        for line in raw.split("\r")[46:-1]:
            row = line[1:].split(",")

            scale = row[0][-3:]
            row[0] = row[0][:-4]

            # row = map(float, row)
            if scale == "MHz":
                row[0] = str(float(row[0])/1000)

            dics[0]["body"].append(row)

        return dics

    def parse_mdif(self, raw):
        dics = []
        i = -1

        for line in raw.split("\r\n"):
            if "Id" in line:
                i += 1
                ids = line.split(" = ")[1][:-3]
                dics.append({"header":
                                 {"vgs": None,
                                  "igs": None,
                                  "vds": None,
                                  "ids": ids,
                                  "option": None}, # GHz S RI R 50
                             "body": []})
            elif "Ig" in line:
                igs = line.split(" = ")[1][:-3]
                dics[i]["header"]["igs"] = igs
            elif "Vds" in line:
                vds = line.split(" = ")[1]
                dics[i]["header"]["vds"] = vds
            elif "Vgs" in line:
                vgs = line.split(" = ")[1]
                dics[i]["header"]["vgs"] = vgs
            elif "# " in line:
                opt = line[4:-2]
                # s2p => GHz, but mdif => GHZ. so change it to lowercase
                dics[i]["header"]["option"] = opt[:2] + opt[2].lower() + opt[3:]
            elif self.is_number(line[0]):
                # dics[i]["body"].append(map(float, line.split(" ")))
                dics[i]["body"].append(line.split(" "))
            else:
                continue

        return dics

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False


# example code
if __name__ == "__main__":
    p = imp.load_source("parser", "parser.py").Parser()

    s2p_fname = "sample.s2p"
    s2p = p.parse(s2p_fname)
    #print s2p

    csv_fname = "Pad_in.csv"
    csv = p.parse(csv_fname)
    #print csv

    mdif_fname = "sample.mdif"
    mdif = p.parse(mdif_fname)
    #print mdif
