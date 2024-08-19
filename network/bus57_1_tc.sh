#!/usr/bin/env bash
interface="ens33"
while getopts i: flag
do
    case "${flag}" in
    i) interface=${OPTARG};;
    esac
done

tc qdisc del dev $interface root
tc qdisc add dev $interface root tbf rate 3970kbit latency 20ms burst 1985
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4430kbit latency 20ms burst 2215
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3640kbit latency 20ms burst 1820
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4830kbit latency 20ms burst 2415
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3830kbit latency 20ms burst 1915
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4460kbit latency 20ms burst 2230
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4080kbit latency 20ms burst 2040
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4950kbit latency 20ms burst 2475
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4080kbit latency 20ms burst 2040
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6290kbit latency 20ms burst 3145
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8480kbit latency 20ms burst 4240
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4040kbit latency 20ms burst 2020
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6150kbit latency 20ms burst 3075
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4960kbit latency 20ms burst 2480
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5670kbit latency 20ms burst 2835
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8170kbit latency 20ms burst 4085
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6040kbit latency 20ms burst 3020
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7090kbit latency 20ms burst 3545
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6110kbit latency 20ms burst 3055
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3360kbit latency 20ms burst 1680
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2660kbit latency 20ms burst 1330
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2530kbit latency 20ms burst 1265
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11600kbit latency 20ms burst 5800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14800kbit latency 20ms burst 7400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16100kbit latency 20ms burst 8050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5890kbit latency 20ms burst 2945
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3960kbit latency 20ms burst 1980
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2130kbit latency 20ms burst 1065
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2530kbit latency 20ms burst 1265
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2740kbit latency 20ms burst 1370
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2680kbit latency 20ms burst 1340
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3000kbit latency 20ms burst 1500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3290kbit latency 20ms burst 1645
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3760kbit latency 20ms burst 1880
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3740kbit latency 20ms burst 1870
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3850kbit latency 20ms burst 1925
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3690kbit latency 20ms burst 1845
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4770kbit latency 20ms burst 2385
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2750kbit latency 20ms burst 1375
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8070kbit latency 20ms burst 4035
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5500kbit latency 20ms burst 2750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5040kbit latency 20ms burst 2520
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4620kbit latency 20ms burst 2310
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6740kbit latency 20ms burst 3370
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4040kbit latency 20ms burst 2020
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4380kbit latency 20ms burst 2190
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3760kbit latency 20ms burst 1880
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5210kbit latency 20ms burst 2605
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4060kbit latency 20ms burst 2030
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5180kbit latency 20ms burst 2590
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3780kbit latency 20ms burst 1890
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7960kbit latency 20ms burst 3980
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2880kbit latency 20ms burst 1440
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3830kbit latency 20ms burst 1915
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4980kbit latency 20ms burst 2490
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5500kbit latency 20ms burst 2750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7130kbit latency 20ms burst 3565
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7020kbit latency 20ms burst 3510
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6650kbit latency 20ms burst 3325
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6290kbit latency 20ms burst 3145
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5920kbit latency 20ms burst 2960
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8810kbit latency 20ms burst 4405
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8420kbit latency 20ms burst 4210
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9840kbit latency 20ms burst 4920
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9260kbit latency 20ms burst 4630
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5030kbit latency 20ms burst 2515
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5250kbit latency 20ms burst 2625
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4740kbit latency 20ms burst 2370
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2680kbit latency 20ms burst 1340
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2350kbit latency 20ms burst 1175
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3730kbit latency 20ms burst 1865
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3960kbit latency 20ms burst 1980
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2750kbit latency 20ms burst 1375
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2880kbit latency 20ms burst 1440
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2870kbit latency 20ms burst 1435
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3430kbit latency 20ms burst 1715
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5120kbit latency 20ms burst 2560
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3800kbit latency 20ms burst 1900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4410kbit latency 20ms burst 2205
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3850kbit latency 20ms burst 1925
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3980kbit latency 20ms burst 1990
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4320kbit latency 20ms burst 2160
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3100kbit latency 20ms burst 1550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3630kbit latency 20ms burst 1815
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4410kbit latency 20ms burst 2205
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3210kbit latency 20ms burst 1605
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5020kbit latency 20ms burst 2510
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2580kbit latency 20ms burst 1290
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4860kbit latency 20ms burst 2430
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4140kbit latency 20ms burst 2070
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4630kbit latency 20ms burst 2315
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6530kbit latency 20ms burst 3265
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5520kbit latency 20ms burst 2760
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3830kbit latency 20ms burst 1915
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2440kbit latency 20ms burst 1220
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4890kbit latency 20ms burst 2445
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5800kbit latency 20ms burst 2900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6230kbit latency 20ms burst 3115
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3070kbit latency 20ms burst 1535
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2730kbit latency 20ms burst 1365
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4110kbit latency 20ms burst 2055
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10900kbit latency 20ms burst 5450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15300kbit latency 20ms burst 7650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16600kbit latency 20ms burst 8300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7890kbit latency 20ms burst 3945
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11400kbit latency 20ms burst 5700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12800kbit latency 20ms burst 6400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13300kbit latency 20ms burst 6650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9860kbit latency 20ms burst 4930
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14200kbit latency 20ms burst 7100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11300kbit latency 20ms burst 5650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11100kbit latency 20ms burst 5550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10400kbit latency 20ms burst 5200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6080kbit latency 20ms burst 3040
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8980kbit latency 20ms burst 4490
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13800kbit latency 20ms burst 6900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16400kbit latency 20ms burst 8200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12700kbit latency 20ms burst 6350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12200kbit latency 20ms burst 6100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12400kbit latency 20ms burst 6200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11400kbit latency 20ms burst 5700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12800kbit latency 20ms burst 6400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10700kbit latency 20ms burst 5350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8950kbit latency 20ms burst 4475
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7970kbit latency 20ms burst 3985
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9410kbit latency 20ms burst 4705
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9580kbit latency 20ms burst 4790
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9220kbit latency 20ms burst 4610
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11600kbit latency 20ms burst 5800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10800kbit latency 20ms burst 5400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11200kbit latency 20ms burst 5600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8330kbit latency 20ms burst 4165
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6440kbit latency 20ms burst 3220
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6160kbit latency 20ms burst 3080
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3430kbit latency 20ms burst 1715
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5640kbit latency 20ms burst 2820
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6820kbit latency 20ms burst 3410
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8840kbit latency 20ms burst 4420
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8760kbit latency 20ms burst 4380
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8490kbit latency 20ms burst 4245
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7030kbit latency 20ms burst 3515
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5030kbit latency 20ms burst 2515
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5780kbit latency 20ms burst 2890
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6090kbit latency 20ms burst 3045
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6000kbit latency 20ms burst 3000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5670kbit latency 20ms burst 2835
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7770kbit latency 20ms burst 3885
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7190kbit latency 20ms burst 3595
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5610kbit latency 20ms burst 2805
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5480kbit latency 20ms burst 2740
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5500kbit latency 20ms burst 2750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6670kbit latency 20ms burst 3335
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8120kbit latency 20ms burst 4060
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8640kbit latency 20ms burst 4320
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11200kbit latency 20ms burst 5600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9410kbit latency 20ms burst 4705
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11200kbit latency 20ms burst 5600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15700kbit latency 20ms burst 7850
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13000kbit latency 20ms burst 6500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15500kbit latency 20ms burst 7750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 22300kbit latency 20ms burst 11150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16300kbit latency 20ms burst 8150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18700kbit latency 20ms burst 9350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 23200kbit latency 20ms burst 11600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14800kbit latency 20ms burst 7400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14500kbit latency 20ms burst 7250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16500kbit latency 20ms burst 8250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16900kbit latency 20ms burst 8450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16400kbit latency 20ms burst 8200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12300kbit latency 20ms burst 6150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14200kbit latency 20ms burst 7100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11300kbit latency 20ms burst 5650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7110kbit latency 20ms burst 3555
sleep 1.0s
tc qdisc add dev $interface root tbf rate 1540kbit latency 20ms burst 770
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2250kbit latency 20ms burst 1125
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3050kbit latency 20ms burst 1525
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4120kbit latency 20ms burst 2060
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5600kbit latency 20ms burst 2800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6100kbit latency 20ms burst 3050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6880kbit latency 20ms burst 3440
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11200kbit latency 20ms burst 5600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15900kbit latency 20ms burst 7950
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12900kbit latency 20ms burst 6450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19900kbit latency 20ms burst 9950
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9800kbit latency 20ms burst 4900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12100kbit latency 20ms burst 6050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9520kbit latency 20ms burst 4760
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12500kbit latency 20ms burst 6250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13200kbit latency 20ms burst 6600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9450kbit latency 20ms burst 4725
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10400kbit latency 20ms burst 5200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6730kbit latency 20ms burst 3365
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10100kbit latency 20ms burst 5050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8410kbit latency 20ms burst 4205
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11500kbit latency 20ms burst 5750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8150kbit latency 20ms burst 4075
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7660kbit latency 20ms burst 3830
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11600kbit latency 20ms burst 5800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10800kbit latency 20ms burst 5400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10600kbit latency 20ms burst 5300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13600kbit latency 20ms burst 6800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18700kbit latency 20ms burst 9350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11300kbit latency 20ms burst 5650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15500kbit latency 20ms burst 7750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13600kbit latency 20ms burst 6800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15500kbit latency 20ms burst 7750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10700kbit latency 20ms burst 5350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7500kbit latency 20ms burst 3750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5090kbit latency 20ms burst 2545
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5150kbit latency 20ms burst 2575
sleep 1.0s
tc qdisc add dev $interface root tbf rate 4470kbit latency 20ms burst 2235
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5220kbit latency 20ms burst 2610
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5890kbit latency 20ms burst 2945
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6280kbit latency 20ms burst 3140
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6500kbit latency 20ms burst 3250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5420kbit latency 20ms burst 2710
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6070kbit latency 20ms burst 3035
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6950kbit latency 20ms burst 3475
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7450kbit latency 20ms burst 3725
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7020kbit latency 20ms burst 3510
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9630kbit latency 20ms burst 4815
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10900kbit latency 20ms burst 5450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11300kbit latency 20ms burst 5650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12300kbit latency 20ms burst 6150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11400kbit latency 20ms burst 5700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14600kbit latency 20ms burst 7300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15400kbit latency 20ms burst 7700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15300kbit latency 20ms burst 7650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14900kbit latency 20ms burst 7450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13200kbit latency 20ms burst 6600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14400kbit latency 20ms burst 7200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15800kbit latency 20ms burst 7900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16300kbit latency 20ms burst 8150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14100kbit latency 20ms burst 7050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12200kbit latency 20ms burst 6100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12900kbit latency 20ms burst 6450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14900kbit latency 20ms burst 7450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14400kbit latency 20ms burst 7200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17500kbit latency 20ms burst 8750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12300kbit latency 20ms burst 6150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12700kbit latency 20ms burst 6350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13300kbit latency 20ms burst 6650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13100kbit latency 20ms burst 6550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12200kbit latency 20ms burst 6100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12400kbit latency 20ms burst 6200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13600kbit latency 20ms burst 6800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16000kbit latency 20ms burst 8000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8050kbit latency 20ms burst 4025
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10500kbit latency 20ms burst 5250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12600kbit latency 20ms burst 6300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10900kbit latency 20ms burst 5450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13000kbit latency 20ms burst 6500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10500kbit latency 20ms burst 5250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14800kbit latency 20ms burst 7400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11200kbit latency 20ms burst 5600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10500kbit latency 20ms burst 5250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9250kbit latency 20ms burst 4625
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15100kbit latency 20ms burst 7550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19100kbit latency 20ms burst 9550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16000kbit latency 20ms burst 8000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 22200kbit latency 20ms burst 11100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20700kbit latency 20ms burst 10350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 22000kbit latency 20ms burst 11000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18900kbit latency 20ms burst 9450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16700kbit latency 20ms burst 8350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17000kbit latency 20ms burst 8500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20200kbit latency 20ms burst 10100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14200kbit latency 20ms burst 7100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19000kbit latency 20ms burst 9500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16800kbit latency 20ms burst 8400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19200kbit latency 20ms burst 9600
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16400kbit latency 20ms burst 8200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15800kbit latency 20ms burst 7900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19000kbit latency 20ms burst 9500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18700kbit latency 20ms burst 9350
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15800kbit latency 20ms burst 7900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17000kbit latency 20ms burst 8500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16500kbit latency 20ms burst 8250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13000kbit latency 20ms burst 6500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14100kbit latency 20ms burst 7050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12900kbit latency 20ms burst 6450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12900kbit latency 20ms burst 6450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13600kbit latency 20ms burst 6800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11900kbit latency 20ms burst 5950
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16600kbit latency 20ms burst 8300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15400kbit latency 20ms burst 7700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10400kbit latency 20ms burst 5200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12600kbit latency 20ms burst 6300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9400kbit latency 20ms burst 4700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11100kbit latency 20ms burst 5550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12100kbit latency 20ms burst 6050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14200kbit latency 20ms burst 7100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10600kbit latency 20ms burst 5300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11100kbit latency 20ms burst 5550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10300kbit latency 20ms burst 5150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9090kbit latency 20ms burst 4545
sleep 1.0s
tc qdisc add dev $interface root tbf rate 5180kbit latency 20ms burst 2590
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6740kbit latency 20ms burst 3370
sleep 1.0s
tc qdisc add dev $interface root tbf rate 8900kbit latency 20ms burst 4450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 3490kbit latency 20ms burst 1745
sleep 1.0s
tc qdisc add dev $interface root tbf rate 2940kbit latency 20ms burst 1470
sleep 1.0s
tc qdisc add dev $interface root tbf rate 7650kbit latency 20ms burst 3825
sleep 1.0s
tc qdisc add dev $interface root tbf rate 6330kbit latency 20ms burst 3165
sleep 1.0s
tc qdisc add dev $interface root tbf rate 9420kbit latency 20ms burst 4710
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10000kbit latency 20ms burst 5000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 10400kbit latency 20ms burst 5200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11900kbit latency 20ms burst 5950
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12000kbit latency 20ms burst 6000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15000kbit latency 20ms burst 7500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15000kbit latency 20ms burst 7500
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15600kbit latency 20ms burst 7800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13100kbit latency 20ms burst 6550
sleep 1.0s
tc qdisc add dev $interface root tbf rate 11800kbit latency 20ms burst 5900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13500kbit latency 20ms burst 6750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13500kbit latency 20ms burst 6750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16500kbit latency 20ms burst 8250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18400kbit latency 20ms burst 9200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17700kbit latency 20ms burst 8850
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15300kbit latency 20ms burst 7650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16500kbit latency 20ms burst 8250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13700kbit latency 20ms burst 6850
sleep 1.0s
tc qdisc add dev $interface root tbf rate 12900kbit latency 20ms burst 6450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17600kbit latency 20ms burst 8800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14800kbit latency 20ms burst 7400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16600kbit latency 20ms burst 8300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13900kbit latency 20ms burst 6950
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16100kbit latency 20ms burst 8050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 14800kbit latency 20ms burst 7400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 21800kbit latency 20ms burst 10900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18900kbit latency 20ms burst 9450
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15600kbit latency 20ms burst 7800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15500kbit latency 20ms burst 7750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 15800kbit latency 20ms burst 7900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 13600kbit latency 20ms burst 6800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 16600kbit latency 20ms burst 8300
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20400kbit latency 20ms burst 10200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17500kbit latency 20ms burst 8750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20100kbit latency 20ms burst 10050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20800kbit latency 20ms burst 10400
sleep 1.0s
tc qdisc add dev $interface root tbf rate 21900kbit latency 20ms burst 10950
sleep 1.0s
tc qdisc add dev $interface root tbf rate 22000kbit latency 20ms burst 11000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18100kbit latency 20ms burst 9050
sleep 1.0s
tc qdisc add dev $interface root tbf rate 21800kbit latency 20ms burst 10900
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19500kbit latency 20ms burst 9750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19300kbit latency 20ms burst 9650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18000kbit latency 20ms burst 9000
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19300kbit latency 20ms burst 9650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17400kbit latency 20ms burst 8700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 21300kbit latency 20ms burst 10650
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18300kbit latency 20ms burst 9150
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20500kbit latency 20ms burst 10250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17500kbit latency 20ms burst 8750
sleep 1.0s
tc qdisc add dev $interface root tbf rate 17600kbit latency 20ms burst 8800
sleep 1.0s
tc qdisc add dev $interface root tbf rate 19700kbit latency 20ms burst 9850
sleep 1.0s
tc qdisc add dev $interface root tbf rate 21400kbit latency 20ms burst 10700
sleep 1.0s
tc qdisc add dev $interface root tbf rate 20400kbit latency 20ms burst 10200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18400kbit latency 20ms burst 9200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18200kbit latency 20ms burst 9100
sleep 1.0s
tc qdisc add dev $interface root tbf rate 22500kbit latency 20ms burst 11250
sleep 1.0s
tc qdisc add dev $interface root tbf rate 18400kbit latency 20ms burst 9200
sleep 1.0s
tc qdisc add dev $interface root tbf rate 21600kbit latency 20ms burst 10800
sleep 1.0s
tc qdisc del dev $interface root
