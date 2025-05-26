def glue_string_lists(log: list[list[str]], max_widths=None, max_line_length: int = 150) -> list[str]:
    if max_widths is None:
        max_widths = []
    split_log = []
    for i in range(len(log)):
        stage = log[i]
        if max_widths is not None:
            width = max_widths[i]
            max_size = max(max_line_length, width)
        else:
            max_size = max_line_length
        split_stage = []
        for line in stage:
            parts = [line[i:i + max_size] for i in range(0, len(line), max_size)]
            split_stage.extend(parts)
        split_log.append(split_stage)

    max_height = max(len(stage) for stage in split_log)

    aligned_log = []
    stage_widths = []
    for i in range(len(split_log)):
        stage = split_log[i]
        stage_width = max(len(line) for line in stage) if stage else 0
        if max_widths is not None:
            stage_width = max(stage_width, max_widths[i])
        stage_widths.append(stage_width)

        needed_padding = max_height - len(stage)
        top_padding = needed_padding // 2
        bottom_padding = needed_padding - top_padding
        padded_stage = [''] * top_padding + stage + [''] * bottom_padding
        aligned_log.append(padded_stage)

    ret = []
    for lines in zip(*aligned_log):
        formatted_lines = [
            line.ljust(width)
            for line, width in zip(lines, stage_widths)
        ]
        ret.append(' | '.join(formatted_lines))
    return ret
