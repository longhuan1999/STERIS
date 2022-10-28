import re

def tableProcess(htmls):
    pattern = r"<table"
    m1 = re.search(pattern, htmls).span()[0]
    pattern = r"</table>"
    m2 = re.search(pattern, htmls).span()[1]
    htmls = htmls[m1:m2]
    htmlsLines = htmls.split('\n')
    htmlsLines[0] = '<table align="center" border="1" cellpadding="5" cellspacing="0">'
    # print(htmlsLines)
    for i in range(0, len(htmlsLines)):
        if '<tr>' in htmlsLines[i] or '</tr>' in htmlsLines[i]:
            htmlsLines[i] = htmlsLines[i].lstrip("\t")
            htmlsLines[i] = htmlsLines[i].lstrip()
            htmlsLines[i] = "\t" + htmlsLines[i]
        elif '<th' in htmlsLines[i] or '<td' in htmlsLines[i]:
            htmlsLines[i] = htmlsLines[i].lstrip("\t")
            htmlsLines[i] = htmlsLines[i].lstrip()
            htmlsLines[i] = "\t\t" + htmlsLines[i]
        else:
            htmlsLines[i] = htmlsLines[i].lstrip("\t")
            htmlsLines[i] = htmlsLines[i].lstrip()
    # print(htmlsLines)
    htmls = ""
    for i in htmlsLines:
        if i == "":
            continue
        htmls += i + "\n"
    return htmls

# f = open("C:\\Users\\longhuan\\Desktop\\成绩查询.html", "r", encoding="utf-8")
# htmls = f.read()
# print(tableProcess(htmls))