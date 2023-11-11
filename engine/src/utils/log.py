import inspect

def error(e):
    print("ERROR: ", e)

def info(e):
    print("INFO: ", e)

def debug(e):
    print("DEBUG: ", e)

def log(e, p=True):
    f = open('log.txt', 'a')
    line = ''

    caller = inspect.stack()
    for call in caller[::-1]:
        call = f"{call[1].split('/')[-1]} • {call[3]} • {call[2]} • {call[4][0].strip()}"
        line += call + ' ► '
    
    line += f" => {e} \n"
    f.write(line)
    f.close()
    if p:
        print(line)

def pprint(e):
    print(e)