lis = [[1,2],[]]
liss = [[[4,6] , [2,8]]]
lis = sorted(lis, key=lambda x: x[1], reverse=True)
print(lis)
liss.append(lis)

f = [[3,4],[1,2]]
f = sorted(f, key=lambda x: x[1], reverse=True)
print(f)
if f in liss:
    print("yeah")
