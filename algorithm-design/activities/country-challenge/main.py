import requests

url = "https://restcountries.com/v3.1/region/europe"

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def process_data(data):
    if not data:
        return []

    processed = []
    for country in data:
        name_en = country.get('name', {}).get('common', 'N/A')
        name_es = country.get('translations', {}).get('spa', {}).get('common', name_en)
        maps = country.get('maps', {}).get('googleMaps', 'N/A')

        processed.append({
            'name_en': name_en,
            'name_es': name_es,
            'maps': maps
        })
    return processed

def order_list(country_list):
    return sorted(country_list, key=lambda x: x['name_en'].lower())
def lineal_search(list, target):
    for i in range(len(list)):
        if list[i]['name_en'].lower() == target.lower():
            return list[i]['name_en'], list[i]['maps'], i
        elif list[i]['name_es'].lower() == target.lower():
            return list[i]['name_es'], list[i]['maps'], i
    return "Not found"

def binary_search(countries, target):
    target = target.lower()

    # Detectar si el target está en español o inglés
    if any(c['name_es'].lower() == target for c in countries):
        sorted_list = sorted(countries, key=lambda x: x['name_es'].lower())
        key_field = 'name_es'
    else:
        sorted_list = sorted(countries, key=lambda x: x['name_en'].lower())
        key_field = 'name_en'

    left, right = 0, len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_value = sorted_list[mid][key_field].lower()
        if mid_value == target:
            return sorted_list[mid][key_field], sorted_list[mid]['maps'], mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    return "Not found"


def menu(countries):
    while True:
        print("Menu:\n1. Search a country\n2. Exit")
        choice = input("Choose an option (1-2): ").strip()

        if choice == '1':
            country_input = input("Enter the name of a European country (English or Spanish): ").strip().lower()

            # Validación en ambos idiomas
            valid_names = [c['name_en'].lower() for c in countries] + [c['name_es'].lower() for c in countries]
            if country_input not in valid_names:
                print(f"'{country_input}' is not a valid country name. Try again.")
                continue

            print("1. Lineal Search\n2. Binary Search")
            search_type = input("Choose search type (1-2): ").strip()
            if search_type == '1':
                return country_input, 'lineal'
            elif search_type == '2':
                return country_input, 'binary'
            else:
                print("Invalid search type. Please try again.")
        elif choice == '2':
            print("Exiting the program.")
            return None, None
        else:
            print("Invalid choice. Please try again.")


def show_results(result):
    if result == "Not found":
        print("Country not found.")
    else:
        name, map_url, index = result
        print(f"Country: {name}")
        print(f"Google Maps: {map_url}")
        print(f"Index: {index}")

def main():
    data = fetch_data(url)
    countries = process_data(data)

    while True:
        country, type_search = menu(countries)
        if country is None or type_search is None:
            break  # El usuario eligió salir

        if type_search == 'lineal':
            result = lineal_search(countries, country)
            show_results(result)
        elif type_search == 'binary':
            countries_sorted = order_list(countries)
            result = binary_search(countries_sorted, country)
            show_results(result)
        else:
            print("Invalid search type.")

if __name__ == "__main__":
    main()