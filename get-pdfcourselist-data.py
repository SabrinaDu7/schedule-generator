from collections import namedtuple
import pandas as pd
import pdfplumber
import re

# Desired matches for a line
Info = namedtuple('Info', 'code sect title prof type day time')
course_info = []
new_code = re.compile(r'(\d{3}[-]\b[A-Z\d]{3}\b[-](\d{2}|[A-Z]{2})) (.*) [F-W][F-W]* \d{4}[-]\d{4}')
new_sect = re.compile(r'\A(\d{5})')
new_time = re.compile(r'([F-W][F-W]*) (\d{4}[-]\d{4})$')
teacher = re.compile(r'(Lecture|Laboratory) (([A-Z]|[a-z]).*[,] [A-Z].*[a-z])')
type_only = re.compile(r'(Lecture|Laboratory)')
unwanted = re.compile(r'[(]cid[:](\d{2}(?=[)])[)])')


# Getting data from each page of pdf
with pdfplumber.open("/Users/sabrinadu/Downloads/schedule_of_classes_winter_2022.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        text = re.sub(unwanted, '', text)  # getting rid of the (cid:10) that pdfplumber inserted

        for line in text.split('\n'):
            if new_code.search(line):
                if 'prof' in locals():
                    course_info.append(
                        Info(code, sect, title, prof, course_type, ', '.join(day_lst), ', '.join(time_lst)))
                if new_sect.search(line):
                    sect = new_sect.search(line).group(1)
                code = new_code.search(line).group(1)
                title = new_code.search(line).group(3)
                day_lst = []
                time_lst = []
            elif teacher.search(line):
                course_type = teacher.search(line).group(1)
                prof = teacher.search(line).group(2)
            elif type_only.search(line):
                course_type = type_only.search(line).group(1)
                prof = 'None'
            if new_time.search(line):
                day = new_time.search(line).group(1)
                time = new_time.search(line).group(2)
                day_lst.append(day)
                time_lst.append(time)

    course_info.append(Info(code, sect, title, prof, course_type, ', '.join(day_lst), ', '.join(time_lst)))

df = pd.DataFrame(course_info)
df.to_csv('scheduleClasses_winter2022.csv')



