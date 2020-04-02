import db.sql_exec as se
import os

sql = "INSERT INTO tb_log (`log_file`, `line`, `time`, `system`, `thread`, `level`, `logger`, `file`, `content`) VALUES (\"{0[8]}\", \"{0[7]}\", \"{0[0]}\", \"{0[1]}\", \"{0[2]}\", \"{0[3]}\", \"{0[4]}\", \"{0[5]}\", \"{0[6]}\")"

logfiles = os.listdir("C:\\Users\\OrderPlus\\Desktop\\opstores.core\\")
for logfile in logfiles:
    if not logfile.startswith("info"):
        continue
    print("file_name:" + logfile)
    with open("C:\\Users\\OrderPlus\\Desktop\\opstores.core\\" + logfile, "r", encoding="UTF-8") as of:
        i = 1
        for line in of:
            line = line.replace("][", "|").replace("] [", "|").replace("[", "").replace("]", "").replace("\n", "")
            opstoresLog = line.split("|")
            try:
                opstoresLog[6] = opstoresLog[6].replace("\"", "\\\"")
                opstoresLog.append(i)
                opstoresLog.append(logfile)
                sql_f = sql.format(opstoresLog)
                se.insert(sql_f, param=None)
            except:
                print(str(i) + ":" + line)
            i += 1
