def glue_string_lists(log: list[list[str]]):
    max_height = max(len(stage) for stage in log)

    padded_stages = []
    for stage in log:
        needed_padding = max_height - len(stage)

        top_padding = needed_padding // 2
        bottom_padding = needed_padding - top_padding
        padded_stage = [''] * top_padding + stage + [''] * bottom_padding
        padded_stages.append(padded_stage)

    stage_widths = [max([len(line) for line in stage]) for stage in log]

    for lines in zip(*padded_stages):
        formatted_lines = [
            f"{line.ljust(width)}"
            for line, width in zip(lines, stage_widths)
        ]

        print('   |   '.join(formatted_lines))