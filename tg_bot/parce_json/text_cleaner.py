def clean_newlines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()

    cleaned_lines = [line.rstrip('\n') for line in lines]

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write('\n'.join(cleaned_lines))

    print(f"Файл обработан. Результат сохранён в {output_file}")


clean_newlines('output_no_headers_footers.txt', 'output_cleaned.txt')