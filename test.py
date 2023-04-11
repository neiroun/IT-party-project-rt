# import csv
#
#
# with open('user_info.csv', 'r', encoding='utf-8') as file:
#     reader = csv.reader(file, delimiter=';')
#     user_info = list(reader)[1:]
#     id = 1
#     cnt = 1
#     for i in user_info:
#         if int(i[0]) == id:
#             del user_info[user_info.index(i)]
#
#     for i in user_info:
#         i[0] = str(cnt)
#         cnt += 1
#
#     file.close()
#
# with open('user_info.csv', 'w', encoding='utf-8') as file:
#     file.write(f'"id";"ФИО";"Направление";"Курс";"Продолжительность в часах";"Учебный день в часах";'
#                f'"Дата_начала";"Дата_окончания";"Организация";"№Договор";"Номер_телефона";"E-mail"\n')
#     for i in user_info:
#         a = i
#         file.write(f'"{i[0]}";"{i[1]}";"{i[2]}";"{i[3]}";"{i[4]}";"{i[5]}";"{i[6]}";"{i[7]}";"{i[8]}";"{i[9]}";'
#                    f'"{i[10]}";"{i[11]}"\n')


