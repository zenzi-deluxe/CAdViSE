import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
import fnmatch
import collections
import os
import pandas as pd
import math
import seaborn as sns
import plotly.express as px

PATTERN = "x"

COLORS = ["tab:blue", "tab:orange", "gold", "tab:green", "cyan"]  # tab:purple
# COLORS = ['#2CBDFE', '#47DBCD', '#F3A0F2', '#F5B14C']
HATCHES = ['xx', '..', '//', 'oo']
ABRS = ["basic", "basic-mcom", "netflix", "netflix-mcom", "bola", "bola-mcom", "sara", "sara-mcom", "medusa", "medusa-mcom"]
VIDEOS = ["tos_5min", "tos_5min_end", "gameplay", "rally"]
ABRS_NEW_NAME = {"basic": "AGG", "basic-mcom": "AGG-mcom", "netflix": "BBA-0", "netflix-mcom": "BBA-0-mcom", "bola": "Bola", "bola-mcom": "Bola-mcom", "sara": "Sara", "sara-mcom": "Sara-mcom", "medusa": "Medusa", "medusa-mcom": "Medusa-MC"}
VIDEOS_NEW_NAME = {"tos_5min": "ToS1", "tos_5min_end": "ToS2", "gameplay": "Gameplay", "rally": "Rally"}
PLUGIN_NAME = "M" # Medusa

# Settings for boxplots
SHOWMEANS = True
SHOWFLIERS = False
WIDTH = 0.2

NET_TRACES = ["4G", "FCC"]

# Dictionary for gathering data from AStream - JSON logs
SEGMENT_NAME = 0
BITRATE = 1
CODEC = 2
VMAF = 3
SEGMENT_SIZE = 4
SEGMENT_DOWNLOAD_TIME = 5


def adjust_box_widths(g, fac):
    """
    Adjust the widths of a seaborn-generated boxplot.
    """

    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():

            # searching for PathPatches
            if isinstance(c, mpatches.PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # setting new width of median line
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])


def fetch_bitrates(jsons):
    bitrates = dict()
    for abr in jsons:
        bitrates[abr] = dict()
        for file in jsons[abr]:
            bits = []
            for segment_name in jsons[abr][file]:
                if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                    continue
                bits.append(jsons[abr][file][segment_name]["bitrate"] / 1000)  # bitrate is in bps -> / 1000 -> kbps
            bitrates[abr][file] = sum(bits)/len(bits)
    # print(bitrates)
    return bitrates
    
    
def fetch_videos_bitrates(jsons):
    bitrates = dict()
    for video in jsons:
        bitrates[video] = dict()
        for abr in jsons[video]:
            bitrates[video][abr] = dict()
            for file in jsons[video][abr]:
                bits = []
                for segment_name in jsons[video][abr][file]:
                    if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                        continue
                    bits.append(jsons[video][abr][file][segment_name]["bitrate"] / 1000)  # bitrate is in bps -> / 1000 -> kbps
                bitrates[video][abr][file] = sum(bits)/len(bits)
    # print(bitrates)
    return bitrates
    
def fetch_traces_videos_bitrates(jsons):
    bitrates = dict()
    for trace in jsons:
        bitrates[trace] = dict()
        for video in jsons[trace]:
            bitrates[trace][video] = dict()
            for abr in jsons[trace][video]:
                bitrates[trace][video][abr] = dict()
                for file in jsons[trace][video][abr]:
                    bits = []
                    for segment_name in jsons[trace][video][abr][file]:
                        if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                            continue
                        bits.append(jsons[trace][video][abr][file][segment_name]["bitrate"] / 1000)  # bitrate is in bps -> / 1000 -> kbps
                    bitrates[trace][video][abr][file] = sum(bits)/len(bits)
    # print(bitrates)
    return bitrates


def fetch_vmafs(jsons):
    vmafs = dict()
    for abr in jsons:
        vmafs[abr] = dict()
        for file in jsons[abr]:
            vmaf = []
            for segment_name in jsons[abr][file]:
                if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                    continue
                vmaf.append(jsons[abr][file][segment_name]["vmaf"])
            vmafs[abr][file] = vmaf
    return vmafs
    
def fetch_sizes(jsons):
    sizes = dict()
    for abr in jsons:
        sizes[abr] = dict()
        for file in jsons[abr]:
            size = []
            for segment_name in jsons[abr][file]:
                if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                    continue
                size.append(jsons[abr][file][segment_name]["segment_size"])
            sizes[abr][file] = size
    return sizes


def fetch_videos_vmafs(jsons):
    vmafs = dict()
    for video in jsons:
        vmafs[video] = dict()
        for abr in jsons[video]:
            vmafs[video][abr] = dict()
            for file in jsons[video][abr]:
                vmaf = []
                for segment_name in jsons[video][abr][file]:
                    if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                        continue
                    vmaf.append(jsons[video][abr][file][segment_name]["vmaf"])
                vmafs[video][abr][file] = vmaf
    return vmafs
    
def fetch_traces_videos_vmafs(jsons):
    vmafs = dict()
    for trace in jsons:
        vmafs[trace] = dict()
        for video in jsons[trace]:
            vmafs[trace][video] = dict()
            for abr in jsons[trace][video]:
                vmafs[trace][video][abr] = dict()
                for file in jsons[trace][video][abr]:
                    vmaf = []
                    for segment_name in jsons[trace][video][abr][file]:
                        if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                            continue
                        vmaf.append(jsons[trace][video][abr][file][segment_name]["vmaf"])
                    vmafs[trace][video][abr][file] = vmaf
    return vmafs
    
def fetch_videos_sizes(jsons):
    sizes = dict()
    for video in jsons:
        sizes[video] = dict()
        for abr in jsons[video]:
            sizes[video][abr] = dict()
            for file in jsons[video][abr]:
                size = []
                for segment_name in jsons[video][abr][file]:
                    if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                        continue
                    size.append(jsons[video][abr][file][segment_name]["segment_size"])
                sizes[video][abr][file] = size
    return sizes
    
def fetch_traces_videos_sizes(jsons):
    sizes = dict()
    for trace in jsons:
        sizes[trace] = dict()
        for video in jsons[trace]:
            sizes[trace][video] = dict()
            for abr in jsons[trace][video]:
                sizes[trace][video][abr] = dict()
                for file in jsons[trace][video][abr]:
                    size = []
                    for segment_name in jsons[trace][video][abr][file]:
                        if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                            continue
                        size.append(jsons[trace][video][abr][file][segment_name]["segment_size"])
                    sizes[trace][video][abr][file] = size
    return sizes


def fetch_stalls(jsons):
    start_up = dict()
    stalls = dict()
    stalls_duration = dict()
    for abr in jsons:
        start_up[abr] = dict()
        stalls[abr] = dict()
        stalls_duration[abr] = dict()
        for file in jsons[abr]:
            sd = []
            for pair in jsons[abr][file]["interruptions"]:
                sd.append(pair[1])
            if len(sd) == 0:
                stalls_duration[abr][file] = 0
            else:
                stalls_duration[abr][file] = sum(sd)
            stalls[abr][file] = len(sd)
            start_up[abr][file] = jsons[abr][file]["initial_buffering_duration"]
    return stalls, stalls_duration, start_up
    
    
def fetch_videos_stalls(jsons):
    start_up = dict()
    stalls = dict()
    stalls_duration = dict()
    for video in jsons:
        start_up[video] = dict()
        stalls[video] = dict()
        stalls_duration[video] = dict()
        for abr in jsons[video]:
            start_up[video][abr] = dict()
            stalls[video][abr] = dict()
            stalls_duration[video][abr] = dict()
            for file in jsons[video][abr]:
                sd = []
                for pair in jsons[video][abr][file]["interruptions"]:
                    sd.append(pair[1])
                if len(sd) == 0:
                    stalls_duration[video][abr][file] = 0
                else:
                    stalls_duration[video][abr][file] = sum(sd) / len(sd)
                stalls[video][abr][file] = len(sd)
                start_up[video][abr][file] = jsons[video][abr][file]["initial_buffering_duration"]
    return stalls, stalls_duration, start_up
    
    
def fetch_traces_videos_stalls(jsons):
    start_up = dict()
    stalls = dict()
    stalls_duration = dict()
    for trace in jsons:
        start_up[trace] = dict()
        stalls[trace] = dict()
        stalls_duration[trace] = dict()
        for video in jsons[trace]:
            start_up[trace][video] = dict()
            stalls[trace][video] = dict()
            stalls_duration[trace][video] = dict()
            for abr in jsons[trace][video]:
                start_up[trace][video][abr] = dict()
                stalls[trace][video][abr] = dict()
                stalls_duration[trace][video][abr] = dict()
                for file in jsons[trace][video][abr]:
                    sd = []
                    for pair in jsons[trace][video][abr][file]["interruptions"]:
                        sd.append(pair[1])
                    if len(sd) == 0:

                        stalls_duration[trace][video][abr][file] = 0
                    else:
                        stalls_duration[trace][video][abr][file] = sum(sd) / len(sd)
                    stalls[trace][video][abr][file] = len(sd)
                    start_up[trace][video][abr][file] = jsons[trace][video][abr][file]["initial_buffering_duration"]
    return stalls, stalls_duration, start_up


def fetch_stalls_from_files(files):
    start_up = dict()
    stalls = dict()
    stalls_duration = dict()
    for abr in files:
        stalls[abr] = dict()
        stalls_duration[abr] = dict()
        start_up[abr] = dict()
        for file in files[abr]:
            df = pd.read_csv(file)
            # print(df)
            df = df.reset_index()  # make sure indexes pair with number of rows
            stalls_d = [v for v in list(df['Stalls']) if v != 0]
            # Integrity check on stalls length
            if len(stalls_d) == 0:
                print("Error! No start-up time present in the csv file '{}' for '{}'.".format(file, abr))
                exit(-1)
            # Start up time
            start_up[abr][file] = stalls_d[0]
            # The first value is start-up time, all following values are actual stalls
            if len(stalls_d) > 1:
                stalls_duration[abr][file] = sum(stalls_d[1:])
                stalls[abr][file] = len(stalls_d) - 1
            else:
                stalls_duration[abr][file] = 0
                stalls[abr][file] = 0
    return stalls, stalls_duration, start_up


def fetch_codecs(jsons):
    codec_switches = dict()
    for abr in jsons:
        codec_switches[abr] = dict()
        for file in jsons[abr]:
            temp_codec = None
            temp_switch = 0
            for segment_name in jsons[abr][file]:
                if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                    continue
                if temp_codec is None:
                    temp_codec = jsons[abr][file][segment_name]["codec"]
                    continue
                if jsons[abr][file][segment_name]["codec"] != temp_codec:
                    temp_switch += 1
                    temp_codec = jsons[abr][file][segment_name]["codec"]
            codec_switches[abr][file] = temp_switch
    return codec_switches
    
    
def fetch_videos_codecs(jsons):
    codec_switches = dict()
    for video in jsons:
        codec_switches[video] = dict()
        for abr in jsons[video]:
            codec_switches[video][abr] = dict()
            for file in jsons[video][abr]:
                temp_codec = None
                temp_switch = 0
                for segment_name in jsons[video][abr][file]:
                    if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                        continue
                    if temp_codec is None:
                        temp_codec = jsons[video][abr][file][segment_name]["codec"]
                        continue
                    if jsons[video][abr][file][segment_name]["codec"] != temp_codec:
                        temp_switch += 1
                        temp_codec = jsons[video][abr][file][segment_name]["codec"]
                codec_switches[video][abr][file] = temp_switch
    return codec_switches
    
def fetch_traces_videos_codecs(jsons):
    codec_switches = dict()
    for trace in jsons:
        codec_switches[trace] = dict()
        for video in jsons[trace]:
            codec_switches[trace][video] = dict()
            for abr in jsons[trace][video]:
                codec_switches[trace][video][abr] = dict()
                for file in jsons[trace][video][abr]:
                    temp_codec = None
                    temp_switch = 0
                    for segment_name in jsons[trace][video][abr][file]:
                        if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                            continue
                        if temp_codec is None:
                            temp_codec = jsons[trace][video][abr][file][segment_name]["codec"]
                            continue
                        if jsons[trace][video][abr][file][segment_name]["codec"] != temp_codec:
                            temp_switch += 1
                            temp_codec = jsons[trace][video][abr][file][segment_name]["codec"]
                    codec_switches[trace][video][abr][file] = temp_switch
    return codec_switches


def fetch_values(json):
    # SegmentId, Bitrate(kbps), Codec, VMAF, Stalls
    bitrates = fetch_bitrates(json)
    codec_switches = fetch_codecs(json)
    sizes = fetch_sizes(json)
    vmafs = fetch_vmafs(json)
    # stalls, stalls_duration, start_ups = fetch_stalls(json)
    stalls, stalls_duration, start_ups = fetch_stalls(json)
    return bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups
    
def fetch_videos_values(json):
    # SegmentId, Bitrate(kbps), Codec, VMAF, Stalls
    bitrates = fetch_videos_bitrates(json)
    codec_switches = fetch_videos_codecs(json)
    vmafs = fetch_videos_vmafs(json)
    sizes = fetch_videos_sizes(json)
    # stalls, stalls_duration, start_ups = fetch_stalls(json)
    stalls, stalls_duration, start_ups = fetch_videos_stalls(json)
    return bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups
    
def fetch_traces_videos_values(json):
    # SegmentId, Bitrate(kbps), Codec, VMAF, Stalls
    bitrates = fetch_traces_videos_bitrates(json)
    codec_switches = fetch_traces_videos_codecs(json)
    vmafs = fetch_traces_videos_vmafs(json)
    sizes = fetch_traces_videos_sizes(json)
    # stalls, stalls_duration, start_ups = fetch_stalls(json)
    stalls, stalls_duration, start_ups = fetch_traces_videos_stalls(json)
    return bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups


def fetch_qoe_from_jsons(jsons):
    qoe = dict()
    for abr in jsons:
        qoe[abr] = dict()
        for file in jsons[abr]:
            print(file)
            # Opening JSON file
            with open(file) as f:
                data = json.load(f)
                # print(data)
                qoe[abr][file] = data["O46"]
    return qoe
    
    
def fetch_videos_qoe_from_jsons(jsons):
    qoe = dict()
    for video in jsons:
        qoe[video] = dict()
        for abr in jsons[video]:
            qoe[video][abr] = dict()
            for file in jsons[video][abr]:
                print(file)
                # Opening JSON file
                with open(file) as f:
                    data = json.load(f)
                    # print(data)
                    qoe[video][abr][file] = data["O46"]
    return qoe
    
def fetch_traces_videos_qoe_from_jsons(jsons):
    qoe = dict()
    for trace in jsons:
        qoe[trace] = dict()
        for video in jsons[trace]:
            qoe[trace][video] = dict()
            for abr in jsons[trace][video]:
                qoe[trace][video][abr] = dict()
                for file in jsons[trace][video][abr]:
                    print(file)
                    # Opening JSON file
                    with open(file) as f:
                        data = json.load(f)
                        # print(data)
                        qoe[trace][video][abr][file] = data["O46"]
    return qoe


def fetch_values_from_jsons(jsons):
    qoe = fetch_qoe_from_jsons(jsons)
    return qoe
    
    
def fetch_videos_values_from_jsons(jsons):
    qoe = fetch_videos_qoe_from_jsons(jsons)
    return qoe
    
def fetch_traces_videos_values_from_jsons(jsons):
    qoe = fetch_traces_videos_qoe_from_jsons(jsons)
    return qoe
    

def plot_bitrates(bitrates, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    print("+++AVERAGE BITRATES+++")
    for abr in bitrates:
        std_vals.append(np.std([bitrates[abr][b] for b in bitrates[abr]]))
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        sum_bitrate = 0
        for b in bitrates[abr]:
            sum_bitrate += bitrates[abr][b]
            print("--> '{:s}' -> '{:.0f}' kbps".format(b, bitrates[abr][b]))
        bars_vals.append(sum_bitrate / len(bitrates[abr]))
    x_pos = np.arange(len(bitrates))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(bitrates)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.0f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.0f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i+1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average Bitrate (kbps)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_bitrates(bitrates, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(bitrates)
    print("+++AVERAGE BITRATES+++")
    for video in bitrates:
        if n_abrs == 0:
            n_abrs = len(bitrates[video])
        elif n_abrs != len(bitrates[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in bitrates[video]:
            std_vals.append(np.std([bitrates[video][abr][b] for b in bitrates[video][abr]]))
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            sum_bitrate = 0
            for b in bitrates[video][abr]:
                sum_bitrate += bitrates[video][abr][b]
                print("--> '{:s}' -> '{:.0f}' kbps".format(b, bitrates[video][abr][b]))
            bars_vals.append(sum_bitrate / len(bitrates[video][abr]))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average Bitrate (kbps)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_difference_bitrates(bitrates, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(bitrates)
    print("+++BITRATE DIFFERENCES+++")
    for video in bitrates:
        if n_abrs == 0:
            n_abrs = len(bitrates[video])
        elif n_abrs != len(bitrates[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in bitrates[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            for b1, b2 in zip(bitrates[video][abr], bitrates[video][abr.split("-")[0]]):
                bit_diff.append((bitrates[video][abr][b1] - bitrates[video][abr.split("-")[0]][b2]) / bitrates[video][abr.split("-")[0]][b2] * 100)    
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average Bitrate Difference (%)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
def flatten(d, c = []):
   for a, b in d.items():
      yield from ([c+[a, b]] if not isinstance(b, dict) else flatten(b, c+[a]))
    
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
    plt.setp(bp['boxes'][0], color='blue')
    plt.setp(bp['caps'][0], color='blue')
    plt.setp(bp['caps'][1], color='blue')
    plt.setp(bp['whiskers'][0], color='blue')
    plt.setp(bp['whiskers'][1], color='blue')
    if len(bp['fliers']) > 0:
        print("0")
        plt.setp(bp['fliers'][0], color='blue')
    if len(bp['fliers']) > 1:
        print("1")
        plt.setp(bp['fliers'][1], color='blue')
    plt.setp(bp['medians'][0], color='blue')

    plt.setp(bp['boxes'][1], color='red')
    plt.setp(bp['caps'][2], color='red')
    plt.setp(bp['caps'][3], color='red')
    plt.setp(bp['whiskers'][2], color='red')
    plt.setp(bp['whiskers'][3], color='red')
    if len(bp['fliers']) > 2:
        print("2")
        plt.setp(bp['fliers'][2], color='red')
    if len(bp['fliers']) > 3:
        print("3")
        plt.setp(bp['fliers'][3], color='red')
    plt.setp(bp['medians'][1], color='red')
        
def boxplot_videos_difference_bitrates(bitrates, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    std_vals = []
    n_abrs = 0
    abrs = []
    print("+++BITRATE DIFFERENCES+++")
    for trace in bitrates:
        bars_vals[trace] = collections.OrderedDict()
        for video in bitrates[trace]:
            if n_abrs == 0:
                n_abrs = len(bitrates[trace][video])
            elif n_abrs != len(bitrates[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in bitrates[trace][video]:
                if not "-mcom" in abr:
                    continue
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)                
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(bitrates[trace][video][abr].items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(bitrates[trace][video][abr.split("-")[0]].items(), key=lambda item: item[1])}
                # for b1, b2 in zip(bitrates[trace][video][abr], bitrates[trace][video][abr.split("-")[0]]):
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    diff = bitrates[trace][video][abr][b1] - bitrates[trace][video][abr.split("-")[0]][b2]
                    perc_diff = (bitrates[trace][video][abr][b1] - bitrates[trace][video][abr.split("-")[0]][b2]) / bitrates[trace][video][abr.split("-")[0]][b2] * 100
                    bars_vals[trace][abr_new_name].append(perc_diff)
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # df = pd.DataFrame(list(flatten(bars_vals)))
    # df = df.assign(names=df[2].astype(str).str.lstrip("[").str.rstrip("]").str.split(",")).explode(2).drop(columns="names")
    # df = df.rename(columns = {0:'Trace', 1:"ABR", 2:"Val"})
    # df["Trace"] = df.Trace.astype(str)
    # df["ABR"] = df.ABR.astype(str)
    # df["Val"] = df.Val.astype(float)
    # print(df.dtypes)
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # Create names on the x-axis
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Bitrate Difference (%) \n(The higher the better)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # Save figure
    plt.savefig("{}/boxplot_difference_bitrate".format(path), bbox_inches='tight')
    # Show graph
    plt.show()


def plot_codec_switches(codec_switches, path):
    # using the pyplot.bar function
    bars_arr = []
    bars_vals = []
    std_vals = []
    print("+++CODEC SWITCHES+++")
    for abr in codec_switches:
        std_vals.append(np.std([codec_switches[abr][s] for s in codec_switches[abr]]))
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        sum_codec_switches = 0
        for s in codec_switches[abr]:
            sum_codec_switches += codec_switches[abr][s]
            print("--> '{:s}' -> '{:.0f}'".format(s, codec_switches[abr][s]))
        bars_vals.append(sum_codec_switches / len(codec_switches[abr]))
    x_pos = np.arange(len(codec_switches))
    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(codec_switches)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.1f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.1f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="center right")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Codec switches")
    plt.gca().set_ylim(bottom=0)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/codec_switches".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_codec_switches(codec_switches, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(codec_switches)
    print("+++CODEC SWITCHES+++")
    for video in codec_switches:
        if n_abrs == 0:
            n_abrs = len(codec_switches[video])
        elif n_abrs != len(codec_switches[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in codec_switches[video]:
            std_vals.append(np.std([codec_switches[video][abr][b] for b in codec_switches[video][abr]]))
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            sum_cs = 0
            for b in codec_switches[video][abr]:
                sum_cs += codec_switches[video][abr][b]
                print("--> '{:s}' -> '{:.0f}' kbps".format(b, codec_switches[video][abr][b]))
            bars_vals.append(sum_cs / len(codec_switches[video][abr]))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr


    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Codec switches")
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/codec_switches".format(path))
    # Show graph
    plt.show()
    

def boxplot_videos_difference_codec_switches(codec_switches, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    std_vals = []
    n_abrs = 0
    abrs = []
    print("+++CODEC SWITCHES DIFFERENCES+++")
    for trace in codec_switches:
        bars_vals[trace] = collections.OrderedDict()
        for video in codec_switches[trace]:
            if n_abrs == 0:
                n_abrs = len(codec_switches[trace][video])
            elif n_abrs != len(codec_switches[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in codec_switches[trace][video]:
                if not "-mcom" in abr:
                    continue
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)                
                # No need to sort, as codec switches for underlying ABRs are none
                sorted_b1 = {k: v for k, v in sorted(codec_switches[trace][video][abr].items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(codec_switches[trace][video][abr.split("-")[0]].items(), key=lambda item: item[1])}
                # for b1, b2 in zip(codec_switches[trace][video][abr], codec_switches[trace][video][abr.split("-")[0]]):
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    diff = codec_switches[trace][video][abr][b1] - codec_switches[trace][video][abr.split("-")[0]][b2]
                    bars_vals[trace][abr_new_name].append(diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # df = pd.DataFrame(list(flatten(bars_vals)))
    # df = df.assign(names=df[2].astype(str).str.lstrip("[").str.rstrip("]").str.split(",")).explode(2).drop(columns="names")
    # df = df.rename(columns = {0:'Trace', 1:"ABR", 2:"Val"})
    # df["Trace"] = df.Trace.astype(str)
    # df["ABR"] = df.ABR.astype(str)
    # df["Val"] = df.Val.astype(float)
    # print(df.dtypes)
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # Create names on the x-axis
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Codec Switches Difference\n(The lower the better)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # Save figure
    plt.savefig("{}/boxplot_difference_codecs".format(path), bbox_inches='tight')
    # Show graph
    plt.show()


def plot_vmafs(vmafs, path):
    markers = ["o", "v", "D", "^", "s", "<", "p", ">", "P", "*", "h", "X", "8"]
    colors = ["red", "yellow", "blue", "magenta", "green", "black", "orange", "cyan", "gray", "pink", "brown"]
    avg_vmafs = dict()
    segments = 0
    # Average the segments VMAF values across files
    for abr in vmafs:
        avg_vmafs[abr] = []
        if isinstance(list(vmafs[abr].values())[0], float):
            segments = len(vmafs[abr])
            for v in vmafs[abr]:
                avg_vmafs[abr].append(vmafs[abr][v])
        else:  # It is an array (multi-array)
            segments = len(list(vmafs[abr].values())[0])
            # Loop through the VMAF values
            for i in range(segments):
                sum_vmafs = 0
                for v in vmafs[abr]:
                    sum_vmafs += vmafs[abr][v][i]
                avg_vmafs[abr].append(sum_vmafs / len(vmafs[abr]))

    # Figure, axis objects
    fig, ax = plt.subplots()
    for i, abr in enumerate(avg_vmafs):
        # print(avg_vmafs[abr])
        # ax.plot(range(1, segments + 1), avg_vmafs[abr], "{}".format(markers[i]), color="{}".format(colors[i]), label="{}".format(abr))
        ax.plot(range(1, segments + 1), avg_vmafs[abr], color="{}".format(colors[i]), label="{}".format(abr))
    # Shrink current axis by 20%  # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # X axis label
    plt.xlabel("Segment Index")
    # Y axis label
    plt.ylabel("VMAF (1-100)")
    plt.gca().set_ylim(bottom=0)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/vmafs".format(path))
    # Show graph
    plt.show()


def plot_avg_vmafs(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    print("+++AVERAGE VMAFS+++")
    for abr in vmafs:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        sum_vmaf = []
        for b in vmafs[abr]:
            temp_avg = sum(vmafs[abr][b]) / len(vmafs[abr][b])
            sum_vmaf.append(temp_avg)
            print("--> '{:s}' -> '{:.0f}'".format(b, temp_avg))
        bars_vals.append(sum(sum_vmaf) / len(sum_vmaf))
        std_vals.append(np.std(sum_vmaf))
    x_pos = np.arange(len(vmafs))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(vmafs)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.1f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.1f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average VMAF (0-100)")
    # plt.ylim([60,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/avg_vmaf".format(path))
    # Show graph
    plt.show()
    
    
def plot_avg_size(size, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    print("+++AVERAGE SEGMENT SIZE+++")
    for abr in size:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        sum_size = []
        for b in size[abr]:
            temp_avg = sum(size[abr][b]) / len(size[abr][b])
            sum_size.append(temp_avg)
            print("--> '{:s}' -> '{:.0f}'".format(b, temp_avg))
        bars_vals.append(sum(sum_size) / len(sum_size))
        std_vals.append(np.std(sum_size))
    x_pos = np.arange(len(size))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(size)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.1f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.1f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average SIZE (KB)")
    # plt.ylim([60,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/avg_size".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_avg_size(size, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(size)
    print(size)
    print("+++AVERAGE SEGMENT SIZE+++")
    for video in size:
        if n_abrs == 0:
            n_abrs = len(size[video])
        elif n_abrs != len(size[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in size[video]:
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            sum_size = []
            for b in size[video][abr]:
                temp_avg = sum(size[video][abr][b]) / (1000 * 8)
                sum_size.append(temp_avg)
                print("--> '{:s}' -> '{:.0f}'KB".format(b, temp_avg))
            bars_vals.append(sum(sum_size) / len(sum_size))
            std_vals.append(np.std(sum_size))
    # x_pos = np.arange(len(size) * len(size[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average transmitted data (KB)")
    plt.ylim([5000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/size".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_difference_avg_size(size, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(size)
    print("+++SIZE DIFFERENCES+++")
    for video in size:
        if n_abrs == 0:
            n_abrs = len(size[video])
        elif n_abrs != len(size[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in size[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            for b1, b2 in zip(size[video][abr], size[video][abr.split("-")[0]]):
                size1 = sum(size[video][abr][b1]) / len(size[video][abr][b1])
                size2 = sum(size[video][abr.split("-")[0]][b2]) / len(size[video][abr.split("-")[0]][b2])
                bit_diff.append((size1 - size2) / size2 * 100)    
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    # x_pos = np.arange(len(size) * len(size[video][])))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Size Difference (%)")
    # plt.ylim([5000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def boxplot_videos_difference_avg_size(size, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    n_abrs = 0
    abrs = []
    print("+++SIZE DIFFERENCES+++")
    for trace in size:
        bars_vals[trace] = collections.OrderedDict()
        for video in size[trace]:
            if n_abrs == 0:
                n_abrs = len(size[trace][video])
            elif n_abrs != len(size[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in size[trace][video]:
                if not "-mcom" in abr:
                    continue
                print(abr)
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)
                temp_dict1 = collections.OrderedDict()
                temp_dict2 = collections.OrderedDict()
                # Before computing the sum and then order everything
                for b1, b2 in zip(size[trace][video][abr], size[trace][video][abr.split("-")[0]]):
                    size1 = sum(size[trace][video][abr][b1]) / len(size[trace][video][abr][b1])
                    temp_dict1[b1] = size1
                    size2 = sum(size[trace][video][abr.split("-")[0]][b2]) / len(size[trace][video][abr.split("-")[0]][b2])  
                    temp_dict2[b2] = size2
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(temp_dict1.items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(temp_dict2.items(), key=lambda item: item[1])}
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    size1 = sorted_b1[b1]
                    size2 = sorted_b2[b2]
                    diff = size1 - size2
                    perc_diff = (size1 - size2) / size2 * 100
                    bars_vals[trace][abr_new_name].append(perc_diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
               
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)

    # Create legend for ABR and MEDUSA
    # ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    # plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Transmitted Data Difference (%) \n(The lower the better)")
    #plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/boxplot_difference_size".format(path), bbox_inches='tight')
    # Show graph
    plt.show()
    
    
def plot_videos_avg_vmafs(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(vmafs)
    print("+++AVERAGE VMAFS+++")
    for video in vmafs:
        if n_abrs == 0:
            n_abrs = len(vmafs[video])
        elif n_abrs != len(vmafs[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in vmafs[video]:
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            sum_vmaf = []
            for b in vmafs[video][abr]:
                temp_avg = sum(vmafs[video][abr][b]) / len(vmafs[video][abr][b])
                sum_vmaf.append(temp_avg)
                print("--> '{:s}' -> '{:.0f}'".format(b, temp_avg))
            bars_vals.append(sum(sum_vmaf) / len(sum_vmaf))
            std_vals.append(np.std(sum_vmaf))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr


    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("VMAF (1-100)")
    plt.ylim([40,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/avg_vmaf".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_difference_avg_vmafs(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(vmafs)
    print("+++VMAF DIFFERENCES+++")
    for video in vmafs:
        if n_abrs == 0:
            n_abrs = len(vmafs[video])
        elif n_abrs != len(vmafs[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in vmafs[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            for b1, b2 in zip(vmafs[video][abr], vmafs[video][abr.split("-")[0]]):
                vmaf1 = sum(vmafs[video][abr][b1]) / len(vmafs[video][abr][b1])
                vmaf2 = sum(vmafs[video][abr.split("-")[0]][b2]) / len(vmafs[video][abr.split("-")[0]][b2])
                bit_diff.append(vmaf1 - vmaf2)    
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    # x_pos = np.arange(len(vmafs) * len(vmafs[video][])))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("VMAF Difference")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def boxplot_videos_difference_avg_vmafs(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    n_abrs = 0
    n_videos = len(vmafs)
    abrs = []
    print("+++VMAF DIFFERENCES+++")
    for trace in vmafs:
        bars_vals[trace] = collections.OrderedDict()
        for video in vmafs[trace]:
            if n_abrs == 0:
                n_abrs = len(vmafs[trace][video])
            elif n_abrs != len(vmafs[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in vmafs[trace][video]:
                if not "-mcom" in abr:
                    continue
                print(abr)
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)
                temp_dict1 = collections.OrderedDict()
                temp_dict2 = collections.OrderedDict()
                # Before computing the sum and then order everything
                for b1, b2 in zip(vmafs[trace][video][abr], vmafs[trace][video][abr.split("-")[0]]):
                    vmafs1 = sum(vmafs[trace][video][abr][b1]) / len(vmafs[trace][video][abr][b1])
                    temp_dict1[b1] = vmafs1
                    vmafs2 = sum(vmafs[trace][video][abr.split("-")[0]][b2]) / len(vmafs[trace][video][abr.split("-")[0]][b2])  
                    temp_dict2[b2] = vmafs2
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(temp_dict1.items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(temp_dict2.items(), key=lambda item: item[1])}
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    vmafs1 = sorted_b1[b1]
                    vmafs2 = sorted_b2[b2]
                    diff = vmafs1 - vmafs2
                    perc_diff = (vmafs1 - vmafs2) / vmafs2 * 100
                    bars_vals[trace][abr_new_name].append(diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("VMAF Difference \n(The higher the better)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/boxplot_difference_vmaf".format(path), bbox_inches='tight')
    # Show graph
    plt.show()


def plot_stalls(stalls, path):
    # using the pyplot.bar function
    bars_arr = []
    bars_vals = []
    std_vals_s = []
    # print(stalls)
    # print(stalls_duration)
    print("+++AVERAGE STALLS+++")
    for abr in stalls:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        sum_s = 0
        std_vals_s.append(np.std([stalls[abr][d] for d in stalls[abr]]))
        for s in stalls[abr]:
            sum_s += stalls[abr][s]
            print("--> '{:s}' -> STALLS: '{:.2f}'".format(s, stalls[abr][s]))
        bars_vals.append(sum_s / len(stalls[abr]))

    x_pos = np.arange(len(stalls))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(stalls)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.2f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.2f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals_s, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    ax.set_xlabel("ABR algorithms")
    # Y axis label
    ax.set_ylabel("# of stalls")
    # Limits
    ax.set_ylim(bottom=0)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/stalls".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_stalls(stalls, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(stalls)
    print("+++AVERAGE STALLS+++")
    for video in stalls:
        if n_abrs == 0:
            n_abrs = len(stalls[video])
        elif n_abrs != len(stalls[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in stalls[video]:
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            sum_s = 0
            std_vals.append(np.std([stalls[video][abr][d] for d in stalls[video][abr]]))
            for s in stalls[video][abr]:
                sum_s += stalls[video][abr][s]
                print("--> '{:s}' -> STALLS: '{:.2f}'".format(s, stalls[video][abr][s]))
            bars_vals.append(sum_s / len(stalls[video][abr]))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr


    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("# of stalls")
    plt.ylim([0,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/stalls".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_difference_stalls(stalls, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(stalls)
    print("+++STALLS DIFFERENCES+++")
    for video in stalls:
        if n_abrs == 0:
            n_abrs = len(stalls[video])
        elif n_abrs != len(stalls[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in stalls[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            for b1, b2 in zip(stalls[video][abr], stalls[video][abr.split("-")[0]]):
                bit_diff.append((stalls[video][abr][b1] - stalls[video][abr.split("-")[0]][b2]))    
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    # x_pos = np.arange(len(stalls) * len(stalls[video][])))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("# Stalls Difference")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def boxplot_videos_difference_stalls(stalls, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    n_abrs = 0
    n_videos = len(stalls)
    abrs = []
    print("+++STALLS DIFFERENCES+++")
    for trace in stalls:
        bars_vals[trace] = collections.OrderedDict()
        for video in stalls[trace]:
            if n_abrs == 0:
                n_abrs = len(stalls[trace][video])
            elif n_abrs != len(stalls[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in stalls[trace][video]:
                if not "-mcom" in abr:
                    continue
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)                
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(stalls[trace][video][abr].items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(stalls[trace][video][abr.split("-")[0]].items(), key=lambda item: item[1])}
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    diff = stalls[trace][video][abr][b1] - stalls[trace][video][abr.split("-")[0]][b2]
                    perc_diff = 0
                    if stalls[trace][video][abr.split("-")[0]][b2] == 0:
                        if stalls[trace][video][abr][b1] == 0:
                            perc_diff = 0
                        else:
                            perc_diff = 100
                    else:
                        perc_diff = (stalls[trace][video][abr][b1] - stalls[trace][video][abr.split("-")[0]][b2]) / stalls[trace][video][abr.split("-")[0]][b2] * 100
                    bars_vals[trace][abr_new_name].append(diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Stalls Difference \n(The lower the better)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/boxplot_difference_stalls".format(path), bbox_inches='tight')
    # Show graph
    plt.show()
    

def plot_stalls_duration(stalls_duration, path):
    # using the pyplot.bar function
    bars_arr = []
    bars_vals = []
    std_vals_d = []
    # print(stalls)
    # print(stalls_duration)
    print("+++AVERAGE STALLS+++")
    for abr in stalls_duration:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        sum_sd = 0
        std_vals_d.append(np.std([stalls_duration[abr][d] for d in stalls_duration[abr]]))
        for v in stalls_duration[abr]:
            sum_sd += stalls_duration[abr][v]
            print("--> '{:s}' -> STALLS_DURATION: '{:.3f}'".format(v, stalls_duration[abr][v]))
        bars_vals.append(sum_sd / len(stalls_duration[abr]))

    x_pos = np.arange(len(stalls_duration))
    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    # for abr in stalls_duration:
        # if i % 2:
            # bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            # ax.bar_label(bars, fmt='%.2f')
        # else:
            # bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            # ax.bar_label(bars, fmt='%.2f')
            # bars = plt.boxplot(bars_vals[i])
    bars = ax.boxplot([[stalls_duration[abr][v] for v in stalls_duration[abr]] for abr in stalls_duration])

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    # plt.errorbar(x_pos, bars_vals, yerr=std_vals_d, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    # x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    # new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    ax.set_xticklabels([abr for abr in stalls_duration])
    # plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    ax.set_xlabel("ABR algorithms")
    # Y axis label
    ax.set_ylabel("Stalls duration (s)")
    # Limits
    # plt.ylim([0,None])
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/stalls_duration".format(path))
    # Show graph
    plt.show()
    

def plot_videos_stalls_duration(stalls_duration, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(stalls_duration)
    print("+++AVERAGE STALL DURATIONS+++")
    for video in stalls_duration:
        if n_abrs == 0:
            n_abrs = len(stalls_duration[video])
        elif n_abrs != len(stalls_duration[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in stalls_duration[video]:
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            sum_sd = 0
            std_vals.append(np.std([stalls_duration[video][abr][d] for d in stalls_duration[video][abr]]))
            for v in stalls_duration[video][abr]:
                sum_sd += stalls_duration[video][abr][v]
                print("--> '{:s}' -> STALLS_DURATION: '{:.3f}'".format(v, stalls_duration[video][abr][v]))
            bars_vals.append(sum_sd / len(stalls_duration[video][abr]))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Stall durations (s)")
    plt.ylim([0,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/stalls_duration".format(path))
    # Show graph
    plt.show()    
    
    
def plot_videos_difference_stalls_duration(stalls_duration, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(stalls_duration)
    print("+++STALLS DURATION DIFFERENCES+++")
    for video in stalls_duration:
        if n_abrs == 0:
            n_abrs = len(stalls_duration[video])
        elif n_abrs != len(stalls_duration[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in stalls_duration[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            for b1, b2 in zip(stalls_duration[video][abr], stalls_duration[video][abr.split("-")[0]]):
                bit_diff.append((stalls_duration[video][abr][b1] - stalls_duration[video][abr.split("-")[0]][b2]))    
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Stalls Duration Difference (s)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def boxplot_videos_difference_stalls_duration(stalls_duration, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    n_abrs = 0
    n_videos = len(stalls_duration)
    abrs = []
    print("+++STALLS DURATION DIFFERENCES+++")
    for trace in stalls_duration:
        bars_vals[trace] = collections.OrderedDict()
        for video in stalls_duration[trace]:
            if n_abrs == 0:
                n_abrs = len(stalls_duration[trace][video])
            elif n_abrs != len(stalls_duration[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in stalls_duration[trace][video]:
                if not "-mcom" in abr:
                    continue
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)                
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(stalls_duration[trace][video][abr].items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(stalls_duration[trace][video][abr.split("-")[0]].items(), key=lambda item: item[1])}
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    diff = stalls_duration[trace][video][abr][b1] - stalls_duration[trace][video][abr.split("-")[0]][b2]
                    perc_diff = 0
                    if stalls_duration[trace][video][abr.split("-")[0]][b2] == 0:
                        if stalls_duration[trace][video][abr][b1] == 0:
                            perc_diff = 0
                        else:
                            perc_diff = 100
                    else:
                        perc_diff = (stalls_duration[trace][video][abr][b1] - stalls_duration[trace][video][abr.split("-")[0]][b2]) / stalls_duration[trace][video][abr.split("-")[0]][b2] * 100
                    bars_vals[trace][abr_new_name].append(diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Stalls Duration Difference (s) \n(The lower the better)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/boxplot_difference_stalls_duration".format(path), bbox_inches='tight')
    # Show graph
    plt.show()


def plot_avg_instability(vmafs, path):
    # using the pyplot.bar function
    bars_arr = []
    bars_vals = []
    std_vals = []
    print("+++AVERAGE INSTABILITY+++")
    for abr in vmafs:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        avg_inst = []
        for b in vmafs[abr]:
            temp_inst = 0
            # print(vmafs[abr][b])
            for i in range(len(vmafs[abr][b]) - 1):
                temp_inst += abs(vmafs[abr][b][i + 1] - vmafs[abr][b][i])
            temp_inst /= (len(vmafs[abr][b]) - 1)
            print("--> '{:s}' -> '{:.2f}'".format(b, temp_inst))
            avg_inst.append(temp_inst)
        std_vals.append(np.std(avg_inst))
        bars_vals.append(sum(avg_inst) / len(avg_inst))

    x_pos = np.arange(len(vmafs))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(vmafs)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.2f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.2f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Instability")
    # plt.ylim([6,None])
    # plt.gca().set_ylim(bottom=0)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/instability".format(path))
    # Show graph
    plt.show()


def plot_videos_avg_instability(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(vmafs)
    print("+++AVERAGE INSTABILITY+++")
    for video in vmafs:
        if n_abrs == 0:
            n_abrs = len(vmafs[video])
        elif n_abrs != len(vmafs[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in vmafs[video]:
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            avg_inst = []
            for b in vmafs[video][abr]:
                temp_inst = 0
                # print(vmafs[abr][b])
                for i in range(len(vmafs[video][abr][b]) - 1):
                    temp_inst += abs(vmafs[video][abr][b][i + 1] - vmafs[video][abr][b][i])
                temp_inst /= (len(vmafs[video][abr][b]) - 1)
                print("--> '{:s}' -> '{:.2f}'".format(b, temp_inst))
                avg_inst.append(temp_inst)
            std_vals.append(np.std(avg_inst))
            bars_vals.append(sum(avg_inst) / len(avg_inst))
    # x_pos = np.arange(len(bitrates) * len(bitrates[video][])))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average instability")
    # plt.ylim([6,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/instability".format(path))
    # Show graph
    plt.show()   
    
    
def plot_videos_difference_avg_instability(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(vmafs)
    print("+++INSTABILITY DIFFERENCES+++")
    for video in vmafs:
        if n_abrs == 0:
            n_abrs = len(vmafs[video])
        elif n_abrs != len(vmafs[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in vmafs[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            temp_inst1 = 0
            temp_inst2 = 0
            for b1 in vmafs[video][abr]:
                for i in range(len(vmafs[video][abr][b1]) - 1):
                    temp_inst1 += abs(vmafs[video][abr][b1][i + 1] - vmafs[video][abr][b1][i])
                temp_inst1 /= (len(vmafs[video][abr][b1]) - 1)
            for b2 in vmafs[video][abr.split("-")[0]]:
                for i in range(len(vmafs[video][abr.split("-")[0]][b2]) - 1):
                    temp_inst2 += abs(vmafs[video][abr.split("-")[0]][b2][i + 1] - vmafs[video][abr.split("-")[0]][b2][i])
                temp_inst2 /= (len(vmafs[video][abr.split("-")[0]][b2]) - 1)
                bit_diff.append((temp_inst1 - temp_inst2) / temp_inst2 * 100)    
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average Instability Difference (%)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()
    
    
def boxplot_videos_difference_avg_instability(vmafs, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    n_abrs = 0
    n_videos = len(vmafs)
    abrs = []
    print("+++VMAF DIFFERENCES+++")
    for trace in vmafs:
        bars_vals[trace] = collections.OrderedDict()
        for video in vmafs[trace]:
            if n_abrs == 0:
                n_abrs = len(vmafs[trace][video])
            elif n_abrs != len(vmafs[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in vmafs[trace][video]:
                if not "-mcom" in abr:
                    continue
                print(abr)
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)
                temp_dict1 = collections.OrderedDict()
                temp_inst1 = 0
                for b1 in vmafs[trace][video][abr]:
                    for i in range(len(vmafs[trace][video][abr][b1]) - 1):
                        temp_inst1 += abs(vmafs[trace][video][abr][b1][i + 1] - vmafs[trace][video][abr][b1][i])
                    temp_dict1[b1] = temp_inst1 / (len(vmafs[trace][video][abr][b1]) - 1)
                temp_dict2 = collections.OrderedDict()
                temp_inst2 = 0
                for b2 in vmafs[trace][video][abr.split("-")[0]]:
                    for i in range(len(vmafs[trace][video][abr.split("-")[0]][b2]) - 1):
                        temp_inst2 += abs(vmafs[trace][video][abr.split("-")[0]][b2][i + 1] - vmafs[trace][video][abr.split("-")[0]][b2][i])
                    temp_dict2[b2] = temp_inst2 / (len(vmafs[trace][video][abr.split("-")[0]][b2]) - 1)
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(temp_dict1.items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(temp_dict2.items(), key=lambda item: item[1])}
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    vmafs1 = sorted_b1[b1]
                    vmafs2 = sorted_b2[b2]
                    diff = vmafs1 - vmafs2
                    perc_diff = (vmafs1 - vmafs2) / vmafs2 * 100
                    bars_vals[trace][abr_new_name].append(perc_diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("VMAF Instability Difference (%) \n(The lower the better)")
    # plt.ylim([-30, 30])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/boxplot_difference_instability".format(path), bbox_inches='tight')
    # Show graph
    plt.show()


def plot_qoe(qoe, path):
    # using the pyplot.bar function
    bars_arr = []
    bars_vals = []
    std_vals = []
    print("+++AVERAGE QoE+++")
    for abr in qoe:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        avg_qoe = []
        for v in qoe[abr]:
            avg_qoe.append(qoe[abr][v])
            print("--> '{:s}' -> '{:.2f}'".format(v, qoe[abr][v]))
        std_vals.append(np.std(avg_qoe))
        bars_vals.append(sum(avg_qoe) / len(avg_qoe))

    x_pos = np.arange(len(qoe))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(qoe)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.2f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.2f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("QoE (1-5)")
    # plt.ylim([2.4,None])
    # plt.gca().set_ylim(bottom=3)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/qoe".format(path))
    # Show graph
    plt.show()
    
    
def plot_videos_qoe(qoe, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(qoe)
    print("+++AVERAGE QoE+++")
    for video in qoe:
        if n_abrs == 0:
            n_abrs = len(qoe[video])
        elif n_abrs != len(qoe[video]):
            print("Error! Different number of ABR algorithms ({}!={}) for '{}' video sequence!".format(len(qoe[video]), n_abrs, video))
            exit(1)
        for abr in qoe[video]:
            if "-mcom" in abr.lower():
                print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
                bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            else:
                print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
                bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
            avg_qoe = []
            for v in qoe[video][abr]:
                avg_qoe.append(qoe[video][abr][v])
                print("--> '{:s}' -> '{:.2f}'".format(v, qoe[video][abr][v]))
            std_vals.append(np.std(avg_qoe))
            bars_vals.append(sum(avg_qoe) / len(avg_qoe))
    x_pos = list(range(n_abrs))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr


    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:n_abrs]])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("Average QoE (1-5)")
    plt.ylim([1,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/qoe".format(path))
    # Show graph
    plt.show()

def plot_videos_difference_qoe(qoe, path):
    # using the pyplot.bar function
    import numpy as np
    bars_arr = []
    bars_vals = []
    std_vals = []
    n_abrs = 0
    n_videos = len(qoe)
    print("+++QOE DIFFERENCES+++")
    for video in qoe:
        if n_abrs == 0:
            n_abrs = len(qoe[video])
        elif n_abrs != len(qoe[video]):
            print("Error! Different number of ABR algorithms in different video sequences!")
            exit(1)
        for abr in qoe[video]:
            if not "-mcom" in abr:
                continue
            print(abr)
            bit_diff = []
            for b1, b2 in zip(qoe[video][abr], qoe[video][abr.split("-")[0]]):
                bit_diff.append((qoe[video][abr][b1] - qoe[video][abr.split("-")[0]][b2]) / qoe[video][abr.split("-")[0]][b2] * 100)
            std_vals.append(np.std(bit_diff))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_vals.append(np.mean(bit_diff))
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.80 / n_videos  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars_handle = []
    
    for i in range(len(VIDEOS)):
        ax.grid(zorder=0)
        delta_p = width*i
        # plt.bar([p + delta_p for p in pos], df[colname], width, color=color, label=lbl)
        bars = ax.bar([p + delta_p for p in x_pos], [bars_vals[i*len(x_pos)+j] for j in x_pos], yerr=[std_vals[i*len(x_pos)+j] for j in range(len(x_pos))], capsize=3, width=width, label=VIDEOS_NEW_NAME[VIDEOS[i]], color=COLORS[i], hatch=HATCHES[i], zorder=3)
        bars_handle.append(bars)
        # ax.bar_label(bars, fmt='%.0f')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = x_pos
    new_bars_arr = bars_arr

    # Create legend for ABR and MEDUSA
    ax.legend(handles=[b for b in bars_handle], loc="best")
    # Create names on the x-axis
    plt.xticks([x + (len(VIDEOS) - 1) * width / 2 for x in x_new_pos], [a for a in new_bars_arr[0:len(x_pos)] if "-medusa" in a.lower()])
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("QoE Difference (%)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    fig.autofmt_xdate()
    # Save figure
    # plt.savefig("{}/bitrate".format(path))
    # Show graph
    plt.show()


def boxplot_videos_difference_qoe(qoe, path):
    # using the pyplot.bar function
    import numpy as np
    bars_vals = collections.OrderedDict()
    n_abrs = 0
    n_videos = len(qoe)
    abrs = []
    print("+++QoE DIFFERENCES+++")
    for trace in qoe:
        bars_vals[trace] = collections.OrderedDict()
        for video in qoe[trace]:
            if n_abrs == 0:
                n_abrs = len(qoe[trace][video])
            elif n_abrs != len(qoe[trace][video]):
                print("Error! Different number of ABR algorithms in different video sequences!")
                exit(1)
            for abr in qoe[trace][video]:
                if not "-mcom" in abr:
                    continue
                abr_new_name = "{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME)
                if abr_new_name not in bars_vals[trace]:
                    bars_vals[trace][abr_new_name] = []
                if abr_new_name not in abrs:
                    abrs.append(abr_new_name)
                print(abr)                
                # Sort dictionaries based on values and then compute the differences
                sorted_b1 = {k: v for k, v in sorted(qoe[trace][video][abr].items(), key=lambda item: item[1])}
                sorted_b2 = {k: v for k, v in sorted(qoe[trace][video][abr.split("-")[0]].items(), key=lambda item: item[1])}
                for b1, b2 in zip(sorted_b1, sorted_b2):
                    diff = qoe[trace][video][abr][b1] - qoe[trace][video][abr.split("-")[0]][b2]
                    perc_diff = (qoe[trace][video][abr][b1] - qoe[trace][video][abr.split("-")[0]][b2]) / qoe[trace][video][abr.split("-")[0]][b2] * 100
                    bars_vals[trace][abr_new_name].append(perc_diff)
    x_pos = list(range(int(n_abrs / 2)))
    width = 0.25  # the width of the bars
    
    # Figure, axis objects
    fig, ax = plt.subplots()
    
    bars_handle = []
    
    # Modify the dict to have two arrays for each ABR --> "ABR1" = [[FCC], [4G]]
    vals_to_print = []
    for trace in bars_vals:
        for j, abr in enumerate(bars_vals[trace]):
            if len(vals_to_print) <= j:
                vals_to_print.append([bars_vals[trace][abr]])
            else:
                vals_to_print[j].append(bars_vals[trace][abr])
               
    xticks = []
    for i in range(len(vals_to_print)): # ABRS
        for j in range(len(vals_to_print[i])):  # TRACES
            c = 'b'
            overflow = - WIDTH / 2 - 0.05
            if j == 1:
                c = 'r'
                overflow = WIDTH / 2 + 0.05
            bp = plt.boxplot(vals_to_print[i][j], positions = [i + overflow], widths = WIDTH, showmeans = SHOWMEANS, showfliers = SHOWFLIERS,
                             patch_artist = True,
                             boxprops=dict(facecolor = "white", color=c),
                             capprops=dict(color=c),
                             whiskerprops=dict(color=c),
                             flierprops=dict(color=c, markeredgecolor=c),
                             medianprops=dict(color=c))
            print("Boxplot properties for '{}' ['{}']".format(abrs[i], c))
            res  = {}
            for key, value in bp.items():
                # print(key)
                # print(value)
                res[key] = []
                for v in value:
                    if hasattr(v, 'get_data') and callable(v.get_data):
                        res[key].append(v.get_data())
            print(res)

        xticks.append(i)

    ax.set_xticks(xticks)
    ax.set_xticklabels(abrs)
    
    ax.yaxis.grid(True)
    
    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('4G-LTE', 'FCC'))
    hB.set_visible(False)
    hR.set_visible(False)
    
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("QoE Difference (%) \n(The higher the better)")
    # plt.ylim([2000,None])
    # plt.gca().set_ylim(bottom=6500)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/boxplot_difference_qoe".format(path), bbox_inches='tight')
    # Show graph
    plt.show()


def plot_qoe_comyco(bitrates, stalls_dur, vmafs, path):
    #--------------------------------
    #based on Comyco paper
    #Quality-Aware Neural Adaptive Video Streaming With Lifelong Imitation Learning
    alpha = 0.8469
    beta = 28.7959
    gamma = 0.2979
    delta = 1.0610
    # delta = gamma

    # using the pyplot.bar function
    bars_arr = []
    qoe_temp_vars = []
    bars_vals = []
    norm_bars_vals = []
    std_vals = []
    print("+++AVERAGE QoE_COMYCO+++")
    for abr in bitrates:
        if "-mcom" in abr.lower():
            print("-> ABR '{}-{}'".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
            bars_arr.append("{}-{}".format(ABRS_NEW_NAME[abr[:-5]].upper(), PLUGIN_NAME))
        else:
            print("-> ABR '{}'".format(ABRS_NEW_NAME[abr].upper()))
            bars_arr.append("{}".format(ABRS_NEW_NAME[abr].upper()))
        mean_bitrate = 0
        sum_vmaf = []
        # for b in bitrates[abr]:
        #     mean_bitrate += bitrates[abr][b]
        # mean_bitrate = mean_bitrate / len(bitrates[abr])
        for v, s in zip(vmafs[abr], stalls_dur[abr]):
            switching_positive = 0
            switching_negative = 0
            sum_stalls = 0
            sumR = 0
            # print(vmafs[abr][v])
            # print(stalls_dur[abr][s])
            sumR = sum(vmafs[abr][v]) # / len(vmafs[abr][v])
            # sum_vmaf.append(temp_avg)
            for i in range(len(vmafs[abr][v]) - 1):
                v1 = vmafs[abr][v][i]
                # print("V1: {}".format(v1))
                v2 = vmafs[abr][v][i+1]
                if v1 <= v2:
                    switching_positive += (v2 - v1)
                else:
                    switching_negative += (v1 - v2)
            #sumR = sum(sum_vmaf) # / len(sum_vmaf)
            sum_stalls += stalls_dur[abr][s]            
            # print("F = {} * {} - {} * {} + {} * {} - {} * {}".format(alpha, sumR, beta, sum_stalls, gamma, switching_positive, delta, switching_negative))
            qoe_temp_vars.append(alpha * sumR - beta * sum_stalls + gamma * switching_positive - delta * switching_negative)
        bars_vals.append(sum(qoe_temp_vars) / len(qoe_temp_vars))
        std_vals.append(np.std(qoe_temp_vars))
    #for val in temp_bars_vals:
    #    bars_vals.append(val / max(temp_bars_vals))

    x_pos = np.arange(len(bars_vals))

    # Figure, axis objects
    fig, ax = plt.subplots()
    # Create bars (print percentages with 2 decimal precision)
    for i in range(len(bitrates)):
        if i % 2:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black', hatch=PATTERN)
            ax.bar_label(bars, fmt='%.0f')
        else:
            bars = ax.bar(i, bars_vals[i], color=COLORS[math.floor(i/2)], edgecolor='black')
            ax.bar_label(bars, fmt='%.0f')

    # bars = ax.bar(x_pos, bars_vals, color=(0.2, 0.4, 0.6, 0.6))
    # ax.bar_label(bars, fmt='%.0f')

    # plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='o')
    plt.errorbar(x_pos, bars_vals, yerr=std_vals, ecolor="black", capsize=10, fmt='none')

    # Use ABR name for pairs and add legend with patterns
    x_new_pos = [(x_pos[i] + x_pos[i + 1]) / 2 for i in range(len(x_pos) - 1) if i % 2 == 0]
    new_bars_arr = [bars_arr[i] for i in range(len(x_pos) - 1) if i % 2 == 0]

    # Create legend for ABR and MEDUSA

    circ1 = mpatches.Patch(facecolor='white', edgecolor='black', label='Original ABR')
    circ2 = mpatches.Patch(facecolor='white', edgecolor='black', hatch='x', label='+MEDUSA')

    ax.legend(handles=[circ1, circ2], loc="best")
    # Create names on the x-axis
    plt.xticks(x_new_pos, new_bars_arr)
    # X axis label
    plt.xlabel("ABR algorithms")
    # Y axis label
    plt.ylabel("QoE (0-1")
    # plt.gca().set_ylim(bottom=3)
    # fig.autofmt_xdate()
    # Save figure
    plt.savefig("{}/qoe-comyco".format(path))
    # Show graph
    plt.show()


def plot_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path):
    plot_bitrates(bitrates, path)
    plot_codec_switches(codec_switches, path)
    # plot_vmafs(vmafs, path)
    plot_avg_vmafs(vmafs, path)
    plot_avg_size(sizes, path)
    plot_avg_instability(vmafs, path)
    plot_stalls(stalls, path)
    plot_stalls_duration(stalls_duration, path)
    plot_qoe(qoe, path)
    plot_qoe_comyco(bitrates, stalls_duration, vmafs, path)
    
    
def plot_videos_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 18})
    plot_videos_bitrates(bitrates, path)
    plot_videos_difference_bitrates(bitrates, path)
    plot_videos_avg_size(sizes, path)
    plot_videos_difference_avg_size(sizes, path)
    plot_videos_codec_switches(codec_switches, path)
    # plot_vmafs(vmafs, path)
    plot_videos_avg_vmafs(vmafs, path)
    plot_videos_difference_avg_vmafs(vmafs, path)
    plot_videos_avg_instability(vmafs, path)
    plot_videos_difference_avg_instability(vmafs, path)
    plot_videos_stalls(stalls, path)
    plot_videos_difference_stalls(stalls, path)
    plot_videos_stalls_duration(stalls_duration, path)
    plot_videos_difference_stalls_duration(stalls_duration, path)
    plot_videos_qoe(qoe, path)
    plot_videos_difference_qoe(qoe, path)
    # plot_videos_qoe_comyco(bitrates, stalls_duration, vmafs, path)
    
    
def boxplot_videos_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 20})
    plt.rcParams['figure.figsize'] = [10, 6]
    # boxplot_videos_bitrates(bitrates, path)
    boxplot_videos_difference_bitrates(bitrates, path)
    boxplot_videos_difference_avg_size(sizes, path)
    boxplot_videos_difference_codec_switches(codec_switches, path)
    # boxplot_videos_avg_vmafs(vmafs, path)
    boxplot_videos_difference_avg_vmafs(vmafs, path)
    # boxplot_videos_avg_instability(vmafs, path)
    boxplot_videos_difference_avg_instability(vmafs, path)
    # boxplot_videos_stalls(stalls, path)
    boxplot_videos_difference_stalls(stalls, path)
    # boxplot_videos_stalls_duration(stalls_duration, path)
    boxplot_videos_difference_stalls_duration(stalls_duration, path)
    # boxplot_videos_qoe(qoe, path)
    boxplot_videos_difference_qoe(qoe, path)
    # plot_videos_qoe_comyco(bitrates, stalls_duration, vmafs, path)


def fetch_and_plot_results(path):

    # Files to fetch the data and draw the graphs
    jsons = collections.OrderedDict()
    qoe_jsons = collections.OrderedDict()
    path = os.path.join(path)
    # Other directories with ABR names
    astream_matches = []
    json_matches = []
    for abr in ABRS:
        jsons[abr] = dict()
        qoe_jsons[abr] = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, 'ASTREAM_*.json'):
            astream_matches.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, 'QOE_*_out.json'):
            json_matches.append(os.path.join(root, filename))
    for match in astream_matches:
        for abr in ABRS:
            if "/{}/".format(abr) in match:
                # if abr not in jsons:
                #     jsons[abr] = []
                print(abr)
                print("Adding file: {}".format(match))
                # jsons[abr].append(match)
                with open(match, 'r') as json_file:
                    json_obj = json.load(json_file)
                    if "playback_type" in json_obj:
                        if json_obj["playback_type"] not in jsons:
                            jsons[json_obj["playback_type"]] = dict()
                        # print(jsons)
                        jsons[json_obj["playback_type"]][match] = dict()
                        for segment_info in json_obj["segment_info"]:
                            segment_vmaf = segment_info[VMAF]
                            if not segment_vmaf:
                                segment_vmaf = 0
                            jsons[json_obj["playback_type"]][os.path.join(match)][segment_info[SEGMENT_NAME]] = {
                                "bitrate": segment_info[BITRATE], "codec": segment_info[CODEC],
                                "vmaf": segment_vmaf, "segment_size": segment_info[SEGMENT_SIZE],
                                "download_time": segment_info[SEGMENT_DOWNLOAD_TIME]}
                    if "playback_info" in json_obj:
                        jsons[json_obj["playback_type"]][os.path.join(match)]["initial_buffering_duration"] = json_obj["playback_info"]["initial_buffering_duration"]
                        jsons[json_obj["playback_type"]][os.path.join(match)]["interruptions"] = []
                        for stall_pair in json_obj["playback_info"]["interruptions"]["events"]:
                            time = stall_pair[0]
                            duration = stall_pair[1] - stall_pair[0]
                            jsons[json_obj["playback_type"]][os.path.join(match)]["interruptions"].append([time, duration])
    for match in json_matches:
        for abr in ABRS:
            if "/{}/".format(abr) in match:
                if abr not in qoe_jsons:
                    qoe_jsons[abr] = []
                print("Adding file: {}".format(match))
                qoe_jsons[abr].append(match)
    pop_keys = []
    for d in jsons:
        if not jsons[d]:
            pop_keys.append(d)
    for p in pop_keys:
        jsons.pop(p)
    pop_keys = []
    for d in qoe_jsons:
        if not qoe_jsons[d]:
            pop_keys.append(d)
    for p in pop_keys:
        qoe_jsons.pop(p)
    # print(jsons)
    # for d in os.listdir(path):
    #     print(os.path.join(path, d))
    #     if os.path.isdir(os.path.join(path, d)):
    #         qoe_jsons[d] = []
    #         path_ = os.path.join(path, d)
    #         for i in os.listdir(path_):
    #             if os.path.isfile(os.path.join(path_, i)) and "astream" == i.lower()[:7] and ".json" == i.lower()[-5:]:
    #                 print("Adding file: {}".format(os.path.join(path_, i)))
    #                 with open(os.path.join(path_, i), 'r') as json_file:
    #                     json_obj = json.load(json_file)
    #                     if "playback_type" in json_obj:
    #                         if json_obj["playback_type"] not in jsons:
    #                             jsons[json_obj["playback_type"]] = dict()
    #                         jsons[json_obj["playback_type"]][os.path.join(path_, i)] = dict()
    #                         for segment_info in json_obj["segment_info"]:
    #                             jsons[json_obj["playback_type"]][os.path.join(path_, i)][segment_info[SEGMENT_NAME]] = {"bitrate": segment_info[BITRATE], "codec": segment_info[CODEC], "vmaf": segment_info[VMAF], "segment_size": segment_info[SEGMENT_SIZE], "download_time": segment_info[SEGMENT_DOWNLOAD_TIME]}
    #                     # print("File '{}' added to ABR '{}'".format(os.path.join(path, i), abr.lower()))
    #             elif os.path.isfile(os.path.join(path_, i)) and "qoe_output" == i.lower()[:10] and ".json" == i.lower()[-5:]:
    #                 print("Adding file: {}".format(os.path.join(path_, i)))
    #                 qoe_jsons[d].append(os.path.join(path_, i))
    for abr in jsons:
        print("'{:.0f}' overall JSON files found for ABR '{:s}'".format(len(jsons[abr]), abr))
    for abr in qoe_jsons:
        print("'{:.0f}' overall QoE JSON files found for ABR '{:s}'".format(len(qoe_jsons[abr]), abr))
    # print(jsons)
    # print(files)
    # Loop through files and gather data
    bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups = fetch_values(jsons)
    # qoe = None
    qoe = fetch_values_from_jsons(qoe_jsons)
    # print(bitrates)
    # print(codec_switches)
    # print(vmafs)
    # print(stalls)
    # print(stalls_duration)
    # print(start_ups)
    # Plot save figures
    plot_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path)
    # print(psnr)
    
    
def fetch_and_plot_single_values(jsons):
    vmafs = []
    segment_size = []
    abr = ""
    fig, ax = plt.subplots()
    ax_twin = ax.twinx()
    handle = []
    i = 0
    for file in jsons:
        vmafs = []
        segment_size = []
        for segment_name in jsons[file]:
            if "segment_" not in segment_name or segment_name[-4:] == ".mp4":  # Initialization segment
                continue
            vmafs.append(jsons[file][segment_name]["vmaf"])
            segment_size.append(jsons[file][segment_name]["segment_size"])
        for a in ABRS:
            if "/{}/".format(a) in file:
                abr = a
        if i == 0:
            p1, = ax.plot(range(1, len(list(jsons[file]))), vmafs, "r-", label="vmafs-{}".format(a))
            p2, = ax_twin.plot(range(1, len(list(jsons[file]))), segment_size, "g-", label="size-{}".format(a))
        else:
            p3, = ax.plot(range(1, len(list(jsons[file]))), vmafs, "r--", label="vmafs-{}".format(a))
            p4, = ax_twin.plot(range(1, len(list(jsons[file]))), segment_size, "g--", label="size-{}".format(a))
        i += 1
    
    # ax.legend(handles=[p1, p2])
    plt.legend()
    ax.set(xlabel="Segment number", ylabel="VMAF")
    ax_twin.set(ylabel="Size (Bytes)")
    # plt.title(abr)
    plt.show()
    
def fetch_and_plot_single_results(path1, path2):
    # Files to fetch the data and draw the graphs
    jsons = collections.OrderedDict()
    qoe_jsons = collections.OrderedDict()
    for root, dirnames, filenames in os.walk(path1):
        for filename in fnmatch.filter(filenames, 'ASTREAM_*.json'):
            jsons[os.path.join(root, filename)] = collections.OrderedDict()
            with open(os.path.join(root, filename), 'r') as json_file:
                json_obj = json.load(json_file)   
                for segment_info in json_obj["segment_info"]:
                    segment_vmaf = segment_info[VMAF]
                    if not segment_vmaf:
                        segment_vmaf = 0
                    jsons[os.path.join(root, filename)][segment_info[SEGMENT_NAME]] = {
                        "bitrate": segment_info[BITRATE], "codec": segment_info[CODEC],
                        "vmaf": segment_vmaf, "segment_size": segment_info[SEGMENT_SIZE],
                        "download_time": segment_info[SEGMENT_DOWNLOAD_TIME]}
    for root, dirnames, filenames in os.walk(path2):
        for filename in fnmatch.filter(filenames, 'ASTREAM_*.json'):
            jsons[os.path.join(root, filename)] = collections.OrderedDict()
            with open(os.path.join(root, filename), 'r') as json_file:
                json_obj = json.load(json_file)   
                for segment_info in json_obj["segment_info"]:
                    segment_vmaf = segment_info[VMAF]
                    if not segment_vmaf:
                        segment_vmaf = 0
                    jsons[os.path.join(root, filename)][segment_info[SEGMENT_NAME]] = {
                        "bitrate": segment_info[BITRATE], "codec": segment_info[CODEC],
                        "vmaf": segment_vmaf, "segment_size": segment_info[SEGMENT_SIZE],
                        "download_time": segment_info[SEGMENT_DOWNLOAD_TIME]}
        for filename in fnmatch.filter(filenames, 'QOE_*_out.json'):
            qoe_jsons[os.path.join(root, filename)] = collections.OrderedDict()
    # Loop through files and gather data
    fetch_and_plot_single_values(jsons)
    # bitrates, codec_switches, vmafs, sizes = fetch_single_values(jsons)
    # qoe = None
    # qoe = fetch_values_from_jsons(qoe_jsons)
    # print(bitrates)
    # print(codec_switches)
    # print(vmafs)
    # print(stalls)
    # print(stalls_duration)
    # print(start_ups)
    # Plot save figures
    # plot_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path)
    # print(psnr)
    
def fetch_and_plot_videos_results(path):
    # Files to fetch the data and draw the graphs
    jsons = collections.OrderedDict()
    qoe_jsons = collections.OrderedDict()
    path = os.path.join(path)
    # Other directories with ABR names
    astream_matches = []
    json_matches = []
    for video in VIDEOS:
        jsons[video] = dict()
        qoe_jsons[video] = dict()
        for abr in ABRS:
            jsons[video][abr] = dict()
            qoe_jsons[video][abr] = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, 'ASTREAM_*.json'):
            astream_matches.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, 'QOE_*_out.json'):
            json_matches.append(os.path.join(root, filename))
    for match in astream_matches:
        for video in VIDEOS:
            for abr in ABRS:
                if "/{}/".format(abr) in match and "/{}/".format(video) in match:
                    print("Adding file: {}".format(match))
                    with open(match, 'r') as json_file:
                        json_obj = json.load(json_file)
                        if "playback_type" in json_obj:
                            if json_obj["playback_type"] not in jsons[video]:
                                jsons[video][json_obj["playback_type"]] = dict()
                            jsons[video][json_obj["playback_type"]][match] = dict()
                            for segment_info in json_obj["segment_info"]:
                                segment_vmaf = segment_info[VMAF]
                                if not segment_vmaf:
                                    segment_vmaf = 0
                                jsons[video][json_obj["playback_type"]][os.path.join(match)][segment_info[SEGMENT_NAME]] = {
                                    "bitrate": segment_info[BITRATE], "codec": segment_info[CODEC],
                                    "vmaf": segment_vmaf, "segment_size": segment_info[SEGMENT_SIZE],
                                    "download_time": segment_info[SEGMENT_DOWNLOAD_TIME]}
                        if "playback_info" in json_obj:
                            jsons[video][json_obj["playback_type"]][os.path.join(match)]["initial_buffering_duration"] = json_obj["playback_info"]["initial_buffering_duration"]
                            jsons[video][json_obj["playback_type"]][os.path.join(match)]["interruptions"] = []
                            for stall_pair in json_obj["playback_info"]["interruptions"]["events"]:
                                time = stall_pair[0]
                                duration = stall_pair[1] - stall_pair[0]
                                jsons[video][json_obj["playback_type"]][os.path.join(match)]["interruptions"].append([time, duration])
    for match in json_matches:
        for video in VIDEOS:
            for abr in ABRS:
                if "/{}/".format(abr) in match and "/{}/".format(video) in match:
                    if abr not in qoe_jsons[video]:
                        qoe_jsons[video][abr] = []
                    print("Adding file: {}".format(match))
                    qoe_jsons[video][abr].append(match)
    for v in jsons:
        pop_keys = []
        for d in jsons[v]:
            if not jsons[v][d]:
                pop_keys.append(d)
        for p in pop_keys:
            jsons[v].pop(p)
    for v in qoe_jsons:
        pop_keys = []
        for d in qoe_jsons[v]:
            if not qoe_jsons[v][d]:
                pop_keys.append(d)
        for p in pop_keys:
            qoe_jsons[v].pop(p)
    for video in VIDEOS:
        print("--> {}".format(video))
        for abr in jsons[video]:
            print("'{:.0f}' overall JSON files found for ABR '{:s}'".format(len(jsons[video][abr]), abr))
        for abr in qoe_jsons[video]:
            print("'{:.0f}' overall QoE JSON files found for ABR '{:s}'".format(len(qoe_jsons[video][abr]), abr))
    # print(jsons)
    # print(files)
    # Loop through files and gather data
    bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups = fetch_videos_values(jsons)
    # qoe = None
    qoe = fetch_videos_values_from_jsons(qoe_jsons)
    # print(bitrates)
    # print(codec_switches)
    # print(vmafs)
    # print(stalls)
    # print(stalls_duration)
    # print(start_ups)
    # Plot save figures
    plot_videos_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path)
    # print(psnr)
    
    
def fetch_and_boxplot_videos_results(path):
    # Files to fetch the data and draw the graphs
    jsons = collections.OrderedDict()
    qoe_jsons = collections.OrderedDict()
    path = os.path.join(path)
    # Other directories with ABR names
    astream_matches = []
    json_matches = []
    for trace in NET_TRACES:
        jsons[trace] = collections.OrderedDict()
        qoe_jsons[trace] = collections.OrderedDict()
        for video in VIDEOS:
            jsons[trace][video] = collections.OrderedDict()
            qoe_jsons[trace][video] = collections.OrderedDict()
            for abr in ABRS:
                jsons[trace][video][abr] = collections.OrderedDict()
                qoe_jsons[trace][video][abr] = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, 'ASTREAM_*.json'):
            astream_matches.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, 'QOE_*_out.json'):
            json_matches.append(os.path.join(root, filename))
    for match in astream_matches:
        for trace in NET_TRACES:
            for video in VIDEOS:
                for abr in ABRS:
                    if "/{}/".format(abr) in match and "/{}/".format(video) in match and "/{}/".format(trace) in match:
                        print("Adding file: {}".format(match))
                        with open(match, 'r') as json_file:
                            json_obj = json.load(json_file)
                            if "playback_type" in json_obj:
                                if json_obj["playback_type"] not in jsons[trace][video]:
                                    jsons[trace][video][json_obj["playback_type"]] = dict()
                                jsons[trace][video][json_obj["playback_type"]][match] = dict()
                                for segment_info in json_obj["segment_info"]:
                                    segment_vmaf = segment_info[VMAF]
                                    if not segment_vmaf:
                                        segment_vmaf = 0
                                    jsons[trace][video][json_obj["playback_type"]][os.path.join(match)][segment_info[SEGMENT_NAME]] = {
                                        "bitrate": segment_info[BITRATE], "codec": segment_info[CODEC],
                                        "vmaf": segment_vmaf, "segment_size": segment_info[SEGMENT_SIZE],
                                        "download_time": segment_info[SEGMENT_DOWNLOAD_TIME]}
                            if "playback_info" in json_obj:
                                jsons[trace][video][json_obj["playback_type"]][os.path.join(match)]["initial_buffering_duration"] = json_obj["playback_info"]["initial_buffering_duration"]
                                jsons[trace][video][json_obj["playback_type"]][os.path.join(match)]["interruptions"] = []
                                for stall_pair in json_obj["playback_info"]["interruptions"]["events"]:
                                    time = stall_pair[0]
                                    duration = stall_pair[1] - stall_pair[0]
                                    jsons[trace][video][json_obj["playback_type"]][os.path.join(match)]["interruptions"].append([time, duration])
    for match in json_matches:
        for trace in NET_TRACES:
            for video in VIDEOS:
                for abr in ABRS:
                    if "/{}/".format(abr) in match and "/{}/".format(video) in match and "/{}/".format(trace) in match:
                        if abr not in qoe_jsons[trace][video]:
                            qoe_jsons[trace][video][abr] = []
                        print("Adding file: {}".format(match))
                        qoe_jsons[trace][video][abr].append(match)
    for t in jsons:
        for v in jsons[t]:
            pop_keys = []
            for d in jsons[t][v]:
                if not jsons[t][v][d]:
                    pop_keys.append(d)
            for p in pop_keys:
                jsons[t][v].pop(p)
    for t in qoe_jsons:
        for v in qoe_jsons[t]:
            pop_keys = []
            for d in qoe_jsons[t][v]:
                if not qoe_jsons[t][v][d]:
                    pop_keys.append(d)
            for p in pop_keys:
                qoe_jsons[t][v].pop(p)
    for trace in NET_TRACES:
        for video in VIDEOS:
            print("--> {}".format(video))
            for abr in jsons[trace][video]:
                print("'{:.0f}' overall JSON files found for ABR '{:s}'".format(len(jsons[trace][video][abr]), abr))
            for abr in qoe_jsons[trace][video]:
                print("'{:.0f}' overall QoE JSON files found for ABR '{:s}'".format(len(qoe_jsons[trace][video][abr]), abr))
    # print(jsons)
    # print(files)
    # Loop through files and gather data
    bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups = fetch_traces_videos_values(jsons)
    # qoe = None
    qoe = fetch_traces_videos_values_from_jsons(qoe_jsons)
    # print(bitrates)
    # print(codec_switches)
    # print(vmafs)
    # print(stalls)
    # print(stalls_duration)
    # print(start_ups)
    # Plot save figures
    boxplot_videos_results(bitrates, codec_switches, vmafs, sizes, stalls, stalls_duration, start_ups, qoe, path)
    # print(psnr)


# Execute the main
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Fetch data from available CSV files and plot the relative graphs.')
    # parser.add_argument('--maxb', type=int, default=1, help='MaxB ABR will be included in the results.')
    # parser.add_argument('--bola', type=int, default=1, help='Bola ABR will be included in the results.')
    # parser.add_argument('--sara', type=int, default=1, help='Sara ABR will be included in the results.')
    # parser.add_argument('--bba', type=int, default=1, help='BBA ABR will be included in the results.')
    # parser.add_argument('--mcom', type=int, default=0, help='MCOM ABR will be included in the results.')
    # parser.add_argument('--mc', type=int, default=1, help='MCOM Plugin will be included in the results.')
    # parser.add_argument('--ss', type=int, default=1, help='Custom Segment Size-optimized MCOM plugin will be included in the results (for Bola and Sara).')
    parser.add_argument('--path', type=str, default="./", help='Path containing the results.')
    parser.add_argument('--video', type=str, default="tos_5min", help='Video to show the result from.')
    parser.add_argument('--onerun2', type=str, default="", help='Path to plot only for one run.')
    parser.add_argument('--onerun1', type=str, default="", help='Path to plot only for one run.')
    

    args = parser.parse_args()

    # Fetch and plot the results
    if args.video == "all":
        fetch_and_plot_videos_results(args.path)
    elif args.video == "allbox":
        fetch_and_boxplot_videos_results(args.path)
    else:
        if args.onerun1 == "" or args.onerun2 == "":
            fetch_and_plot_results(os.path.join(args.path, args.video))
        else:
            fetch_and_plot_single_results(args.onerun1, args.onerun2)
