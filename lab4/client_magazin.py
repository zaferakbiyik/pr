import requests
import json
import os
import urllib3

# Dezactivăm avertismentele SSL pentru dezvoltare
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ClientMagazin:
    def __init__(self, base_url="https://localhost:5001"):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
        self.timeout = 10
    
    def _trimite_cerere(self, metoda, endpoint, date=None):
        url = f"{self.base_url}{endpoint}"
        
        # Pentru debugging
        print(f"Trimitere cerere {metoda} către {url}")
        if date:
            print(f"Date: {json.dumps(date)}")
        
        try:
            if metoda == "GET":
                response = requests.get(url, headers=self.headers, verify=False, timeout=self.timeout)
            elif metoda == "POST":
                response = requests.post(url, headers=self.headers, json=date, verify=False, timeout=self.timeout)
            elif metoda == "PUT":
                response = requests.put(url, headers=self.headers, json=date, verify=False, timeout=self.timeout)
            elif metoda == "DELETE":
                response = requests.delete(url, headers=self.headers, verify=False, timeout=self.timeout)
            else:
                raise ValueError(f"Metodă HTTP nesuportată: {metoda}")
            
            # Pentru debugging
            print(f"Status: {response.status_code}")
            
            if response.status_code in [200, 201, 204]:
                if response.text:
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        return response.text
                return True
            else:
                print(f"Eroare: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Eroare de conectare: {e}")
            return None
    
    def lista_categorii(self):
        """Obține lista tuturor categoriilor"""
        result = self._trimite_cerere("GET", "/api/Category/categories")
        print("Răspuns brut categorii:", json.dumps(result, indent=2))
        return result
    
    def detalii_categorie(self, id_categorie):
        """Obține detaliile unei categorii specifice"""
        result = self._trimite_cerere("GET", f"/api/Category/categories/{id_categorie}")
        print("Răspuns brut detalii categorie:", json.dumps(result, indent=2))
        return result
    
    def creeaza_categorie(self, titlu, descriere=""):
        """Creează o categorie nouă"""
        date = {"title": titlu, "description": descriere}
        return self._trimite_cerere("POST", "/api/Category/categories", date)
    
    def sterge_categorie(self, id_categorie):
        """Șterge o categorie existentă"""
        return self._trimite_cerere("DELETE", f"/api/Category/categories/{id_categorie}")
    
    def actualizeaza_categorie(self, id_categorie, titlu_nou):
        """Actualizează titlul unei categorii"""
        date = {"title": titlu_nou}
        return self._trimite_cerere("PUT", f"/api/Category/{id_categorie}", date)
    
    def lista_produse(self, id_categorie):
        """Obține lista produselor dintr-o categorie"""
        result = self._trimite_cerere("GET", f"/api/Category/categories/{id_categorie}/products")
        print("Răspuns brut produse:", json.dumps(result, indent=2))
        return result
    
    def adauga_produs(self, id_categorie, nume, descriere, pret, stoc):
        """Adaugă un produs nou într-o categorie"""
        # Din schema Swagger, vedem că ProductShortDto are title, nu name
        # și are price, categoryId
        date = {
            "title": nume,
            "description": descriere,
            "price": pret,
            "stock": stoc,
            "categoryId": int(id_categorie)
        }
        return self._trimite_cerere("POST", f"/api/Category/categories/{id_categorie}/products", date)

def curata_ecran():
    """Curăță ecranul consolei"""
    os.system('cls' if os.name == 'nt' else 'clear')

def afiseaza_meniu():
    """Afișează meniul principal"""
    print("\n===== CLIENT MAGAZIN UTM =====")
    print("1. Lista categorii")
    print("2. Detalii categorie")
    print("3. Creează categorie nouă")
    print("4. Șterge categorie")
    print("5. Actualizează titlu categorie")
    print("6. Lista produse din categorie")
    print("7. Adaugă produs nou")
    print("0. Ieșire")
    print("=============================")

def main():
    client = ClientMagazin()
    print("Inițializare client magazin...")
    
    while True:
        afiseaza_meniu()
        optiune = input("Selectați o opțiune: ")
        
        if optiune == "1":
            # Lista categorii
            curata_ecran()
            print("\n===== LISTA CATEGORII =====")
            categorii = client.lista_categorii()
            if categorii:
                # Verificăm dacă categorii este o listă (array)
                if isinstance(categorii, list):
                    for cat in categorii:
                        # Verificăm dacă fiecare element este un dicționar
                        if isinstance(cat, dict):
                            # Afișează toate cheile disponibile pentru debugging
                            if cat.get('id') is not None:
                                # Încercăm mai multe variante de nume pentru câmpul de titlu
                                titlu = cat.get('title') or cat.get('Title') or cat.get('name') or cat.get('Name') or "Fără titlu"
                                print(f"ID: {cat.get('id')} - Titlu: {titlu}")
                            else:
                                print(f"Categorie: {cat}")
                else:
                    print("Format neașteptat pentru categorii:", categorii)
            else:
                print("Nu există categorii sau a apărut o eroare.")
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "2":
            # Detalii categorie
            curata_ecran()
            id_cat = input("Introduceți ID-ul categoriei: ")
            categorie = client.detalii_categorie(id_cat)
            if categorie:
                print(f"\n===== DETALII CATEGORIE =====")
                # Verificăm dacă categorie este un dicționar
                if isinstance(categorie, dict):
                    print(f"ID: {categorie.get('id')}")
                    titlu = categorie.get('title') or categorie.get('Title') or categorie.get('name') or categorie.get('Name') or "Fără titlu"
                    print(f"Titlu: {titlu}")
                    descriere = categorie.get('description') or categorie.get('Description') or "Fără descriere"
                    print(f"Descriere: {descriere}")
                else:
                    print("Format neașteptat pentru categorie:", categorie)
            else:
                print(f"Nu s-a putut găsi categoria cu ID-ul {id_cat}.")
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "3":
            # Creează categorie
            curata_ecran()
            titlu = input("Introduceți titlul categoriei: ")
            descriere = input("Introduceți descrierea (opțional): ")
            rezultat = client.creeaza_categorie(titlu, descriere)
            if rezultat:
                print(f"\nCategoria a fost creată cu succes!")
                if isinstance(rezultat, dict):
                    print(f"ID: {rezultat.get('id', 'Necunoscut')}")
            else:
                print("\nNu s-a putut crea categoria.")
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "4":
            # Șterge categorie
            curata_ecran()
            id_cat = input("Introduceți ID-ul categoriei de șters: ")
            confirmare = input(f"Sigur doriți să ștergeți categoria {id_cat}? (d/n): ")
            if confirmare.lower() == "d":
                if client.sterge_categorie(id_cat):
                    print(f"\nCategoria {id_cat} a fost ștearsă cu succes!")
                else:
                    print(f"\nNu s-a putut șterge categoria {id_cat}.")
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "5":
            # Actualizează categorie
            curata_ecran()
            id_cat = input("Introduceți ID-ul categoriei: ")
            titlu_nou = input("Introduceți noul titlu: ")
            rezultat = client.actualizeaza_categorie(id_cat, titlu_nou)
            if rezultat:
                print(f"\nTitlul categoriei a fost actualizat cu succes!")
            else:
                print(f"\nNu s-a putut actualiza categoria {id_cat}.")
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "6":
            # Lista produse
            curata_ecran()
            id_cat = input("Introduceți ID-ul categoriei: ")
            produse = client.lista_produse(id_cat)
            if produse:
                print(f"\n===== PRODUSE DIN CATEGORIA {id_cat} =====")
                if isinstance(produse, list):
                    for produs in produse:
                        if isinstance(produs, dict):
                            # Verificăm ambele variante: title și name
                            nume = produs.get('title') or produs.get('Title') or produs.get('name') or produs.get('Name') or "Fără nume"
                            pret = produs.get('price') or produs.get('Price') or 0
                            stoc = produs.get('stock') or produs.get('Stock') or 0
                            print(f"ID: {produs.get('id')} - Nume: {nume} - Preț: {pret} - Stoc: {stoc}")
                else:
                    print("Format neașteptat pentru produse:", produse)
            else:
                print(f"\nNu există produse în această categorie sau a apărut o eroare.")
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "7":
            # Adaugă produs
            curata_ecran()
            id_cat = input("Introduceți ID-ul categoriei: ")
            nume = input("Introduceți numele produsului: ")
            descriere = input("Introduceți descrierea produsului: ")
            
            try:
                pret = float(input("Introduceți prețul produsului: "))
                stoc = int(input("Introduceți stocul disponibil: "))
                
                rezultat = client.adauga_produs(id_cat, nume, descriere, pret, stoc)
                if rezultat:
                    print(f"\nProdusul a fost adăugat cu succes!")
                    print("Răspuns adăugare produs:", json.dumps(rezultat, indent=2))
                else:
                    print(f"\nNu s-a putut adăuga produsul.")
            except ValueError:
                print("\nEroare: Prețul și stocul trebuie să fie numere.")
            
            input("\nApăsați ENTER pentru a continua...")
        
        elif optiune == "0":
            # Ieșire
            print("La revedere!")
            break
        
        else:
            print("Opțiune invalidă!")

if __name__ == "__main__":
    main()
