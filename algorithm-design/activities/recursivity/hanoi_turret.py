turret_1 = [1,2,3]
turret_2 = []
turret_3 = []
def hanoi(n, source, auxiliary, target):
    if n == 1:
        disk = source.pop()
        target.append(disk)
        print(f"Move disk {disk} from {source} to {target}")
        print(f"State: {turret_1}, {turret_2}, {turret_3}")
    else:
        hanoi(n - 1, source, target, auxiliary)
        disk = source.pop()
        target.append(disk)
        print(f"Move disk {disk} from {source} to {target}")
        print(f"State: {turret_1}, {turret_2}, {turret_3}")
        hanoi(n - 1, auxiliary, source, target)
hanoi(len(turret_1), turret_1, turret_2, turret_3)
