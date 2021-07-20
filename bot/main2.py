import discord
import database
import funcoes
from discord.ext import commands, tasks
from time import time
from datetime import datetime, timedelta
from pytz import timezone


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = commands.Bot(command_prefix='.', case_insensitive=True)


@client.event
async def on_ready():
    funcoes.load_data()
    print(f'{client.user.name} is ready.\n\n')
    weekreset.start()


@client.event
async def on_message(message):
    if message.channel.id == CHANNELID:
        msg = message.content
        msg_split = msg.split('\n')
        oficial = (((msg_split[1])[12:]).rstrip().split(' '))
        # ID
        id = int(oficial[0])

        # Nome
        nome = ''
        for i in range(len(oficial[1:])):
            nome += f'{oficial[i + 1]} '

        # Status
        status = 1 if 'ENTROU' in msg_split[2] else 0

        # Data
        data = ((msg_split[3]).split(' '))
        dia = data[1]
        hora = data[3][:8]

        if id in funcoes.id_list:
            if funcoes.status_list[funcoes.id_list.index(id)] == 1:
                database.ponto_entrada(status, hora, id)
            else:
                hora_inicio = '00:00:00'
                hora_ponto = '00:00:00'

                # Horário de serviço
                hora_inicio = funcoes.hora_inicio_list[funcoes.id_list.index(id)]
                servico = datetime.strptime(str(hora), '%H:%M:%S') - datetime.strptime(str(hora_inicio), '%H:%M:%S')
                if servico.days < 0:
                    servico = timedelta(days=0, seconds=servico.seconds, microseconds=servico.microseconds)

                # Coletando horário total
                hora_ponto = funcoes.hora_total_list[funcoes.id_list.index(id)]

                # Calculo
                time_list = [str(servico), str(hora_ponto)]
                mysum = timedelta()
                for i in time_list:
                    (h, m, s) = i.split(':')
                    d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    mysum += d
                hora_total = str(mysum)

                # Update Database
                database.ponto_saida(status, hora_total, id)
                time_list.clear()
                funcoes.load_data()
        else:
            database.add_oficial(id, nome, hora)
            funcoes.load_data()


@tasks.loop(seconds=60)
async def weekreset():
    reset_date = datetime.now(timezone('Brazil/East')).strftime("%a %H%M")
    if reset_date == "Sun 0001":
        x = datetime.now().strftime("%d/%m")
        y = (datetime.now() + timedelta(days=6)).strftime("%d/%m")
        channel = client.get_channel(CHANNELID)

        for id in funcoes.id_list:
            if funcoes.status_list[funcoes.id_list.index(id)] == 1:
                hora_inicio = '00:00:00'
                hora_ponto = '00:00:00'

                # Horário de serviço
                hora_inicio = funcoes.hora_inicio_list[funcoes.id_list.index(id)]
                servico = datetime.strptime('00:00:00', '%H:%M:%S') - datetime.strptime(str(hora_inicio), '%H:%M:%S')
                if servico.days < 0:
                    servico = timedelta(days=0, seconds=servico.seconds, microseconds=servico.microseconds)
                # Coletando horário total
                hora_ponto = funcoes.hora_total_list[funcoes.id_list.index(id)]
                # Calculo
                time_list = [str(servico), str(hora_ponto)]
                mysum = timedelta()
                for i in time_list:
                    (h, m, s) = i.split(':')
                    d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    mysum += d
                hora_total = str(mysum)
                # Update Database
                database.ponto_saida(1, hora_total, id)
                time_list.clear()
                funcoes.load_data()
        funcoes.get_planilha()
        text = f'```PONTO TOTAL DA SEMANA {x} ATÉ {y} FECHADO.```\n\n'
        await channel.send(text, file=discord.File('autoponto.xlsx'))
        database.reset_horas()


client.run(token, bot=True, reconnect=True)
