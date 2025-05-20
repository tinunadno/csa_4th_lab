def glue_string_lists(log: list[list[str]], max_widths: list[int] = None, max_line_length: int = 150):
    # Разбиваем длинные строки во всех блоках
    split_log = []
    for i in range(len(log)):
        stage = log[i]
        if max_widths != None:
            width = max_widths[i]
            max_size = max(max_line_length, width)
        else:
            max_size = max_line_length
        split_stage = []
        for line in stage:
            # Разбиваем строку на части по max_line_length
            parts = [line[i:i + max_size] for i in range(0, len(line), max_size)]
            split_stage.extend(parts)
        split_log.append(split_stage)

    # Находим максимальное количество строк среди всех блоков
    max_height = max(len(stage) for stage in split_log)

    # Выравниваем все блоки по центру
    aligned_log = []
    stage_widths = []
    for i in range(len(split_log)):
        stage = split_log[i]
        # Вычисляем ширину текущего блока
        stage_width = max(len(line) for line in stage) if stage else 0
        if max_widths != None:
            stage_width = max(stage_width, max_widths[i])
        stage_widths.append(stage_width)

        # Добавляем отступы сверху и снизу для выравнивания по центру
        needed_padding = max_height - len(stage)
        top_padding = needed_padding // 2
        bottom_padding = needed_padding - top_padding
        padded_stage = [''] * top_padding + stage + [''] * bottom_padding
        aligned_log.append(padded_stage)

    # Выводим результат с разделителями
    for lines in zip(*aligned_log):
        formatted_lines = [
            line.ljust(width)
            for line, width in zip(lines, stage_widths)
        ]
        print(' | '.join(formatted_lines))