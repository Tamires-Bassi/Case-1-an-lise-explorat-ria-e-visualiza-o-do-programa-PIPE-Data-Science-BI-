import pandas as pd 
import re 

# --------------- Carregar os dados brutos ---------------
try:
    df = pd.read_excel('resultado_case1.xlsx')
except FileNotFoundError:
    # Caso o arquivo seja um CSV
    df = pd.read_csv('resultado_case1.csv')

# Função para limpar textos gerais, remove quebras de linha e espaços extras
def limpar_texto(texto):
    # Se o texto for um valor nulo/NaN, retorna sem processar
    if pd.isna(texto):
        return texto
    
    # Remove quebras de linha, tabulações e espaços duplos
    texto_limpo = str(texto).replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    return ' '.join(texto_limpo.split())

# Aplicar limpeza básica em todas as colunas de texto
colunas_texto = ['Nome da Pesquisa', 'Pesquisador Responsável', 'Beneficiário', 
                 'Instituição Sede', 'Linha de Fomento', 'Área do Conhecimento', 'Assunto']

# Percorre cada coluna de texto e aplica a função de limpeza
for column in colunas_texto:
    if column in df.columns:
        df[column] = df[column].apply(limpar_texto)

# --------------- Separar e formatar as datas de vigência ---------------
def extrair_datas(vigencia):
        # Se a vigência for nula ou não encontrada, retorna None para ambas as datas
    if pd.isna(vigencia) or vigencia == "Não encontrado":
        return "Não encontrado", "Não encontrado"
    
    # Dicionário para converter meses
    meses = {
        'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
        'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
        'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
    }

    # Regex para capturar as datas
    padrao = r'(\d{1,2}) de ([a-zç]+) de (\d{4})'
    matches = re.findall(padrao, vigencia.lower())

    # Cria lista vazia para armazenar as datas extraídas e formatadas
    datas_formatadas = []

    # Processa cada data encontrada e converte para formato ISO
    for dia, mes_nome, ano in matches:
        mes_num = meses.get(mes_nome)
        # Se o mês foi encontrado, formata a data
        if mes_num:
            data_iso = f"{ano}-{mes_num}-{dia.zfill(2)}"
            # Adiciona a data formatada à lista
            datas_formatadas.append(data_iso)
    
    # Define a data de início como o primeiro elemento da lista
    data_inicio = datas_formatadas[0] if len(datas_formatadas) > 0 else None
    # Define a data de fim como o segundo elemento da lista
    data_fim = datas_formatadas[1] if len(datas_formatadas) > 1 else None
    
    return data_inicio, data_fim

# Se a coluna 'Vigência' existe no DataFrame antes de processar
if 'Vigência' in df.columns:
    # Aplica a função e cria novas colunas
    df[['Data Início', 'Data Fim']] = df['Vigência'].apply(
        lambda x: pd.Series(extrair_datas(x))
    )

    # Converte para datetime para permitir cálculos
    df['Data Início'] = pd.to_datetime(df['Data Início'], errors='coerce')
    df['Data Fim'] = pd.to_datetime(df['Data Fim'], errors='coerce')

    # Formatação visual DD-MM-AAAA
    df['Data Início'] = df['Data Início'].dt.strftime('%d-%m-%Y')
    df['Data Fim'] = df['Data Fim'].dt.strftime('%d-%m-%Y')

    # Remover a coluna vigência original
    df.drop(columns=['Vigência'], inplace=True)

# --------------- Extrair Cidade e UF ---------------
def processar_instituicao(texto_sede):
    if pd.isna(texto_sede) or texto_sede == "Não encontrado":
        return "Não encontrado", "Não encontrado"
    
    # Inicializa a variável com o texto original antes de processar
    nome_limpo = texto_sede
    cidade = None
    uf = None

    # Regex para encontrar a Cidade e UF no final ou meio da string
    match = re.search(r'([A-Za-zÀ-ÿ\s]+)\s*,\s*([A-Z]{2})', texto_sede)

    # Se o padrão foi encontrado, extrai cidade e UF
    if match:
         # Extrai a cidade do primeiro grupo capturado e remove espaços
        cidade = match.group(1).strip()
        # Extrai a UF do segundo grupo capturado e remove espaços
        uf = match.group(2).strip()
    
        # Limpar o nome da instituição
        nome_limpo = texto_sede[:match.start()].strip()
        # Remove ponto final se tiver sobrado
        if nome_limpo.endswith('.'):
            nome_limpo = nome_limpo[:-1].strip()
    
    return nome_limpo, cidade, uf

if 'Instituição Sede' in df.columns:
    # Aplica a função e atualiza as colunas
    resultado_inst = df['Instituição Sede'].apply(lambda x: pd.Series(processar_instituicao(x)))
    
    # Atualiza a coluna original com o nome limpo e cria as novas
    df['Instituição Sede'] = resultado_inst[0]
    df['Cidade'] = resultado_inst[1]
    df['UF'] = resultado_inst[2]

# --------------- Tratar Áreas do Conhecimento ---------------
def extrair_area_principal(area_texto):
    if pd.isna(area_texto):
        return "Não Informado"
    # Pega apenas a primeira área antes da vírgula
    return area_texto.split(',')[0].strip()

if 'Área do Conhecimento' in df.columns:
    df['Área Principal'] = df['Área do Conhecimento'].apply(extrair_area_principal)


df.drop(columns=['Área do Conhecimento'], inplace=True)

# --------------- Salvar o arquivo limpo ---------------
df.to_excel('dados_limpos_case1.xlsx', index=False)
print("Dados limpos e salvos em 'dados_limpos_case1.xlsx'")