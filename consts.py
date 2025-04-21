def bytes2int(str):
     return int(str.encode('hex'), 16)

def bytes2hex(str):
    return '0x'+str.encode('hex')

def int2bytes(i):
    h = int2hex(i)
    return hex2bytes(h)

def int2hex(i):
    return hex(i)

def hex2int(h):
    if len(h) > 1 and h[0:2] == '0x':
        h = h[2:]

    if len(h) % 2:
        h = "0" + h

    return int(h, 16)

def hex2bytes(h):
    if len(h) > 1 and h[0:2] == '0x':
        h = h[2:]

    if len(h) % 2:
        h = "0" + h

    return h.decode('hex')

h = "0x6a09e667 0xbb67ae85 0x3c6ef372 0xa54ff53a 0x510e527f 0x9b05688c 0x1f83d9ab 0x5be0cd19"
head = h.split(" ")
i = 0
print("Head values")
for k in head:
    print(i, " ", hex2int(k))
    i += 1

# str = "0x6a09e667 0xbb67ae85 0x3c6ef372 0xa54ff53a 0x510e527f 0x9b05688c 0x1f83d9ab 0x5be0cd19 0x428a2f98 0x71374491 0xb5c0fbcf 0xe9b5dba5 0x3956c25b 0x59f111f1 0x923f82a4 0xab1c5ed5 0xd807aa98 0x12835b01 0x243185be 0x550c7dc3 0x72be5d74 0x80deb1fe 0x9bdc06a7 0xc19bf174 0xe49b69c1 0xefbe4786 0x0fc19dc6 0x240ca1cc 0x2de92c6f 0x4a7484aa 0x5cb0a9dc 0x76f988da 0x983e5152 0xa831c66d 0xb00327c8 0xbf597fc7 0xc6e00bf3 0xd5a79147 0x06ca6351 0x14292967 0x27b70a85 0x2e1b2138 0x4d2c6dfc 0x53380d13 0x650a7354 0x766a0abb 0x81c2c92e 0x92722c85 0xa2bfe8a1 0xa81a664b 0xc24b8b70 0xc76c51a3 0xd192e819 0xd6990624 0xf40e3585 0x106aa070 0x19a4c116 0x1e376c08 0x2748774c 0x34b0bcb5 0x391c0cb3 0x4ed8aa4a 0x5b9cca4f 0x682e6ff3 0x748f82ee 0x78a5636f 0x84c87814 0x8cc70208 0x90befffa 0xa4506ceb 0xbef9a3f7 0xc67178f2"
# consts = str.split(" ")

# i = 0
# for k in consts:
#     print(i, " ", hex2int(k))
#     i += 1


#out = [5603756193672356509, 6987150372895004522]
out = [13436514500253700074]
#out = [20830232562625521771, 6661896319230646040, 1291978048813090396, 1697349070656623771]

print("Out result")
for a in out:
    print(int2hex(a))

#print(int2hex(6987150372895004522))

#4c94485e0c21ae6c41ce1dfe7b6bfaceea5ab68e40a2476f50208e526f506080
    

# k[j] = 1116352408
# counter = 0
# a = 1779033703
# b = 3144134277
# c 1013904242
# d 2773480762
# e 1359893119
# f 2600822924
# g 528734635
# h 1541459225
# data 1633837952