__author__ = 'whyjay'
import sys
import os
import imp
import codecs

def valid_d():
    # number of arguments should be 5. file_name, option, csv, s2p, csv
    if len(sys.argv) != 5:
        print "Argument error : need 3 files(csv, s2p, csv) to do de-embedding."
        return 0

    # file format should be csv, s2p, csv
    if sys.argv[2].split(".")[-1] != "csv" or \
        sys.argv[3].split(".")[-1] != "s2p" or \
        sys.argv[4].split(".")[-1] != "csv":
        print "File format error : 3 input files should have csv, s2p and csv format (in order)."
        return 0

    # file existence check
    for i in range(2,5):
        if not check_existence(sys.argv[i]):
            return 0

    return 1

def valid_c(argv):
    # number of arguments should be 3. file_name, option, s2p/mdif
    if len(argv) != 3:
        print "Argument error : please specifiy input file (either s2p or mdif format)"
        return 0

    # file format should be s2p or mdif
    if argv[2].split(".")[-1] != "s2p" and argv[2].split(".")[-1] != "mdif":
        print "File format error : input file should have s2p or mdif format"
        return 0

    # file existence check
    if not check_existence(argv[2]):
        return 0

    return 1

def check_existence(name):
    if not os.path.exists("./input/{}".format(name)):
        print "File does not exist : {}".format(name)
        print "please check if the file is in './input' folder"
        return 0
    return 1

def help_message():
    print " "
    print "1) To convert file format, run with '-c' option as follows : "
    print " "
    print ">> python run.py -c filename.s2p"
    print " or "
    print ">> python run.py -c file_name.mdif"
    print " "
    print "2) To de-embed, run with '-d' option as follows : "
    print " "
    print ">> python run.py -d left_pad_name.csv file_name.s2p right_pad_name.csv"
    print " "
    print "** Caution **"
    print "* all input data should be in './input' folder"
    print "* output data will be created at './output' folder"
    print " "

if __name__ == "__main__":
    in_dir = "./input"
    out_dir = "./output"

    parser = imp.load_source('parser', 'parser.py').Parser()
    converter = imp.load_source('converter', 'converter.py').Converter()
    de_embeder = imp.load_source('de_embeder', 'de_embeder.py').DeEmbeder()

    op = sys.argv[1]

    if op == "-d" or op == "d" or op == "-D" or op == "D":
        if valid_d():
            result_dic = de_embeder.de_embed(*map(parser.parse, sys.argv[2:5]))
            result_str = converter.dic2s2p(result_dic)
            new_name = "./output/de_embeded_{}.s2p".format(result_dic["name"])

            with codecs.open(new_name, encoding='utf-8', mode='w') as fp:
                fp.write(result_str)
            print "De-embedding complete! the output file is .."
            print " ./output/{}".format(new_name)

    elif op == "-c" or op == "c" or op == "-C" or op == "C":
        if valid_c(sys.argv):
            dic = parser.parse(sys.argv[2])
            converter.convert(dic)
            t = "s2p"
            if dic["type"] == "s2p":
                t = "mdif"
            print "Conversion complete! the output file is .."
            print " ./output/{}.{} ".format(dic["name"], t)

    elif op == "-h" or op == "h" or op == "-H" or op == "H":
        help_message()

    else:
        print "Wrong input"
        help_message()

