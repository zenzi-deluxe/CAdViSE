import os
import fnmatch
import json
from p1203Pv_extended.p1203Pv_extended import P1203Pv_codec_extended
from itu_p1203 import P1203Standalone

# pattern = "QOE_*[!out].json"
pattern = "*[!out].json"

def compute_qoe(dir, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    print(matches)
    for el in matches:
        with open(el, "r") as in_fp:
            results = P1203Standalone(json.load(in_fp), Pv=P1203Pv_codec_extended).calculate_complete()
            json_out_file = "{}".format("{}_out.{}".format(".".join(el.split(".")[:-1]), el.split(".")[-1]))
            with open(json_out_file, 'w') as outfile:
                json.dump(results, outfile, indent=4)
                
def change_screen_res(screen_res, dir, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    print(matches)
    json_in_file = None
    for el in matches:
        with open(el, "r") as in_fp:
            json_in_file = json.load(in_fp)
            json_in_file["IGen"]["displaySize"] = screen_res
        with open(el, 'w') as outfile:
            json.dump(json_in_file, outfile, indent=4)


import argparse

parser = argparse.ArgumentParser(description='Compute QoE recursively in the given path.')
# parser.add_argument('--maxb', type=int, default=1, help='MaxB ABR will be included in the results.')
# parser.add_argument('--bola', type=int, default=1, help='Bola ABR will be included in the results.')
# parser.add_argument('--sara', type=int, default=1, help='Sara ABR will be included in the results.')
# parser.add_argument('--bba', type=int, default=1, help='BBA ABR will be included in the results.')
# parser.add_argument('--mcom', type=int, default=0, help='MCOM ABR will be included in the results.')
# parser.add_argument('--mc', type=int, default=1, help='MCOM Plugin will be included in the results.')
# parser.add_argument('--ss', type=int, default=1, help='Custom Segment Size-optimized MCOM plugin will be included in the results (for Bola and Sara).')
parser.add_argument('--path', type=str, default="/home/zenzi/Documents/CAdViSE/logs", help='Path containing the results.')
parser.add_argument('--screen', type=str, default="", help='Edit screen resolution (displaySize) parameter in input json files.')
parser.add_argument('--qoe', type=bool, default=False, help='Compute QoE recursively in the given path.')

args = parser.parse_args()

compute_qoe(args.path)
# print(os.path.isfile("/home/zenzi/Documents/CAdViSE/logs/cascade/sara-mcom/1681716080_3.122.127.168/ASTREAM_LOGS/QOE_INPUT_2023-04-17.07_26_07.json"))
