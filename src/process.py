import sys

ordersFile = sys.argv[1]
productsFile = sys.argv[2]
outputFile = sys.argv[3]

products = {}  # key= product id. value = dept id

p_stats = {}  # key = dept id {orders: 0, firstOrders: 0}

with open(productsFile) as pFile:
    next(pFile)  # skip first line
    for productLine in pFile:
        p = productLine.split(',')
        products[int(p[0])] = int(p[-1].rstrip())
        #print('{0}, {1}'.format(p[0], p[-1]))

p_stats = {}
with open(ordersFile) as f_obj:
    next(f_obj)  # skip first line
    for orderLine in f_obj:
        o = orderLine.split(',')

        orderedPId = int(o[1])
        firstOrder = int(o[3])

        try:
            orderedPDeptId = products[orderedPId]  # get dept id for ordered product
        except KeyError as e:  # Handle missing product id in Products file
            print(e)

        # does dict contain dept id already
        if orderedPDeptId in p_stats:  # check if row exists for dept
            deptStat = p_stats[orderedPDeptId]  # get dept stat if exists
            deptStat['orders'] += 1  # increment order count

            if firstOrder == 0:
                deptStat['firstOrders'] += 1  # increment first orders
        else:
            p_stats[orderedPDeptId] = {'orders': 1, 'firstOrders': (1 if (firstOrder == 0) else 0)}  # add new dept

with open(outputFile, 'w') as f:
    f.write("department_id,number_of_orders,number_of_first_orders,percentage\n");
    for k,v in sorted(p_stats.items()):
        f.write("{0},{1},{2},{3:.2f}\n".format(k, v['orders'], v['firstOrders'], (int(v['firstOrders'])/int(v['orders']))))

f.close()

