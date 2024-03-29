from tkinter import *
from tkinter import ttk
import sqlite3



root = Tk()

class Funcoes():
    def limpa_tela(self):
        self.entry_codigo.delete(0,END)
        self.entry_material.delete(0,END)
        self.entry_quantidade.delete(0,END)
        self.entry_tipo.delete(0,END)
        self.entry_data.delete(0,END)

    def conecta_bd(self):
        self.conn = sqlite3.connect('estoque.bd')
        self.cursor = self.conn.cursor()

        print('Conectado ao Banco Estoque')
    
    def desconecta_bd(self):
        self.conn.close()

    def monta_tabelas(self):
        self.conecta_bd()
        print('Banco Desconectado')

    # Criar Tabelas
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS cordeirinho (
                                codigo INTEGER PRIMARY KEY,
                                material VARCHAR(100) NOT NULL,
                                quantidade INTEGER NOT NULL,
                                tipo VARCHAR(30),
                                data DATA
                                )
                            """)

        self.conn.commit(); print('Tabela cordeirinho Criada')
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.entry_codigo.get()
        self.material = self.entry_material.get()
        self.quantidade = self.entry_quantidade.get()
        self.tipo = self.entry_tipo.get()
        self.data = self.entry_data.get()

    def add_material(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""
                            INSERT INTO cordeirinho(codigo,material,quantidade,tipo,data)
                            VALUES (?,?,?,?,?)""",(self.codigo,self.material,self.quantidade,self.tipo,self.data))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.lista_material.delete(*self.lista_material.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
                                SELECT codigo, material,quantidade,tipo,data 
                                FROM cordeirinho 
                                ORDER BY material ASC""")
        for i in lista:
            self.lista_material.insert('','end', values=i)


        self.lista_total.delete(*self.lista_total.get_children())
        lista = self.cursor.execute("""
                                        SELECT codigo,material,quantidade 
                                        FROM cordeirinho 
                                        ORDER BY material ASC""")
        for i in lista:
            self.lista_total.insert('', 'end', values=i)

        self.desconecta_bd()

    def OnDoubleClick(self,event):
        self.limpa_tela()
        self.lista_material.selection()
        
        for n in self.lista_material.selection():
            col1,col2,col3,col4,col5 = self.lista_material.item(n, 'values')
            
            self.entry_codigo.insert(END,col1)
            self.entry_material.insert(END,col2)
            self.entry_quantidade.insert(END,col3)
            self.entry_tipo.insert(END,col4)
            self.entry_data.insert(END,col5)

        self.lista_total.selection()
        for n in self.lista_total.selection():
            col1, col2,col3 = self.lista_total.item(n, 'values')

            self.entry_codigo.insert(END,col1)
            self.entry_material.insert(END, col2)
            self.entry_quantidade.insert(END, col3)

    def deleta_material(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""
                                DELETE FROM cordeirinho WHERE codigo = ? """,(self.codigo,))
        self.conn.commit()   
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def alterar(self):
        self.variaveis()
        self.conecta_bd()


        self.cursor.execute("""
                            UPDATE cordeirinho SET material=?, quantidade=?, tipo=?, data =? 
                            WHERE codigo = ? """,(self.material,self.quantidade,self.tipo,self.data,self.codigo))

        
        self.conn.commit()
        
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela() 
        
    def entrada_estoque(self):
        self.variaveis()
        self.conecta_bd()
        self.lista_total.delete(*self.lista_total.get_children())

        self.entry_material.insert('end','%')
        nome = self.entry_material.get()


        self.cursor.execute("""
                                SELECT SUM(quantidade),material
                                FROM cordeirinho
                                WHERE material
                                LIKE '%s' ORDER BY material ASC""" % nome )
        busca = self.cursor.fetchall();print(busca)

        for i in busca:
            self.lista_total.insert('',END,values=i)
        self.limpa_tela()

        self.desconecta_bd()

    def saida_estoque(self):
        self.variaveis()
        self.conecta_bd()
        self.lista_total.delete(*self.lista_total.get_children())

        self.entry_material.insert('end', '%')
        nome = self.entry_material.get()
        self.cursor.execute("""
                                        SELECT SUM(quantidade),material
                                        FROM cordeirinho
                                        WHERE material
                                        LIKE '%s' ORDER BY material ASC""" % nome)
        busca = self.cursor.fetchall() ;print(busca) #completo

        total = busca[0]; print(total) #tupla

        lista_atual = list(total); print(lista_atual) #lista

        lista2 = lista_atual[0]; print(lista2) # primeiro valor da lista

        lista3 = int(lista2) - int(self.quantidade); print(lista3) # redução do valor

        lista_atual.insert(1,lista3); print(lista_atual)

        for i in busca:
            self.lista_total.insert('', END, values=i)
        self.limpa_tela()

        self.desconecta_bd()




class Application(Funcoes):
    def __init__(self,master=None):
        self.root = root
        self.tela()
        self.frames()
        self.widgts()
        self.lista_frame3()
        self.lista_frame2()
        self.monta_tabelas()
        self.select_lista()


        root.mainloop()

    def tela(self):
        self.root.title('Controle material')
        self.root.geometry('900x700+10+10')
        self.root.configure(background='gray')
        self.root.minsize(width=400,height=300)

    def frames(self):
        self.frame_1 = Frame(self.root,bd= 4,highlightbackground='black',highlightthickness=2,bg='red')
        self.frame_1.place(relx=0.01,rely=0.01,relwidth=0.98,relheight=0.15)

        self.frame_2 = Frame(self.root, bd= 4,highlightbackground='black',highlightthickness=2,bg='blue')
        self.frame_2.place(relx=0.01, rely=0.17, relwidth=0.98, relheight=0.42)

        self.frame_3 = Frame(self.root, bd= 4,highlightbackground='black',highlightthickness=2 ,bg='green')
        self.frame_3.place(relx=0.01, rely=0.60, relwidth=0.98, relheight=0.39)

    def widgts(self):
    # Titulo
        self.label_titulo = Label(self.frame_1, text='estoque - cordeirinho'.upper(), font='verdana 40 bold')
        self.label_titulo.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
    # ID
        self.label_cod = Label(self.frame_2, text='cod'.upper(),font='verdana 10 bold')
        self.label_cod.place(relx=0.07, rely=0.05, relwidth=0.04, relheight=0.08)

        self.entry_codigo = Entry(self.frame_2, font='verdana 10 bold')
        self.entry_codigo.place(relx=0.12, rely=0.05, relwidth=0.10, relheight=0.08)
    # Data
        self.label_data = Label(self.frame_2, text='data'.upper(), font='verdana 10 bold')
        self.label_data.place(relx=0.30, rely=0.05, relwidth=0.05, relheight=0.08)

        self.entry_data = Entry(self.frame_2, font='verdana 10 bold')
        self.entry_data.place(relx=0.36, rely=0.05, relwidth=0.12, relheight=0.08)
    # Material
        self.label_material = Label(self.frame_2, text='material'.upper(), font='verdana 10 bold')
        self.label_material.place(relx=0.01, rely=0.17, relwidth=0.10, relheight=0.08)

        self.entry_material = Entry(self.frame_2, font='verdana 10 bold')
        self.entry_material.place(relx=0.12, rely=0.17, relwidth=0.36, relheight=0.08)
    # Quantidade
        self.label_quantidade = Label(self.frame_2, text='quantidade'.upper(), font='verdana 8 bold')
        self.label_quantidade.place(relx=0.01, rely=0.29, relwidth=0.10, relheight=0.08)

        self.entry_quantidade = Entry(self.frame_2, font='verdana 10 bold')
        self.entry_quantidade.place(relx=0.12, rely=0.29, relwidth=0.10, relheight=0.08)

    # Tipo
        self.label_tipo = Label(self.frame_2, text='tipo'.upper(), font='verdana 10 bold')
        self.label_tipo.place(relx=0.30, rely=0.29, relwidth=0.05, relheight=0.08)

        self.entry_tipo = Entry(self.frame_2, font='verdana 10 bold')
        self.entry_tipo.place(relx=0.36, rely=0.29, relwidth=0.12, relheight=0.08)

    # Botao Cadastrar Material

        self.bt_Material = Button(self.frame_2,text='Cadastrar Material'.upper(),command=self.add_material)
        self.bt_Material.place(relx=0.01, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Entrada = Button(self.frame_2, text='entrada no estoque'.upper(),command=self.entrada_estoque)
        self.bt_Entrada.place(relx=0.18, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Saida = Button(self.frame_2, text='saida do estoque'.upper(),command=self.saida_estoque)
        self.bt_Saida.place(relx=0.35, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Inserir_Data = Button(self.frame_2, text='inserir data'.upper())
        self.bt_Inserir_Data.place(relx=0.49, rely=0.05, relwidth=0.10, relheight=0.12)

        self.bt_limpar = Button(self.frame_2, text='limpar tela'.upper(),command=self.limpa_tela)
        self.bt_limpar.place(relx=0.49, rely=0.20, relwidth=0.10, relheight=0.12)
    
    # Alterar
        self.bt_alterar = Button(self.frame_2, text='alterar'.upper(),command=self.alterar)
        self.bt_alterar.place(relx=0.01, rely=0.50, relwidth=0.16, relheight=0.10)

        self.bt_excluir = Button(self.frame_2, text='excluir'.upper(),command=self.deleta_material)
        self.bt_excluir.place(relx=0.01, rely=0.60, relwidth=0.16, relheight=0.10)




    def lista_frame3(self):
        self.lista_material = ttk.Treeview(self.frame_3,height=3,columns=('col1','col2','col3','col4','col5'))
        self.lista_material.heading('#0',text='')
        self.lista_material.heading('#1', text='codigo')
        self.lista_material.heading('#2', text='material')
        self.lista_material.heading('#3', text='quantidade')
        self.lista_material.heading('#4', text='tipo')
        self.lista_material.heading('#5', text='data')

        self.lista_material.column('#0',width=1)
        self.lista_material.column('#1', width=40)
        self.lista_material.column('#2', width=200)
        self.lista_material.column('#3', width=100)
        self.lista_material.column('#4', width=50)
        self.lista_material.column('#5', width=50)

        self.lista_material.place(relx=0.01,rely=0.01,relwidth=0.97,relheight=0.95)

    # Barra de Rolagem
        self.scroollista = Scrollbar(self.frame_3,orient='vertical')
        self.lista_material.configure(yscroll= self.scroollista.set)
        self.scroollista.place(relx=0.98,rely=0.01,relwidth=0.02,relheight=0.95)
        
        self.lista_material.bind('<Double-1>',self.OnDoubleClick)

    def lista_frame2(self):
        self.lista_total = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2','col3'))
        self.lista_total.heading('#0', text='')
        self.lista_total.heading('#1',text='Código/TOTAL')
        self.lista_total.heading('#2', text='Material')
        self.lista_total.heading('#3', text='Quantidade')

        self.lista_total.column('#0', width=0)
        self.lista_total.column('#1',width=50)
        self.lista_total.column('#2', width=100)
        self.lista_total.column('#3', width=40)

        self.lista_total.place(relx=0.60, rely=0.01, relwidth=0.40, relheight=0.95)

        # Barra de Rolagem
        self.scrool_total = Scrollbar(self.frame_2, orient='vertical')
        self.lista_total.configure(yscroll=self.scrool_total.set)
        self.scrool_total.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)


        self.lista_total.bind('<Double-1>', self.OnDoubleClick)



Application()
