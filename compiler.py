
import subprocess
import tempfile
import pathlib
import config
import shutil
import os





# ##### * DELETANDO OS ARQUIVOS RESIDUAIS CRIADOS
current_path                = os. getcwd()
path_main_script            = f'\\dist\\{config.script_main}'
path_robo_script            = f'\\dist\\{config.script_robo}'
cmd_del_main_script         = f'rmdir {current_path}{path_main_script} /s/q'
cmd_del_robo_script         = f'rmdir {current_path}{path_robo_script} /s/q'
cmd_del_baseZip             = f'del base.zip /q'
cmd_del_shortcut            = f'del {config.softer_name}_{config.softer_version}.lnk /q'

os.system(cmd_del_main_script)
os.system(cmd_del_robo_script)
os.system(cmd_del_baseZip)
os.system(cmd_del_shortcut)



##### * COMPILA O SCRIPT PRINCIPAL DO SOFTER
os.system(f"""pyinstaller --add-data "c:\\Users\Israel\\anaconda3\\Lib\\site-packages\\customtkinter;customtkinter/" --noconfirm {config.script_main}.py""")



##### * COMPILA O SCRIPT DA MAQUINA DO ROBO
os.system(f"""pyinstaller --noconfirm {config.script_robo}.py""")



##### * COPIA ARQUIVOS ADICIONAIS DA MAQUINA DO ROBO PARA A PASTA COMPILADA DO SCRIPT PRINCIPAL
shutil.copy2(f'chromedriver.exe'    ,f'./dist/{config.script_main}/')
shutil.copy2(f'Dados.xlsx'          ,f'./dist/{config.script_main}/')
os.system(f'xcopy dist\{config.script_robo} dist\main /e/h/r/y')



##### * CRIA O ATALHADO QUE SERÁ USADO NO INSTALADOR
def create_shortcut(shortcut_path, target, arguments='', working_dir=''):
    shortcut_path = pathlib.Path(shortcut_path)
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)

    def escape_path(path):
        return str(path).replace('\\', '/')

    def escape_str(str_):
        return str(str_).replace('\\', '\\\\').replace('"', '\\"')

    shortcut_path       = escape_path(shortcut_path)
    target              = escape_path(target)
    working_dir         = escape_path(working_dir)
    arguments           = escape_str(arguments)

    js_content = f'''
        var sh = WScript.CreateObject("WScript.Shell");
        var shortcut = sh.CreateShortcut("{shortcut_path}");
        shortcut.TargetPath = "{target}";
        shortcut.Arguments = "{arguments}";
        shortcut.WorkingDirectory = "{working_dir}";
        shortcut.Save();'''

    fd, path = tempfile.mkstemp('.js')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(js_content)
        subprocess.run([R'wscript.exe', path])
    finally:
        os.unlink(path)
create_shortcut(f'{config.softer_name}_{config.softer_version}.lnk',
f'{config.dir_install}{config.softer_name}_{config.softer_version}/{config.softer_name}_{config.softer_version}.exe')



##### * COPIA O ATALHO PARA A PASTA DO SCRIPT PRINCIPAL COMPILADO
shutil.copy2(f'{config.softer_name}_{config.softer_version}.lnk',f'./dist/{config.script_main}/')



##### * RENOMEIA O EXECUTÁVEL PRINCIPAL
try: os.rename(f'./dist/{config.script_main}/{config.script_main}.exe',f'./dist/{config.script_main}/{config.softer_name}_{config.softer_version}.exe')
except: print('Falha ao tentar renomear o executável principal')



##### * COMPACTA A PASTA DO SCRIPT COMPILADO PRINCIPAL, PARA SER USADO NA COMPILAÇÃO DO SCRIPT DO INSTALADOR
shutil.make_archive('base', 'zip', f'./dist/{config.script_main}')



##### * COMPILANDO O INSTALADOR DE SOFTER
os.system(f"""pyinstaller --add-data "c:\\Users\Israel\\anaconda3\\Lib\\site-packages\\customtkinter;customtkinter/" --add-binary="base.zip;." --onefile installer.py""")


##### * RENOMENADO O INSTALADOR
os.rename('./dist/installer.exe',f'./dist/Instalador_{config.softer_name}_{config.softer_version}.exe')













