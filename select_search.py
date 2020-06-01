import re
cmd = """select * from person where age > ( select * from dual  where name = 'jack')"""
pat = r"select \* from [^\s]+\s?"
it = re.finditer(pat, cmd)
for match in it:
    print(match.group())
