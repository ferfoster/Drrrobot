# -*- coding:utf-8 -*-
import json
import locale
import time
import requests
from html.parser import HTMLParser
import re
import random
import threading
import smtplib
import os, re
from chatterbot.trainers import ListTrainer #Treiner
from chatterbot import ChatBot #chatbot
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint




global ts_last_greeting
ts_last_greeting = 0

class Bot(object):
    def __init__(self, name='Porteiro', icon='zaika'):
        # locale.setlocale(locale.LC_CTYPE, 'chinese')
        self.name = name
        self.icon = icon
        self.session = requests.session()

    def save_cookie(self, file_name):
        f = open(file_name, 'w+')
        f.write(str(self.session.cookies.get_dict()))
        f.close()

    def load_cookie(self, file_name):
        f = open(file_name, 'r')
        self.session.cookies.update(eval(f.read()))
        f.close()

    def leave_room(self):
        leave_body = {
            'leave': 'leave'
        }
        lr = self.session.post('https://drrr.com/room/?ajax=1', leave_body)
        lr.close()

    def kick_room(self):
        kick_body = {
            'kick': 'kick'
        }
        kc = self.session.post('https://drrr.com/room/?ajax=1', kick_body)
        kc.close()

    def new_host(self, new_host_id):
        new_host_body = {
            'new_host': new_host_id
        }
        nh = self.session.post('https://drrr.com/room/?ajax=1', new_host_body)
        nh.close()

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(url='https://drrr.com/room/?ajax=1', data=post_body)
        p.close()

    def share_music(self, url, name=''):
        share_music_body = {
            'music': 'music',
            'name': name,
            'url': url
        }
        p = self.session.post(url='https://drrr.com/room/?ajax=1', data=share_music_body)
        p.close()

    def login(self):
        home = self.session.get('https://drrr.com')
        token = re.search('<input type="hidden" name="token" data-value=".*?">', home.text).group(0)[-34:-2]
        home.close()
        login_body = {
            'name': self.name,
            'login': 'ENTER',
            'token': token,
            'direct-join': '',
            'language': 'zh-CN',
            'icon': self.icon
        }
        li = self.session.post('https://drrr.com', login_body)
        li.close()

    def room_enter(self, url_room):
        re = self.session.get(url_room)
        re.close()
        room = self.session.get('https://drrr.com/json.php?fast=1')
        # talks = re.findall('{"id".*?"message":".*?"}', re.search('"talks":.*', room).group(0))
        return room.text

    def room_update(self, room_text):
        global ts_last_greeting
        # update timestamp
        update = re.search('"update":\d+.\d+', room_text).group(0)[9:]
        #========inteligencia artificial=========#
        #bot = ChatBot('Porteiro')
        #conversa = ['oi', 'olá', 'Tudo bem?', 'Eu estou bem','Oque está fazendo?','nada','vamos conversa','esse lugar e uma merda']
        #bot.set_trainer(ListTrainer)
        #bot.train(conversa)
        # room update request url
        url_room_update = 'https://drrr.com/json.php?update=' + update
        while 1:
            time.sleep(1)
            ru = self.session.get(url_room_update)
            update = re.search('"update":\d+.\d+', ru.text).group(0)[9:]
            url_room_update = 'https://drrr.com/json.php?update=' + update
            # search "talks" block in room update response
            if 'talks' in ru.text:
                talks_update = re.findall('{"id".*?"message":".*?"}', re.search('"talks":.*', ru.text).group(0))
                # talk in "talks" block
                for tu in talks_update:
                    info_sender = re.findall('"from":{.*?}', tu)
                    info_sender = info_sender[0]
                    name_sender = re.findall('"name":".*?"', info_sender)[0][8:-1]
                    message = re.search('"message":".*?"', tu).group(0)[11:-1].encode(encoding='utf-8').decode(
                        encoding='unicode-escape')
                    print('@%s: %s' % (name_sender,message))#
                    #painel do terminal da interface grafica 
                    term_txt=open('terminal.txt','a')
                    term_txt.write('@%s: %s\n'%(name_sender,message))
                    term_txt.close()
                    if '/' in message or '@Porteiro' in message:
                        # search "from" blockw
                        info_sender = re.findall('"from":{.*?}', tu)
                        if info_sender:
                            info_sender = info_sender[0]
                            name_sender = re.findall('"name":".*?"', info_sender)[0][8:-1]
                            if name_sender == u'Porteiro':
                                continue
                            id_sender = re.findall('"id":".*?"', info_sender)[0][6:-1]
                            # search "to" block in html
                            info_receiver = re.findall('"to":{.*?}', tu)
                            if info_receiver:
                                # info_receiver = info_receiver[0].decode('unicode_escape').encode('utf-8')
                                is_leave = self.handle_private_message(message=message, id_sender=id_sender,
                                                                       name_sender=name_sender)
                                if is_leave:
                                    return True
                            else:
                                self.handle_message(message=message, name_sender=name_sender)
                            self.write_log(name_sender=name_sender, message=message)
                    elif '好' in message or '安' in message or 'time':
                        global ts_last_greeting
                        if time.time() - ts_last_greeting > 60:
                            ts_last_greeting = time.time()
                            # search "from" block
                            info_sender = re.findall('"from":{.*?}', tu)
                            if info_sender:
                                info_sender = info_sender[0]
                                name_sender = re.findall('"name":".*?"', info_sender)[0][8:-1]
                                if name_sender == u'Porteiro':
                                    continue
                                self.reply_greeting(message)
            if '"type":"join"' in ru.text:
                self.post('Bem-Vindo!')
            ru.close()
        



    def give_time(self):
        while 1:
            timestamp = time.time()
            hour = int(time.strftime('%H',time.localtime(time.time())))
            if 8 < hour < 24:
                if timestamp % 600 < 5:
                    self.post_time()
                    time.sleep(590)
            else:
                if timestamp % 1800 < 5:
                    self.post_time()
                    time.sleep(1790)
#mostra horas em determinado tempo^
    def post_time(self):
        give_time = time.strftime('Horas : %H:%M -- /%d/%m/%Y', time.localtime(time.time()))
        self.post('/me %s' % give_time)

#não utilizada
    def tips(self):
        while 1:
            time.sleep(10000 * random.random())
            if 1 < int(time.strftime('%m', time.localtime(time.time()))) < 4:
                list_tips = []
                list_tips_index = int(1 * random.random())
                self.post(list_tips[list_tips_index])



    def certeza(self, message, name_sender, to=''):
         self.post(message='Créditos', url='https://i.imgur.com/Ybg7jSj.jpg', to=to)

    def help(self, message, name_sender, to=''):
        self.post(message='|/gifs|/time|/dicas|/sms menssagem (privado)|/dados| admin:|/room|/exit|/kick| @%s' % (name_sender))

    def groom(self,name_sender, new_host_id):
         if name_sender == u'londarks':
             new_host_body = {
                 'new_host': new_host_id
             }
             nh = self.session.post('https://drrr.com/room/?ajax=1', new_host_body)
             nh.close()
             return True
         else:
          self.post(message='Você Não tem permissão! @%s' % (name_sender),to=to)



    def gexit(self, message, name_sender, to=''):
         if name_sender == u'londarks#Bb8/DUMRJU':
             leave_body = {
                 'leave': 'leave'
             }
             lr = self.session.post('https://drrr.com/room/?ajax=1', leave_body)
             lr.close()
             return True
         else:
          self.post(message='Você Não tem permissão! @%s' % (name_sender))

#comandos criados para testar erros de defs [podem ser auterados]
    def alice(self, message, name_sender, to=''):
        self.post(message='Hug @%s' % (name_sender), url='https://media.giphy.com/media/XpgOZHuDfIkoM/giphy.gif',to=to)



    def punch(self, message, name_sender, to=''):
        self.post(message='punch @%s' % (name_sender), url='https://pa1.narvii.com/6397/a87128b051685c1f006819269a04db7270fe4d92_hq.gif',to=to)

    def kiss(self, message, name_sender, to=''):
        self.post(message='Kiss @%s' % (name_sender), url='https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif',to=to)

    def pipi(self, message, name_sender, to=''):
        list_pipi = ['Você é um merda', 'Você é um lixo', 'Você é um inutil', 'Você é um homúnculo', 'Você é um resto de aborto', 'Sua mãe Não te ama',
                     'Seu Filho da puta', 'Resto de aborto', 'Vadil', 'Pedaço de bosta', 'Desgraçado', 'Va a merda rapaz','imbecil fica discutindo com bot',]
        list_pipi = random.choice(list_pipi)
        self.post(' %s' % list_pipi) # se no final tiver to=to ex: self.post(' %s' % list_pipi to=to) a mensagem e enviada pro privado da pessoa


    def provocar(self, message, name_sender, to=''):
        list_provocar = ['Tenha um Bom-Dia', 'Bom dia, Boa tarde, Boa noite', 'Bip...Bop...', 'Esta um dia lindo. Hojé', 'Como Vocês estão', 'Que conversa agradavel', 'Ai que sono',]
        list_provocar = random.choice(list_provocar)
        self.post('%s' % list_provocar)
       #self.post('/me %s' % list_ground)

#publicidade.
    def kalebe(self, message, name_sender, to=''):
         self.post(message='Procurando um Estilo de desenho diferente?', url='https://2.bp.blogspot.com/-_zsR5To5xvQ/WgCAXtB4koI/AAAAAAAAKn0/9HjHvGo7HscEyOw4X9w_JDbrHDw7aqDKQCLcBGAs/s1600/kalebe-n--.jpg')
         time.sleep(10)
         self.post(message='Acessem.KalebeNectar', url='http://kalebenectar.com.br')
         self.post(message='Nha.!!', url='http://kalebenectar.com.br/images/kalebe.gif?crc=3846800725')

    def download(self, message,to=''):
         message = '1° @Annie (5-5-5)'
         self.post(message)

    def mensagemprivate(self, message, name_sender, to=''):
        if re.findall('/sms .*', message):
           message = message[5:] #conta 5 carateres e depois imprime aquilo escrito
           self.post(message='%s' % (message)) #imprime a menssagem dita



#testando a função sleep
#repetidor
    def possitivo(self, message, name_sender, to=''):
        contador =0
        while (contador<100000):
          time.sleep(100) #delay de 5 segundos
          self.post(message='...')
        contador =contador+1

    def dado(self, message, name_sender, to=''):
          list_dados = ['1','2','3','4','5','6',]
          list_dados2 = ['1','2','3','4','5','6',]
          list_dados3 = ['1','2','3','4','5','6',]
          list_dados4 = ['1','2','3','4','5','6',]
          list_dados = random.choice(list_dados)
          list_dados2 = random.choice(list_dados2)
          list_dados3 = random.choice(list_dados3)
          list_dados4 = random.choice(list_dados4)
          time.sleep(2)
          self.post(message='Irei girar o dado @%s, se sair com um trio de: %s você ganha. Caiu em: %s-%s-%s' % (name_sender, list_dados, list_dados2, list_dados3, list_dados4))


    def ping(self, message, name_sender, to=''):
        if re.findall('/ping .*', message):
           message = message[6:]
        pergunta = (message)
        cmd = "ping -c4" + pergunta
        r = "".join(os.popen(cmd).readlines())


        if re.search ("64 bytes from", r):
           self.post(message=r)
        else:
           self.post(message='Server Off')

    def ghipy(self, message, name_sender, to=''):
        if re.findall('/gif .*', message):
           message = message[5:]
           api_instance = giphy_client.DefaultApi()
           api_key = 'oe533d6kfwvoxrJgC6fDSi6WcSnqyEPb' # str | Giphy API Key.
           tag = message # str | Filters results by specified tag. (optional)
           rating = 'g' # str | Filters results by specified rating. (optional)
           fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

        try:
    # Random Endpoint
           api_response = api_instance.gifs_random_get(api_key, tag=tag, rating=rating, fmt=fmt)
           time.sleep(1)
           self.post(message='Gif %s-@%s' % (message, name_sender), url='%s' % (api_response.data.image_url))
        except ApiException as e:
             self.post(message='sem Resultados %s' %e)
#========================================construção=====================================#
    #d

    def send_msg(self,message='oiiii'):
        self.post(message) # deixa a sala

#============================================================================================#

#delay  time.sleep(100) #delay de 100 segundos
#fim dos gif

#sistema de musica ainda em manutenção
    def music(self, message, name_sender, to=''):
        if re.findall('/m', message):
            message = message[4:]
            r_link = message
            #print(message)
            link = "https://www.youtube.com/watch?v=%s" % (r_link)
            url="http://michaelbelgium.me/ytconverter/convert.php?youtubelink=%s " % (link)
            open_bbc_page = requests.get(url).json() 
            #print(link)
            #time.sleep(1)
            self.share_music(url=open_bbc_page['file'],name=open_bbc_page['title'] )


    def handle_message(self, message, name_sender):
        if '/m' in message:
            t_music = threading.Thread(target=self.music, args=(message, name_sender))
            t_music.start()

        #elif '/help' in message:
        #    t_help = threading.Thread(target=self.help, args=(message, name_sender))
        #    t_help.start()

        elif '/hug' in message:
            t_alice = threading.Thread(target=self.alice, args=(message, name_sender))
            t_alice.start()

        elif '/punch' in message:
            t_punch = threading.Thread(target=self.punch, args=(message, name_sender))
            t_punch.start()


        elif '/kiss' in message:
            t_kiss = threading.Thread(target=self.kiss, args=(message, name_sender))
            t_kiss.start()

        elif '/creditos' in message:
            t_certeza = threading.Thread(target=self.certeza, args=(message, name_sender))
            t_certeza.start()

#fim
        elif '/time' in message:
            t_post_time = threading.Thread(target=self.post_time)
            t_post_time.start()

        elif '/dicas' in message:
            t_sair_sala = threading.Thread(target=self.sair_sala, args=(message))
            t_sair_sala.start()
#admin
        elif '/search' in message:
            t_busca = threading.Thread(target=self.busca, args=(message, name_sender))
            t_busca.start()
        elif '/download' in message:
            t_download = threading.Thread(target=self.download, args=(message, name_sender))
            t_download.start()
        elif '/exit' in message:
            t_gexit = threading.Thread(target=self.gexit, args=(message, name_sender))
            t_gexit.start()
        elif '/dado' in message:
            t_dado = threading.Thread(target=self.dado, args=(message, name_sender))
            t_dado.start()
        elif '/ping' in message:
            t_ping = threading.Thread(target=self.ping, args=(message, name_sender))
            t_ping.start()
        elif '/gif' in message:
            t_ghipy = threading.Thread(target=self.ghipy, args=(message, name_sender))
            t_ghipy.start()
        elif '/rank' in message:
            t_rank = threading.Thread(target=self.download, args=(message))
            t_rank.start()
        elif '/groom' in message:
            t_groom = threading.Thread(target=self.groom, args=(message, name_sender))
            t_groom.start()



#mensagens privadas para o bot

    def handle_private_message(self, message, id_sender, name_sender):
        if '/leave_room' in message:
            self.leave_room() # deixa a sala
            return True
        elif '/room_pass' in message:
            self.new_host(new_host_id=id_sender)# da host pra pessoa po ser auterado
        elif '/m' in message:
            t_music = threading.Thread(target=self.music, args=(message, name_sender, id_sender))
            t_music.start()
        elif '/help' in message:
            t_help = threading.Thread(target=self.help, args=(name_sender, id_sender))
            t_help.start()
        elif '/suicide' in message:
            t_pipi = threading.Thread(target=self.pipi, args=(message, name_sender, id_sender))
            t_pipi.start()
        elif '/pk' in message:
            t_possitivo = threading.Thread(target=self.possitivo, args=(message, name_sender, id_sender))
            t_possitivo.start()
        elif '/kalebe' in message:
            t_kalebe = threading.Thread(target=self.kalebe, args=(message, name_sender, id_sender))
            t_kalebe.start()
        elif '/sms' in message:
            t_mensagemprivate = threading.Thread(target=self.mensagemprivate, args=(message, name_sender, id_sender))
            t_mensagemprivate.start()
        elif '/provocar' in message:
            t_provocar = threading.Thread(target=self.provocar, args=(message, name_sender, id_sender))
            t_provocar.start()
        elif '/suicide' in message:
                t_suicide = threading.Thread(target=self.suicide, args=(message, name_sender, id_sender))
                t_suicide.start()
        elif '/room' in message:
                t_groom = threading.Thread(target=self.groom, args=(message, name_sender, id_sender))
                t_groom.start()
        elif '/exit' in message:
                t_gexit = threading.Thread(target=self.gexit, args=(message, name_sender, id_sender))
                t_gexit.start()
        elif '/giveroom' in message:
                t_groom = threading.Thread(target=self.groom, args=(message, name_sender, id_sender))
                t_groom.start()
        return False


#    def reply_greeting(self, message):
#        if ('' in message or '/olá' in message):
#            self.post('oii')
#        elif 'boa tarde' in message:
#            self.post('boa tarde')
#        elif 'vsf' in message:
#            self.post('Sem palavroes no chat')

    def reply_greeting(self, message):
        if ('bom dia' in message or 'boa tarde' in message):
            self.post('bom dia')
        elif 'oii' in message:
            self.post('oii')

    def write_log(self, name_sender, message):
        logs = open('logs', 'a')
        log = '@%s：%s\n%s\n\n' % (
        name_sender.encode('utf-8'), message.encode('utf-8'), time.strftime('%Y/%m/%d/ %H:%M:%S', time.localtime(time.time())))
        logs.write(log)
        logs.close()
