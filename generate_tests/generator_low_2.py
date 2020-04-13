#!/usr/bin/python

import random
import os, subprocess
import sys

dir_name = "tests_low_2"
number_of_tests = 100
if len(sys.argv) == 2:
    number_of_tests = int(sys.argv[1])
number_of_msgs = 500
msgSizeMin = 0
msgSizeMax = 1000
periodMin = 100
periodMax = 100000
tMaxMin = 100
tMaxMax = 100000
destNumMin = 1
destNumMax = 1

numberOfGroups = 5
partGroups = [[18], [19], [4], [5], [6]]

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
    msgSize = random.randint(msgSizeMin, msgSizeMax)
    period = random.randint(periodMin, periodMax)
    tMax = random.randint(tMaxMin, tMaxMax)
    destNumber = random.randint(destNumMin, destNumMax)
    sourceInfo = generateSource()
    dests = generateDests(sourceInfo['group'], destNumber)
    return generate_one_df(sourceInfo['id'], dests, 0, msgSize, period, tMax, id)

def generateOneTest():
    f = open('test_arch_2.afdxxml', 'r')
    textArr = f.readlines()
    text = "".join(textArr[:-2])
    for id in range(1, number_of_msgs + 1):
        text += generate_random_df(id) + os.linesep
    text += "\t</dataFlows>" + os.linesep
    text += "</afdxxml>" + os.linesep
    f.close()
    return text

num_of_requests = number_of_msgs

num_of_assigned = {'lim_1': 0, 'lim_2': 0, 'lim_3': 0, 'c1 = 0.0 c2 = 1.0': 0, 'c1 = 0.1 c2 = 0.9': 0, 'c1 = 0.2 c2 = 0.8': 0, 'c1 = 0.3 c2 = 0.7': 0, 'c1 = 0.4 c2 = 0.6': 0, 'c1 = 0.5 c2 = 0.5': 0, 'c1 = 0.6 c2 = 0.4': 0, 'c1 = 0.7 c2 = 0.3': 0, 'c1 = 0.8 c2 = 0.2': 0, 'c1 = 0.9 c2 = 0.1': 0, 'c1 = 1.0 c2 = 0.0': 0}

num_len = {'lim_1': 0.0, 'lim_2': 0.0, 'lim_3': 0.0, 'c1 = 0.0 c2 = 1.0': 0.0, 'c1 = 0.1 c2 = 0.9': 0.0, 'c1 = 0.2 c2 = 0.8': 0.0, 'c1 = 0.3 c2 = 0.7': 0.0, 'c1 = 0.4 c2 = 0.6': 0.0, 'c1 = 0.5 c2 = 0.5': 0.0, 'c1 = 0.6 c2 = 0.4': 0.0, 'c1 = 0.7 c2 = 0.3': 0.0, 'c1 = 0.8 c2 = 0.2': 0.0, 'c1 = 0.9 c2 = 0.1': 0.0, 'c1 = 1.0 c2 = 0.0': 0.0}

num_of_vls = {'lim_1': 0, 'lim_2': 0, 'lim_3': 0, 'c1 = 0.0 c2 = 1.0': 0, 'c1 = 0.1 c2 = 0.9': 0, 'c1 = 0.2 c2 = 0.8': 0, 'c1 = 0.3 c2 = 0.7': 0, 'c1 = 0.4 c2 = 0.6': 0, 'c1 = 0.5 c2 = 0.5': 0, 'c1 = 0.6 c2 = 0.4': 0, 'c1 = 0.7 c2 = 0.3': 0, 'c1 = 0.8 c2 = 0.2': 0, 'c1 = 0.9 c2 = 0.1': 0, 'c1 = 1.0 c2 = 0.0': 0}

configs = {'lim_1': '--limited-search-depth=1', 'lim_2': '--limited-search-depth=2', 'lim_3': '--limited-search-depth=3', 'c1 = 0.0 c2 = 1.0': '--coefficient-c1=0.0 --coefficient-c2=1.0', 'c1 = 0.1 c2 = 0.9': '--coefficient-c1=0.1 --coefficient-c2=0.9', 'c1 = 0.2 c2 = 0.8': '--coefficient-c1=0.2 --coefficient-c2=0.8', 'c1 = 0.3 c2 = 0.7': '--coefficient-c1=0.3 --coefficient-c2=0.7', 'c1 = 0.4 c2 = 0.6': '--coefficient-c1=0.4 --coefficient-c2=0.6', 'c1 = 0.5 c2 = 0.5': '--coefficient-c1=0.5 --coefficient-c2=0.5', 'c1 = 0.6 c2 = 0.4': '--coefficient-c1=0.6 --coefficient-c2=0.4', 'c1 = 0.7 c2 = 0.3': '--coefficient-c1=0.7 --coefficient-c2=0.3', 'c1 = 0.8 c2 = 0.2': '--coefficient-c1=0.8 --coefficient-c2=0.2', 'c1 = 0.9 c2 = 0.1': '--coefficient-c1=0.9 --coefficient-c2=0.1', 'c1 = 1.0 c2 = 0.0': '--coefficient-c1=1.0 --coefficient-c2=1.0'}

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

    for i in range(1, number_of_tests + 1):
        flag = True;
        while flag:
            os.system("rm -rf tests_low_2/*")
            fileName = dir_name + '/' + 'test_'+ str(i) +'.afdxxml'
            f = open(fileName, 'w')
            f.write(generateOneTest())
            f.close()

            if sys.platform.startswith("win"):
                name = "../algo/AFDX_DESIGN.exe"
            else:
                name = "../algo/AFDX_DESIGN"

            flag = False
            j = 0
            for config in configs.keys():
                process = subprocess.Popen(name + ' ' + fileName + ' ' +  dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml ' + " a " + configs[config], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, shell=True)
  #              print config + " for test " + str(i) + " done"
 #               print name + ' ' + fileName + ' ' +  dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml ' + " a " + configs[config]
                process.communicate()

                try:
                    calc_num_of_assigned(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
                    calc_num_of_vls(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
                    calc_length(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
                except:
                    flag = True;
                j += 1
        j = 0
        for config in configs.keys():
            num_of_assigned[config] += calc_num_of_assigned(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
            num_of_vls[config] += calc_num_of_vls(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
            num_len[config] += calc_length(dir_name + '/test_out' + str(i) + '_' + str(j) + '.afdxxml')
            j += 1
#        print str(i) + ' done'

    print 
    for config in configs.keys():
        ans = config
        ans += '\t' + str(num_of_requests)
        ans += '\t' + str(int(float(num_of_assigned[config]) / number_of_tests))
        ans += '\t' + str(int(float(num_of_vls[config]) / number_of_tests))
        ans += '\t' + str(num_len[config] / number_of_tests)
        print ans

generate_and_run()
