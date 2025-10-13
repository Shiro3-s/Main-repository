import random

class cards:
    number_cards = list(range(1,14)) #up to 53
    cards_club = ["h","c","d","s"] #hearts, cloves, diamonds and spades

class deck:
    @staticmethod
    def shuffle_deck():
        deck_list = []  #the list where all cards are 
        for card_club in cards.cards_club:
            for number in cards.number_cards:
                deck_list.append(f"{number}{card_club}")
        random.shuffle(deck_list)
        return deck_list
    
    #funtion to separate the cards in the deck for deck
    def separate_by_clubs(self):
        my_deck = self.shuffle_deck()
        #create 4 list, representing each deck
        h = []
        c = []
        d = []
        s = []
        #in this loop we separate de club and the number, divide and convert to an int
        for card in my_deck:
            if card.endswith("h"):
                h.append(int(card[:-1]))
            elif card.endswith("c"):
                c.append(int(card[:-1]))
            elif card.endswith("d"):
                d.append(int(card[:-1]))
            elif card.endswith("s"):
                s.append(int(card[:-1]))
        #this funtion returns 4 list with numbers
        return h,c,d,s

    def decks_before_sort(self):
        h_list, c_list, d_list, s_list = self.separate_by_clubs()
        return h_list, c_list, d_list, s_list
    
    def insertion_sort(self, lista):
        n = len(lista)
    # Recorre la lista desde el segundo elemento
        for i in range(1, n):
            key = lista[i]
            j = i - 1
            print(f"Clave actual: {key}, Índice: {i}")
            print(j)
        # Mueve los elementos de la lista ordenada que son mayores que la 'key' a una posición adelante de su posición actual
            while j >= 0 and key < lista[j]:
                print(lista)
                lista[j + 1] = lista[j]
                print(lista)

                j -= 1
            lista[j + 1] = key
            print(lista)
            print(f"Lista actual: {lista}")
        return lista

    def decks_after_sort(self):
        h_list, c_list, d_list, s_list = self.decks_before_sort()
        
        # We sort each list using the instance method
        h_list_sorted = self.insertion_sort(h_list)
        c_list_sorted = self.insertion_sort(c_list)
        d_list_sorted = self.insertion_sort(d_list)
        s_list_sorted = self.insertion_sort(s_list)
        
        return h_list_sorted, c_list_sorted, d_list_sorted, s_list_sorted

