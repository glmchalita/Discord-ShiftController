import mysql.connector

con = mysql.connector.connect(host='HOST', database='DATABASE', user='USER', password='PASSWORD')


def oficiais():
    con.connect()
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tbl_oficiais")
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        return rows


def ids_db():
    con.connect()
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute("SELECT id FROM tbl_oficiais")
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        return rows


def add_oficial(id, nome, hora):
    con.connect()
    if con.is_connected():
        cursor = con.cursor()
        sql = f"INSERT INTO tbl_oficiais(id, nome, status, horaInicio, horatotal) " \
              f"VALUES ({id}, '{nome.title()}', 0, '{hora}', '00:00:00');"
        cursor.execute(sql)
        con.commit()
        cursor.close()
        con.close()


def ponto_entrada(status, hora, id):
    con.connect()
    if con.is_connected():
        cursor = con.cursor()
        sql = f"UPDATE tbl_oficiais SET status = {status}, horaInicio = '{hora}' WHERE id = {id};"
        cursor.execute(sql)
        con.commit()
        cursor.close()
        con.close()


def ponto_saida(status, hora, id):
    con.connect()
    if con.is_connected():
        cursor = con.cursor()
        sql = f"UPDATE tbl_oficiais SET status = {status}, horatotal = '{hora}' WHERE id = {id};"
        cursor.execute(sql)
        con.commit()
        cursor.close()
        con.close()


def reset_horas():
    con.connect()
    if con.is_connected():
        cursor = con.cursor()
        sql = f"UPDATE tbl_oficiais SET horaInicio = '00:00:00', horatotal = '00:00:00'"
        cursor.execute(sql)
        con.commit()
        cursor.close()
        con.close()
