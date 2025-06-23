# client.py

import socket

def start_client():
    # Adresa si portul serverului la care ne conectam
    HOST = '127.0.0.1'
    PORT = 12345

    # Cream un socket si ne conectam la server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Conectat la serverul de dictionar. Scrie 'exit' pentru a iesi.")
            print("Comenzi disponibile:")
            print("  i                - (re)initializeaza dictionarul")
            print("  l                - listeaza tot continutul dictionarului")
            print("  a <cuvant>       - adauga un cuvant nou")
            print("  d <cuvant>       - adauga/modifica o definitie pentru un cuvant")
            print("  s <cuvant>       - sterge un cuvant")
            
        except ConnectionRefusedError:
            print("EROARE: Nu m-am putut conecta la server. Asigura-te ca server.py ruleaza.")
            return

        # Bucla pentru a trimite comenzi
        while True:
            # Citim input de la utilizator
            try:
                user_input = input("> ")
            except KeyboardInterrupt:
                # Permite inchiderea cu Ctrl+C
                break
                
            if not user_input or user_input.lower() == 'exit':
                break
            
            # Trimitem comanda la server
            try:
                s.sendall(user_input.encode('utf-8'))
            except socket.error:
                print("EROARE: Conexiunea cu serverul s-a pierdut.")
                break

            command = user_input.split(' ', 1)[0].lower()

            try:
                # Logica speciala pentru comanda 'd'
                if command == 'd':
                    # Asteptam raspunsul initial de la server
                    initial_response = s.recv(1024).decode('utf-8')
                    
                    # Daca serverul e gata pentru definitie
                    if initial_response == "READY_FOR_DEF":
                        definitie = input("Introdu definitia: ")
                        # Trimitem definitia
                        s.sendall(definitie.encode('utf-8'))
                        # Acum asteptam raspunsul final
                        final_response = s.recv(4096).decode('utf-ar 8')
                        print(f"Server: {final_response}")
                    else:
                        # Daca am primit direct o eroare (ex: cuvant inexistent)
                        print(f"Server: {initial_response}")
                else:
                    # Pentru orice alta comanda, doar asteptam raspunsul
                    response = s.recv(4096).decode('utf-8')
                    print(f"Server: {response}")
            except socket.error:
                print("EROARE: Conexiunea cu serverul s-a pierdut.")
                break


    print("\nDeconectat de la server.")

if __name__ == "__main__":
    start_client()