import argparse
from typing import Sequence, Union
import re

def find_line_index(lines: Sequence[str], content: str, required: bool=True, skip=0):
    matches = [line for line in lines[skip:] if content in line]
    if len(matches) > 1:
        raise ValueError(f"Multiple line with content: {content}")
    if len(matches) == 0 and required:
        raise ValueError(f"No line with content: {content}")
    if len(matches) == 0 and not required:
        return None
    return lines.index(matches[0])

def iterate_sections(lines: Sequence[str]):
    for index, line in enumerate(lines):
        match =  re.match("<!-- *\[START (?P<section>.+?) file.*-->", line)
        if not match:
            continue
        pattern = "<!-- *\[START (?P<section>.+?) file='(?P<file>[^']+?)'( pre='(?P<pre>[^']+?)'){0,1}( post='(?P<post>[^']+?)'){0,1} *\] *-->"
        params_find = re.match(pattern, match.group(0))
        if not params_find:
            raise ValueError(f"Invalid format of parameter: {match.group(0)}")
        params = params_find.groupdict()
        yield index, params

def replace_list_items(source: Sequence[str], start: int, end: int, items: Sequence[str]):
    return source[:start] + items + source[end:]

def read_section_lines(params):
    with open(params['file'], 'r') as f:
        include_lines = f.readlines()
        pre = find_line_index(include_lines, f"[START {params['section']}]")
        post = find_line_index(include_lines, f"[END {params['section']}]", skip=pre)
        # print({"pre": pre, "post": post, "content": })
        section_lines = include_lines[pre+1:post]
    if params["pre"]:
        section_lines.insert(0, f"{params['pre']}\n")
    if params["post"]:
        section_lines.append(f"{params['post']}\n")
    return section_lines

def render_content(lines):
    for index, params in iterate_sections(lines):
        section_lines = read_section_lines(params)
        include_start_pos = index+1
        include_end_pos = find_line_index(lines, f"[END {params['section']}]", required=False, skip=index)
        if include_end_pos is None:
            section_lines.insert(include_start_pos, f"[END {params['section']}]\n")
            include_end_pos = include_start_pos
        lines = replace_list_items(lines, include_start_pos, include_end_pos, section_lines)
    return "".join(lines)

def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument('--dry-run', action='store_true', help="Skip update file content")
    args = parser.parse_args(argv)
    retval = 0

    for filename in args.filenames:
        with open(filename, 'r+') as f:
            lines = f.readlines()
            new_content = render_content(lines)

            if "".join(lines) != new_content:
                print(f'Fixing file `{filename}`')
                if not args.dry_run:
                    f.seek(0)
                    f.write(new_content)
                    f.truncate()
                else:
                    print(new_content)
                retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())