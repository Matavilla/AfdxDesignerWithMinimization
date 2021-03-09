#!/usr/bin/python

import random
import os, subprocess
import sys

dir_name = "test_3"
number_of_tests = 1
if len(sys.argv) == 2:
    number_of_tests = int(sys.argv[1])
number_of_msgs = 150
msgSizeMin = [1000, 16]
msgSizeMax = [100000, 100]
periodMin = [100, 10]
periodMax = [10000, 100]
tMaxMin = [10, 10]
tMaxMax = [1000, 100]
destNumMin = 1
destNumMax = 1

numberOfGroups = 4
partGroups = [[5, 6], [7, 8], [1, 2], [3, 4]]

def generate_one_df(fromPartition, toPartitions, jMax, msgSize, period, tMax, id):
    dest = ""
    for part in toPartitions:
        dest += str(part) + ','
    dest = dest[:-1]
    ans = '\t\t<dataFlow dest="' + dest + '" id="Data Flow ' + str(id) + '" jMax="' + str(jMax) + '" msgSize="' + str(msgSize) + '" period="' + str(period)
    ans += '" source="' + str(fromPartition) + '" tMax="' + str(tMax) + '" vl="None"/>'

    return ans

def generateSource():
    group = random.randint(0, numberOfGroups - 1)
    id = random.randint(0, len(partGroups[group])- 1)
    return {'id': partGroups[group][id], 'group': group}

def generateDests(sourceGroup, destNumber):
    dests = []
    for i in range(destNumber):
        id = -1
        while id == -1 or (id in dests):
            group = sourceGroup

            while group == sourceGroup:
                group = random.randint(0, numberOfGroups - 1)
            index = random.randint(0, len(partGroups[group])- 1)
            id = partGroups[group][index]

        dests.append(id)
    return dests

def generate_random_df(id):
    t = random.randint(0, 100);
    t = t % 2
    msgSize = random.randint(msgSizeMin[t], msgSizeMax[t])
    period = random.randint(periodMin[t], periodMax[t])
    time = msgSize / 12500.0
    while (time / period > 0.05):
        period = random.randint(periodMin[t], periodMax[t])
        time = msgSize / 12500.0
    tmp = ((msgSize - msgSizeMin[t] + 1.0) / msgSizeMax[t])
    tMax = tMaxMin[t] + int((tMaxMax[t] - tMaxMin[t]) * tmp)
    destNumber = random.randint(destNumMin, destNumMax)
    sourceInfo = generateSource()
    dests = generateDests(sourceInfo['group'], destNumber)
    return generate_one_df(sourceInfo['id'], dests, 0, msgSize, period, tMax, id)

def generateOneData():
    text = ""
    for id in range(1, number_of_msgs + 1):
        text += generate_random_df(id) + os.linesep
    return text;

def generateOneTest(t, data):
    if (t == 1):
        f = open('test_2_Base.afdxxml', 'r')
    else:
        f = open('test_2_Full.afdxxml', 'r')
    textArr = f.readlines()
    text = "".join(textArr[:-2])
    text += data
    text += "\t</dataFlows>" + os.linesep
    text += "</afdxxml>" + os.linesep
    f.close()
    return text

num_of_requests = number_of_msgs

num_of_assigned = {'c1 = 0.5 c2 = 0.5': 0}

num_len = {'c1 = 0.5 c2 = 0.5': 0}

num_of_vls = {'c1 = 0.5 c2 = 0.5': 0}

configs = {'c1 = 0.5 c2 = 0.5': '--coefficient-c1=0.5 --coefficient-c2=0.5'}

def calc_num_of_assigned(name):
    process = subprocess.Popen(['grep', 'vl="None"', name, "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = int(process.communicate()[0])
    return num_of_requests - output

def calc_num_of_vls(name):
    process = subprocess.Popen(['grep', '<virtualLink ', name, "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = int(process.communicate()[0])
    return output

def calc_length(name):
    process = subprocess.Popen(['grep', 'Sum length link: ', name, "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = float(process.communicate()[0])
    return output

def generate_and_run():
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    os.system("rm -rf test_3/*")
    for i in range(1, number_of_tests + 1):
        flag = True;
        while flag:
            data = generateOneData();
            fileName = dir_name + '/' + 'test_'+ str(i) +'.afdxxml'
            f = open(fileName, 'w')
            f.write(generateOneTest(1, data))
            f.close()

            fileNameForFull = dir_name + '/' + 'test_'+ str(i) + '_full' + '.afdxxml'
            f = open(fileNameForFull, 'w')
            f.write(generateOneTest(2, data))
            f.close()

            if sys.platform.startswith("win"):
                name = "../algo/AFDX_DESIGN.exe"
            else:
                name = "../algo/AFDX_DESIGN"

            flag = False
            j = 0
            for config in configs.keys():
                process = subprocess.Popen(name + ' ' + fileName + ' ' +  dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml ' + " a " + configs[config], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, shell=True)
                process.wait()
                t1 = calc_num_of_assigned(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
                t2 = calc_num_of_vls(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
                t3 = calc_length(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
                if t1 != number_of_msgs:
                    flag = True
                else:
                    ans = config
                    ans += '\t' + str(num_of_requests)
                    ans += '\t' + str(t1)
                    ans += '\t' + str(t2)
                    ans += '\t' + str(t3)
                    print ans
                    t1, t2, t3 = 0, 0, 0
                    process = subprocess.Popen(name + ' ' + fileNameForFull + ' ' +  dir_name + '/test_out' + str(i) + '_' + str(j) + '_full' + '.afdxxml ' + " a " + configs[config], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, shell=True)
# print name + ' ' + fileNameForFull + ' ' +  dir_name + '/test_out' + str(i) + '_' + str(j) + '_full' + '.afdxxml ' + " a " + configs[config]
                    process.wait()
                    t1 = calc_num_of_assigned(dir_name + '/test_out' + str(i) + '_' + str(j) + '_full' + '.afdxxml')
                    t2 = calc_num_of_vls(dir_name + '/test_out' + str(i) + '_' + str(j) + '_full' + '.afdxxml')
                    t3 = calc_length(dir_name + '/test_out' + str(i) + '_' + str(j) + '_full' +  '.afdxxml')
                    ans = config
                    ans += '\t' + str(num_of_requests)
                    ans += '\t' + str(t1)
                    ans += '\t' + str(t2)
                    ans += '\t' + str(t3)
                    print ans
                j += 1

        j = 0
        for config in configs.keys():
            num_of_assigned[config] += calc_num_of_assigned(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
            num_of_vls[config] += calc_num_of_vls(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
            num_len[config] += calc_length(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
            j += 1
        print str(i) + ' done'

    for config in configs.keys():
        ans = config
        ans += '\t' + str(num_of_requests)
        ans += '\t' + str(int(float(num_of_assigned[config]) / number_of_tests))
        ans += '\t' + str(int(float(num_of_vls[config]) / number_of_tests))
        ans += '\t' + str(num_len[config] / number_of_tests)
        print ans

generate_and_run()
