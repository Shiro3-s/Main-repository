import poker_deck_lib as deck_lib

#instance of the deck object
my_deck_instance = deck_lib.deck()
print(my_deck_instance.shuffle_deck())
# Get the lists before sorting
h_before, c_before, d_before, s_before = my_deck_instance.decks_before_sort()
print("Listas antes del ordenamiento:")
print("Corazones:", h_before)
print("Tréboles:", c_before)
print("Diamantes:", d_before)
print("Picas:", s_before)

# Get the lists after sorting
h_after, c_after, d_after, s_after = my_deck_instance.decks_after_sort()
print("\nListas después del ordenamiento:")
print("Corazones:", h_after)
print("Tréboles:", c_after)
print("Diamantes:", d_after)
print("Picas:", s_after)