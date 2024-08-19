import os
import time
import threading
import sys
import json
sys.path.insert(1, '/home/zenzi/Documents/CAdViSE/')
# sys.path.insert(2, '/lalisa/qoe[P1203]')
# sys.path.insert(2, '/home/farzad/Desktop/LALISA/')
# from artemis.qoe.ConfigPath import  abr, title, iteration, video,segment_duration
# from last_updates import main_def
update_player = 0
# it=0
# Define constants
AWS_KEY = "Daniele.pem"
CLIENT_LOG_DIR = "/home/zenzi/Documents/CAdViSE/logs/"
CLIENT_TEMP_LOG_DIR = "/home/zenzi/Documents/CAdViSE/temp_logs"
EC2_LOG_DIR = "/ASTREAM_LOGS/"
# NET_TRACE = "network/cascade.json"
# NET_TRACE = "/home/zenzi/Documents/CAdViSE/network/4G_trace.json"
NET_TRACE = "network/network0.json"
REAL_NET_TRACE = ["FCC"]  # "cascade", "4G", "FCC", "competition"
BUFFER_SIZE = [20, 40]  # 20, 40 (s)
# title = "rally"
MCOM_VERSION = ""  # "-instability"
# ABRS = ["basic"]
# ABRS = ["basic", "sara", "netflix", "bola", "basic-mcom", "sara-mcom", "netflix-mcom", "bola-mcom"]
# ABRS = ["netflix", "netflix-mcom", "bola", "bola-mcom"]
ABRS = ["basic", "basic-mcom", "bola", "bola-mcom", "netflix", "netflix-mcom", "sara", "sara-mcom"]
VIDEOS = ["tos_5min", "tos_5min_end", "gameplay", "rally"]
# VIDEOS = ["rally"]
# VIDEOS = ["rally"]
# abr = "sara"  # "BASIC", "NETFLIX", "SARA", "BOLA", "{ABR}-MCOM"
TOTAL_RUNS = 1

def downloader(cmd):
    os.system(cmd)
    time.sleep(2)


def dataprovider(it, client, abr, video, net, exp_id, clientIP, buff_size):
    time.sleep(30)
    abr_log_dir = os.path.join(CLIENT_LOG_DIR, "{}s".format(str(buff_size)), str(net), str(video), "{}{}".format(abr, MCOM_VERSION), str(exp_id) + '_' + str(client))
    os.makedirs(abr_log_dir, exist_ok=True)
    # print('iteration: ' + str(it) + ' network: ' + str(net) + ' abr: ' + abr + '----------------Collecting results')
    # cmd = ' ssh -y -oStrictHostKeyChecking=no -i ' + AWS_KEY + ' ec2-user@' + client
    # os.system(cmd)
    # time.sleep(2)
    print ('iteration:' + str(it) + ' client: ' + str(client) + '----------------Collecting details ')
    # cmd = ' scp -rp -oStrictHostKeyChecking=no -i ' + AWS_KEY + ' ec2-user@' + client + ':' + EC2_LOG_DIR + ' ' + abr_log_dir + '_' + str(
    #     bl) + '_' + str(net) + '_' + exp_id + '_' + clientIP[client] + '-original.log'
    cmd = ' scp -rp -oStrictHostKeyChecking=no -i ' + AWS_KEY + ' ec2-user@' + client + ':' + EC2_LOG_DIR + ' ' + abr_log_dir
    os.system(cmd)
    time.sleep(5)
    clientInstanceIds = ""
    serverInstanceId = ""
    with open("{}/instances.json".format(exp_id)) as f:
        json_data = json.load(f)
        for instance in json_data["Instances"]:
            clientInstanceIds += "{} ".format(instance["InstanceId"])
    with open("{}/instance.json".format(exp_id)) as f:
        json_data = json.load(f)
        for instance in json_data["Instances"]:
            serverInstanceId += "{} ".format(instance["InstanceId"])
    cmd = 'aws ec2 terminate-instances --instance-ids {} {} > /dev/null &'.format(clientInstanceIds, serverInstanceId)
    os.system(cmd)


def run_scenario(it, net_trace_path, real_net_trace, video, abr, buff_size):
    global update_player
    net = net_trace_path.split('/')[-1].split('.')[0]
    medusa = 0
    if "mcom" in abr:
        medusa = 1
    print('iteration:' + str(it) + ' buffer_size: ' + str(buff_size) + 's network: ' + str(real_net_trace) + ' video: ' + video + ' abr:' + abr + '------------Start')
    cmd = './run.sh --abr ' + abr.split("-")[0] + ' --medusa ' + str(medusa) + ' --title ' + video + ' --shaper ' + net_trace_path + ' --realtrace ' + real_net_trace + ' --bsize ' + str(buff_size) + ' --awsKey ' + AWS_KEY.split(".")[0]
    log = 'iteration_' + str(it) + '_abr_' + abr + '_network_' + str(real_net_trace) + '.log'
    os.makedirs(CLIENT_TEMP_LOG_DIR, exist_ok=True)
    log_path = os.path.join(CLIENT_TEMP_LOG_DIR, log)
    f = open(log_path, 'w')
    os.system(cmd + ' > ' + log_path + '&')
    cnt = True
    vrpcIP = []
    clientIP = {}
    allreadlines = []
    last_print=""
    flag=0
    while cnt:
        f2 = open(log_path, 'r')
        data = f2.readlines()
        if len(data)>0 and data[-1]!=last_print:
            print(data[-1])
            last_print=data[-1]
        for l in data:
            if l not in allreadlines or ('0:0' in l and l==data[-1]):
                allreadlines.append(l)
                if 'Experiment' in l:
                    l = l.replace('\x1b[0m\n', '')
                    exp_id = l.split(':')[1].replace(' ', '')
                    print('exp_id', exp_id)
                if ('0:0' in l and flag == 1) or ("Requesting the analytics data" in l):
                    print("Entering datacollection phase...")
                    for client in clientIP.keys():
                        x = threading.Thread(target=dataprovider, args=(it, client, abr, video, real_net_trace, exp_id, clientIP, buff_size))
                        x.start()
                    cnt = False
                    # download vrp.log from vrpc
                    # main_def('stop')

                # if '0:0' in l:
                #     # update players and vrpc
                #     if not (update_player):
                #         main_def('start')
                #         update_player = 1

                if 'Running experiment' in l:
                    print("Flag modified to 1")
                    flag = 1

                # if '***vrpc***' in l:
                #     l = l.replace('\x1b[0m\n', '')
                #     if l.split('***vrpc***')[1] not in vrpcIP:
                #         vrpcIP.append(l.split('***vrpc***')[1])
                #         print('iteration:' + str(it) + ' network: ' + str(net) + ' vrpcIP', vrpcIP)
                if '***client***' in l:
                    l = l.replace('\x1b[0m\n', '')
                    if l.split('***client***')[1] not in clientIP.keys():
                        clientIP[l.split('***client***')[1]] = l.split('***')[0].split(' ')[-2].replace('[',
                                                                                                        '').replace(']',
                                                                                                                    '')
                        print(
                            'iteration:' + str(it) + ' network: ' + str(net) + ' client ' + l.split('***client***')[1],
                            clientIP[l.split('***client***')[1]])
                        if os.path.isfile("ip_name.csv"):
                            ip_name = open('ip_name.csv', 'a')
                        else:
                            ip_name = open('ip_name.csv', 'w')
                        # ip_name = open('clientlog/ip_name.csv', 'a')
                        ip_name.write(str(exp_id) + ',' + l.split('***client***')[1] + ',' + clientIP[
                            l.split('***client***')[1]] + '\n')
                        ip_name.close()
        time.sleep(1)
    print('iteration:' + str(it) + ' network: ' + str(net) + ' video: ' + video + ' abr:' + abr + '------------Finish')


# def xdef():
#     os.system('rm templog/*.log')
#     # if allow_to_del_known_host:
#     os.system('truncate -s 0 /root/.ssh/known_hosts')
#     os.system('rm clientlog/*.*')
#     os.system('rm vrpclog/*.*')
#     iteration1 = iteration
#
#     # -----------------------------
#     player_number = [10]
#     ladder1 = 'ladder'
#     network1 = 'network'
#     # -----------------------------
#     for pn in player_number:
#         fn = abr[0].upper() + abr[1:] + '|' + video + str(segment_duration) + ' |client ' + str(pn) + '|LTE-' + str(
#             network1) + 's|ladder ' + ladder1
#         for it in range(0, iteration1):
#             # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<' + fn + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> round '+str(it))
#             # os.system('rm templog/*.log')
#             # os.system('truncate -s 0 /root/.ssh/known_hosts')
#             run_scenario(it, str(network1), ladder1)


if __name__ == '__main__':
    # os.system('rm {}/*.log'.format(CLIENT_TEMP_LOG_DIR))
    # if allow_to_del_known_host:
    # os.system('truncate -s 0 /root/.ssh/known_hosts')
    # os.system('rm {}/*.*'.format(CLIENT_LOG_DIR))
    #-----------------------------
    player_number = 20
    # ladder1='ladder'
    # network1='network'
    # -----------------------------
    # for pn in player_number:
        # fn=abr[0].upper()+abr[1:]+'|'+video+str(segment_duration)+' |client '+str(pn)+'|LTE-'+str(network1)+'s|ladder '+ladder1
        # for it in range(0, iteration1):
        #     # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<' + fn + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> round '+str(it))
        #     # os.system('rm templog/*.log')
        #     # os.system('truncate -s 0 /root/.ssh/known_hosts')
        #     run_scenario(it, network1, ladder1)
    # for it in range(0, player_number):
            # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<' + fn + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> round '+str(it))
            # os.system('rm templog/*.log')
            # os.system('truncate -s 0 /root/.ssh/known_hosts')
            # x = threading.Thread(target=run_scenario, args=(it, NET_TRACE))
            # x.start()
            # time.sleep(5)
    it = 0
    for i in range(TOTAL_RUNS):  # Run for TOTAL_RUNS time
        for trace in REAL_NET_TRACE:
            for b in BUFFER_SIZE:
                for video in VIDEOS:
                    for abr in ABRS:
                        # x = threading.Thread(target=run_scenario, args=(it, NET_TRACE, REAL_NET_TRACE, video, abr, BUFFER_SIZE))
                        # x.start()
                        run_scenario(it, NET_TRACE, trace, video, abr, b)
                        it += 1
                        # time.sleep(5)

