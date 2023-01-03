import argparse
import zipfile


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
            if str1[j - 1] != str2[i - 1]: k = 1
            else: k = 0
            curr_row[j] = min(prev_row[j] + 1, curr_row[j - 1] + 1, prev_row[j - 1] + k)

    return round(1 - curr_row[len(str1)]/max(len(str1), len(str2)), 3)


def parsing():
    parser = argparse.ArgumentParser(prog='Anti-plagiarism', description='Comparison of two files')
    parser.add_argument("input_path", type=str, help='Input dir for text input')
    parser.add_argument("output_path", type=str, help='Output dir for text scores')
    arguments = parser.parse_args()

    return arguments


def comparison():
    args = parsing()
    arch = zipfile.ZipFile('plagiat.zip', 'r')

    inp = open(f'{args.input_path}', 'r')
    outp = open(f'{args.output_path}', 'w')

    for line in inp.readlines():
        if '\n' in line:
            str1, str2 = line[:-1].split()
        else:
            str1, str2 = line.split()
        print("Checking files..")

        try:
            print("File association: \n", str1, str2, '\n')
            str1 = arch.open(str1).read().decode()
            str2 = arch.open(str2).read().decode()
            outp.write(str(leven_func(str1, str2)) + '\n')
        except KeyError:
            print("One of the files is missing!")

    arch.close()
    inp.close()
    outp.close()


def main():
    comparison()
    print("")

ts1, ts2 = "котик", "жмотик"
print("Levenshtein's function testing:\nTest strings: ", ts1, ' ', ts2, "\nCoefficient: ", leven_func(ts1, ts2), "\n")
print("Launching the main program.")
main()
