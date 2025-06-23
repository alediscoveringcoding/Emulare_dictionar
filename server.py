# server.py

import socket

def start_server():
    # Adresa IP a serverului (localhost) si portul pe care asculta
    HOST = '127.0.0.1'
    PORT = 12345

    # Variabila care va tine minte dictionarul. Initial este None.
    dictionar = None

    # Cream un obiect socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Legam socket-ul de adresa si port
        s.bind((HOST, PORT))
        # Setam serverul sa asculte pentru conexiuni
        s.listen()
        print(f"Serverul a pornit si asculta pe {HOST}:{PORT}")

        # Bucla infinita pentru a accepta noi clienti
        while True:
            # Acceptam o noua conexiune. 'conn' este un nou socket pentru comunicarea cu clientul.
            conn, addr = s.accept()
            with conn:
                print(f"Client nou conectat: {addr}")

                # Bucla pentru a gestiona toate comenzile de la un client
                while True:
                    # Primim date de la client (pana la 1024 bytes)
                    try:
                        data = conn.recv(1024).decode('utf-8').strip()
                    except ConnectionResetError:
                        # Clientul a inchis conexiunea brusc
                        break

                    # Daca nu primim date, inseamna ca clientul s-a deconectat
                    if not data:
                        break

                    print(f"Clientul {addr} a trimis: {data}")

                    # Despartim comanda de argument
                    parts = data.split(' ', 1)
                    command = parts[0].lower() # Convertim comanda la litere mici
                    arg = parts[1] if len(parts) > 1 else ""
                    
                    response = ""

                    # Comanda de initializare
                    if command == 'i':
                        dictionar = {}
                        response = "OK: Dictionarul a fost initializat."
                    # Daca dictionarul nu este initializat, orice alta comanda da eroare
                    elif dictionar is None:
                        response = "EROARE: Dictionarul nu a fost initializat. Foloseste comanda 'i'."
                    # Comanda de listare (NOUA)
                    elif command == 'l':
                        if not dictionar: # Verifică dacă dicționarul este gol
                            response = "Dictionarul este gol."
                        else:
                            # Construim un string cu tot conținutul
                            response_lines = ["Continutul dictionarului:"]
                            for cuvant, definitie in dictionar.items():
                                # Afișăm un text ajutător dacă definiția este goală
                                text_definitie = definitie if definitie else "[fara definitie]"
                                response_lines.append(f"- {cuvant}: {text_definitie}")
                            
                            # Unim toate liniile într-un singur mesaj, separate de newline
                            response = "\n".join(response_lines)
                    # Comanda de adaugare cuvant
                    elif command == 'a':
                        if not arg:
                            response = "EROARE: Trebuie specificat un cuvant. Exemplu: a <cuvant>"
                        elif arg in dictionar:
                            response = f"EROARE: Cuvantul '{arg}' exista deja in dictionar."
                        else:
                            dictionar[arg] = "" # Adaugam cuvantul cu o definitie goala
                            response = f"OK: Cuvantul '{arg}' a fost adaugat."
                    # Comanda de adaugare definitie
                    elif command == 'd':
                        if not arg:
                            response = "EROARE: Trebuie specificat un cuvant. Exemplu: d <cuvant>"
                        elif arg not in dictionar:
                            response = f"EROARE: Cuvantul '{arg}' nu a fost gasit."
                        else:
                            # Trimitem un semnal clientului ca suntem gata sa primim definitia
                            conn.sendall("READY_FOR_DEF".encode('utf-8'))
                            # Primim definitia de la client
                            definitie = conn.recv(4096).decode('utf-8')
                            dictionar[arg] = definitie
                            response = f"OK: Definitia pentru '{arg}' a fost adaugata/modificata."
                    # Comanda de stergere
                    elif command == 's':
                        if not arg:
                             response = "EROARE: Trebuie specificat un cuvant. Exemplu: s <cuvant>"
                        elif arg in dictionar:
                            del dictionar[arg]
                            response = f"OK: Cuvantul '{arg}' si definitia lui au fost sterse."
                        else:
                            response = f"EROARE: Cuvantul '{arg}' nu a fost gasit."
                    # Comanda necunoscuta
                    else:
                        response = "EROARE: Comanda necunoscuta."

                    # Trimitem raspunsul inapoi la client
                    conn.sendall(response.encode('utf-8'))

                print(f"Clientul {addr} s-a deconectat.")

if __name__ == "__main__":
    start_server()