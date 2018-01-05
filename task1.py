#question2 
#Given:
L1 = ['a', 'b', 'c']
L2 = ['b', 'd']

def common():
    count = 0
    for i in L1:
        for j in L2:
            if(i == j):
                print("{} is one of the common element".format(i))
                count = count + 1

    print("The total number of common elements are :{}".format(count))


def elements_a():
    setl1 = set(L1)
    setl2 = set(L2)
    # Set Subtraction
    result = setl1 - setl2
    print(result)


common()
elements_a()
