import requests
import pandas as pd

# Função para carregar as categorias do arquivo
def load_categories(file_path):
    with open(file_path, 'r') as categories_file:
        categories_lines = categories_file.readlines()

    categories_dict = {}
    for line in categories_lines:
        parts = line.strip().split('.')
        current_dict = categories_dict
        for part in parts:
            current_dict = current_dict.setdefault(part, {})

    return categories_dict


# Função para obter atrações da API Geoapify
def get_attractions_from_api(latitude, longitude, radius, categories):
    url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{longitude},{latitude},{radius}&bias=proximity:{longitude},{latitude}&apiKey=35118c1b7ad845a2a867abdd28654992"

    response = requests.get(url)
    return response.json().get('features', [])


# Função para obter a moeda de um país usando a API Restcountries
def get_currency_by_country(country_name):
    base_url = "https://restcountries.com/v2/name"
    url = f"{base_url}/{country_name}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data and isinstance(data, list) and data[0].get("currencies"):
            currencies = data[0]["currencies"]

            if currencies and isinstance(currencies, list):
                return currencies[0]["name"]
            else:
                return "Currency information not available for this country."
        else:
            return "Country not found or currency information not available."
    else:
        return f"Error: {response.status_code}"


# Função principal
def main():
    # Carregar categorias do arquivo categories.txt
    categories_file_path = 'C:/FP/aulaT/trabalho 2/categories.txt'
    categories_dict = load_categories(categories_file_path)

    # Obter informações do usuário
    latitude = float(input("Digite a latitude de partida: "))
    longitude = float(input("Digite a longitude de partida: "))
    radius = int(input("Digite a distância desejada em kilometros: ")) * 1000
    selected_categories = input("Digite as categorias desejadas, separadas por vírgula: ")

    # Obter atrações da API Geoapify
    attractions_from_api = get_attractions_from_api(latitude, longitude, radius, selected_categories)

    # Criar um DataFrame vazio
    df_atracoes = pd.DataFrame(columns=[
        'Nome da Atração',
        'País',
        'Latitude',
        'Longitude',
        'Distância à localização de partida',
        'Rua',
        'Entidade',
        'Código Postal',
        'Distrito'
    ])

    # Mostrar informações detalhadas sobre as atrações filtradas
    count = 0
    media = 0
    for attraction in attractions_from_api:
        attraction = attraction["properties"]

        count += 1

        name = attraction.get('name', "Nome desconhecido")
        country = attraction['country']
        latitude = attraction['lat']
        longitude = attraction['lon']
        distance = attraction['distance'] / 1000
        media += distance

        amenity = attraction.get('datasource', {}).get('raw', {}).get('amenity', "Indefinido")
        street = attraction.get('street', "Rua desconhecida")
        postcode = attraction.get('postcode', "Codigo postal não encontrado")
        district = attraction.get('district', "Rua não encontrada")
        currency = get_currency_by_country(country)

        # Tratamento de erro para o caso "United States" e informações desconhecidas
        if (country == "United States"):
            currency = "American dollar"

        if (name == "Nome desconhecido" and district == "Rua não encontrada"):
            continue

        # Imprimir informações detalhadas sobre a atração
        print(f"Nome da Atração: {name}")
        print(f"País: {country}")
        print(f"Localização: Latitude {latitude}, Longitude {longitude}")
        print(f"Distância à localização de partida: {distance:.2f} km")
        print(f"Rua: {street} ")
        print(f"Entidade: {amenity} ")
        print(f"Código Postal: {postcode} ")
        print(f"Distrito: {district} ")
        print(f"Moeda: {currency} ")
        print("--------------------------------------------------------------------")

        # Adicionar os dados de cada atração ao DataFrame
        data_to_append = {
            'Nome da Atração': [name],
            'País': [country],
            'Latitude': [latitude],
            'Longitude': [longitude],
            'Distância à localização de partida': [distance],
            'Rua': [street],
            'Entidade': [amenity],
            'Código Postal': [postcode],
            'Distrito': [district]
        }

        # Concatenar apenas se houver dados
        if not pd.DataFrame(data_to_append).empty:
            df_atracoes = pd.concat([df_atracoes, pd.DataFrame(data_to_append)], ignore_index=True, sort=False)

    # Opções de ordenação e filtragem
    print("\nOpções de ordenação:")
    print("1. Ordenar por Nome da Atração")
    print("2. Ordenar por Distância à localização de partida")

    opcao = int(input("\nEscolha uma opção (0 para sair): "))

    while opcao != 0:
        if opcao == 1:
            df_atracoes = df_atracoes.sort_values("Nome da Atração")
            break
        elif opcao == 2:
            df_atracoes = df_atracoes.sort_values('Distância à localização de partida')
            break
        else:
            print("Opção inválida.")

    # Especificar o caminho do arquivo CSV (substitua pelo caminho desejado)
    caminho_arquivo_csv_atracoes = 'C:/FP/aulaT/trabalho 2/projeto 2 grupo/atracoes.csv'

    # Exportar o DataFrame para um arquivo CSV
    df_atracoes.to_csv(caminho_arquivo_csv_atracoes, index=False, encoding='utf-8')


if __name__ == "__main__":
    main()
