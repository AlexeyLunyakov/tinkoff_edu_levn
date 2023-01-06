import argparse
import zipfile
import ast
import re
import os


def leven_func(str1, str2):
    # Минимизируем использование памяти
    if len(str1) > len(str2):
        str1, str2 = str2, str1
    '''
    Формируем матрицу D(i,j) (матрицу сравнения двух строк), используя алгоритм Вагнера-Фишера;
        - Главное условие заполнения элементов матрицы i>0 j>0: min( D(i,j-1) + 1, D(i-1,j) + 1, D(i-1,j-1) + k),
              где k = 1, если элементы в ячейках i и j не совпадают и 0 в противном случае
        - Также нет необходимости хранить все строки матрицы - оставим в памяти только текущую и предыдущую строки
    '''
    curr_row = range(len(str1) + 1)
    for i in range(1, len(str2) + 1):
        prev_row = curr_row
        curr_row = [i] + [0] * len(str1)
        for j in range(1, len(str1) + 1):
            if str1[j - 1] != str2[i - 1]:
                k = 1
            else:
                k = 0
            curr_row[j] = min(prev_row[j] + 1, curr_row[j - 1] + 1, prev_row[j - 1] + k)

    return round(1 - curr_row[len(str1)]/max(len(str1), len(str2)), 3)


def parsing():
    parser = argparse.ArgumentParser(prog='Anti-plagiarism', description='Comparison of two files')
    parser.add_argument("input_path", type=str, help='Input dir for text input')
    parser.add_argument("output_path", type=str, help='Output dir for text scores')
    arguments = parser.parse_args()

    return arguments


def comparison(arch, flag):
    global outp, inp
    args = parsing()
    print("Checking files..")
    try:
        inp = open(f'{args.input_path}', 'r')
        outp = open(f'{args.output_path}', 'w')
    except FileNotFoundError:
        print("One of the files is missing!")

    for line in inp.readlines():
        if '\n' in line:
            str1, str2 = line[:-1].split()
        else:
            str1, str2 = line.split()
        try:
            if '.py' in str1 and '.py' in str2:
                try:
                    print("File association: \n", str1, str2, '\n')
                    str1 = arch.open(str1).read().decode()
                    str2 = arch.open(str2).read().decode()
                    if flag != 0:
                        str1 = normalization(str1)
                        str2 = normalization(str2)
                        outp.write(str(leven_func(str1, str2)) + '\n')
                    else:
                        outp.write(str(leven_func(str1, str2)) + '\n')
                except KeyError:
                    print("File parsing problem!")
            else:
                print("One of the selected files is not a Python file: ")
        except KeyError:
            print("Wrong file extension error!")

    arch.close()
    inp.close()
    outp.close()


def normalization(tmp_str):
    ast_str = ast.parse(tmp_str)
    # Нормализация названий переменных
    for node in ast.walk(ast_str):
        if isinstance(node, ast.Name):
            node.id = 'x'
    new_str = ast.unparse(ast_str)
    # Нормализация комментариев
    new_str = re.sub('#.*', '', new_str, len(tmp_str))
    new_str = re.sub('\n', '_n', new_str, len(tmp_str))
    new_str = re.sub("'''.*'''", '', new_str, len(tmp_str))
    new_str = re.sub('_n', '\n', new_str, len(tmp_str))

    return new_str


def main():
    answ = input("Do you want to test Levenshtein's function? (y/n)\n")
    if answ == 'y' or answ == 'Y':
        ts1, ts2 = "котик", "жмотик"
        print("Test strings:", ts1, ' | ', ts2, "\nCoefficient: ", leven_func(ts1, ts2), "\n")

    flag = 5
    while flag != 0 and flag != 1:
        try:
            flag = int(input("Do you want to normalize texts? (1/0)\n"))
        except ValueError:
            print("Enter correct statement!")

    print("Launching the main program..\n")
    arch_file = zipfile.ZipFile('plagiat.zip', 'r')
    comparison(arch_file, flag)

    print("The analysis is completed, the data is displayed in the file scores.txt")
    os.startfile('scores.txt')


if __name__ == '__main__':
    main()
