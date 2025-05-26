import re


class define:
    def __init__(self, lines, idx):
        #eg simple define
        if "{" not in lines[idx] and "(" not in lines[idx]:
            line = lines[idx].split(" ")
            self.is_simple = True
            self.name = line[1]
            self.val = line[2]
            lines[idx] = ""
        else:
            if "(" not in lines[idx] or ")" not in lines[idx]:
                raise SyntaxError(f"no arguments brackets in define: {lines[idx]}")
            self.is_simple = False
            line = lines[idx]
            self.name = line[line.find("#define ") + 8 : line.find("(")].strip()
            self.args = line[line.find("(") + 1 : line.find(")")].replace(" ", "").split(",")
            self.body = ""
            idx_macro_start = idx
            while idx < len(lines) and "{" not in lines[idx]:
                idx += 1
            if idx == len(lines):
                raise SyntaxError(f"no opening bracket in define: {lines[idx_macro_start]}")
            if lines[idx].strip() != "{":
                self.body += lines[idx][lines[idx].find("{") + 1 : lines[idx].find("}")]
            while idx < len(lines) and "}" not in lines[idx]:
                if not "{" in lines[idx]:
                    self.body += "\n" + lines[idx]
                idx+=1
            if idx == len(lines):
                raise SyntaxError(f"no closing brackets in define: {lines[idx_macro_start]}")
            if "#define" not in lines[idx]:
                self.body += "\n" + lines[idx][:lines[idx].find("}")]
            # removing macro definition
            for i in range(idx_macro_start, idx + 1):
                if "}" in lines[idx_macro_start]:
                    lines[idx_macro_start] = lines[idx_macro_start][lines[idx_macro_start].find("}")+1 : ]
                    break
                else:
                    lines.pop(idx_macro_start)
    def substitute(self, code):
        if self.is_simple:
            code = re.sub(r'\b' + re.escape(self.name) + r'\b', self.val, code)

        match = re.search(r'\b' + re.escape(self.name) + r'\b', code)
        while match:
            start, end = match.span()
            macro_usage_end = code.find("}", start)
            macro_usage = code[start : macro_usage_end]
            macro_body = macro_usage[macro_usage.find("{") + 1 : macro_usage.find("}")]
            args = macro_usage[macro_usage.find("(") + 1 : macro_usage.find(")")].replace(" ", "").split(",")
            processed_macro = self.body
            for i in range(len(self.args)):
                processed_macro = re.sub(r'\b' + re.escape(self.args[i]) + r'\b', str(args[i]), processed_macro)
            processed_macro =  re.sub(r'\b' + re.escape("body") + r'\b', str(macro_body), processed_macro)
            code = code[:start] + processed_macro + code[macro_usage_end + 1:]
            match = re.search(r'\b' + re.escape(self.name) + r'\b', code)
        return code

def preprocess_macros(code: str, file_dir_path: str) -> str:
    lines = code.split("\n")
    defines = []
    i = 0
    current_lines_size = len(lines)
    while i < current_lines_size:
        if ";" in lines[i]:
            lines[i] = lines[i][: lines[i].find(";")].strip()
        if "#include" in lines[i]:
            include_path = lines[i][lines[i].find("\"") + 1 : lines[i].rfind("\"")]
            include_path = file_dir_path + include_path
            try:
                included_lines = open(include_path).read().split("\n")
            except:
                raise SyntaxError("included file doesn't exist: " + lines[i] + "  " + include_path)
            lines.pop(i)
            lines[i:i] = included_lines
        if "#define" in lines[i]:
            defines.append(define(lines, i))
        i += 1
        current_lines_size = len(lines)
    code = "\n".join(lines)
    for i in defines[::-1]:
        code = i.substitute(code)
    return code
