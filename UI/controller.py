import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_airportA = None
        self._selected_airportP = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handelAnalizza(self, e):
        self._view._txt_result.controls.clear()
        d = self._view._txtInNumC.value
        if d is None or d == '':
            self._view._txt_result.controls.append(ft.Text("Inserisci una soglia minima!", color='red'))
            self._view.update_page()
            return
        try:
            d = int(d)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserisci una soglia in formato numerico!", color='red'))
            self._view.update_page()
            return
        flag = self._model.buildGraph(d)
        if flag:
            self._view._txt_result.controls.append(ft.Text(self._model.getGraphDetails()))
            #gestsici il dropdown
            self._view._ddAeroportoP.options.clear()
            nodi = self._model.get_nodes()
            for n in nodi:
                self._view._ddAeroportoP.options.append(
                    ft.dropdown.Option(text=n.AIRPORT, data=n, on_click=self.readDDAirportP))
                self._view._ddAeroportoA.options.append(
                    ft.dropdown.Option(text=n.AIRPORT, data=n, on_click=self.readDDAirportA))
            self._view._btnConnessi.disabled = False
            self._view.update_page()
            return
        else:
            self._view._txt_result.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
            self._view.update_page()
            return

    def handleConnessi(self, e):
        self._view._txt_result.controls.clear()
        if self._selected_airportP is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un aeroporto!", color='red'))
            self._view.update_page()
            return
        if len(self._model.graph.nodes) == 0:
            self._view._txt_result.controls.append(ft.Text("Crea un grafo!", color='red'))
            self._view.update_page()
            return
        result = self._model.connessi(self._selected_airportP)
        if len(result) > 0:
            for r in result:
                self._view._txt_result.controls.append(ft.Text(f"{r[0]} --> {r[1]}"))
            self._view._btnPercorso.disabled = False
            self._view._btnCercaItinerario.disabled = False
            self._view.update_page()
            return

    def handleTestConnessione(self, e):
        pass

    def handleCercaItinerario(self, e):
        self._view._txt_result.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_airportP is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare un aeroporto di partenza!", color='red'))
            self._view.update_page()
            return
        if self._selected_airportA is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare un aeroporto di arrivo!", color='red'))
            self._view.update_page()
            return
        d = self._view._txtInNumTratte.value
        if d is None or d == '':
            self._view._txt_result.controls.append(ft.Text("Inserire una soglia massima!", color='red'))
            self._view.update_page()
            return
        try:
            d = int(d)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserisci una soglia in formato numerico!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(d+1, self._selected_airportP, self._selected_airportA)
        if componenti:
            self._view._txt_result.controls.append(ft.Text(f"Numero totale di voli: {self._model._bestLen}"))
            for c in componenti:
                self._view._txt_result.controls.append(ft.Text(f"{c}"))
            self._view.update_page()
            return
        else:
            self._view._txt_result.controls.append(ft.Text("Nessun percorso trovato!", color='red'))
            self._view.update_page()
            return

    def readDDAirportP(self, e):
        if e.control.data is None:
            self._selected_airportP = None
        else:
            self._selected_airportP = e.control.data
    
    def readDDAirportA(self, e):
        if e.control.data is None:
            self._selected_airportA = None
        else:
            self._selected_airportA = e.control.data


