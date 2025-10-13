def sum_int_numbers(target):
    if target == 0:
        return 0
    else:
        return target % 10 + sum_int_numbers(target // 10)

target = int(input("Enter a non-negative integer: "))
print(sum_int_numbers(target))