import datetime, os


def log(zkzh, content):
    path = "logs\\"
    if not os.path.exists(path) and not os.path.isdir(path):
        os.mkdir(path)
    if zkzh == "024920431210":
        zkzh = "admin"
    path += zkzh + "\\"
    nowtime = datetime.datetime.now()
    if os.path.exists(path) and os.path.isdir(path):
        files_list = []
        for files in os.walk(path):
            for file in files[2]:
                if "log-" in file:
                    data_time = file[file.find("-", 4)+1:-4]
                    files_list.append(data_time)
        if len(files_list) > 0:
            time1 = datetime.datetime.strptime("1900-01-01-00-00-00", "%Y-%m-%d-%H-%M-%S")
            for data_time in files_list:
                time2 = datetime.datetime.strptime(data_time, "%Y-%m-%d-%H-%M-%S")
                if time2 > time1:
                    time1 = time2
        else:
            time1 = nowtime
        file_name = path + "log-" + zkzh + time1.strftime("-%Y-%m-%d-%H-%M-%S") + ".txt"
        if os.path.exists(file_name):
            h = open(file_name, 'r', encoding="utf-8")
            line_count = 0
            for count, line in enumerate(h):
                line_count += 1
            h.close()
        else:
            line_count = 0
        f = open(file_name, "a+", encoding="utf-8")
        if line_count >= 1000:
            f.close()

            file_name = path + "log-" + zkzh + nowtime.strftime("-%Y-%m-%d-%H-%M-%S") + ".txt"
            g = open(file_name, "a", encoding="utf-8")
            g.write(content)
            g.close()
            return True
        elif line_count < 1000:
            f.write(content)
            f.close()
            return True
    elif not os.path.exists(path):
        os.mkdir(path)
        file_name = path + "log-" + zkzh + nowtime.strftime("-%Y-%m-%d-%H-%M-%S") + ".txt"
        f = open(file_name, "a", encoding="utf-8")
        f.write(content)
        f.close()
        return True

# zkzh = "024920431210"
# import string, random
# lenth = len(string.printable)
# for i in range(0,random.randint(2000, 4000)):
#     content = ""
#     for j in range(0, random.randint(10, 100)):
#         content += string.printable[random.randint(0, lenth-1)]
#     content += "\n"
#     log(zkzh, content)