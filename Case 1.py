from requests import get # Biblioteca para fazer requisições HTTP
from bs4 import BeautifulSoup # Biblioteca para navegar pela estrutura HTML e procurar elementos específicos
import re # Biblioteca para usar expressões regulares

url = "https://bv.fapesp.br/pt/pesquisa/buscador/?q2=(PIPE)%20AND%20(*:*)" # URL da API
response = get(url).text # Faz a requisição GET para a URL e converte a resposta em texto

soup = BeautifulSoup(response, 'html.parser') # Formata a string resposta para HTML

Table_details = soup.find_all('div', class_='table_details') # Encontra todos os elementos com a classe 'rotulo'

for Table_detail in Table_details:
    # ------------- Encontra o nome da pesquisa -------------
    nome_pesquisa = Table_detail.find('h2', class_='no_float')

    # Se o título for encontrado, extrai o texto e remove espaços em branco do início e fim
    if nome_pesquisa:
        string_nome_pesquisa = nome_pesquisa.text.strip()

        # Se o texto extraído não estiver vazio, imprime o nome da pesquisa
        if string_nome_pesquisa:
            print("Nome da pesquisa:", string_nome_pesquisa)
        else:
            print("Nome da pesquisa: Valor não encontrado")
    else:
        print("Nome da pesquisa: Rótulo não encontrado")

    # ------------- Encontra o número do processo -------------
    rotulo_processo = Table_detail.find('td', class_='rotulo', string='Processo:')

    # Se o rótulo foi encontrado, procuramos o elemento vizinho, que contém o valor
    if rotulo_processo:
        # Encontre o próximo elemento <td> no mesmo nível (sibling)
        num_processo = rotulo_processo.find_next_sibling('td')

        # Se o valor foi encontrado, extraia o texto do valor
        if num_processo:
            num = num_processo.text.strip()
            print("Processo:", num)
        else:
            print("Processo: Valor não encontrado")
    else:
        print("Processo: Rótulo não encontrado")

    #------------- Encontra a linha de fomento -------------
    rotulo_linha_fomento = Table_detail.find('td', class_='rotulo', string='Linha de fomento:')

    if rotulo_linha_fomento:
        string_linha_fomento = rotulo_linha_fomento.find_next_sibling('td')

        if string_linha_fomento:
            linha_fomento = string_linha_fomento.text.strip()
            print("Linha de fomento:", linha_fomento)
        else:
            print("Linha de fomento: Valor não encontrado")
    else:
        print("Linha de fomento: Rótulo não encontrado")
    
    #------------- Encontra a vigência -------------
    rotulo_vigencia = Table_detail.find('td', class_='rotulo', string='Vigência:')

    if rotulo_vigencia:
        string_vigencia = rotulo_vigencia.find_next_sibling('td')

        if string_vigencia:
            vigencia = string_vigencia.text
            # Remove os caracteres de nova linha e tabulação e remove os espaços em branco
            vigencia_limpa = vigencia.replace('\n', ' ').replace('\t', ' ').strip()
            # Remove os espaços em branco extras
            vigencia_final = ' '.join(vigencia_limpa.split())
            print("Vigência:", vigencia_final)
        else:
            print("Vigência: Valor não encontrado")
    else:
        print("Vigência: Rótulo não encontrado")
    
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

            # Formata a lista como uma única string separada por vírgulas
            area_conhecimento_final = ', '.join(area_conhecimento_lista)

            print("Área do conhecimento:", area_conhecimento_final)
        else:
            print("Área do conhecimento: Valor não encontrado")
    else:
        print("Área do conhecimento: Rótulo não encontrado")
    
    #------------- Encontra o perquisador responsável -------------
    rotulo_perquisador_responsavel = Table_detail.find('td', class_='rotulo', string='Pesquisador responsável:')

    if rotulo_perquisador_responsavel:
        string_perquisador_responsavel = rotulo_perquisador_responsavel.find_next_sibling('td')

        if string_perquisador_responsavel:
            nome_pesquisador = string_perquisador_responsavel.text.strip()
            print("Perquisador responsável:", nome_pesquisador)
        else:
            print("Perquisador responsável: Valor não encontrado")
    else:
        print("Perquisador responsável: Rótulo não encontrado")
    
    #------------- Encontra o beneficiário -------------
    rotulo_beneficiario = Table_detail.find('td', class_='rotulo', string='Beneficiário:')

    if rotulo_beneficiario:
        string_beneficiario = rotulo_beneficiario.find_next_sibling('td')

        if string_beneficiario:
            nome_beneficiario = string_beneficiario.text.strip()
            print("Beneficiário:", nome_beneficiario)
        else:
            print("Beneficiário: Valor não encontrado")
    else:
        print("Beneficiário: Rótulo não encontrado")
    
    #------------- Encontra o surpervisor -------------
    # Usamos expressões regulares para encontrar o rótulo "Supervisor:" mesmo que ele tenha espaços extras
    rotulo_supervisor = Table_detail.find('td', class_='rotulo', string=re.compile(r'Supervisor:'))

    if rotulo_supervisor:
        string_supervisor = rotulo_supervisor.find_next_sibling('td')

        if string_supervisor:
            nome_supervisor = string_supervisor.text.strip()
            print("Supervisor:", nome_supervisor)
        else:
            print("Supervisor: Valor não encontrado")
    else:
        print("Supervisor: Rótulo não encontrado")

    #------------- Encontra a instituição sede -------------
    rotulo_instituicao_sede = Table_detail.find('td', class_='rotulo', string='Instituição-sede:')

    if rotulo_instituicao_sede:
        string_instituicao_sede = rotulo_instituicao_sede.find_next_sibling('td')

        if string_instituicao_sede:
            nome_instituicao = string_instituicao_sede.text.strip()
            print("Instituição sede:", nome_instituicao)
        else: 
            print("Instituição sede: Valor não encontrado")
    else:
        print("Instituição sede: Rótulo não encontrado")

    # ------------- Encontra a instituição sede -------------
    rotulo_local_pesquisa = Table_detail.find('td', class_='rotulo', string='Local de pesquisa:')

    if rotulo_local_pesquisa:
        string_local_pesquisa = rotulo_local_pesquisa.find_next_sibling('td')

        if string_local_pesquisa:
            nome_local = string_local_pesquisa.text.strip()
            local_limpo = nome_local.replace('\n', ' ').replace('\t', ' ').strip()
            local_final = ' '.join(local_limpo.split())
            print("Local de pesquisa:", local_final)
        else: 
            print("Local de pesquisa: Valor não encontrado")
    else:
        print("Local de pesquisa: Rótulo não encontrado")
    
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

            assunto_final = ', '.join(assunto_lista)
            print("Assunto(s):", assunto_final)
        else: 
            print("Assunto(s): Valor não encontrado")
    else:
        print("Assunto(s): Rótulo não encontrado")

    # ------------- Pula uma linha -------------
    print("\n") 