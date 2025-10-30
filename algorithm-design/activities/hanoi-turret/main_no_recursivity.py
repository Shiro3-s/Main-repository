import random

# Crear lista inicial de discos y desordenarla
firt_tower = [7, 6, 5, 4, 3, 2, 1]
random.shuffle(firt_tower)

second_tower = []
third_tower = []

print("Initial Randomized State:")
print("First Tower:", firt_tower)
print("Second Tower:", second_tower)
print("Third Tower:", third_tower)
print()

def source_name(tower):
    if tower is firt_tower:
        return "First Tower"
    elif tower is second_tower:
        return "Second Tower"
    elif tower is third_tower:
        return "Third Tower"
    return "Unknown Tower"

def print_state():
    print("Current State:")
    print("First Tower:", firt_tower)
    print("Second Tower:", second_tower)
    print("Third Tower:", third_tower)
    print()

def move_disk(src, dest):
    if src and (not dest or src[-1] < dest[-1]):
        disk = src.pop()
        dest.append(disk)
        print(f"Move disk {disk} from {source_name(src)} to {source_name(dest)}")
        print_state()
    elif dest and (not src or dest[-1] < src[-1]):
        disk = dest.pop()
        src.append(disk)
        print(f"Move disk {disk} from {source_name(dest)} to {source_name(src)}")
        print_state()

def iterative_hanoi(n, src, aux, dest):
    # Si n es par, intercambiar destino y auxiliar
    if n % 2 == 0:
        aux, dest = dest, aux

    total_moves = 2**n - 1

    for move in range(1, total_moves + 1):
        if move % 3 == 1:
            move_disk(src, dest)
        elif move % 3 == 2:
            move_disk(src, aux)
        elif move % 3 == 0:
            move_disk(aux, dest)

num_disks = len(firt_tower)
iterative_hanoi(num_disks, firt_tower, second_tower, third_tower)
