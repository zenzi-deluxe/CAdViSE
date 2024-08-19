# To convert windows scripts to unix scripts use the following command:
# sed -i 's/\r//g' file

import json

def fix_trace(file):

    network_traces = ""

    with open(file, 'r') as f:
        for line in f:
            if "rate" in line and "latency" in line and "burst" in line:
                # rate = float(re.compile(r"rate ([0-9]+)kbit ").search(line).group(1))  # in Kbit/s
                # burst = rate * 1000 / 8 / HZ
                # if burst < 1:
                #     burst = rate
                # network_traces += re.sub(r"burst [0-9]+", "burst {:.0f}".format(burst), line)
                words = line.split(" ")
                rate_ind = 0
                burst_ind = 0
                for ind, word in enumerate(words):
                    if word == "rate":
                        rate_ind = ind + 1
                    elif word == "burst":
                        burst_ind = ind + 1
                rate = float(words[rate_ind][:-4])  # in Kbit/s
                meas = words[rate_ind][-4:]
                # burst = rate * 1000 / 8 / HZ
                burst = rate
                if burst < 1:
                    burst = rate
                words[burst_ind] = "{:.0f}".format(burst)
                network_traces += ' '.join(words) + '\n'
            else:
                network_traces += line
            # network_traces += "\n"

    # File name and extension from input file
    file_name, ext = file.split(".")
    with open("{}_new.{}".format(file_name, ext), 'w') as wf:
        wf.write(network_traces)


def generate_trace_from_file(file, kernel_HZ, max_seconds):

    global useHZ

    network_traces = "#!/usr/bin/env bash\n"
    network_traces += "interface=\"ens33\"\n"
    network_traces += "while getopts i: flag\n"
    network_traces += "do\n"
    network_traces += "    case \"${flag}\" in\n"
    network_traces += "    i) interface=${OPTARG};;\n"
    network_traces += "    esac\n"
    network_traces += "done\n\n"
    network_traces += "tc qdisc del dev $interface root\n"

    with open(file, 'r') as f:
        lines = f.readlines()
        rate = float(lines[0]) / 1000  # in kbps
        burst = rate
        if useHZ:
            burst = rate * 1000 / 8 / kernel_HZ
        network_traces += "tc qdisc add dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(rate, burst)
        network_traces += "sleep 1.0s\n"
        seconds = 1
        for line in lines[1:]:
            rate = float(line) / 1000  # in kbps
            burst = rate
            if useHZ:
                burst = rate * 1000 / 8 / kernel_HZ
            network_traces += "tc qdisc change dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(rate, burst)
            network_traces += "sleep 1.0s\n"
            seconds += 1
            if seconds > max_seconds:
                break
        network_traces += "tc qdisc del dev $interface root\n"

    # File name and extension from input file
    file_name, ext = file.split(".")
    with open("{}_new.{}".format(file_name, "sh"), 'w') as wf:
        wf.write(network_traces)


def generate_trace_from_ghent_log(log_file, kernel_HZ, max_seconds):
    global useHZ

    network_traces = "#!/usr/bin/env bash\n"
    network_traces += "interface=\"ens33\"\n"
    network_traces += "while getopts i: flag\n"
    network_traces += "do\n"
    network_traces += "    case \"${flag}\" in\n"
    network_traces += "    i) interface=${OPTARG};;\n"
    network_traces += "    esac\n"
    network_traces += "done\n\n"
    network_traces += "tc qdisc del dev $interface root\n"

    # Log_file format:
    # - Number of milliseconds since epoch;
    # - Number of milliseconds since start of experiment;
    # - GPS latitude in decimal degrees;
    # - GPS longitude in decimal degrees;
    # - Number of bytes received since last datapoint;
    # - Number of milliseconds since last datapoint.

    rate_trend = []

    with open(log_file, 'r') as f:
        lines = f.readlines()
        ms_since_epoch, ms_since_exp, latitude, longitude, bytes, ms = lines[0].split(" ")
        rate = float(bytes) / float(ms)  # in kbps
        burst = rate
        if useHZ:
            burst = rate * 1000 / 8 / kernel_HZ
        network_traces += "tc qdisc add dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(
            rate, burst)
        network_traces += "sleep 1.0s\n"
        seconds = 1
        rate_trend.append(rate)
        for line in lines[1:]:
            ms_since_epoch, ms_since_exp, latitude, longitude, bytes, ms = line.split(" ")
            rate = float(bytes) / float(ms)  # in kbps
            burst = rate
            if useHZ:
                burst = rate * 1000 / 8 / kernel_HZ
            network_traces += "tc qdisc change dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(
                rate, burst)
            network_traces += "sleep 1.0s\n"
            rate_trend.append(rate)
            seconds += 1
            if seconds > max_seconds:
                break
        network_traces += "tc qdisc del dev $interface root\n"

    # File name and extension from input file
    file_name = log_file.split(".")[0]
    with open("{}_new.{}".format(file_name, "sh"), 'w') as wf:
        wf.write(network_traces)

    # Plot the network trace and save the figure
    import matplotlib.pyplot as plt
    # Figure, axis objects
    fig, ax = plt.subplots()
    ax.plot(rate_trend)
    # Title
    plt.title("Network trace")
    # X axis label
    plt.xlabel("Time (s)")
    # Y axis label
    plt.ylabel("Throughput (kbps)")
    # Save figure
    plt.savefig("{}_new".format(file_name))
    # Show figure
    plt.show()


def generate_trace_from_nyu_csv(log_file, kernel_HZ, max_seconds):
    global useHZ

    network_traces = "#!/usr/bin/env bash\n"
    network_traces += "interface=\"ens33\"\n"
    network_traces += "while getopts i: flag\n"
    network_traces += "do\n"
    network_traces += "    case \"${flag}\" in\n"
    network_traces += "    i) interface=${OPTARG};;\n"
    network_traces += "    esac\n"
    network_traces += "done\n\n"
    network_traces += "tc qdisc del dev $interface root\n"

    rate_trend = []

    with open(log_file, 'r') as f:
        lines = f.readlines()
        rate, mu = lines[0].split(",")
        print(mu)
        crate = 1
        if mu.strip() == "Mbits/sec":
            crate = 1000  # kbits
        elif mu.strip() == "Kbits/sec":
            crate = 1  # Kbits
        new_rate = float(rate) * crate
        burst = new_rate
        if useHZ:
            burst = new_rate * 1000 / 8 / kernel_HZ
        network_traces += "tc qdisc add dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(
            new_rate, burst)
        network_traces += "sleep 1.0s\n"
        seconds = 1
        rate_trend.append(new_rate)
        for line in lines[1:]:
            rate, mu = line.split(",")
            if mu == "Mbits/sec":
                crate = 1000  # kbits
            elif mu == "Kbits/sec":
                crate = 1  # Kbits
            new_rate = float(rate) * crate
            burst = new_rate
            if useHZ:
                burst = new_rate * 1000 / 8 / kernel_HZ
            print(new_rate)
            network_traces += "tc qdisc add dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(
                new_rate, burst)
            network_traces += "sleep 1.0s\n"
            rate_trend.append(new_rate)
            seconds += 1
            if seconds > max_seconds:
                break
        network_traces += "tc qdisc del dev $interface root\n"

    # File name and extension from input file
    file_name = log_file.split(".")[0]
    with open("{}_tc.{}".format(file_name, "sh"), 'w') as wf:
        wf.write(network_traces)

    return "{}_tc.{}".format(file_name, "sh")



def generate_json_from_sh(sh_file, output_json_file):
    network_traces = []
    with open(sh_file, 'r') as f:
        rate = 0
        for line in f:
            if "rate" in line and "latency" in line and "burst" in line:
                # rate = float(re.compile(r"rate ([0-9]+)kbit ").search(line).group(1))  # in Kbit/s
                # burst = rate * 1000 / 8 / HZ
                # if burst < 1:
                #     burst = rate
                # network_traces += re.sub(r"burst [0-9]+", "burst {:.0f}".format(burst), line)
                words = line.split(" ")
                rate_ind = 0
                for ind, word in enumerate(words):
                    if word == "rate":
                        rate_ind = ind + 1
                rate = int(words[rate_ind][:-4])  # in Kbit/s
                # meas = words[rate_ind][-4:]
                # burst = rate * 1000 / 8 / HZ
                step_trace = {}
            elif "sleep" in line:
                sleep_for = float(line.split(" ")[1][:-2])
                if sleep_for == 0:
                    continue
                network_traces.append(
                    {"duration": int(sleep_for),
                     "serverIngress": 0,
                     "serverEgress": 0,
                     "serverLatency": 0,
                     "clientIngress": rate,
                     "clientEgress": 0,
                     "clientLatency": 0})

    print(network_traces)
    # File name and extension from input file
    with open(output_json_file, 'w') as wf:
        json.dump(network_traces, wf, indent=4)


def generate_trace_v2(csv_file, kernel_HZ):
    # Timestamp, DL_bitrate
    # Timestamp format: 2018.02.05_15.07.33
    import pandas as pd
    from datetime import datetime
    import time
    import math
    df = pd.read_csv(csv_file)
    # print(df)
    df = df.reset_index()  # make sure indexes pair with number of rows
    timestamps = []
    for t in list(df['Timestamp']):
        timestamps.append(time.mktime(datetime.strptime(t, "%Y.%m.%d_%H.%M.%S").timetuple()))
    # print(timestamps)
    bitrates = list(df['DL_bitrate'])  # kbps
    # print(bitrates)
    global useHZ

    network_traces = "#!/usr/bin/env bash\n"
    network_traces += "interface=\"ens33\"\n"
    network_traces += "while getopts i: flag\n"
    network_traces += "do\n"
    network_traces += "    case \"${flag}\" in\n"
    network_traces += "    i) interface=${OPTARG};;\n"
    network_traces += "    esac\n"
    network_traces += "done\n\n"
    network_traces += "tc qdisc del dev $interface root\n"

    if len(timestamps) == 0 or len(bitrates) == 0:
        print("No value found in the csv file for either timestamp or bitrate. Exiting now.")
        exit(1)
    # First add network trace
    burst = bitrates[0]
    if useHZ:
        burst = bitrates[0] * 1000 / 8 / kernel_HZ
    if math.floor(bitrates[0]) == 0:
        network_traces += "tc qdisc add dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(1, 1)
    else:
        network_traces += "tc qdisc add dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(bitrates[0], burst)
    if len(timestamps) > 1:
        network_traces += "sleep {:.1f}s\n".format(timestamps[1] - timestamps[0])
    # Iterate through the list
    for b_ind, b in enumerate(bitrates[1:], start=1):
        # Burst cannot be lower than 1 except when rate is 0
        burst = b
        if useHZ:
            burst = math.floor(b * 1000 / 8 / kernel_HZ)
        if math.floor(b) == 0:
            network_traces += "tc qdisc change dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(1, 1)
            network_traces += "echo \"Bitrate {:.0f}kbit, latency 20ms, burst {:.0f}\"\n".format(1, 1)
        else:
            network_traces += "tc qdisc change dev $interface root tbf rate {:.0f}kbit latency 20ms burst {:.0f}\n".format(b, burst)
            network_traces += "echo \"Bitrate {:.0f}kbit, latency 20ms, burst {:.0f}\"\n".format(b, burst)
        if b_ind + 1 < len(bitrates):
            network_traces += "sleep {:.1f}s\n".format(timestamps[b_ind + 1] - timestamps[b_ind])
    network_traces += "tc qdisc del dev $interface root\n"

    # File name and extension from input file
    file_name = csv_file.split(".")[0]
    with open("{}_new.{}".format(file_name, "sh"), 'w') as wf:
        wf.write(network_traces)
    # Plot the network trace and save the figure
    import matplotlib.pyplot as plt
    # Figure, axis objects
    fig, ax = plt.subplots()
    ax.plot(bitrates)
    # Title
    plt.title("Network trace")
    # X axis label
    plt.xlabel("Time (s)")
    # Y axis label
    plt.ylabel("Throughput (kbps)")
    # Save figure
    plt.savefig("{}_new".format(file_name))
    # Show figure
    plt.show()


def generate_wondershaper_from_file(sh_file, max_seconds=None):
    network_traces = "# !/bin/bash\n"
    rates = []
    with open(sh_file, 'r') as f:
        rate = 0
        seconds = 0
        for line in f:
            if max_seconds and seconds > max_seconds:
                break
            if "rate" in line and "latency" in line and "burst" in line:
                # rate = float(re.compile(r"rate ([0-9]+)kbit ").search(line).group(1))  # in Kbit/s
                # burst = rate * 1000 / 8 / HZ
                # if burst < 1:
                #     burst = rate
                # network_traces += re.sub(r"burst [0-9]+", "burst {:.0f}".format(burst), line)
                words = line.split(" ")
                rate_ind = 0
                for ind, word in enumerate(words):
                    if word == "rate":
                        rate_ind = ind + 1
                rate = int(words[rate_ind][:-4])  # in Kbit/s
                # meas = words[rate_ind][-4:]
                # burst = rate * 1000 / 8 / HZ
                network_traces += "sudo /home/ec2-user/wondershaper/wondershaper -a eth0 -c\n"
                network_traces += "sudo /home/ec2-user/wondershaper/wondershaper -a eth0 -d {} -u 50000\n".format(rate)
                rates.append(rate)
            elif "sleep" in line:
                sleep_for = float(line.split(" ")[1][:-2])
                seconds += sleep_for
                if sleep_for == 0:
                    continue
                network_traces += "sleep {}\n\n".format(int(sleep_for))

    # File name and extension from input file
    with open("{}_wondershaper.{}".format(sh_file.split(".")[0], "sh"), 'w') as wf:
        wf.write(network_traces)

    # Plot the network trace and save the figure
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 14})
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(rates, marker="^")
    # Settings
    plt.xlim([0,None])
    plt.ylim([0,None])
    # Title
    plt.title("NYU bus LTE network trace")
    # X axis label
    plt.xlabel("Time (s)")
    # Y axis label
    plt.ylabel("Throughput (kbps)")
    # Save figure
    plt.savefig("{}_new.pdf".format(sh_file.split(".")[0]), format="pdf")
    # Show figure
    plt.show()
    
def plot_trace_from_sh(sh_file):
    rates = []
    with open(sh_file, 'r') as f:
        rate = 0
        for line in f:
            if " -d " in line:
                words = line.split(" ")
                rate_ind = 0
                for ind, word in enumerate(words):
                    if word == "-d":
                        rate_ind = ind + 1
                rate = int(words[rate_ind])  # in Kbit/s
            # Check also if "rate" is in line (for tc commands)
            elif "sleep" in line:
                sleep_for = int(line.split(" ")[1].strip())
                for i in range(sleep_for):
                    rates.append(rate)
    # Plot the network trace and save the figure
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 14})
    # Figure, axis objects
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(rates, marker="^")
    # Settings
    plt.xlim([0,400])
    plt.ylim([0,None])
    # Title
    plt.title("Amazon FCC network trace")
    # X axis label
    plt.xlabel("Time (s)")
    # Y axis label
    plt.ylabel("Throughput (kbps)")
    # Save figure
    plt.savefig("{}.pdf".format(sh_file.split(".")[0]), format="pdf")
    # Show figure
    plt.show()

def compute_total_length_from_json(output_json_file):
    with open(output_json_file, 'r') as f:
        json_handler = json.load(f)
        length = sum(j["duration"] for j in json_handler)
        print(length)


if __name__ == '__main__':
    # import re

    useHZ = True
    #
    HZ = 250
    #
    script_max_seconds = 6 * 60  # 6 minutes

    # parser = argparse.ArgumentParser(
    #     description='Fix trace settings in a trace script based on assigned rate.')
    # parser.add_argument('--file', type=str, default="4G_trace.sh", help='Path to file/script containing the network trace.')
    #
    # args = parser.parse_args()
    #
    # file = args.file

    TRACES_FOLDER = "network"
    # script_file = "4G_trace.sh"
    # csv_file = "edge.csv"
    csv_file = "{}/bus57_1.csv".format(TRACES_FOLDER)
    sh_file = "{}/4G_trace.sh".format(TRACES_FOLDER)
    output_json_file = "{}/4G_trace.json".format(TRACES_FOLDER)
    wondershaper_file = "{}/amzonfcc.sh".format(TRACES_FOLDER)

    # fix_trace(script_file)
    # generate_trace_from_file(csv_file, HZ, script_max_seconds)
    # generate_trace_from_ghent_log(txt_file, HZ, script_max_seconds)
    # generate_trace_v2(csv_file, HZ)
    # generate_json_from_sh(sh_file, output_json_file)
    # generate_wondershaper_from_file(generate_trace_from_nyu_csv(csv_file, HZ, script_max_seconds))
    # generate_wondershaper_from_file(sh_file, script_max_seconds)
    # compute_total_length_from_json(output_json_file)
    plot_trace_from_sh(wondershaper_file)
