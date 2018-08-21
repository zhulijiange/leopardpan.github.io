---
layout: post
title: '学生信息管理系统'
description: Python项目
tag: 博客
---   
### main.py
    import menu as m
    import student_info as si

    def main():
        L = []
        while True:
            m.show_menu()
            s = input('请选择:')
            if s == 'q':
                break
            elif s == '1':
                si.input_student(L)
            elif s == '2':
                si.output_student(L)
            elif s == '3':
                si.del_student(L)
            elif s == '4':
                si.update_student(L)
            elif s == '5':
                si.score_ul_student(L)
            elif s == '6':
                si.score_lu_student(L)
            elif s == '7':
                si.age_ul_student(L)
            elif s == '8':
                si.age_lu_student(L)

    if __name__ == 'main':
        main()

### menu.py
    def show_menu():
        print('+--------------------------------+')
        print('| 1) 添加学生信息                |')
        print('| 2) 显示学生信息                |')
        print('| 3) 删除学生信息                |')
        print('| 4) 修改学生信息                |')
        print('| 5) 按学生成绩高-低显示学生信息 |')
        print('| 6) 按学生成绩低-高显示学生信息 |')
        print('| 7) 按学生年龄高-低显示学生信息 |')
        print('| 8) 按学生年龄低-高显示学生信息 |')
        print('| q) 退出管理系统                |')
        print('+--------------------------------+')

### student_info.py
    def input_student(L):
        while True:
            name = input('请输入姓名:')
            if name == '':
                break
            age = int(input('请输入年龄:'))
            score = int(input('请输入成绩:'))
            d = {'name': name, 'age': age, 'score': score}
            L.append(d)
        return L


    def get_chinese_char_count(x):
        l = list(x)
        n = len(x)
        count_zh = 0
        for a in range(n):
            if ord(l[a]) > 127:
                count_zh += 1
        return count_zh


    def output_student(L):
        if L == []:
            print('不存在学生数据')
        else:
            fir = '+' + '-' * 15 + '+' + '-' * 10 + '+' + '-' * 10 + '+'
            sec = '|' + 'name'.center(15) + '|' + 'age'.center(10)\
             + '|' + 'score'.center(10) + '|'
            print(fir)
            print(sec)
            print(fir)
            for d in L:
                n = (d['name'])
                a = (d['age'])
                s = (d['score'])
                chn = get_chinese_char_count(n)
                print('|' + n.center(15 - chn) + '|' + str(a).center(10)
                 + '|' + str(s).center(10) + '|')
            print(fir)


    def del_student(L):
        while True:
            m = input('请输入要删除的学生姓名:')
            if m == '':
                break
            else:
                for i in range(len(L)):
                    if L[i]['name'] == m:
                        del L[i]
                        break
                    else:
                        print('不存在此学生!')
        return L


    def update_student(L):
        while True:
            na = input('请输入要修改的学生姓名:')
            if na == '':
                break
            else:
                for i in range(len(L)):
                    if L[i]['name']  == na:
                        n = input('请输入修改后的姓名:')
                        a = int(input('请输入修改后的年龄:'))
                        s = int(input('请输入修改后的成绩:'))
                        if n != '':
                            L[i]['name'] = n
                        if a != '':
                            L[i]['age'] = a
                        if s != '':
                            L[i]['score'] = s
                    else:
                        print('不存在此学生!')
        return L


    def score_ul_student(L):
        if L == []:
            print('不存在学生数据')
        else:
            l = sorted(L, key=lambda d: d['score'], reverse = True)
            output_student(l)


    def score_lu_student(L):
        if L == []:
            print('不存在学生数据')
        else:
            l = sorted(L, key=lambda d: d['score'])
            output_student(l)


    def age_ul_student(L):
        if L == []:
            print('不存在学生数据')
        else:
            l = sorted(L, key=lambda d: d['age'], reverse = True)
            output_student(l)


    def age_lu_student(L):
        if L == []:
            print('不存在学生数据')
        else:
            l = sorted(L, key=lambda d: d['age'])
            output_student(l)
