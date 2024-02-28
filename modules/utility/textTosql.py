import requests
from qgis.PyQt.QtWidgets import QMessageBox

from . import database_schema


class MakeSQL:
    def __init__(self):
        pass
    # Funzione per convertire lo schema in formato testuale (esempio semplificato)
    @staticmethod
    def schema_to_text(metadata):
        schema_text = ""
        for table in metadata.tables.values():
            # Inizia con il nome della tabella
            table_description = f"{table.name} ("
            # Aggiungi ogni colonna e il suo tipo
            columns_descriptions = [f"{col.name}" for col in table.columns]
            table_description += ", ".join(columns_descriptions)
            table_description += ");"
            # Aggiungi la descrizione della tabella al testo dello schema
            schema_text += table_description + "\n"
        return schema_text

    # Utilizzo della funzione per includere lo schema nella richiesta API
    @staticmethod
    def make_api_request(prompt,db,apikey):
        # Preparazione dello schema
        #schema = Base.metadata  # Assuming Campioni_table is part of Base
        schema_text = MakeSQL.schema_to_text(database_schema.metadata)  # Converti lo schema in testo
        #QMessageBox.information(None, "Schema", schema_text)
        api_key = apikey  # Sostituisci con la tua chiave API
        url = "https://www.text2sql.ai/api/sql/generate"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "type": db,
            "schema": schema_text  # Utilizzo dello schema convertito
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            print(f"Response Status Code: {response.status_code}")  # Debug print
            response.raise_for_status()

            response_json = response.json()
            print(f"Response JSON: {response_json}")  # Debug print
            generated_sql = response_json.get('output', '')  # Extract the SQL statement
            #QMessageBox.information(None, "SQL", generated_sql)  # Show the SQL statement in the message box
            return generated_sql
        except requests.exceptions.HTTPError as he:
            print(f"HTTP Error: {he}")
            QMessageBox.critical(None, "HTTP Error", str(he))
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(None, "Error", str(e))
            return None

        return None

    @staticmethod
    def explain_request(prompt, apikey):
        # Preparazione dello schema
        # schema = Base.metadata  # Assuming Campioni_table is part of Base
        #schema_text = MakeSQL.schema_to_text(database_schema.metadata)  # Converti lo schema in testo
        # QMessageBox.information(None, "Schema", schema_text)
        api_key = apikey  # Sostituisci con la tua chiave API
        url = "https://www.text2sql.ai/api/sql/explain"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            print(f"Response Status Code: {response.status_code}")  # Debug print
            response.raise_for_status()

            response_json = response.json()
            print(f"Response JSON: {response_json}")  # Debug print
            generated_sql = response_json.get('output', '')  # Extract the SQL statement
            #QMessageBox.information(None, "SQL", generated_sql)  # Show the SQL statement in the message box
            return generated_sql
        except requests.exceptions.HTTPError as he:
            print(f"HTTP Error: {he}")
            QMessageBox.critical(None, "HTTP Error", str(he))
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(None, "Error", str(e))
            return None

        return None


