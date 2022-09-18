from pathlib import Path
from datetime import date
from shutil import make_archive, move
import os
import json
import sys

file_name = date.today().isoformat()
path_origin_bk = Path()
path_destiny_bk = Path()

def app():
  pr('Inicializando o sistema de backup')
  pr('---------------------------------')
  if get_file_conf():
    pr('Arquivo de configuração localizado.','GREEN')
    pr('---------------------------------')
    pr(f'Atenção! Aguarde a finalização do processo de backup de arquivos antes de desligar o PC ou utilizar o repositório {path_origin_bk.absolute()}', 'BOLD')
    pr('---------------------------------')
    pr(f'Iniciando compactação de arquivos do diretório: {path_origin_bk.absolute()}...','BLUE')
    compact_dir()
    pr('Compactação executada.')
    pr('---------------------------------')
    pr(f'Movendo o arquivo compactado para o destino em {path_destiny_bk.absolute()}')
    origin = '%s.zip' % (file_name)
    # move(origin, path_destiny_bk.absolute())
    if move_file(origin=origin, destiny=path_destiny_bk.absolute()):
      pr('Arquivo movido com sucesso.','GREEN')
    pr('---------------------------------')
    pr('Processo de backup finalizado.')

  else:
    pr('Arquivo de configuração com problemas.','RED')
    pr('Sistema de Backup abortado.','RED')

  return

def move_file(origin, destiny:Path):
  file_to_move = Path(origin)
  # destiny_of_file = Path(destiny)
  if not file_to_move.is_file or not file_to_move.exists():
    pr(f'Não foi localizado o arquivo [{file_to_move} para mover', 'RED')
    return False
  if not destiny.is_dir or not destiny.exists():
    pr(f'Não foi localizado o destino do arquivo [{destiny.absolute()}] para mover', 'RED')
    return False
  try:
    move(origin, destiny.absolute())
    return True
  except:
    pr('Ocorreu algum erro na movimentação do arquivo para o destino.')
    local = Path()
    pr(f'O arquivo compactado encontra-se em {local.absolute()} e pode ser movido manualmente.')
    return False

def compact_dir():
  try:
    make_archive(f'{file_name}', 'zip', path_origin_bk)
  except:
    pr('Ocorreu um erro na compactação.', 'RED')

def get_file_conf():
  global path_origin_bk
  global path_destiny_bk
  config_file = Path() / 'app.conf'
  if config_file.exists() and config_file.is_file():
    with config_file.open() as f:
      content_config_file = json.load(f)
      f.seek(0)
      read_file = f.read()
      if read_file.find('origem') == -1 or read_file.find('destino') == -1 :
        pr('Falta ORIGEM ou DESTINO no arquivo app.conf', 'RED')
        return False

      for key, value in content_config_file.items():
        if key == 'origem': path_origin_bk = Path(value)
        if key == 'destino': path_destiny_bk = Path(value)

      if not (path_origin_bk.exists() and path_origin_bk.is_dir()):
        pr('Caminho para ORIGEM do backup é inválida', 'RED')
        return False
      elif not (path_destiny_bk.exists() and path_destiny_bk.is_dir()):
        pr('Caminho para DESTINO do backup é inválida', 'RED')
        return False

      return True

  return False

def pr(text, color = 'RESET'):
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
