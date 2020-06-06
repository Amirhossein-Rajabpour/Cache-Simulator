#Amirhossein Rajabpour 9731085
import math
dirty_bits = set()
#getting base information about the cache
info = input().rstrip('\n')
info2 = info.split(' - ')
block_size = int(info2[0])
is_separated = info2[1]
associativity = int(info2[2])
write_policy = info2[3]
write_miss = info2[4]

def set_finder(my_index, how_many_sets):
    my_index = my_index[::-1]
    my_set = int(my_index) % how_many_sets
    return my_set

def index_finder(address,block_size, num_blocks):
    power1 = math.log(block_size, 2)
    sets = int(num_blocks / associativity)
    power2 = math.log(sets, 2)
    index = address[:: -1]
    index = index[int(power1) : int(power1) + int(power2)]
    return index

def tag_finder(address,num_blocks):
    power1 = math.log(block_size, 2)
    sets = int(num_blocks / associativity)
    power2 = math.log(sets, 2)
    address = address[:: -1]
    tag = address[int(power2) + int(power1):]
    return tag[::-1]

def tag_checking(address, queue, num_blocks):
    exist = False
    for i in queue:
        if tag_finder(address,num_blocks) == tag_finder(i,num_blocks):
            queue.remove(i)
            exist = True
    return exist

#initializing cache structure with a list of empty queues
if is_separated == '0':
    cache_size = input().rstrip('\n')
    number_of_blocks = int(int(cache_size) / block_size)
    cache = []
    for q in range(int(number_of_blocks/associativity)):
        queue = []
        cache.append(queue)
else:
    cache_size = input().rstrip('\n').split(' - ')
    #initializing instruction cache
    instruction_size = cache_size[0]
    number_of_inst_blocks = int(int(instruction_size) / block_size)
    i_cache = []
    for q in range(int(number_of_inst_blocks/associativity)):
        queue = []
        i_cache.append(queue)
    # initializing data cache
    data_size = cache_size[1]
    number_of_data_blocks = int(int(data_size) / block_size)
    d_cache = []
    for q in range(int(number_of_data_blocks/associativity)):
        queue = []
        d_cache.append(queue)

#factors that should be calculated
d_accesses = 0
d_misses = 0
d_replace = 0
i_accesses = 0
i_misses = 0
i_replace = 0
fetch = 0
copies_back = 0

#if the structure is von-nuemann
if is_separated == '0':

    lines = []
    read = True
    while read:
        line = input()
        if line == '':
            read = False
            break
        else:
            lines.append(line)

    for d in lines:
        tmp = d.split(' ')
        tmp = tmp[:2]
        # Code to convert hex to binary
        res = "{0:032b}".format(int(tmp[1], 16))
        res = str(res)

        index = index_finder(res, block_size, number_of_blocks)
        tmp_set = set_finder(index, int(number_of_blocks / associativity))

        if tmp[0] == '0' or tmp[0] == '2':

            if tmp[0] == '0': d_accesses += 1
            else: i_accesses += 1

            if tag_checking(res,cache[tmp_set],number_of_blocks):   cache[tmp_set].append(res)
            else:
                fetch += (block_size / 4)
                if len(cache[tmp_set]) == associativity:
                    evicted = cache[tmp_set].pop(0)
                    if evicted[:-int(math.log(block_size, 2))] in dirty_bits:
                        copies_back += (block_size / 4)
                        dirty_bits.remove(evicted[:-int(math.log(block_size, 2))])
                    cache[tmp_set].append(res)
                    if tmp[0] == '0':
                        d_misses += 1
                        d_replace += 1
                    else:
                        i_misses += 1
                        i_replace += 1
                else:
                    cache[tmp_set].append(res)
                    if tmp[0] == '0':   d_misses += 1
                    else:   i_misses += 1

        elif tmp[0] == '1':

            d_accesses += 1

            if write_policy == 'wt' and write_miss == 'wa':

                copies_back += 1
                if tag_checking(res,cache[tmp_set],number_of_blocks):   cache[tmp_set].append(res)
                else:
                    fetch += (block_size / 4)
                    d_misses += 1
                    if len(cache[tmp_set]) == associativity:
                        cache[tmp_set].pop(0)
                        cache[tmp_set].append(res)
                        d_replace += 1
                    else:   cache[tmp_set].append(res)

            elif write_policy == 'wt' and write_miss == 'nw':

                copies_back += 1
                if tag_checking(res,cache[tmp_set],number_of_blocks):   cache[tmp_set].append(res)
                else:   d_misses += 1

            elif write_policy == 'wb' and write_miss == 'wa':

                dirty_bits.add(res[:-int(math.log(block_size, 2))])
                if tag_checking(res, cache[tmp_set], number_of_blocks): cache[tmp_set].append(res)
                else:
                    d_misses += 1
                    fetch += (block_size / 4)
                    if len(cache[tmp_set]) == associativity:
                        evicted = cache[tmp_set].pop(0)
                        if evicted[:-int(math.log(block_size, 2))] in dirty_bits:
                            copies_back += (block_size / 4)
                            dirty_bits.remove(evicted[:-int(math.log(block_size, 2))])
                        cache[tmp_set].append(res)
                        d_replace += 1
                    else:   cache[tmp_set].append(res)

            elif write_policy == 'wb' and write_miss == 'nw':
                if tag_checking(res, cache[tmp_set], number_of_blocks):
                    cache[tmp_set].append(res)
                    dirty_bits.add(res[:-int(math.log(block_size, 2))])
                else:
                    d_misses += 1
                    copies_back += 1


#if the structure is harvard
else:
    lines = []
    read = True
    while read:
        line = input()
        if line == '':
            read = False
            break
        else:
            lines.append(line)

    for d in lines:
        tmp = d.split(' ')
        tmp = tmp[:2]
        # Code to convert hex to binary
        res = "{0:032b}".format(int(tmp[1], 16))
        res = str(res)

        #reading data
        if tmp[0] == '0':
            d_accesses += 1
            index = index_finder(res, block_size,number_of_data_blocks )
            tmp_set = set_finder(index, int(number_of_data_blocks / associativity))

            if tag_checking(res,d_cache[tmp_set],number_of_data_blocks):    d_cache[tmp_set].append(res)
            else:
                fetch += (block_size / 4)
                d_misses += 1
                if len(d_cache[tmp_set]) == associativity:
                    evicted = d_cache[tmp_set].pop(0)
                    if evicted[:-int(math.log(block_size, 2))] in dirty_bits:
                        copies_back += (block_size / 4)
                        dirty_bits.remove(evicted[:-int(math.log(block_size, 2))])
                    d_cache[tmp_set].append(res)
                    d_replace += 1
                else:   d_cache[tmp_set].append(res)

        #reading instruction
        elif tmp[0] == '2':
            i_accesses += 1
            index = index_finder(res, block_size,number_of_inst_blocks)
            tmp_set = set_finder(index, int(number_of_inst_blocks / associativity))

            if tag_checking(res,i_cache[tmp_set],number_of_inst_blocks):    i_cache[tmp_set].append(res)
            else:
                fetch += (block_size / 4)
                i_misses += 1
                if len(i_cache[tmp_set]) == associativity:
                    evicted = i_cache[tmp_set].pop(0)
                    i_cache[tmp_set].append(res)
                    i_replace += 1
                else:   i_cache[tmp_set].append(res)

        #writing data
        elif tmp[0] == '1':

            index = index_finder(res, block_size,number_of_data_blocks )
            tmp_set = set_finder(index, int(number_of_data_blocks / associativity))

            d_accesses += 1

            if write_policy == 'wt' and write_miss == 'wa':

                copies_back += 1
                if tag_checking(res,d_cache[tmp_set],number_of_data_blocks):    d_cache[tmp_set].append(res)
                else:
                    fetch += (block_size / 4)
                    d_misses += 1
                if len(d_cache[tmp_set]) == associativity:
                        d_cache[tmp_set].pop(0)
                        d_cache[tmp_set].append(res)
                        d_replace += 1
                else:   d_cache[tmp_set].append(res)

            elif write_policy == 'wt' and write_miss == 'nw':

                copies_back += 1
                if tag_checking(res,d_cache[tmp_set],number_of_data_blocks):    d_cache[tmp_set].append(res)
                else:   d_misses += 1

            elif write_policy == 'wb' and write_miss == 'wa':
                dirty_bits.add(res[:-4])
                if tag_checking(res, d_cache[tmp_set], number_of_data_blocks):  d_cache[tmp_set].append(res)
                else:
                    fetch += (block_size / 4)
                    d_misses += 1
                    if len(d_cache[tmp_set]) == associativity:
                        evicted = d_cache[tmp_set].pop(0)
                        if evicted[:-int(math.log(block_size, 2))] in dirty_bits:
                            copies_back += (block_size / 4)
                            dirty_bits.remove(evicted[:-int(math.log(block_size, 2))])
                        d_cache[tmp_set].append(res)
                        d_replace += 1
                    else:   d_cache[tmp_set].append(res)

            elif write_policy == 'wb' and write_miss == 'nw':
                if tag_checking(res, d_cache[tmp_set], number_of_data_blocks):
                    d_cache[tmp_set].append(res)
                    dirty_bits.add(res[:-int(math.log(block_size, 2))])
                else:
                    copies_back += 1
                    d_misses += 1

copies_back += (len(dirty_bits) * int(block_size/4) )

print('***CACHE SETTINGS***')
if is_separated == '0':
    print('Unified I- D-cache')
    print('Size:',cache_size)
else:
    print('Split I- D-cache')
    print('I-cache size:', instruction_size)
    print('D-cache size:', data_size)
print('Associativity:',associativity)
print('Block size:',block_size)
if write_policy == 'wb': print('Write policy: WRITE BACK')
else: print('Write policy: WRITE THROUGH')
if write_miss == 'wa': print('Allocation policy: WRITE ALLOCATE')
else: print('Allocation policy: WRITE NO ALLOCATE')
print()
print('***CACHE STATISTICS***')
print('INSTRUCTIONS')
print('accesses:',i_accesses)
print('misses:',i_misses)
if i_accesses != 0:
    i_miss_rate = i_misses / i_accesses
    i_hit_rate = 1 - i_miss_rate
    print('miss rate:', "{:.4f}".format(i_miss_rate),'(hit rate', "{:.4f}".format(i_hit_rate) +')')
else: print('miss rate: 0.0000 (hit rate 0.0000)')
print('replace:',i_replace)
print('DATA')
print('accesses:',d_accesses)
print('misses:',d_misses)
if d_accesses != 0:
    d_miss_rate = d_misses / d_accesses
    d_hit_rate = 1 - d_miss_rate
    print('miss rate:', "{:.4f}".format(d_miss_rate) ,'(hit rate',"{:.4f}".format(d_hit_rate) +')')
else: print('miss rate: 0.0000 (hit rate 0.0000)')
print('replace:',d_replace)
print('TRAFFIC (in words)')
print('demand fetch:',int(fetch))
print('copies back:',int(copies_back))