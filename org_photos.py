import os
import shutil
import exifread
from datetime import datetime

# Pasta de origem das fotos
pasta_origem = './ORIGEM'

# Pasta de destino para organizar as fotos
pasta_destino = './DESTINO'

# Função para obter a data de criação da foto a partir dos metadados EXIF


def obter_data_criacao(foto):
    with open(foto, 'rb') as f:
        tags = exifread.process_file(f)
        if 'EXIF DateTimeOriginal' in tags:
            data_original = tags['EXIF DateTimeOriginal'].values
            return datetime.strptime(data_original, '%Y:%m:%d %H:%M:%S')
    return None


# Loop através de todas as fotos na pasta de origem
for nome_arquivo in os.listdir(pasta_origem):
    foto_path = os.path.join(pasta_origem, nome_arquivo)

    # Verificar se é um arquivo de imagem (você pode adicionar mais extensões, se necessário)
    if foto_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff')):
        data_criacao = obter_data_criacao(foto_path)

        # Se não conseguirmos obter a data de criação, usamos a data de modificação
        if not data_criacao:
            data_criacao = datetime.fromtimestamp(os.path.getmtime(foto_path))

        # Criar uma pasta com o ano e o mês da data de criação
        pasta_ano = data_criacao.strftime('%Y')
        pasta_mes = data_criacao.strftime('%m')
        pasta_destino_ano = os.path.join(pasta_destino, pasta_ano)
        pasta_destino_mes = os.path.join(pasta_destino_ano, pasta_mes)
        os.makedirs(pasta_destino_mes, exist_ok=True)

        # Copiar a foto para a pasta de destino
        shutil.copy(foto_path, os.path.join(pasta_destino_mes, nome_arquivo))

print("Organização concluída!")
