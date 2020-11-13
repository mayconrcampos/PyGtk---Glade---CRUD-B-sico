import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3

class DB:
    def conecta_db(self):
        self.conn = sqlite3.connect("nomes.db")
        self.cursor = self.conn.cursor()
    
    def desconecta_db(self):
        self.conn.close()
    
    def cria_db(self):
        self.conecta_db()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER NOT NULL
            );
        """)
        self.conn.commit()
        self.desconecta_db()



class Janela(DB):
    def __init__(self):
        # Chamando classe Builder para chamar a janela do arquivo glade
        arquivo = "exemplo.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(arquivo)

        # Chamando janela
        self.janela = self.builder.get_object("janela")
        self.janela.connect("delete-event", Gtk.main_quit)
        # Chamando Widgets
        self.id = self.builder.get_object("id")

        self.nome = self.builder.get_object("nome")
        self.idade = self.builder.get_object("idade")
        self.btn_add = self.builder.get_object("btn_add")
        self.btn_add.connect("clicked", self.on_btn_add_clicked)

        self.btn_update = self.builder.get_object("btn_update")
        self.btn_update.connect("clicked", self.on_btn_update_clicked)

        self.btn_delete = self.builder.get_object("btn_delete")
        self.btn_delete.connect("clicked", self.on_btn_delete_clicked)

        self.btn_limpa = self.builder.get_object("limpa")
        self.btn_limpa.connect("clicked", self.on_limpa_clicked)

        self.tview = self.builder.get_object("liststore1")

        self.seleciona = self.builder.get_object("seleciona")
        self.seleciona.connect("changed", self.item_selecionado)


        self.cria_db()
        self.tview_show()

        self.janela.show()

    def on_limpa_clicked(self, widget):
        self.id.set_text("")
        self.nome.set_text("")
        self.idade.set_text("")


    def item_selecionado(self, selecionado):
        model, row = selecionado.get_selected()
        if row:
            self.id.set_text(str(model[row][0]))
            self.nome.set_text(model[row][1])
            self.idade.set_text(str(model[row][2]))
    
    def tview_show(self):
        self.conecta_db()
        lista = self.cursor.execute("""SELECT id, nome, idade FROM dados;""")
        for linha in lista:
            self.tview.append(linha)

        self.desconecta_db()
    
    def on_btn_add_clicked(self, widget):
        nome = self.nome.get_text()
        idade = int(self.idade.get_text())
        self.conecta_db()
        self.cursor.execute("""INSERT INTO dados (nome, idade) VALUES (?,?)""",(nome, idade))
        self.conn.commit()
        self.desconecta_db()
        self.id.set_text("")
        self.nome.set_text("")
        self.idade.set_text("")
        self.tview.clear()
        self.tview_show()
    

    def on_btn_update_clicked(self, widget):
        ide = self.id.get_text()
        nome = self.nome.get_text()
        idade = self.idade.get_text()
        if ide:
            self.conecta_db()
            self.cursor.execute("""UPDATE dados SET nome=?, idade=? WHERE id=?""",(nome, idade, ide))
            self.conn.commit()
            self.desconecta_db()
#
            self.id.set_text("")
            self.nome.set_text("")
            self.idade.set_text("")
            self.tview.clear()
            self.tview_show()
    
    def on_btn_delete_clicked(self, widget):
        ide = self.id.get_text()
        if ide:
            self.conecta_db()
            self.cursor.execute("""DELETE FROM dados WHERE id=?""",(ide,))
            self.conn.commit()
            self.desconecta_db()
            self.nome.set_text("")
            self.idade.set_text("")
            self.id.set_text("")
            self.tview.clear()
            self.tview_show()
    
    
janela = Janela()
Gtk.main()