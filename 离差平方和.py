import time
import os
#创建列表
sentences = [
    "坚持计算，答案就在前方！",
    "认真分析每一组数据，你超棒的！",
    "离差平方和正在飞速运算中~",
    "静下心，最优分组马上出现！",
    "数学的乐趣藏在每一次分割里",
    "再等等，马上算出最小组间平方和！",
    "细心运算，结果不会辜负你",
    "数据处理中，保持耐心！",
    "Good good study,day day towards up"
    "一步步拆解，难题迎刃而解",
    "即将完成全部分组对比！"
]
input_datas = []
average_1 = []
average_2 = []
split_info = []
while True:
    #主循环
    m = 1
    x = 0
    #获取数据个数
    while True:
        prompt_1 = "请输入数据个数(输入'q'以退出):"
        input_1 = input(prompt_1)
        try:
            input_1 = int(input_1)
            if input_1 >= 2:
                break
            elif input_1 < 2:
                print("错误:至少2个数据才能分成2组！")
                continue
        except:
            if input_1 == 'q':
               exit()
            else:
                print("错误：请输入一个整数！")
    #得到足够的数据
    for i in range(input_1):
        prompt_2 = f"请输入第{m}个数(输入'q'以退出):"
        while True:
            input_2 = input(prompt_2)
            try:
                input_2 = float(input_2)
                input_datas.append(input_2)
                m = m + 1
                break
            except:
                if input_2 == 'q':
                    exit()
                else:
                    print("错误：请输入数字！")
    #计算必要的中间数
    n = len(input_datas)
    #全体数据总平均值
    total_sum = sum(input_datas)
    total_mean = total_sum / n
    #总平方和固定不变
    sst = 0
    for num in input_datas:
        cha = num - total_mean
        sst = sst + cha ** 2
    print("\n========================")
    print(f"原始数据：{input_datas}")
    print(f"数据总数n = {n}")
    print(f"全部数据平均值：{total_mean:g}")
    print(f"总平方和 = {sst:g}")
    print("========================\n")
    #生成（n-1)种方案
    loop_times = input_1 - 1
    print("正在计算所有分组方案，加载进度：")
    # 加载进度条
    for i in range(loop_times):
        # 简易进度条
        percent = int((i + 1) / loop_times * 50)
        bar = "█" * percent + " " * (50 - percent)
        # 切换励志句子
        tip = sentences[i % len(sentences)]
        print(f"\r[{bar}] {(i+1)/loop_times*100:.1f}%  {tip}", end="")
        # 控制总加载时长约10秒
        time.sleep(10 / loop_times)
        group_1 = input_datas[0 : 1 + x]
        group_2 = input_datas[1 + x : n - 1]
        print(f"\n----------第{i+1}/{loop_times}种分组----------")
        print(f"第一组：{group_1}，第二组：{group_2}")
        #第一组均值、组内离差平方和
        if len(group_1) == 0:
            g1_mean = 0
            sse1 = 0
        else:
            g1_sum = sum(group_1)
            g1_mean = g1_sum / len(group_1)
            sse1 = 0
            for num in group_1:
                cha = num - g1_mean
                sse1 = sse1 + cha ** 2
        average_1.append(g1_mean)
        print(f"第1组平均值={g1_mean:g},第1组组内离差平方和={sse1:g}")
        #第二组均值、组内离差平方和
        if len(group_2) == 0:
            g2_mean = 0
            sse2 = 0
        else:
            g2_sum = sum(group_2)
            g2_mean = g2_sum / len(group_2)
            sse2 = 0
            for num in group_2:
                cha = num - g2_mean
                sse2 = sse2 + cha ** 2
        average_2.append(g2_mean)
        print(f"第2组平均值={g2_mean:g},第2组组内离差平方和={sse2:g}")
        #总组内离差平方和
        sum_sse = sse1 + sse2
        print(f"总组内离差平方和(SSE) = {sse1:g} + {sse2:g} = {sum_sse:g}")
        #组间离差平方和
        ssa = sst - sum_sse
        print(f"组间离差平方和(SSA) = {sst:g} - {sum_sse:g} = {ssa:g}")
        #打印空行
        print()
        #保存数据
        split_info.append({
            "序号": i+1,
            "分割位置": x+1,
            "组1": group_1,
            "组2": group_2,
            "组1平方和": sse1,
            "组2平方和": sse2,
            "总组内SSE": sum_sse,
            "组间SSA": ssa
        })
        x = x + 1
    print("\n全部分组计算完成！")
    #排序组间离差平方和
    split_info_sorted = sorted(split_info, key=lambda d: d["组间SSA"])
    min_ssa_item = split_info_sorted[0]
    #方案排序
    print("========================")
    print("所有分组方案【按组间离差平方和从小到大排序】")
    print("========================")
    for item in split_info_sorted:
        print(f"方案{item['序号']} | 组间平方和SSA={item['组间SSA']:g}")
    #结果输出
    print("\n========================")
    print("组间离差平方和最小的分割方案：")
    print(f"方案序号：{min_ssa_item['序号']}")
    print(f"第一组数据：{min_ssa_item['组1']}")
    print(f"第二组数据：{min_ssa_item['组2']}")
    print(f"该方案组间离差平方和 = {min_ssa_item['组间SSA']:g}")
    print("========================\n")
    #清空列表
    input_datas.clear()
    average_1.clear()
    average_2.clear()
    split_info.clear()
    #判断是否继续
    while True:
        op = input("是否重新输入一组数据计算？(y/n):")
        if op.lower() == "y":
            break
        elif op.lower() == "n":
            print("程序结束")
            exit()
        else:
            print("请输入y或n")