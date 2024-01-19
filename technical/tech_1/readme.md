expectation:
    1. When the function InitiatorOfDiscount is given array/list params, it will be returned int as position where reduction happen
    2. example [3, 4, 1] it will be index of 2 that reduction happen. So im using a logic about looping and sumDifference, then append the index to list

for my case:
function -> InitiatorOfDiscount([3, 4, 1, 7, 8, 5, 2])
initial sumDifference = 0
reducing by params[i] - params[i+1]
loop i = 0 -> 3 - 4 = -1, i added sumDifference += -1
loop i = 1 -> 4 -1 = 3, i added sumDifference = -1 to sumDifference += 3 -> now sumDifference is 2
loop i = 2 -> 1 - 7 = -6, i added sumDifference = 2 to sumDifference += -6 -> now sumDifference is -4
loop i = 3 -> 7 - 8 = -1, i added sumDifference = -4 to sumDifference += -1 -> now sumDifference is -5
loop i = 4 -> 8 - 5 = 3, i added sumDifference = -5 to sumDifference += 3 -> now sumDifference is -2
loop i = 5 -> 5 - 2 = 3, i added sumDifference -2 to sumDifference += 3 -:> now sumDifference is 1

then if i == len(params) - 1:
    and the sumDifference > 0: 
        i added smallerPosition base on i / position of reduction
        break looping
    
variable of overalValueIsSame is checked if the params has same of value example: [3, 3, 3, 3]
if smallerPostion has array's length 0, it will return 0
