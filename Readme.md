Olá, esse projeto é um leitor de uma log dos turnos de
um servidor de FiveM. Ele pega a entrada e sáida dos
usuários e calcura a diferença de horários para poder
saber quantas horas foi o seu turno.

Após calcular o turno, ele é armazenado no banco de dados
MySQL correspondente a cada ID do usuário.

A cada uma semana, todo domingo as 00:01, é feito um
calculo de todos os usuários e é apresentado em forma de
planilha as horas totais que os usuários fizeram durante
a semana.
