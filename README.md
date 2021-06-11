# ElectiveCoruses
Sorting elective volunteer by analysing list order in NCU by implementing web scraping along with python  
Required library(python 3):  
  urllib.request(currently unused)  
  webbrowser(currently unused)  
  pandas  
  bs4(currently unused)  
  re  
  inspect  
  os  
  
Included file:  
方針.txt: not effecting script work, just noting NCU course system and behavior  
department.txt: store facultys and belonging departments, main.py will grab data here  
main.py: run main.py and the application will begin  

## Input section example
input course's id and semester(example: 09047 1092): {course's id} {academic year with semester 3 + 1 = 4 number in total}  
input user's department, grade and volunteer order(example: 資訊工程學系 3 1): {your department} {your grade} {your volunteer number}  
Note: Since this project is currently a prototype, some of the department are whether not recorded or from other school(other university or high school students for example)  
Current resolve method is users keyin new data by themself(unefficient and unfortunately input data not adding to txt currently)  
Department Exception Format: 
Oops! Department name {the department not recorded} does not exist, help us add new department in dictionary  
Please input the system and faculty that unknown department belongs to(example: 博士班 資電學院): {system} {faculty}  
  
## Output section example
/*****************************************  
Input example:  
52025 1101  
資訊工程學系 4 1  

Output explanation:
"中選:": shows the students in list are selected  
"待分發:": shows the students in list are in queue  
"無法加選:": shows by analysing list order, the students in list cannot be selected by system
"順位 num1, 第 num2 志願": shows students will be num1 th order when their volunteer is num2  
"==選課結果==": shows the course studends limit, number of selected and number in queue  
/*****************************************  
  
待分發： 順位 1 , 第 1 志願  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 4年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
        資訊工程學系 3年級 志願1 待分  
待分發： 順位 2 , 第 1 志願  
        資訊電機學院學士班 4年級 志願1 待分  
        資訊電機學院學士班 4年級 志願1 待分  
        資訊電機學院學士班 3年級 志願1 待分  
        資訊電機學院學士班 3年級 志願1 待分  
        資訊電機學院學士班 3年級 志願1 待分  
無法加選：
        資訊管理學系 4年級 志願1 待分  
        數學系 4年級 志願1 待分  
        數學系 4年級 志願1 待分  
        數學系 4年級 志願1 待分  
        經濟學系 4年級 志願1 待分  
        電機工程學系 4年級 志願1 待分  
        工學院學士班 3年級 志願1 待分  
        大氣科學學系(大氣組) 3年級 志願1 待分  
  
  
==名次結果==  
人數限制： 40  
中選人數： 0  
待分人數： 40  
