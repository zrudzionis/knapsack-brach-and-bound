    while size != 0:
        print stack
        if size < itemsCount:
            stack.append(1)
            size += 1
        else:
            taken = stack.pop()
            size -= 1
            if taken == 1:
                stack.append(-1)
                size += 1
            else:
                nextTaken = stack.pop()
                size -= 1
                while nextTaken != 1 and size > 0:
                    nextTaken = stack.pop()
                    size -= 1
                if nextTaken == 1:
                    stack.append(-1)
                    size += 1

