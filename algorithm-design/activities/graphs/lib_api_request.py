import requests
from typing import Dict, List, Any, Optional

class PokemonAPI:
    BASE_URL = "https://pokeapi.co/api/v2"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_evolution_chain_url(self, pokemon_name: str) -> Optional[str]:
        pokemon_name = pokemon_name.lower().strip()
        species_url = f"{self.BASE_URL}/pokemon-species/{pokemon_name}/"
    
        print(f"Searching for species: {pokemon_name.capitalize()}...")
        try:
            response = self.session.get(species_url, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            
            chain_url = json_data['evolution_chain']['url']
            print(f"Evolution chain URL found.")
            return chain_url

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Error 404: Pokémon '{pokemon_name.capitalize()}' not found.")
            else:
                print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None
    
    def get_evolution_chain(self, chain_url: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(chain_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Consumption Error (Chain): {e}")
            return None
    
    def build_evolution_dict(self, chain_data: Dict[str, Any]) -> Dict[str, List[str]]:
        evolution_graph: Dict[str, List[str]] = {}
        
        def build_graph_recursive(node: Dict[str, Any]):
            current_pokemon = node['species']['name']
            evolutions = []
            
            for evolution in node.get('evolves_to', []):
                evolution_name = evolution['species']['name']
                evolutions.append(evolution_name)
                build_graph_recursive(evolution)
            
            if evolutions:
                evolution_graph[current_pokemon] = evolutions
        
        build_graph_recursive(chain_data['chain'])
        return evolution_graph
        