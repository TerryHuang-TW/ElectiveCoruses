import urllib.request as req
import webbrowser
import pandas as pd
import bs4
import re
import inspect, os


## basic variables declaration ##
script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))     #path of script
system_list = ["學士班", "碩士班", "博士班"]
faculties_list = ["文學院", "理學院", "工學院", "管理學院", "資電學院", "地科學院", "客家學院", "生醫理工學院"]


## methods define ##
def check_exclude(name):
    if name[0] == "非":
        name = name[1:]
    
    return name


def filter_checking(stu_item, current_filter, exclude):
    if exclude == False:
        if stu_item in current_filter:
            return True
        else:
            return False
    else:
        if stu_item not in current_filter:
            return True
        else:
            return False



## dictionary initialize ##
DSF_dict = {}     #the dictionary including system, faculty and department seperation

with open( script_path + '/department.txt', 'r', encoding="utf-8") as f:       #initialize departments dictionary
    f_all = f.read()    #get string content from file f
    for faculty in faculties_list:
        content = re.findall(r'%s\n\{\n(.*?)\n\}' %faculty, f_all, flags=re.DOTALL)
        departments_list = content[0].split('\n    ')
        departments_list[0] = departments_list[0][4:]   #remove /t from first elment

        for department in departments_list:
            DSF_dict[department] = []
            if "博士" in department:
                DSF_dict[department].append("博士班")
                DSF_dict[department].append(faculty)
                #SFD_dict["博士班"][faculty].append(department)
            elif "碩士" in department:
                DSF_dict[department].append("碩士班")
                DSF_dict[department].append(faculty)
                #SFD_dict["碩士班"][faculty].append(department)
            elif "學系" in department or "學士" in department:
                DSF_dict[department].append("學士班")
                DSF_dict[department].append(faculty)
                #SFD_dict["學士班"][faculty].append(department)
            else:
                DSF_dict[department].append("博士班")
                DSF_dict[department].append(faculty)
                #SFD_dict["博士班"][faculty].append(department)
#print(DSF_dict)


## input section ##
"""
input example:
09047 1092
資訊工程學系 3 1
"""
course_id, semester= input("input course's id and semester(example: 09047 1092): ").split()
user_department, in_grade, in_volunteer = input("input user's department, grade and volunteer order(example: 資訊工程學系 3 1): ").split()
user_grade = int(in_grade)
user_volunteer = int(in_volunteer)


## priority section ##
#"https://cis.ncu.edu.tw/Course/main/query/byKeywords?limit=" + course_id + "&semester=" + semester

print("crwaling course's filter data...")
url = "https://cis.ncu.edu.tw/Course/main/query/byKeywords?limit=" + course_id + "&semester=" + semester
table = pd.read_html(url)
sub = table[1]
sub.columns = ["Order", "Limit"]
sub = sub.drop([0])
#print(sub)
#print(sub.Limit)
limit_list = sub.Limit.tolist()
#print(limit_list)
ordered_filter_list = []    #ordered filter, is excluded
for i in range(len(limit_list)):
    priority_type = ["學制", "學院", "系所", "年級"]
    is_exclude = []
    SFDG_filter = [[], [], [], []]    # system, faculty, department, grade

    for ptype in priority_type:
        content = re.findall(r'%s:限(.*?)。' %ptype, limit_list[i])
        try:    #check if priority type exist
            priority_elements = content[0].split(u'\u3001')     #\u3001 = '、'
        except:
            is_exclude.append(0)
            continue

        #which contain both include and exclude elements
        if ptype == "學制":
            for system in priority_elements:
                system = check_exclude(system)
                SFDG_filter[0].append(system)
        elif ptype == "學院":
            for faculty in priority_elements:
                faculty = check_exclude(faculty)
                SFDG_filter[1].append(faculty)
        elif ptype == "系所":
            for department in priority_elements:
                department = check_exclude(department)
                SFDG_filter[2].append(department)
        else:
            for grade in priority_elements:
                grade = check_exclude(grade)
                if grade == "一年級":
                    SFDG_filter[3].append(1)
                elif grade == "二年級":
                    SFDG_filter[3].append(2)
                elif grade == "三年級":
                    SFDG_filter[3].append(3)
                elif grade == "四年級":
                    SFDG_filter[3].append(4)
        
        if priority_elements[0][0] == "非":
            is_exclude.append(1)
        else:
            is_exclude.append(0)

    sub_list = []
    sub_list.append(SFDG_filter)
    sub_list.append(is_exclude)
    ordered_filter_list.append(sub_list)

#print(ordered_filter_list)


## student list ##
#"https://cis.ncu.edu.tw/Course/main/query/byKeywords?courselist=" + course_id
print("crawling students list data...")
url = "https://cis.ncu.edu.tw/Course/main/query/byKeywords?courselist=" + course_id
table = pd.read_html(url)
columns_name = ["Id", "Name", "Department", "Grade", "Gender", "CEsubject", "VolunteerOrder", "Lotnum", "Status"]
subtable = table[0]
subtable.columns = columns_name
total_limit = subtable.Name.tolist()[10]    #course student maximum
subtable = table[1]
subtable.columns = columns_name

## creating list
status_list = subtable.Status.tolist()
department_list = subtable.Department.tolist()
grade_list = subtable.Grade.tolist()
volunteer_list = subtable.VolunteerOrder.tolist()

selected_count = 0
waiting_count = 0
for item in status_list:    #count status
    if item[:2] == "中選":
        selected_count += 1
    else:
        waiting_count += 1

ignore_count = 0
students_list = []      #department, grade, volunteer, status
for i in range(len(status_list)):
    student = []
    try:    #if there is special case student we ignore and mind user        
        student.append(department_list[i])
        if type(grade_list[i]) == str:
            student.append(grade_list[i][:1])   #remove class
        else:
            student.append(grade_list[i])
        student.append(volunteer_list[i])
        student.append(status_list[i][:2])      #remove unecessary words

        students_list.append(student)
    except Exception as e:
        print("To Admin error message:", e)
        ignore_count += 1

#print(total_limit)
#print(selected_count, waiting_count)
#print(students_list)


## comparision section ##
## needed item...
# DSF_dict
# total_limit
# selected_count, waiting_count
# students_list
# ordered_filter_list
scoring_list = []

for student in students_list:
    stu_department = student[0]
    stu_grade = int(student[1])
    stu_volunteer = student[2]
    stu_status = student[3]
    try:    # !!Need help, current method: user add new tmp department
        stu_system = DSF_dict[stu_department][0]
        stu_faculty = DSF_dict[stu_department][1]
    except:
        print()
        print("Oops! Department name \"", stu_department, "\" does not exist, help us add new department in dictionary", sep='')
        unknown_s, unknown_f = input("Please input the system and faculty that unknown department belongs to(example: 博士班 資電學院): ").split()
        DSF_dict[stu_department] = []
        DSF_dict[stu_department].append(unknown_s)
        DSF_dict[stu_department].append(unknown_f)
        stu_system = DSF_dict[stu_department][0]
        stu_faculty = DSF_dict[stu_department][1]

    if stu_status == "中選":
        scoring_list.append(99999)
        continue
    #result = False

    for order in range(len(ordered_filter_list)):
        priority_point = len(ordered_filter_list) - order
        priority_point *= 100
        priority_point -= stu_volunteer

        for i in range(4):      #if not match then break and the student won't get point(with the current condition)
            current_filter = ordered_filter_list[order][0][i]
            if not current_filter:      #if filter is empty
                continue
            exclude = ordered_filter_list[order][1][i]

            if i == 0:      #system
                result = filter_checking(stu_system, current_filter, exclude)
            elif i == 1:    #faculty
                result = filter_checking(stu_faculty, current_filter, exclude)
            elif i == 2:    #department
                result = filter_checking(stu_department, current_filter, exclude)
            else:           #grade
                result = filter_checking(stu_grade, current_filter, exclude)
            if result == False:
                break
        
        if result == True:
            scoring_list.append(priority_point)
            break
        elif order == len(ordered_filter_list) - 1:
            scoring_list.append(0)

#print(len(scoring_list), len(students_list))


## user scoring section ##
user_score = 0
user_system = DSF_dict[user_department][0]
user_faculty = DSF_dict[user_department][1]

for order in range(len(ordered_filter_list)):
    priority_point = len(ordered_filter_list) - order
    priority_point *= 100
    priority_point -= user_volunteer

    for i in range(4):
        current_filter = ordered_filter_list[order][0][i]
        if not current_filter:      #if filter is empty
            continue
        exclude = ordered_filter_list[order][1][i]

        if i == 0:      #system
            result = filter_checking(user_system, current_filter, exclude)
        elif i == 1:    #faculty
            result = filter_checking(user_faculty, current_filter, exclude)
        elif i == 2:    #department
            result = filter_checking(user_department, current_filter, exclude)
        else:           #grade
            result = filter_checking(user_grade, current_filter, exclude)
        if result == False:
            break

    if result == True:
        user_score = priority_point
        break

## output section ##
priority_dict = {}
score_key = []
user_rank = 1
same_rank = 0

for i in range(len(scoring_list)):
    #print(students_list[i], scoring_list[i])
    if scoring_list[i] not in score_key:
        score_key.append(scoring_list[i])
    if scoring_list[i] not in priority_dict:
        priority_dict[scoring_list[i]] = []
    priority_dict[scoring_list[i]].append(students_list[i])

score_key.sort(reverse=True)
for score in score_key:
    if score == 99999:
        print("中選：")
    else:
        if score > 0:
            print("待分發： 順位", len(ordered_filter_list) - int(score / 100), ", 第",sep=' ', end=' ')
            print(100 - (score % 100), "志願")
        else:
            print("無法加選：")

    for student in priority_dict[score]:
        print('\t', end='')
        for i in range(len(student)):
            if i == 1:
                print(student[i], "年級", sep='', end=' ')
            elif i == 2:
                print("志願", student[i], sep='', end=' ')
            else:
                print(student[i], end=' ')
        print()

        if user_score < score and score != 99999:
            user_rank += 1
        if user_score == score:
            same_rank += 1

print('\n')
print("==名次結果==")
print("人數限制：", total_limit)
print("中選人數：", selected_count)
print("待分人數：", waiting_count)
if ignore_count > 0:
    print("非一般選修人數(表單忽略)：", ignore_count)
#print("\n您的分數：", user_score)
print()
if user_score == 0:
    print("你無法加選該課程")
else:
    print("你在待分人數中的排名：", user_rank)
    print("與你同名次的待分人數：", same_rank)