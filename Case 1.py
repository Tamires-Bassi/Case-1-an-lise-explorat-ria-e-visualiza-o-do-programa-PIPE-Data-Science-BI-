from requests import get # Biblioteca para fazer requisições HTTP
from bs4 import BeautifulSoup # Biblioteca para navegar pela estrutura HTML e procurar elementos específicos
import re # Biblioteca para usar expressões regulares
import time # Biblioteca para dar pausas e não bloquear o IP
import pandas as pd # Biblioteca para criar o Excel

# Headers para fingir que somos um navegador (CRUCIAL para evitar erro 500)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Lista para guardar todos os dados de todas as páginas
all_data =[]

#Começando pela página 1
pag = 1 

# Loop para percorrer todos as páginas no site
while True:

    # Print para acompanhar o processo
    print(f"Lendo página {pag}...")

    # URL dinâmica com o número da página
    url = "https://bv.fapesp.br/pt/pesquisa/buscador/?q2=(PIPE)%20AND%20(*:*)&page={pag}"
    
    try:
        response = get(url) # Faz a requisição GET para a URL e converte a resposta em texto

        # Se der erro na requisição, para o loop
        if response.status_code != 200:
            print(f"Erro ao acessar página {pag}. Status: {response.status_code}")
            break

        soup = BeautifulSoup(response, 'html.parser') # Formata a string resposta para HTML

        Table_details = soup.find_all('div', class_='table_details') # Encontra todos os elementos com a classe 'rotulo'

        # Se não tiver projetos na página, significa que acabou
        if not Table_details:
            print("Fim dos resultados encontrados.")
            break

        for Table_detail in Table_details:
            # Dicionário para guardar os dados deste projeto específico
            projeto = {}

            # ------------- Encontra o nome da pesquisa -------------
            nome_pesquisa = Table_detail.find('h2', class_='no_float')

            # Se o título for encontrado, extrai o texto e remove espaços em branco do início e fim
            if nome_pesquisa:
                projeto['Nome da Pesquisa'] = nome_pesquisa.text.strip()
            else:
                projeto['Nome da Pesquisa'] = "Não encontrado"

            # ------------- Encontra o número do processo -------------
            rotulo_processo = Table_detail.find('td', class_='rotulo', string='Processo:')

            # Se o rótulo foi encontrado, procuramos o elemento vizinho, que contém o valor
            if rotulo_processo:
                # Encontre o próximo elemento <td> no mesmo nível (sibling)
                num_processo = rotulo_processo.find_next_sibling('td')

                # Se o valor foi encontrado, extraia o texto do valor
                if num_processo:
                    projeto['Processo'] = num_processo.text.strip()
                else:
                    projeto['Processo'] = "Não encontrado"
            else:
                projeto['Processo'] = "Não encontrado"

            #------------- Encontra a linha de fomento -------------
            rotulo_linha_fomento = Table_detail.find('td', class_='rotulo', string='Linha de fomento:')

            if rotulo_linha_fomento:
                string_linha_fomento = rotulo_linha_fomento.find_next_sibling('td')

                if string_linha_fomento:
                    projeto['Linha de Fomento'] = string_linha_fomento.text.strip()
                else:
                    projeto['Linha de Fomento'] = "Não encontrado"
            else:
                projeto['Linha de Fomento'] = "Não encontrado"
            
            #------------- Encontra a vigência -------------
            rotulo_vigencia = Table_detail.find('td', class_='rotulo', string='Vigência:')

            if rotulo_vigencia:
                string_vigencia = rotulo_vigencia.find_next_sibling('td')

                if string_vigencia:
                    vigencia = string_vigencia.text
                    # Remove os caracteres de nova linha e tabulação e remove os espaços em branco
                    vigencia_limpa = vigencia.replace('\n', ' ').replace('\t', ' ').strip()
                    # Remove os espaços em branco extras
                    projeto['Vigência'] = ' '.join(vigencia_limpa.split())
                else:
                    projeto['Vigência'] = "Não encontrado"
            else:
                projeto['Vigência'] = "Não encontrado"
            
            # ------------- Encontra a área do conhecimento -------------
            rotulo_area_conhecimento = Table_detail.find('td', class_='rotulo', string='Área do conhecimento:')

            if rotulo_area_conhecimento:
                string_area_conhecimento = rotulo_area_conhecimento.find_next_sibling('td')

                if string_area_conhecimento:
                    # Encontra todas as tags <a> dentro desse <td>
                    tags_a = string_area_conhecimento.find_all('a')
                    
                    # Inicializa a lista para armazenar as áreas de conhecimento
                    area_conhecimento_lista = []

                    # Extrai o texto limpo de cada tag <a> e adiciona à lista
                    for tag_a in tags_a:
                        area_conhecimento = tag_a.text.strip()
                        area_conhecimento_lista.append(area_conhecimento)

                    projeto['Área do Conhecimento'] = ', '.join(area_conhecimento_lista)
                else:
                    projeto['Área do Conhecimento'] = "Não encontrado"
            else:
                projeto['Área do Conhecimento'] = "Não encontrado"
            
            #------------- Encontra o perquisador responsável -------------
            rotulo_perquisador_responsavel = Table_detail.find('td', class_='rotulo', string='Pesquisador responsável:')

            if rotulo_perquisador_responsavel:
                string_perquisador_responsavel = rotulo_perquisador_responsavel.find_next_sibling('td')

                if string_perquisador_responsavel:
                    projeto['Pesquisador Responsável'] = string_perquisador_responsavel.text.strip()
                else:
                    projeto['Pesquisador Responsável'] = "Não encontrado"
            else:
                projeto['Pesquisador Responsável'] = "Não encontrado"
            
            #------------- Encontra o beneficiário -------------
            rotulo_beneficiario = Table_detail.find('td', class_='rotulo', string='Beneficiário:')

            if rotulo_beneficiario:
                string_beneficiario = rotulo_beneficiario.find_next_sibling('td')

                if string_beneficiario:
                    projeto['Beneficiário'] = string_beneficiario.text.strip()
                else:
                    projeto['Beneficiário'] = "Não encontrado"
            else:
                projeto['Beneficiário'] = "Não encontrado"
            
            #------------- Encontra o surpervisor -------------
            # Usamos expressões regulares para encontrar o rótulo "Supervisor:" mesmo que ele tenha espaços extras
            rotulo_supervisor = Table_detail.find('td', class_='rotulo', string=re.compile(r'Supervisor:'))

            if rotulo_supervisor:
                string_supervisor = rotulo_supervisor.find_next_sibling('td')

                if string_supervisor:
                    projeto['Instituição Sede'] = string_supervisor.text.strip()
                else:
                    projeto['Instituição Sede'] = "Não encontrado"
            else:
                projeto['Instituição Sede'] = "Não encontrado"

            #------------- Encontra a instituição sede -------------
            rotulo_instituicao_sede = Table_detail.find('td', class_='rotulo', string='Instituição-sede:')

            if rotulo_instituicao_sede:
                string_instituicao_sede = rotulo_instituicao_sede.find_next_sibling('td')

                if string_instituicao_sede:
                    projeto['Instituição Sede'] = string_instituicao_sede.text.strip()
                else: 
                    projeto['Instituição Sede'] = "Não encontrado"
            else:
                projeto['Instituição Sede'] = "Não encontrado"

            # ------------- Encontra o Local de pesquisa -------------
            rotulo_local_pesquisa = Table_detail.find('td', class_='rotulo', string='Local de pesquisa:')

            if rotulo_local_pesquisa:
                string_local_pesquisa = rotulo_local_pesquisa.find_next_sibling('td')

                if string_local_pesquisa:
                    nome_local = string_local_pesquisa.text.strip()
                    local_limpo = nome_local.replace('\n', ' ').replace('\t', ' ').strip()
                    projeto['Local de Pesquisa'] = ' '.join(local_limpo.split())
                else: 
                    projeto['Local de Pesquisa'] = "Não encontrado"
            else:
                projeto['Local de Pesquisa'] = "Não encontrado"
            
            #------------- Encontra o assunto -------------
            rotulo_assunto = Table_detail.find('td', class_='rotulo', string='Assunto(s):')

            if rotulo_assunto:
                string_assunto = rotulo_assunto.find_next_sibling('td')

                if string_assunto:
                    tags_a = string_assunto.find_all('a')

                    assunto_lista = []

                    for tag_a in tags_a:
                        assunto = tag_a.text.strip()
                        assunto_lista.append(assunto)

                    projeto['Assunto'] = ', '.join(assunto_lista)
                    
                else: 
                    projeto['Assunto'] = "Não encontrado"
            else:
                projeto['Assunto'] = "Não encontrado"

            # Adiciona o dicionário desse projeto na lista geral
            all_data.append(projeto)

        # Avança para a próxima página
        pag += 1

        # Pausa para não sobrecarregar o servido
        time.sleep(1)

    # Se ocorrer um erro na requisição GET para a URL
    except Exception as e:
        print(f"Ocorreu um erro na página {pag}: {e}")
        break

# Cria o DataFrame
df = pd.DataFrame(all_data)

# # Define o nome do arquivo Excel que será gerado
result = 'resultado_case1.xlsx'
# Exporta o DataFrame para o arquivo Excel sem incluir o índice
df.to_excel(result, index=False)
# Confirma que o arquivo foi criado com sucesso
print(f"Arquivo '{result}' gerado com sucesso!")