# coding=utf-8

import time
import random
import os
import os.path
import re
import csv

# 保存各种数据的全局变量
FACILITY_NUM = 0  # 工厂数量
CUSTOMER_NUM = 0  # 顾客数量
OPENING_COST = []  # 工厂开放开销
CAPACITY = []  # 工厂容量
DEMAND = []  # 每个顾客的需求
ASSIGNMENT_COST = []  # 每个顾客分配给工厂时候的开销
OPEN_STATUS = []  # 每个工厂开闭状态，1表示开，0表示关


# 读取文件，加载各种数据
def load(file_path):
    with open(file_path, 'r') as f:
        # 声明全局变量
        global FACILITY_NUM
        global CUSTOMER_NUM
        global OPENING_COST
        global CAPACITY
        global DEMAND
        global ASSIGNMENT_COST
        global OPEN_STATUS

        # 获取数据
        FACILITY_NUM, CUSTOMER_NUM = f.readline().strip("\n").split()
        FACILITY_NUM = int(FACILITY_NUM)
        CUSTOMER_NUM = int(CUSTOMER_NUM)

        OPEN_STATUS = [0] * FACILITY_NUM

        for i in range(FACILITY_NUM):
            line = f.readline().strip("\n").split()
            CAPACITY.append(int(line[0]))
            OPENING_COST.append(int(float(line[1])))

        data_set = []
        source_in_line = f.readlines()
        for line in source_in_line:
            temp1 = line.strip("\n")
            temp2 = temp1.split()
            data_set.append(temp2)

        data = []
        for i in data_set:
            for j in i:
                data.append(j)

        for i in range(CUSTOMER_NUM):
            DEMAND.append(int(float(data[i])))

        begin = CUSTOMER_NUM
        for i in range(CUSTOMER_NUM):
            temp = []  # 保存每个顾客分配给每个工厂的开销
            for j in range(FACILITY_NUM):
                temp.append(int(float(data[begin])))
                begin += 1
            ASSIGNMENT_COST.append(temp)


# 贪心算法
def greedy(output_file, input_file):
    begin_time = time.clock()  # 记录开始时间

    global CAPACITY

    capacity = CAPACITY[:]
    open_status = [0] * FACILITY_NUM  # 每个工厂的开闭状态
    assign_cost = 0  # 客户分配给工厂的总开销
    open_cost = 0  # 工厂开放总开销
    total_cost = 0  # 总开销
    assignment = [-1] * CUSTOMER_NUM  # 每个顾客分配到工厂的索引

    for cus in range(CUSTOMER_NUM):
        facility_index = []  # 可以被选中的工厂（即容量足够当前顾客使用）
        for i in range(FACILITY_NUM):
            if capacity[i] >= DEMAND[cus]:
                facility_index.append(i)

        # 获取当前顾客分配给每个工厂时的开销
        cur_assignment_cost = ASSIGNMENT_COST[cus]

        # 计算对于当前顾客每个工厂的分配开销和开启开销总和
        cur_total_cost = [sum(x) for x in zip(cur_assignment_cost, OPENING_COST)]

        # 选择可用的最小的cur_total_cost的工厂
        selected_index = facility_index[0]
        for i in facility_index:
            if cur_total_cost[i] < cur_total_cost[selected_index]:
                selected_index = i

        # 设置选中时的状态
        open_status[selected_index] = 1
        capacity[selected_index] = capacity[selected_index] - DEMAND[cus]
        assignment[cus] = selected_index

        # 累加分配开销
        assign_cost += cur_assignment_cost[selected_index]

    # 累加工厂开放开销
    for i in range(FACILITY_NUM):
        open_cost += open_status[i] * OPENING_COST[i]

    # 计算总开销
    total_cost = open_cost + assign_cost

    # 记录结束时间
    end_time = time.clock()
    # 计算运行时间
    used_time = end_time - begin_time

    # 输出结果
    # 输出结果到csv文件
    with open('sum.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow([input_file[10:], total_cost, used_time])

    # 输出结果到txt文件
    with open(output_file, "a") as f:
        start = time.clock()  # 记录开始时间
        # 输出输入样例
        f.write("%s \n" % input_file)
        # 输出总开销
        f.write("Result: %d \n" % total_cost)
        # 输出工厂开闭状态
        f.write("Status of facilities: {} \n".format(open_status))
        # 输出每个顾客分配到哪个工厂
        f.write("The assignment of customers to facilities: {} \n".format(assignment))
        # 输出运行时间
        f.write("Time used: %f \n" % float(used_time))
        # 输出换行符
        f.write("\n")

    # 返回最终结果
    return total_cost


# 随机生成一个解
class Solution:
    assignment = []  # 每个顾客分配到哪个工厂
    capacity = []  # 每个工厂剩余容量
    open_status = []  # 每个工厂开放状态
    assgin_cost = 0  # 分配总开销
    open_cost = 0  # 开放总开销
    total_cost = 0  # 总开销

    # 构造函数
    def __init__(self):
        # 初始化变量
        self.assignment = [-1] * CUSTOMER_NUM
        self.capacity = CAPACITY[:]
        self.open_status = [0] * FACILITY_NUM

        for cus in range(CUSTOMER_NUM):
            facility_index = []  # 可被选中的工厂索引集合
            for i in range(FACILITY_NUM):
                if self.capacity[i] >= DEMAND[cus]:
                    facility_index.append(i)

            # 获取当前顾客分配给每个工厂时的开销
            cur_assignment_cost = ASSIGNMENT_COST[cus]

            # 计算对于当前顾客每个工厂的分配开销和开启开销总和
            cur_total_cost = [sum(x) for x in zip(cur_assignment_cost, OPENING_COST)]

            # 选择可用的最小的cur_total_cost的工厂
            selected_index = facility_index[0]
            for i in facility_index:
                if cur_total_cost[i] < cur_total_cost[selected_index]:
                    selected_index = i

            self.capacity[selected_index] = self.capacity[selected_index] - DEMAND[cus]
            self.assignment[cus] = selected_index

            self.assgin_cost += ASSIGNMENT_COST[cus][selected_index]
            self.open_status[selected_index] = 1

        for i in range(FACILITY_NUM):
            self.open_cost += self.open_status[i] * OPENING_COST[i]

        self.total_cost = self.assgin_cost + self.open_cost

    def result(self):
        return self.total_cost


# 计算在随机交换两个customer对应的工厂后的total_cost
def random_swap(solution, iter_times):
    local_assignment = solution.assignment[:]
    local_capacity = solution.capacity[:]

    for i in range(iter_times):
        customer1 = random.randint(0, CUSTOMER_NUM - 1)
        customer2 = random.randint(0, CUSTOMER_NUM - 1)
        while customer1 == customer2:
            customer2 = random.randint(0, CUSTOMER_NUM - 1)

        factory1 = local_assignment[customer1]
        factory2 = local_assignment[customer2]
        assignment_cost1 = ASSIGNMENT_COST[customer1]
        assignment_cost2 = ASSIGNMENT_COST[customer2]
        capacity1 = local_capacity[factory1]
        capacity2 = local_capacity[factory2]

        if(capacity1 >= abs(DEMAND[customer1] - DEMAND[customer2])
                and capacity2 >= abs(DEMAND[customer1] - DEMAND[customer2])):
            result = (solution.total_cost + assignment_cost1[factory2] + assignment_cost2[factory1]
                    - assignment_cost1[factory1] - assignment_cost2[factory2])
            solution.assignment[customer1] = factory2
            solution.assignment[customer2] = factory1
            solution.total_cost = result
            break


# 局部搜索函数
def local_search(output_file, input_file):
    begin_time = time.clock()  # 记录开始时间
    init_solution = Solution()  # 生产一个随机解

    iter_times = 1000  # 迭代次数

    random_swap(init_solution, iter_times)

    # 记录结束时间
    end_time = time.clock()
    # 计算运行时间
    used_time = end_time - begin_time

    # 输出结果
    # 输出结果到csv文件
    with open('sum.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow([input_file[10:], init_solution.total_cost, used_time])

    # 输出结果到txt文件
    with open(output_file, "a") as f:

        # 输出输入样例
        f.write("%s \n" % input_file)
        # 输出总开销
        f.write("Result: %d \n" % init_solution.total_cost)
        # 输出工厂开闭状态
        f.write("Status of facilities: {} \n".format(init_solution.open_status))
        # 输出每个顾客分配到哪个工厂
        f.write("The assignment of customers to facilities: {} \n".format(init_solution.assignment))
        # 输出运行时间
        f.write("Time used: %f \n" % float(used_time))
        # 输出换行符
        f.write("\n")

    return init_solution.total_cost


# 清空数据
def clear_data():
    # 声明全局变量
    global FACILITY_NUM
    global CUSTOMER_NUM
    global OPENING_COST
    global CAPACITY
    global DEMAND
    global ASSIGNMENT_COST
    global OPEN_STATUS

    # 清空数据
    FACILITY_NUM = 0  # 工厂数量
    CUSTOMER_NUM = 0  # 顾客数量
    OPENING_COST = []  # 工厂开放开销
    CAPACITY = []  # 工厂容量
    DEMAND = []  # 每个顾客的需求
    ASSIGNMENT_COST = []  # 每个顾客分配给工厂时候的开销
    OPEN_STATUS = []  # 每个工厂开闭状态，1表示开，0表示关


# 主函数
def main():
    path_dir = "Instances"  # 输入数据文件夹
    files = os.listdir(path_dir)  # 保存文件夹下的全部文件名

    p = re.compile("(\d+)")

    def my_cmp(v1, v2):
        d1 = [int(i) for i in p.findall(v1)][0]
        d2 = [int(i) for i in p.findall(v2)][0]
        return cmp(d1, d2)
    files.sort(my_cmp)

    method = int(raw_input("贪心算法输入1，局部搜索算法输入2： "))

    for file_name in files:

        file_path = path_dir + "\\" + file_name
        print(file_path)
        # 加载文件中数据
        load(file_path)
        if method == 1:
            # 采用贪心算法
            greedy("greedy.txt", file_path)
        elif method == 2:
            # 采用局部搜索算法
            local_search("localsearch.txt", file_path)
        else:
            pass
        clear_data()


# load("Instances\p4")
main()


