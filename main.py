import flet as ft
from flet import app, TextField
from flet.controls import alignment

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    myText = ft.Text(value="Aggiungi Nuovo Strumento",
                     size = 28,
                     weight = ft.FontWeight.BOLD
                     )


    input_tipo_txt = ft.TextField(label= "tipo strumento" ,
                                  width=400  )
    input_marca_txt = ft.TextField(label = "marca strumento",
                                   width = 400)
    input_anno_txt = ft.TextField(label = "anno acquisto",
                                  keyboard_type=ft.KeyboardType.NUMBER,
                                  width = 400)
    input_prezzo_txt = ft.TextField(label = "prezzo",
                                    value = "0",
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                    width=400)
    def diminuisci_prezzo(e):
                try:
                    valore_attuale = float(input_prezzo_txt.value)
                    if valore_attuale > 0:
                        input_prezzo_txt.value = str(valore_attuale - 1)
                        page.update()
                except ValueError:
                    pass
    def aumenta_prezzo(e):
            try:
                valore_attuale = float(input_prezzo_txt.value)
                input_prezzo_txt.value = str(valore_attuale + 1)
                page.update()
                page.update()
            except ValueError:
                pass
    contatore_prezzo = ft.Row(controls = [ft.IconButton(ft.Icons.REMOVE, on_click = diminuisci_prezzo),
                                              input_prezzo_txt,
                                              ft.IconButton(ft.Icons.ADD, on_click = aumenta_prezzo)],
                                  alignment = ft.MainAxisAlignment.CENTER
                                  )

    # --- FUNZIONI APP ---



    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    my_button_responsabile = ft.Button()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    def aggiungi_nuovo_strumento(e):
        tipo = input_tipo_txt.value
        marca = input_marca_txt.value
        anno = input_anno_txt.value
        prezzo = input_prezzo_txt.value

        if tipo and marca and anno and prezzo:
            try:

                anno_int = int(anno)
                prezzo_float = float(prezzo)

                deposito.aggiungi_strumento(tipo, marca, anno_int, prezzo_float)


                input_tipo_txt.value = ""
                input_marca_txt.value = ""
                input_anno_txt.value = ""
                input_prezzo_txt.value = "0"

                aggiorna_lista_strumenti()
            except ValueError:
                alert.show_alert("❌ Anno e prezzo devono essere valori numerici!")
        else:
            alert.show_alert("❌ Compila tutti i campi dello strumento!")
        page.update()

    pulsante_aggiungi_strumento = ft.Button("Salva Strumento", on_click=aggiungi_nuovo_strumento)

    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"

            # Formattazione della riga della lista
            riga = ft.Text(f"{stato} {strumento.codice}: {strumento.tipo} {strumento.marca} - {strumento.valore}€")
            lista_strumenti.controls.append(riga)

        page.update()

     #--- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=20,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Column(
            controls=[
                myText,
                input_tipo_txt,
                input_marca_txt,
                input_anno_txt,
                ft.Text("Prezzo (Euro):"),
                contatore_prezzo,
                pulsante_aggiungi_strumento
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.run(main)