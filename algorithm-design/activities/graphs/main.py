from lib_graphs import Graph, binary_search
from lib_api_request import PokemonAPI
from typing import List, Optional

class PokemonEvolutionChain:
    def __init__(self):
        self.api = PokemonAPI()
        self.graph = Graph()
        self.sorted_nodes: List[str] = []
    
    def build_chain(self, pokemon_name: str) -> bool:
        # Get the evolution chain URL
        chain_url = self.api.get_evolution_chain_url(pokemon_name)
        if not chain_url:
            return False
        
        # Get the evolution chain data
        print(f"Fetching data from: {chain_url}")
        chain_data = self.api.get_evolution_chain(chain_url)
        if not chain_data:
            return False
        
        # Build the evolution dictionary
        evolution_dict = self.api.build_evolution_dict(chain_data)
        
        # Build the graph from the dictionary
        self.graph.build_from_dict(evolution_dict)
        
        # Update sorted nodes list
        nodes = self.graph.get_all_nodes()
        nodes.add(pokemon_name)  # Add the search pokemon in case it's not in the graph
        self.sorted_nodes = sorted(list(nodes))
        
        return True
    
    def print_results(self, pokemon_name: str) -> None:
        """Prints the evolution chain and performs the binary search test"""
        print(f"\n--- Evolution Graph of {pokemon_name.capitalize()} (Adjacency List) ---")
        self.graph.print_graph()
        
        print("\n--- Sorted Chain Nodes (for Binary Search) ---")
        print([node.capitalize() for node in self.sorted_nodes])
        
        print("\n--- Interactive Binary Search Test ---")
        test_target = self._get_test_target()
        target_to_find = input(f"Enter a Pokémon name to check if it's in this chain (e.g., '{test_target}'): ").lower().strip()
        
        if target_to_find:
            is_found = binary_search(self.sorted_nodes, target_to_find, 0, None)
            print(f"Is '{target_to_find.capitalize()}' in the {pokemon_name.capitalize()}'s chain? -> {'YES' if is_found else 'NO'}")
    
    def _get_test_target(self) -> str:
        if len(self.sorted_nodes) > 1:
            return self.sorted_nodes[1].capitalize()
        elif self.sorted_nodes:
            return self.sorted_nodes[0].capitalize()
        return "Ivysaur"

def main():
    try:
        pokemon_to_search = input("Enter the name of the Pokémon to get its evolution chain (e.g., 'charmander', 'eevee'): ").lower().strip()
    except EOFError:
        print("\nInput skipped.")
        pokemon_to_search = ""

    if not pokemon_to_search:
        print("Exiting program.")
        return

    # Create and build the evolution chain
    evolution_chain = PokemonEvolutionChain()
    if evolution_chain.build_chain(pokemon_to_search):
        evolution_chain.print_results(pokemon_to_search)
    else:
        print(f"\nCould not retrieve the chain for {pokemon_to_search.capitalize()}.")

if __name__ == "__main__":
    main()