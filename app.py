# app.py
import customtkinter as ctk
from tkinter import messagebox

import produto as modulo_produto
import estoque as modulo_estoque
from produto import Produto
from estoque import Estoque

from banco import BancoDados

from aba_cadastrar import AbaCadastrar
from aba_buscar import AbaBuscar
from aba_listar import AbaListar

if "categoria" not in Produto.__init__.__code__.co_varnames:
    raise SystemExit("produto.py desatualizado (sem 'categoria').")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AppEstoque(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Estoque")
        self.geometry("950x750")

        # 1) Abre o banco e injeta no estoque
        self.bd = BancoDados("estoque.db")
        self.estoque = Estoque(bd=self.bd)

        # 2) Carrega dados persistidos
        self.bd.carregar_para_estoque(self.estoque)

        # 3) Interface
        self.abas = ctk.CTkTabview(
            self,
            segmented_button_selected_color="#A37BD6",
            segmented_button_selected_hover_color="#8358BE",
        )
        self.abas.pack(fill="both", expand=True, padx=10, pady=10)

        tab_cadastrar = self.abas.add("Cadastrar")
        tab_buscar = self.abas.add("Consultar")
        tab_listar = self.abas.add("Listar no Estoque")

        self.aba_cadastrar = AbaCadastrar(tab_cadastrar, self)
        self.aba_buscar = AbaBuscar(tab_buscar, self)
        self.aba_listar = AbaListar(tab_listar, self)

        # 4) Fechamento limpo
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    # ---------- categorias ----------
    def criar_categoria(self):
        dialogo = ctk.CTkInputDialog(
            text="Nome da nova categoria:", title="Nova categoria"
        )
        nome = dialogo.get_input()
        if not nome:
            return None
        if self.estoque.criar_categoria(nome):
            self.atualizar_categorias()
            return nome.strip()
        messagebox.showerror("Erro", "Categoria vazia ou já existe.")
        return None

    def atualizar_categorias(self):
        self.aba_cadastrar.atualizar_categoria_values(self.estoque.categorias)
        self.aba_listar.atualizar_categoria_values(self.estoque.categorias)

    # ---------- refresh ----------
    def refresh_listar(self):
        """Ponto único de sincronização após cadastrar/alterar/excluir."""
        self.aba_listar.acao_listar()

    # ---------- fechamento ----------
    def _ao_fechar(self):
        try:
            self.bd.fechar()
        finally:
            self.destroy()


if __name__ == "__main__":
    app = AppEstoque()
    app.mainloop()