import os
from PyPDF2 import PdfReader
import re


def cutByQuarters(pdfText, page_marker="--- Page"):
    tempStr = ""
    quarter1 = []
    quarter2 = []
    quarter3 = []
    quarter4 = []
    extra = []
    title = ""
    with open(os.path.join(pdfText), "r", encoding="utf-8") as file:
        title = file.readline()
        title += file.readline()
        title += file.readline()
        for line in file:
            if "Second Quarter" in line:
                quarter1.append(tempStr)
                tempStr = ""
                print("Q1 added")   
            elif "Third Quarter" in line:
                quarter2.append(tempStr)
                tempStr = ""
                print("Q2 added")
            elif "Fourth Quarter" in line:
                quarter3.append(tempStr)
                tempStr = ""
                print("Q3 added")
            elif "Extra Question" in line:
                quarter4.append(tempStr)
                tempStr = ""
                print("Q4 added")
            elif not("History Bowl" in line):
                tempStr += line
        extra.append(tempStr)
    return quarter1, quarter2, quarter3, quarter4, extra, title

def cutByQuestions(quarter):
    questions = re.split(r'\(\d+\)', quarter)
    i = 0
    while i < len(questions):
        # Remove newlines and leading spaces
        questions[i] = questions[i].replace("\n", "").lstrip()
        # Split the question into parts by 'ANSWER:' or 'BONUS:'
        questions[i] = re.split(r'ANSWER:|BONUS:', questions[i])
        if len(questions[i]) == 4:
            questions.insert(i + 1, questions[i][2:])
            i = i + 1
        i += 1
    questions = questions[1:]
    questions[-1][-1] = questions[-1][-1][:-2]
    return questions



def cutBySentences(text: str) -> list[str]:
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences

def bonusSplitter(n):
    if (n%2 == 0):
        return str(n/2) + ".B"
    else:
        return str(n/2+1) + ".A"

if __name__ == "__main__":
    # Define the path to the 'sets' folder
    txtName = "2020-2021 History Bowl Set"

    # Process the quarters
    quarter1, quarter2, quarter3, quarter4, extraQ, title = cutByQuarters(os.path.join(os.path.dirname(__file__), "output", txtName + ".txt"))
    Q1Questions = cutByQuestions(quarter1[0])
    Q2Questions = cutByQuestions(quarter2[0])
    Q3Questions = cutByQuestions(quarter3[0])
    Q4Questions = cutByQuestions(quarter4[0])
    for i in range(len(Q1Questions)):
        Q1Questions[i][0] = cutBySentences(Q1Questions[i][0])
    for i in range(len(Q2Questions)):
        Q2Questions[i][0] = cutBySentences(Q2Questions[i][0])
    for i in range(len(Q4Questions)):
        Q4Questions[i][0] = cutBySentences(Q4Questions[i][0])

    # Write the processed text to the formattedText.txt file
    with open(os.path.join(os.path.dirname(__file__), "output", txtName + "_formattedText.txt"), "w", encoding="utf-8") as file:
        for i in range(len(Q1Questions)):
            for j in range(len(Q1Questions[i][0])):
                file.write(Q1Questions[i][0][j] + "|" + Q1Questions[i][1][1:] + "|" + "1." + str(i+1) + "." + str(j+1) + "/" + str(len(Q1Questions[i][0])) + "\n")
        for i in range(len(Q2Questions)):
            for j in range(len(Q2Questions[i][0])):
                file.write(Q2Questions[i][0][j] + "|" + Q2Questions[i][1][1:]  + "|" + "2." + bonusSplitter(i+1) + "." + str(j+1) + "/" + str(len(Q2Questions[i][0])) + "\n")
        for i in range(len(Q3Questions)):
            file.write(Q3Questions[i][0] + "|" + Q3Questions[i][1][1:]  + "|" + "3." + str(i+1) + "." + str(j+1) + "/" + "1" + "\n")
        for i in range(len(Q4Questions)):
            for j in range(len(Q4Questions[i][0])):
                file.write(Q4Questions[i][0][j] + "|" + Q4Questions[i][1][1:]  + "|" + "4." + str(i+1) + "." + str(j+1) + "/" + str(len(Q4Questions[i][0])) + "\n")