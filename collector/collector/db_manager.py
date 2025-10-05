import psycopg2
import util
import sys
import log
import os

"""
SOURCES:
    - https://stackoverflow.com/questions/10598002/how-do-i-get-tables-in-postgres-using-psycopg2
    - https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
    - https://www.lewuathe.com/python/postgresql/remind-for-insert-into-with-psycopg2.html
"""

config_path = str(os.path.dirname(os.path.realpath(__file__))) + "/../config.json"
config = util.read_json(config_path)
table_name = os.getenv("DB_T1_NAME")

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
    os.getenv("DB_HOST"),
    os.getenv("DB_NAME"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASS"),
)

conn_object = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)


def execute(cmd):
    output = ""
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(str(cmd))
        conn.commit()
        try:
            output = cursor.fetchall()
        except:
            pass
        cursor.close()
        conn.close()
    except Exception as err:
        log.debug(str(execute.__name__) + "() error : " + str(err))
        output = None
    return output


def insert(data):
    valid_keys = config["database"]["columns"]

    if len(data) != len(valid_keys) or type(data) != dict:
        log.error(
            "the provided data "
            + str(data)
            + ", with type "
            + str(type(data))
            + ", is either not the same length as valid_keys or data is not type dict"
        )
        return False

    for key in data:
        if str(key) not in valid_keys:
            return False

    cmd = "INSERT INTO {} (SOURCE,URL,TITLE,DATE,RECORDED,DETAILS,HTML) VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}');".format(
        table_name.upper(),
        data["source"],
        data["url"],
        data["title"],
        data["date"],
        data["recorded"],
        data["details"],
        data["html"],
    )

    exe_out = execute(cmd)
    if exe_out == None:
        log.error(
            "execute() return None to insert() for the following data: " + str(data)
        )
        return False

    return True


def search(targets=[], option="AND"):
    # if output is None then an error happened
    output = None

    if str(option) != "AND" and str(option) != "OR":
        option = "AND"

    cmd = "SELECT * FROM {}".format(table_name.upper())

    if len(targets) == 0:
        output = execute(str(cmd + ";"))
        return output

    try:
        cmd += " WHERE "
        for value in targets:
            if type(value) == list:
                cmd += "("
                for index in value:
                    if type(index) == list:
                        column = index[0]
                        opt = index[1]
                        val = index[2]
                        tmp = "{} {} '{}'"
                        if type(val) != str:
                            tmp = "{} {} {}"
                        cmd += tmp.format(str(column), str(opt), str(val))
                    if type(index) == str:
                        cmd += " {} ".format(str(index))
                cmd += ")"
            else:
                cmd += " {} ".format(str(value))
        cmd += ";"
    except Exception as err:
        log.debug(str(search.__name__) + "() error : " + str(err))

    output = execute(cmd)

    return output


def db_api_search(data):
    func_output = {"error": None, "result": None}

    if type(data) != dict:
        func_output["error"] = "input is not type dict/json"
        return func_output

    data = util.validate_input(data)
    if data == None:
        func_output["error"] = "input is not in a valid format"
        return func_output

    sources = data["sources"]
    after = data["after"]
    filter_words = data["filter"]

    # build array query for db search
    targets = [[["recorded", ">", float(after)]], "AND", []]
    for i in range(len(sources)):
        source = sources[i]
        targets[-1].append(["source", "=", str(source)])
        if i != len(sources) - 1:
            targets[-1].append("OR")

    data = search(targets)

    if data == None:
        func_output["error"] = "database failed, try again later"
        return func_output

    output = []
    for value in data:
        entry = {
            "source": value[0],
            "url": value[1],
            "title": value[2],
            "date": value[3],
            "recorded": value[4],
            "details": value[5],
        }

        if len(filter_words) == 0:
            output.append(entry)
            continue

        for word in filter_words:
            word = str(word).lower()
            if word in str(entry["url"]).lower():
                output.append(entry)
                break
            if word in str(entry["title"]).lower():
                output.append(entry)
                break
            if word in str(entry["details"]).lower():
                output.append(entry)
                break

    func_output["result"] = output

    return func_output


def get_all_col(col_name):
    try:
        cur = conn_object.cursor()
        cur.execute("SELECT {} FROM {}".format(str(col_name), table_name))
        rows = cur.fetchall()
        cur.close()
        urls = []
        for row in rows:
            urls.append(row[0])

        return urls
    except:
        return None
