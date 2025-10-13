#Si pes t ^ Q es f implica q

p = True
q = False

def cambiar_valores_pq(p, q):
    return not p, not q
def cambiar_valores_p(p):
    return not p
def cambiar_valores_q(q):
    return not q

while True:
    print("Valores actuales: p =", p, ", q =", q)
    espera = input("Presione Enter para continuar...")
    print("1. Cambiar valor de p")
    print("2. Cambiar valor de q")
    print("3. Cambiar valores de p y q")
    print("4. Operaciones logicas")
    print("5. Salir")
    opcion = input("Seleccione una opción (1-5): ")
    if opcion == '1':
        p = cambiar_valores_p(p)
    elif opcion == '2':
        q = cambiar_valores_q(q)
    elif opcion == '3':
        p, q = cambiar_valores_pq(p, q)
    elif opcion == '4':
        print("p and q:", p and q)
        print("p or q:", p or q)
        print("not p:", not p)
        print("not q:", not q)
        print("p implies q:", (not p) or q)
        print("q implies p:", (not q) or p)
        print("p if and only if q:", p == q)
        espera = input("Presione Enter para continuar...")
    elif opcion == '5':
        break
    else:
        print("Opción no válida. Intente de nuevo.")
