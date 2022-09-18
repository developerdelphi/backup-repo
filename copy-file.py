from pathlib import Path
from datetime import date
import shutil
import json
import sys


# DEVE RECEBER UMA ORIGEM E UM DESTINO
pathOrigem = '/home/leo/projetos/python/project-backup/files-to-copy'
pathDestino = '/home/leo/projetos/python/project-backup/files-of-backup'

# today RECEBE A DATA ATUAL COMO PARÂMETRO NOME DA PASTA E EXCLUSÃO DE COPIAS ANTIGAS
today = date.today()
path_origin_bk = Path()
path_destiny_bk = Path()

def app():
  if get_file_conf():
    resp('Arquivo de configuração localizado.','GREEN')
    resp(f'Atenção! Aguarde a finalização do processo de backup de arquivos antes de desligar o PC ou utilizar o repositório {path_origin_bk.name}', 'BOLD')
    resp(f'Iniciando compactação de arquivos do diretório: {path_origin_bk.absolute()}...','BLUE')
    resp(f'Tamanho do diretório: {format_size_file(path_origin_bk.stat().st_size)}', 'CYAN')
    # compact_dir()


  else:
    resp('Arquivo de configuração com problemas.')
    resp('Sistema de Backup abortado.')

  return

# def compact_dir():



def get_file_conf():
  config_file = Path() / 'app.conf'
  if config_file.exists() and config_file.is_file():
    with config_file.open() as f:
      content_config_file = json.load(f)
      f.seek(0)
      read_file = f.read()

      if read_file.find('origem') == -1 or read_file.find('destino') == -1 :
        resp('Falta ORIGEM ou DESTINO no arquivo app.conf', 'RED')
        return False
      path_origin = path_destiny = ''
      for key, value in content_config_file.items():

        if key == 'origem': path_origin_bk = Path(value)
        if key == 'destino': path_destiny_bk = Path(value)

      # origin = Path(path_origin)
      # destiny = Path(path_destiny)
      if not (path_origin_bk.exists() and path_origin_bk.is_dir()):
        resp('Caminho para ORIGEM do backup é inválida', 'RED')
        return False
      elif not (path_destiny_bk.exists() and path_destiny_bk.is_dir()):
        resp('Caminho para DESTINO do backup é inválida', 'RED')
        return False

      return True

  return False

def resp(text, color = 'RESET'):
  print_color = ''
  if 'RED' in color: print_color = "\033[1;31m"
  if 'BLUE' in color: print_color  = "\033[1;34m"
  if 'CYAN' in color: print_color  = "\033[1;36m"
  if 'GREEN' in color: print_color = "\033[0;32m"
  if 'RESET' in color: print_color = "\033[0;0m"
  if 'BOLD' in color: print_color    = "\033[;1m"
  if 'REVERSE' in color: print_color = "\033[;7m"
  sys.stdout.write(print_color)
  print(text)

def format_size_file(size):
  base = 1024
  kilo = base
  mega = base ** 2
  giga = base ** 3
  tera = base ** 4
  peta = base ** 5

  if size < kilo:
    txt = 'B'
  elif size < mega:
    size /= kilo
    txt = 'K'
  elif size < giga:
    size /= mega
    txt = 'M'
  elif size < tera:
    size /= giga
    txt = 'G'
  elif size < peta:
    size /= tera
    txt = 'T'
  else:
    size /= peta
    txt = 'P'

  size = round(size, 2)
  return f'{size}{txt}'



app()
# checarDestino = Path(pathDestino)

# print('Hoje é:', today.isoformat())

# for child in checarDestino.iterdir(): ultimo_diretorio = child

# print('este é o último diretorio:', ultimo_diretorio.stem)

# for child in checarDestino.iterdir():
#   if(child.stem == today.isoformat()):
#     print('Diretório encontrado: ', child.stem)



# origem = Path(pathOrigem)
# print('Origem: ', origem.absolute())
# for child in origem.iterdir(): print(child)
# shutil.copytree(origem.absolute(), pathDestino)

# backup = Path(pathDestino)
# for(f to origem.glob('*')):

# print('Existe o backup: ', (list(origem.glob('**/*'))))
# verificarBackup = Path(pathDestino)
# print('Lista Destino':, verificarBackup)
