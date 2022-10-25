pointlist = {}
roaddict = {}

temp_line = ''
with open('OG0012067.nwk', 'r') as ff :
    for line in ff :
        temp_line = line.strip()

deepflag = []
regionstr = ''
for i in temp_line :

    if '(' == i : 
        deepflag.append('0')
        #print('(', ''.join(deepflag))
        continue

    if ')' == i : 
        deepstr = ''.join(deepflag)
        deepflag.pop()

        splitstr = regionstr.split(':')
        if splitstr[0].startswith('X') :
            pointlist.setdefault(splitstr[0], deepstr)
            roaddict.setdefault(deepstr, float(splitstr[1]))
            
        else :
            roaddict.setdefault(deepstr, float(splitstr[1]))
        regionstr = ''
        #print(')', deepstr)
        continue

    if ',' != i : regionstr += i; continue

    splitstr = regionstr.split(':')
    deepstr = ''.join(deepflag)
    if splitstr[0].startswith('X') :
        pointlist.setdefault(splitstr[0], deepstr)
        roaddict.setdefault(deepstr, float(splitstr[1]))
        deepflag[-1] = str(int(deepflag[-1])+1)
        deepstr = ''.join(deepflag)
    else :
        roaddict.setdefault(deepstr, float(splitstr[1]))
        deepflag[-1] = str(int(deepflag[-1])+1)
        deepstr = ''.join(deepflag)
    regionstr = ''
    #print(',', deepstr)

#print(roaddict)
#print(pointlist)

def calc_sum(t1, t2) :
    if t1 == t2 : return 0

    code1, code2 = pointlist[t1], pointlist[t2]
    res = 0
    for s in range(min(len(code1), len(code2))) : 
        if code1[s] != code2[s] : break

    for i in range(s+1, len(code1)+1) : res += roaddict.get(code1[:i], 0)#; print(code1[:i], roaddict.get(code1[:i], 0))
    for i in range(s+1, len(code2)+1) : res += roaddict.get(code2[:i], 0)#; print(code2[:i], roaddict.get(code1[:i], 0))

    return res

res_matrix = {}

for t1 in list(pointlist.keys()) : 
    for t2 in list(pointlist.keys()) :
        tres = calc_sum(t1, t2)
        #print('{} {} : {}'.format(t1, t2, tres))
        if t1 not in res_matrix : res_matrix.setdefault(t1, {t2: tres}); continue
        if t2 not in res_matrix[t1] : res_matrix[t1].setdefault(t2, tres); continue

print('\n\n\ntab\t'+'\t'.join(list(res_matrix.keys())))
for k, v in res_matrix.items() :
    print(k, end='\t')
    print('\t'.join([str(x) for x in list(v.values())]))
'''
test1 = 'XP_008355427.2'
test2 = 'XP_008386409.1'
print('\n\n\n', test1, test2, calc_sum(test1, test2))

test1 = 'XP_020867760.1'
test2 = 'XP_015575846.2'
print('\n\n\n', test1, test2, calc_sum(test1, test2))
'''