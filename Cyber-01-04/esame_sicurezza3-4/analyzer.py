import pandas as pd
import chardet
import re
import datetime

def analyze_logs_pandas(log_file, encoding):
    """Analisi del file di log con pandas"""

    try:
        # Lettura di un file di log (formato CSV) con pandas
        df = pd.read_csv(log_file, # percorso del file
                           sep=r'\s-\s-\s\[', # definizione del separatore di campo (esempio in24.inetnebr.com - - [ )
                           engine='python', # usa python per interpretare il regex
                           header=None, # il file non ha una riga di intestazione
                           names=['host', 'combined'], # i nomi da utilizzare per le colonne
                           usecols=['host', 'combined'], # selezione delle colonne da leggere
                           encoding=encoding) # specifica l'encoding del file
    # gestione degli errori
    except FileNotFoundError:
        print(f"Error: File '{log_file}' not found.")
        return

    except pd.errors.ParserError:
        print(f"Error: Could not parse the log file. Check the format.")
        return
    
    # split della colonna 'combined' in righe
    def split_combined(row):
        try:
            # utilizzo della funzione re.split per dividere la stringa in righe
            ts_req, req_status = row['combined'].split(']', 1) # split la stringa in due parti - richiesta timestamp e status
            req_status = req_status.strip('"') # rimuovi i caratteri di apertura e chiusura

            req_parts = req_status.rsplit('"', 1) # split la stringa in due parti
            req = req_parts[0] # prendi la prima parte - la richiesta
            status_bytes = req_parts[1] if len(req_parts) > 1 else ""  # prendi la seconda parte (eventualmente vuota se non esiste) - comprende codice di stato HTTP e dimensione bytes

            parts = status_bytes.split() # split la stringa in righe
            status = parts[0] if parts else None # prendi la prima riga (eventualmente vuota se non esiste) - codice di stato HTTP
            bytes_sent = parts[-1] if parts and len(parts) > 1 else None  # prendi l'ultima riga (eventualmente vuota se non esiste) - dimensione bytes

            return pd.Series([ts_req, req, status, bytes_sent]) # restituisce una serie con le informazioni estratte altrimenti None
        except (ValueError, IndexError):
            return pd.Series([None, None, None, None])

    # applicazione della funzione di split alla colonna 'combined'
    df[['timestamp_request', 'request', 'status', 'bytes_sent']] = df.apply(split_combined, axis=1)
    df.drop(columns=['combined'], inplace=True) # toglie colonna combined

    # Conversione della colonna 'timestamp_request' in formato datetime
    df['timestamp'] = pd.to_datetime(df['timestamp_request'], format="%d/%b/%Y:%H:%M:%S %z", errors='coerce')
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)  # Rimuove la Timezone
    df.drop(columns=['timestamp_request'], inplace=True) # toglie colonna timestamp_request

    # Prende metodo e path della richiesta
    df['method'] = df['request'].str.split().str[0]
    df['method'] = df['method'].str.replace('"', '', regex=False)
    df['path'] = df['request'].str.split().str[1]

    # Converte le colonne status e bytes_sent in numerici
    df['status'] = pd.to_numeric(df['status'].str.strip(), errors='coerce').astype('Int64')
    df['bytes_sent'] = df['bytes_sent'].str.strip()  # Rimuove lo whitespace
    df['bytes_sent'] = pd.to_numeric(df['bytes_sent'], errors='coerce').astype('Int64')

    # Toglie colonna request
    df.drop(columns=['request'], inplace=True)
    
    # Vari print per controllare i dati
    #print("--- Request Counts per Host ---")
    #print(df['host'].value_counts().head(10))

    #print("\n--- Top 10 Requested Paths ---")
    #print(df['path'].value_counts().head(10))

    #print("\n--- Bytes Sent per Host ---")
    #print(df.groupby('host')['bytes_sent'].sum().nlargest(10))

    #print("\n--- Hourly Traffic ---")
    df['hour'] = df['timestamp'].dt.strftime('%Y-%m-%d %H')  # Crea colonna con l'ora della richiesta
    #print(df['hour'].value_counts())

    #print("\n--- Status Code Distribution ---")
    #print(df['status'].value_counts())

   # print("\n--- Error Requests (Status Codes 4xx and 5xx) ---")
   # error_requests = df[df['status'].between(400, 599)].copy()  # Crea una copia

   # if not error_requests.empty:
   #     error_requests = error_requests.drop(columns=['bytes_sent']) # Toglie colonna di bytes sent per errori
   #     error_requests.index = error_requests.index + 1  # Aggiusta l'index offset per la stampa
   #     print(error_requests.head(10))
   # else:
   #     print("No error requests found.")

    time = str(datetime.datetime.now())
    report_file = "report_"+time+".log" # Nome del file di report
    with open(report_file, "w") as f:  # Apre il file in scrittura
        def write_section(title, content):  # Funzione per scrivere sezioni del report
            f.write(f"{title}\n")
            f.write(f"{content}\n\n")

        write_section("--- Request Counts per Host ---", df['host'].value_counts().head(10).to_string())
        write_section("\n--- Requested Paths ---", df['path'].value_counts().head(10).to_string())
        write_section("\n--- Bytes Sent per Host ---", df.groupby('host')['bytes_sent'].head(10).sum().to_string())
        write_section("\n--- Average Bytes Sent per Host ---", df.groupby('host')['bytes_sent'].head(10).mean().to_string())
        write_section("\n--- Hourly Traffic ---", df['hour'].value_counts().head(10).to_string())
        write_section("\n--- Status Code Distribution ---", df['status'].value_counts().to_string())

        error_requests = df[df['status'].between(400, 599)].copy()
        if not error_requests.empty:
            error_requests = error_requests.drop(columns=['bytes_sent'])
            error_requests.index = error_requests.index + 1
            write_section("\n--- Error Requests (Status Codes 4xx and 5xx) ---", error_requests.to_string())
        else:
            f.write("\n--- Error Requests (Status Codes 4xx and 5xx) ---\n")
            f.write("No error requests found.\n\n")

        #Aggiunta delle attività sospette
        f.write("\n--- Suspicious Activity Analysis ---\n")

        # 1. Molti errori da uno stesso IP:
        high_error_hosts = df[df['status'].between(400, 599)].groupby('host')['status'].count() / df.groupby('host')['status'].count() * 100
        high_error_hosts = high_error_hosts[high_error_hosts > 10] # Il 10% delle richieste è un errore.
        if not high_error_hosts.empty:
            f.write("Hosts with high error rates ( > 10%):\n")
            f.write(high_error_hosts.to_string() + "\n\n")
        else:
            f.write("No hosts with high error rates detected.\n\n")

        # 2. Pattern di richieste fuori dalla norma (esempi: URL molto lunghi, caratteri inusuali):
        unusual_requests = df[df['path'].str.len() > 100]  # URL più lunghi di 100 caratteri.
        if not unusual_requests.empty:
            f.write("Unusual request patterns (long URLs):\n")
            f.write(unusual_requests[['host', 'timestamp', 'method', 'path', 'status']].to_string() + "\n\n")
        else:
            f.write("No unusual request patterns detected.\n\n")

        # 3. Un numero alto di richieste da un singolo IP in breve tempo:
        df['time_interval'] = df['timestamp'].dt.floor('1min')  # Raggruppato in minuti
        high_request_ips = df.groupby(['host', 'time_interval'])['path'].count()
        high_request_ips = high_request_ips[high_request_ips > 20] #Esempio: Più di 20 richieste al minuto
        if not high_request_ips.empty:
            f.write("IPs with high request rates in short time intervals:\n")
            f.write(high_request_ips.to_string() + "\n\n")
        else:
            f.write("No IPs with high request rates detected.\n\n")
        
        # 4. Metodi HTTP diversi dalla norma (esempio: PUT, DELETE)
        unusual_methods = df[~df['method'].isin(['GET', 'POST'])] # Toglie dalla ricerca i metodi GET e POST
        if not unusual_methods.empty:
            f.write("Unusual HTTP Methods detected:\n")
            f.write(unusual_methods[['host', 'timestamp', 'method', 'path']].to_string() + "\n\n")
        else:
            f.write("No unusual HTTP Methods detected.\n\n")
        
        f.write(f"\n\nThis is a report made on {log_file}")
        
        print(f"\n\nReport written to {report_file}")


def main():
    log_file_path = "NASA_access_log_Aug95.log"
    encoding = ""
    with open(log_file_path, 'rb') as f:
        #Trova il giusto encoding
        encoding = chardet.detect(f.read())['encoding']


    analyze_logs_pandas(log_file_path, encoding)

if __name__ == "__main__":
    main()