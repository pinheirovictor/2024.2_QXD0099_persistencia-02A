import yaml
import json
import logging

# Função para configurar o logging
def configure_logging(config):
    level = getattr(logging, config["level"], logging.INFO)
    logging.basicConfig(
        level=level,
        filename=config["file"],
        format=config["format"],
        filemode="a"
    )

# Função para processar os dados JSON
def process_data(json_file):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            logging.info(f"Arquivo JSON '{json_file}' carregado com sucesso.")
    except FileNotFoundError:
        logging.error(f"Arquivo JSON '{json_file}' não encontrado.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar o JSON: {e}")
        return []

    # Simulação de processamento de dados
    for record in data:
        try:
            if "name" not in record or record["age"] is None:
                raise ValueError(f"Dado inválido: {record}")
            logging.info(f"Processando registro: {record}")
        except ValueError as e:
            logging.warning(f"Erro no registro: {e}")

    return data

# Função principal
def main():
    # Carrega as configurações do YAML
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Configura o logging
    configure_logging(config["logging"])

    # Processa os dados JSON
    process_data(config["data"]["file"])

# Executa o programa
if __name__ == "__main__":
    main()
