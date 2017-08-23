
with open('test_input.s4p', 'r') as f:
    line_lst = list(f)
with open('test_output.txt','w') as f:
    for line in line_lst:
        f.write(line)
