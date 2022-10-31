'''
创建人员: Nerium
创建日期: 2022/10/25
更改人员: xiaommms
更改日期: 2022/10/27
'''
import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='nwk to matrix')
parser.add_argument("-n","--nwk",)
parser.add_argument("-f","--file",)
args = parser.parse_args()
file = args.nwk
path= args.file

pointlist = {}
roaddict = {}

temp_line = ''
with open(file, 'r') as ff :
    for line in ff :
        temp_line = line.strip()

deepflag = []
regionstr = ''
for i in temp_line :

    if '(' == i : 
        deepflag.append('0')   #节点深度
        continue

    if ')' == i :   #中间节点
        deepstr = ''.join(deepflag) 
        deepflag.pop() #深度-1

        splitstr = regionstr.split(':')
        if splitstr[0].startswith('X') :
            pointlist.setdefault(splitstr[0], deepstr)     #叶子节点字典，叶子节点名为key,深度路径为value
        roaddict.setdefault(deepstr, float(splitstr[1]))    #进化树所有节点字典，深度路径为key,支长为value
        regionstr = ''
        continue

    if ',' != i : regionstr += i; continue  #节点名获取

    splitstr = regionstr.split(':')
    deepstr = ''.join(deepflag)

    if splitstr[0].startswith('X') :
        pointlist.setdefault(splitstr[0], deepstr)
        roaddict.setdefault(deepstr, float(splitstr[1]))
        deepflag[-1] = str(int(deepflag[-1])+1) #深度加1
        deepstr = ''.join(deepflag)
    else :
        roaddict.setdefault(deepstr, float(splitstr[1]))
        deepflag[-1] = str(int(deepflag[-1])+1)
        deepstr = ''.join(deepflag)
    regionstr = ''

def calc_sum(t1, t2) :
    if t1 == t2 : return 0

    code1, code2 = pointlist[t1], pointlist[t2]
    res = 0
    for s in range(min(len(code1), len(code2))) : 
        if code1[s] != code2[s] : break

    for i in range(s+1, len(code1)+1) : res += roaddict.get(code1[:i], 0)
    for i in range(s+1, len(code2)+1) : res += roaddict.get(code2[:i], 0)

    return ("%.2f"%float(res))

res_matrix = {}
mat1 = np.zeros([len(list(pointlist.keys())),len(list(pointlist.keys()))])
table = pd.DataFrame(mat1,columns = list(pointlist.keys()),index=list(pointlist.keys()))

for t1 in list(pointlist.keys()) : 
    for t2 in list(pointlist.keys()) :
        tres = calc_sum(t1, t2)
        if t1 not in res_matrix : res_matrix.setdefault(t1, {t2: tres}); continue
        if t2 not in res_matrix[t1] : res_matrix[t1].setdefault(t2, tres); continue

key = list(res_matrix.keys())
for k in range(len(key)):
    va = list(res_matrix[key[k]].values())
    for v in range(k,len(va)):
        table.iloc[k,v] = va[v]
        table.iloc[v,k] = va[v]
table.to_csv(path)