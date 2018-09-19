#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import drrrobot
import os
import threading
import time
from urllib.request import URLopener
import os
from functools import partial
import random

def sair():
  root.quit()

def sair_da_sala():
  b = drrrobot.Bot()
  s = drrrobot.leave_room(b)
  s()
def enviar_menssagem():
  niji = drrrobot.Bot(name='porteiro',icon='zaika')
  comando = niji.send_msg(message='')

# globalvariaveis

global guarda
guarda = []

def pegar(botao):
  guarda.append(botao['text'])

def bt_click():
  t_loop = threading.Thread(target=loop_login)
  t_loop.start()

def loop_login():
  avatar_bot = guarda[0]
  prosi = ed.get()
  sala =  ed2.get()
  nome =  ed3.get()
  #os.remove("niji.cookie")
  name = '%s'% nome
  icon = '%s' % avatar_bot
  file_name = 'niji.cookie'
  url_room = '%s'%sala
  niji = drrrobot.Bot(name=name,icon=icon)

  # Main
  while 1:
      try:
          if not os.path.isfile(file_name):
              niji.login()
              niji.save_cookie(file_name=file_name)
              room = niji.room_enter(url_room=url_room)
              is_leave = niji.room_update(room_text=room)
              if is_leave == True:
                  break
          else:
              niji.load_cookie(file_name=file_name)
              room = niji.room_enter(url_room=url_room)
              is_leave = niji.room_update(room_text=room)
              if is_leave == True:
                  break
          time.sleep(3)
      except BaseException as e:
          print(e)
          print("[--ERR0--]")


def info(): # info
    info = Toplevel(root)
    info.title("informações")
    fundinho = Label(info, width=700, height=600, image=info_bg)
    fundinho.pack()
    info.geometry("650x387+100+100")


def credits():
  credits = Toplevel(root)
  credits.title("Créditos")
  display2 = Label(credits,width=700,height=600,image=creditos_background)
  display2.pack()
  credits.geometry("650x387+300+20")


def close_window():
    global root
    root.quit()

def engrenagem_bot():
  pass

def terminal_th():
  terminal_txt = open('terminal.txt','r')
  lb = Listbox(terminal_code,bg="black",font="18",fg="#07FB00")
  lb.pack(side=LEFT,expand=True,fill="both")
  sb = Scrollbar(terminal_code)
  sb.pack(side=RIGHT,fill="y")
  sb.configure(command=lb.yview)
  lb.configure(yscrollcommand=sb.set)
  while True:
   terminal_txt=open('terminal.txt','r')
   for i in terminal_txt.readlines():
    lb.insert(END,i)
    terminal_txt=open("terminal.txt","w")
    terminal_txt.write("")
    terminal_txt.close()
    time.sleep(2)

def terminal_bot():
  #janela
  global terminal_code
  terminal_code = Toplevel(root)
  terminal_code.title("Terminal")
  terminal_code["bg"] = "#202020"
  terminal_code.geometry("1000x1000+500+10")
#botoes
  button_leave = Button (terminal_code,width=150,bg ='#202020',height=36,image=icon_leave_room, command = sair_da_sala)
  button_send = Button (terminal_code,width=150,bg ='#202020', height=36,image=send_message, command = enviar_menssagem)
  button_ban = Button(terminal_code,width=150,bg="#202020",height=36,image=ban_bg)
  button_clear_console = Button(terminal_code,width=150,bg="#202020",height=36,image=clear_console,command = reload_terminal)
  input_menssagem = Entry(terminal_code,width=150)
  tsd_alinhamento = Label(terminal_code,bg ='#202020',width=500,height=20, image=tds)
  tsd_alinhamento.pack()
  button_send.pack()
  button_clear_console.pack()
  button_ban.pack()
  button_leave.pack()
  #tela terminal
  #terminal_txt=open("terminal.txt")
  input_menssagem.pack()
  t_terminal = threading.Thread(target=terminal_th)
  t_terminal.start()


#sistema de reload terminal
def reload_terminal():
  t_reload = threading.Thread(target=reload_t)
  t_reload.start()

#resolver
def reload_t():
  terminal_txt=open("terminal","w")
  terminal_txt.write("")
  terminal_txt.close()
  terminal_code.reload()

def limpar_logs():
  terminal_txt=open("logs","w")
  terminal_txt.write("")
  terminal_txt.close()

#sistema de logs registro de conversa
def logs():
  #sistema de belezA
  logs_t = Toplevel(root)
  logs_t.title("Logs")
  logs_t["bg"]="#202020"
  logs_t.geometry("800x500+0+0")
  #sistema de registro de conversa
  terminal_txt=open("logs.txt")
  lb = Listbox(logs_t,bg="#202020",font="18",fg="white")
  lb.pack(side=LEFT,expand=True,fill="both")
  sb = Scrollbar(logs_t)
  sb.pack(side=RIGHT,fill="y")
  sb.configure(command=lb.yview)
  lb.configure(yscrollcommand=sb.set)
  for i in terminal_txt.readlines():
   lb.insert(END,i)

def ajuda():
  ajuda_r = Toplevel(root)
  ajuda_r.title("Ajuda")
  display  = Label(ajuda_r,width=700,height=600,image=ajuda_bg)
  display.pack()
  ajuda_r.geometry("650x387+0+0")

#class apliction
global root
root=tk.Tk()
#janelas dem cima do programa
principal=Menu(root,fg='white',bg='#202020')
Porteiro_bot=Menu(principal)
#coisas dentro de Porteiro_bot
Porteiro_bot.add_command(label="Informações",command=info)
Porteiro_bot.add_command(label="Oque não fazer")
Porteiro_bot.add_command(label="Onde achar proxy")
#logs menu
Logs_bot=Menu(principal)
#coisas dentro de logs
Logs_bot.add_command(label="View logs",command=logs)
Logs_bot.add_command(label="Clear logs",command=limpar_logs)
#menu em cima da janela V V V
principal.add_cascade(label="Porteiro-Bot",menu=Porteiro_bot)
principal.add_command(label="Terminal",command=terminal_bot)
principal.add_cascade(label="Logs",menu=Logs_bot)
principal.add_cascade(label="Rooms",menu=Logs_bot)
principal.add_command(label="Credits",command=credits)
principal.add_command(label="Help",command=ajuda)
principal.add_command(label="Exit",command=sair)
root.configure(menu=principal)

#nome da janela(variavel) ou nome do programa
icon = PhotoImage(file='img/icon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)

#icones e imagens da janelas
#aréa de importação de imagens
icone_button = tk.PhotoImage(file="img/drrr.png")
name_label = tk.PhotoImage(file="img/nome.png")
url_label = tk.PhotoImage(file="img/url.png")
icone_label = tk.PhotoImage(file="img/icone.png")
proxy_label = tk.PhotoImage(file="img/proxy.png")
info_button = tk.PhotoImage(file="img/?.png")
creditos_button = tk.PhotoImage(file="img/creditos.png")
v1_button = tk.PhotoImage(file="avatar/v1.png")
v2_button = tk.PhotoImage(file="avatar/v2.png")
v3_button = tk.PhotoImage(file="avatar/v3.png")
v4_button = tk.PhotoImage(file="avatar/v4.png")
v5_button = tk.PhotoImage(file="avatar/v5.png")
v6_button = tk.PhotoImage(file="avatar/v6.png")
v7_button = tk.PhotoImage(file="avatar/v7.png")
v8_button = tk.PhotoImage(file="avatar/v8.png")
v9_button = tk.PhotoImage(file="avatar/v9.png")
terminal_button = tk.PhotoImage(file="img/terminal.png")
engre_button = tk.PhotoImage(file="img/engre.png")
londarks_label = tk.PhotoImage(file="img/londarks.png")
logo_client = tk.PhotoImage(file="img/logo.png")
login_logo = tk.PhotoImage(file="img/login.gif")

#mandando imagem pra outras janelas
global icon_leave_room
icon_leave_room = tk.PhotoImage(file="img/leave_room.png")
global send_message
send_message = tk.PhotoImage(file="img/messagem.png")
global tds
tds = tk.PhotoImage(file="img/tds.png")
global creditos_background
creditos_background = tk.PhotoImage(file="img/creditos.png")
global ajuda_bg
ajuda_bg = tk.PhotoImage(file="img/ajuda_bg.png")
global info_bg
info_bg = tk.PhotoImage(file="img/info_bg.png")
global ban_bg
ban_bg = tk.PhotoImage(file="img/ban.png")
global clear_console
clear_console = tk.PhotoImage(file="img/clear_console.png")

#sem usos
#global reload_button
#reload_button = tk.PhotoImage(file="img/reload.png")
#button_reload = Button (terminal_code,width=150,bg ='#202020',height=36,image=reload_button)

#titulo da janela
root.title('Porteito-Bot')


#largura e altura da janela e onde ela aparece
root.resizable(width=False, height=False) #janela que não da pra almentar
#root.maxsize(width=700, height=650) janelas definidas com padroẽs de autura e largura
#root.minsize(width=700, height=500)
Canvas(root, width=700, height=600, bg='#202020').pack()
root.geometry("700x600+300+20")


#buttons suporte
#terminal_bt = Button(root,width=39,height=31,image=terminal_button, command = terminal_bot)
#terminal_bt.place(x=656, y=65)

#engrenagem_bt = Button(root,width=31,height=31,image=engre_button, command = engrenagem_bot)
#engrenagem_bt.place(x=663, y=25)

#icones
v1 = Button(root,bg='#202020',width=60,text="kanra", height=60,image=v1_button,)
v1 ["command"]= partial(pegar,v1)

v2 = Button(root,bg='#202020',width=60,text="eight", height=60,image=v2_button,)
v2 ["command"]= partial(pegar,v2)

v3 = Button(root,bg='#202020',width=60,text="tanaka" ,height=60,image=v3_button)
v3 ["command"]= partial(pegar,v3)

v4 = Button(root,bg='#202020',width=60,text="gg" ,height=60,image=v4_button)
v4 ["command"]= partial(pegar,v4)

v5 = Button(root,bg='#202020',width=60,text="zawa" ,height=60,image=v5_button)
v5 ["command"]= partial(pegar,v5)

v6 = Button(root,bg='#202020',width=60,text="setton" ,height=60,image=v6_button)
v6 ["command"]= partial(pegar,v6)

v7 = Button(root,bg='#202020',width=60,text="zaika" ,height=60,image=v7_button)
v7 ["command"]= partial(pegar,v7)

v8 = Button(root,bg='#202020',width=60,text="bakyura" ,height=60,image=v8_button)
v8["command"]= partial(pegar,v8)

v1.place(x=225, y=384)
v2.place(x=287, y=384)
#fileira 1
v3.place(x=225, y=320)
v4.place(x=287, y=320)
v5.place(x=347, y=320)
v6.place(x=406, y=320)
#fileira 2
v7.place(x=347, y=384)
v8.place(x=406, y=384)



#botão
button_start = Button(root, width=90, height=27,image=icone_button, command=bt_click)
button_start.place(x=310, y=470)

#bt3 = Button(root, width=90, height=27,image=info_button, command=info)
#bt3.place(x=310, y=475)

#bt4 = Button(root, width=90, height=27,image=creditos_button, command=creditos)
#bt4.place(x=310, y=510)

logo_l = Label(root,width=410, height=56, image=logo_client)
logo_l.place(x=150, y=30)

londarks_logo = Label(root,width=300, height=36, image=londarks_label)
londarks_logo.place(x=210, y=553)



#label
lb = Label(root,width=167, height=30,image=proxy_label)
lb.place(x=255, y=135)
#input box text
ed = Entry(root, width=20)
ed.place(x=270, y=165 )
#label
lb2 = Label(root, width=167, height=27,image=url_label)
lb2.place(x=250, y=185)
#input box text
ed2 = Entry(root, width=20)
ed2.place(x=270, y=215 )
#label
lb2 = Label(root, width=167, height=30,image=name_label)
lb2.place(x=255, y=235)
#input box text
ed3 = Entry(root, width=20)
ed3.place(x=270, y=265 )
#icone
lb3 = Label(root, width=160, height=30,image=icone_label)
lb3.place(x=255, y=285)
#input box text
#ed4 = Entry(root, width=20)
#ed4.place(x=275, y=265 )


#icone da janela
#root.wm_iconbitmap('lon.ico')

#cor da tela
root["bg"] = "#202020"



root.mainloop()
