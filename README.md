# Emulare_dictionar

Cerință: Aplicație Client-Server - Dicționar
Să se realizeze o aplicație client-server care simulează funcționalitatea unui dicționar.

Specificații generale:

Dicționarul: Aplicația va gestiona o colecție de cuvinte, unde fiecare cuvânt are asociată o singură definiție.
Inițializare: Dicționarul trebuie inițializat explicit de către client înainte ca orice altă operație să poată fi executată. Se va semnala o eroare dacă se încearcă o operație (ex: adăugare, ștergere) pe un dicționar neinițializat.
Operații:
Adăugare cuvânt: Clientul poate adăuga un cuvânt nou în dicționar.
Adăugare/Modificare definiție: Pentru un cuvânt existent, se poate adăuga sau înlocui definiția. O definiție nu poate fi ștearsă separat, ci doar înlocuită (este permisă și o definiție vidă/goală).
Ștergere cuvânt: Un cuvânt poate fi șters din dicționar împreună cu definiția sa.
Server: Serverul implementat va fi de tip iterativ.
Comenzi disponibile clientului:

i - (Re)inițializează dicționarul. Orice conținut existent este șters, iar dicționarul devine gol și pregătit pentru operații.
a|A <cuvant> - Adaugă un cuvânt nou (<cuvant>) în dicționar, inițial fără definiție.
d <cuvant> - Definește sau modifică definiția pentru cuvântul <cuvant>. Clientul va fi solicitat să introducă noua definiție.
s <cuvant> - Șterge cuvântul <cuvant> împreună cu definiția sa din dicționar.
l - Listează toate cuvintele din dicționar împreună cu definițiile lor, într-un format clar.