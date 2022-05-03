from tkinter import *
from tkinter import ttk
import sqlite3 as lite
from tkinter import messagebox


# Cores

cor0 = "#000000"  # preta
cor1 = "#59656F"
cor2 = "#feffff"  # branca
cor3 = "#0074eb"  # azul
cor4 = "#f04141"  # vermelho
cor5 = "#59b356"  # verde
cor6 = "#cdd1cd"  # cizenta


janela = Tk()
janela.title('To-do App')
# janela.geometry('500x225')
janela.configure(bg=cor1)
janela.resizable(width=FALSE, height=FALSE)
janela.iconbitmap('to-do.ico')  # icon do app


style = ttk.Style(janela)
style.theme_use('clam')

# * CRIANDO BANCO DE DADOS COM SUAS FUNÇÕESD DE: (ADICIONAR, ATUALIZAR E DELETAR)

con = lite.connect('to_do.db')

# Criou o BD

"""
with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE Tarefa(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')
"""

# Inserindo informações no bd


def inserir(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Tarefa(nome) VALUES(?)"
        cur.execute(query, i)


def selecionar():
    lista_tarefa = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Tarefa")
        row = cur.fetchall()

        for r in row:
            lista_tarefa.append(r)
    return lista_tarefa


def deletar(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Tarefa WHERE id=?"
        cur.execute(query, i)


def atualizar(i):
    with con:
        cur = con.cursor()
        query = "UPDATE Tarefa SET nome=? WHERE id=?"
        cur.execute(query, i)

# Dividindo a janela em 2 frames


frame_esquerda = Frame(janela, width=300, height=200, bg=cor2, relief='flat')
frame_esquerda.grid(row=0, column=0, sticky=NSEW)

frame_direita = Frame(janela, width=200, height=250,
                      bg='#48337d', relief='flat')
frame_direita.grid(row=0, column=1, sticky=NSEW)


# Dividindo o frame esquerda em 2 partes

frame_cima = Frame(frame_esquerda, width=300,
                   height=50, bg=cor2, relief='flat')
frame_cima.grid(row=0, column=0, sticky=NSEW)

frame_baixo = Frame(frame_esquerda, width=300,
                    height=150, bg=cor2, relief='flat')
frame_baixo.grid(row=1, column=0, sticky=NSEW)


def main(a):
    # novo
    if a == 'novo':

        for widget in frame_baixo.winfo_children():
            widget.destroy()

        def adicionar():
            tarefa_entry = entry.get()
            inserir([tarefa_entry])
            entry.delete(0, END)
            mostrar()

        label_b = Label(frame_baixo, text='Insira nova tarefa',
                        width=42, height=5, pady=15, anchor=CENTER)
        label_b.grid(row=0, column=0, sticky=NSEW)

        entry = Entry(frame_baixo, width=15)
        entry.grid(row=1, column=0, sticky=NSEW)
        # entry.delete(0, END)
        botao_adicionar = Button(frame_baixo, command=adicionar, text='Adicionar', width=9, height=1,
                                 bg='#48337d', fg='white', font='8', anchor='center', relief='raised', overrelief='ridge', pady=10)
        botao_adicionar.grid(row=2, column=0, sticky=NSEW, pady=15)
        
    try:
        # atualizar
        if a == 'atualizar':

            for widget in frame_baixo.winfo_children():
                widget.destroy()

            def on():

                label_b = Label(frame_baixo, text='Atualizar tarefa',
                                width=42, height=5, pady=15, anchor=CENTER)
                label_b.grid(row=0, column=0, sticky=NSEW)

                entry = Entry(frame_baixo, width=15)
                entry.grid(row=1, column=0, sticky=NSEW)

                valor_selecionado = listbox.curselection()[0]
                palavra = listbox.get(valor_selecionado)
                entry.insert(0, palavra)

                tarefas = selecionar()

                def alterar():
                    for item in tarefas:
                        if palavra == item[1]:
                            nova = [entry.get(), item[0]]
                            atualizar(nova)
                            entry.delete(0, END)
                    mostrar()

                botao_alterar = Button(frame_baixo, command=alterar, text='Atualizar', width=9, height=1, bg='#48337d',
                                       fg='white', font='8', anchor='center', relief='raised', overrelief='ridge', pady=10)
                botao_alterar.grid(row=2, column=0, sticky=NSEW, pady=15)

            on()
    except IndexError:
        messagebox.showwarning(
            'Atenção!', 'Selecione um dos dados da tabela para poder atualizar')

# funcao remover


def remover():
    try:
        valor_selecionado = listbox.curselection()[0]
        palavra = listbox.get(valor_selecionado)
        tarefas = selecionar()

        for item in tarefas:
            if palavra == item[1]:
                deletar([item[0]])
        mostrar()
    except IndexError:
        messagebox.showerror(
            'Erro!', 'Selecione um dos dados da tabela para poder Deletar')


# Criando botoes do frame cima

botao_novo = Button(frame_cima, command=lambda: main('novo'), text='Novo', width=10, height=1,
                    bg=cor3, fg='white', font='5', anchor='center', relief='raised', overrelief='ridge')
botao_novo.grid(row=0, column=0, sticky=NSEW, pady=1)

botao_remover = Button(frame_cima, command=remover, text='Remover', width=10, height=1,
                       bg=cor4, fg='white', font='5', anchor='center', relief='raised', overrelief='ridge')
botao_remover.grid(row=0, column=1, sticky=NSEW, pady=1)

botao_atualizar = Button(frame_cima, command=lambda: main('atualizar'), text='Atualizar', width=10,
                         height=1, bg=cor5, fg='white', font='5', anchor='center', relief='raised', overrelief='ridge')
botao_atualizar.grid(row=0, column=2, sticky=NSEW, pady=1)


# Adicionando a Label e a Listbox em baixo

label = Label(frame_direita, text='Tarefas', width=37, height=1, pady=7, padx=225,
              relief='flat', anchor=W, font=('System 20'), fg='#48337d', bg='#d9d9d9')
label.grid(row=0, column=0, sticky=NSEW, pady=1)


listbox = Listbox(frame_direita, font=('Verdana 10 bold'), width=1)
listbox.grid(row=1, column=0, sticky=NSEW, pady=5)


# Adicionando tarefas na listbox

def mostrar():

    listbox.delete(0, END)

    tarefas = selecionar()

    for item in tarefas:
        listbox.insert(END, item[1])


mostrar()


# * Centralizando o arquivo

# Dimensoes da janela
largura = 870
altura = 227

# Resolução do nosso sistema
largura_screen = janela.winfo_screenwidth()
altura_screen = janela.winfo_screenwidth()
# print(largura_screen, altura_screen)  # para saber as dimensoes do monitor


# Posição da janela
posx = largura_screen/2 - largura/1.8
posy = altura_screen/5 - altura/5

# Definir a geometria
janela.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))


janela.mainloop()
