import os

command = 'ipython -c "%run <filename>.ipynb"'

print(command.replace('<filename>', 'test_run'))

# os.system('ipython -c "%run test_run.ipynb"')
os.system(command.replace('<filename>', 'test_run'))