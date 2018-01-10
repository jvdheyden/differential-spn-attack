import sys
import re

def differentialAttack(pairs,permutation_table):
    # generate all possible keys
    l = [(a,b) for a in range(0,16) for b in range(0,16)]
    count = dict.fromkeys(l,0)
    for (x,x_star,y,y_star) in pairs:
        y_third_block = (y >> 4) & 15
        y_fourth_block = y & 15
        y_star_third_block = (y_star >> 4) & 15
        y_star_fourth_block = y_star & 15
        # we are using y-differential from excercise 41
        # u4' = 0001 0001 0000 0000
        # filtering: check if y'(3) and y'(4) are 0
        if (y_third_block == y_star_third_block and
                y_fourth_block == y_star_fourth_block):
            y_first_block = (y  >> 12)
            y_second_block = (y >> 8) & 15
            y_star_first_block = (y_star  >> 12)
            y_star_second_block = (y_star >> 8) & 15
            for a in range(0,16):
                for b in range(0,16):
                    v4_first_block = a ^ y_first_block
                    v4_second_block = b ^ y_second_block
                    u4_first_block = permutation_table.index(v4_first_block)
                    u4_second_block = permutation_table.index(v4_second_block)
                    v4_star_first_block = a ^ y_star_first_block
                    v4_star_second_block = b ^ y_star_second_block
                    u4_star_first_block = permutation_table.index(
                            v4_star_first_block)
                    u4_star_second_block = permutation_table.index(
                            v4_star_second_block)
                    u4_xor_first_block = u4_first_block ^ u4_star_first_block
                    u4_xor_second_block = u4_second_block ^ u4_star_second_block
                    if ((u4_xor_first_block == 1) and (
                        u4_xor_second_block == 1)):
                        count[(a,b)] += 1
    max_num = -1
    # select key with highest absolute bias
    for a in range(0,16):
        for b in range(0,16):
            # print (count[(a,b)])
            if count[(a,b)] > max_num:
                max_num = count[(a,b)]
                max_key = (a,b)
    #print(max_num)
    return max_key

def getNumberOfRequiredKeys(key, pairs, permutation_table, f):
    key = key[0:2]
    correct = False
    i = 1
    while (not correct):
        result = f(pairs[0:i],permutation_table)
        result = str(hex(result[0]))[2:] + str(hex(result[1]))[2:]
        correct = (result == key)
        i += 1
        if (i > len(pairs)):
            sys.exit('not enough keys')
    return i

def main():
    permutation_table = [14,2,1,3,13,9,0,6,15,4,5,10,8,12,7,11]

    # preparing pairs of plaintext, cryptotext
    pairs = []
    with open('spn/keys.txt','r') as f:
        data = f.read().splitlines()
    for i in data:
        pair_tuple = i.split(',')
        pairs.append((int(pair_tuple[0],16),int(pair_tuple[1],16),
            int(pair_tuple[2],16), int(pair_tuple[3],16)))

    print(getNumberOfRequiredKeys('26B7',pairs, permutation_table,
        differentialAttack))

if __name__ == "__main__":
    main()
