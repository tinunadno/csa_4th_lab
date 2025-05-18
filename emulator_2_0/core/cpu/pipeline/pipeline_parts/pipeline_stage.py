from csa_4th_lab.emulator_2_0.parsing.handlers.handler_pool import handler, handler_pool


class pipeline_stage:
    def __init__(self, stage_description, hp: handler_pool):
        self.stage_name = stage_description["name"]
        self.dependencies = stage_description["dependencies"]
        self.behaviour = stage_description["behaviour"]
        self.stage_handler: handler = hp.get_handler(stage_description["behaviour"]["handler"])

    def get_stage_info_as_lines(self) -> list[str]:
        content_lines = []

        content_lines.append(f"STAGE: {self.stage_name}")
        content_lines.append("")

        content_lines.append("DEPENDENCIES:")
        content_lines.extend(f"  • {dep}" for dep in self.dependencies)
        content_lines.append("")

        content_lines.append("BEHAVIOUR:")
        for action in self.behaviour:
            if isinstance(action, dict):
                for key, value in action.items():
                    if isinstance(value, (list, dict)):
                        content_lines.append(f"  {key}:")
                        if isinstance(value, dict):
                            for k, v in value.items():
                                content_lines.append(f"    • {k}: {v}")
                        else:
                            content_lines.extend(f"    • {item}" for item in value)
                    else:
                        content_lines.append(f"  • {key}: {value}")
        content_lines.append("")

        content_lines.append("HANDLER:")
        content_lines.append(f"  • Type: {type(self.stage_handler).__name__}")

        max_len = max(len(line) for line in content_lines)
        border = '=' * (max_len + 4)

        result = [border]
        result.extend(f"= {line.ljust(max_len)} =" for line in content_lines)
        result.append(border)

        return result
