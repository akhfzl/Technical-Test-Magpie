def InitiatorOfDiscount(N):
    smallerPosition = []
    sumDifference = 0
    overalValueIsSame = all(x == N[0] for x in N)
    if overalValueIsSame:
        return 0
    
    for i, v in enumerate(N):
        if i == len(N) - 1:
            if sumDifference > 0:
                smallerPosition.append(i)
            break
        difference = v - N[i+1]
        sumDifference += difference
    
    return 0 if len(smallerPosition) == 0 else smallerPosition[0]




x = InitiatorOfDiscount([3, 3, 3])
print(x)