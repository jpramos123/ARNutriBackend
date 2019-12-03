import pandas as pd
import seaborn as sns
import numpy as np
import math
import random
from random import randint
import time

cnf = pd.read_csv('./flaskr/nutrition_with_igs.csv', sep=',', decimal='.')

# Breakfast and Snack
breakfast_cereals = np.matrix(cnf[cnf['Grupo'] == 'Breakfast cereals'])
fruits_and_juices = np.matrix(cnf[cnf['Grupo'] == 'Fruits and fruit juices'])
baked_products = np.matrix(cnf[cnf['Grupo'] == 'Baked Products'])
dairy_and_egg = np.matrix(cnf[cnf['Grupo'] == 'Dairy and Egg Products'])
snacks = np.matrix(cnf[cnf['Grupo'] == 'Snacks'])

# Lunch and Dinner
cereals_grains_pasta = np.matrix(cnf[cnf['Grupo'] == 'Cereals, Grains and Pasta'])
entree = np.matrix(cnf[cnf['Grupo'].isin(['Poultry Products', 'Pork Products', 'Beef Products', 'Finfish and Shellfish Products', 'Lamb, Veal and Game'])])
side = np.matrix(cnf[cnf['Grupo'] == 'Soups, Sauces and Gravies'])
fats_oils = np.matrix(cnf[cnf['Grupo'] == 'Fats and Oils'])
drinks = np.matrix(cnf[cnf['Grupo'].isin(['Fruits and fruit juices', 'Beverages'])])
sweets = np.matrix(cnf[cnf['Grupo'] == 'Sweets'])

groups = {
    'breakfast': [
        breakfast_cereals,
        fruits_and_juices,
        baked_products,
        dairy_and_egg
    ],
    'lunch': [
        cereals_grains_pasta,
        entree,
        side,
        fats_oils,
        drinks,
        sweets
    ],
    'snack': [
        sweets,
        baked_products,
        snacks
    ],
    'dinner': [
        cereals_grains_pasta,
        entree,
        side,
        fats_oils,
        drinks,
        sweets
    ]
}

def fitness(populacao, nutrientes_paciente):
    for individuo in populacao:
        individuo['fitness'], _,_,_,_,_ = single_fitness_fast(individuo, nutrientes_paciente)
    return populacao

def single_fitness_fast(individuo, nutrientes_paciente, specific_meal=None):
    calorias_paciente = nutrientes_paciente[0,0]
    carboidratos_paciente = nutrientes_paciente[0,1]
    proteinas_paciente = nutrientes_paciente[0,2]
    gorduras_paciente = nutrientes_paciente[0,3]
    
    igs_fontes_de_carboidratos = []
    calorias_cardapio = 0
    carboidratos_cardapio = 0.0
    proteinas_cardapio = 0.0
    gorduras_cardapio = 0.0
    flag = False

    for meal, meal_groups in groups.items():
        for i, group in enumerate(meal_groups):
            calorias_cardapio += group[individuo[meal][i], 4] / 100 *  individuo['amounts'][meal][i]
            carboidratos_cardapio +=  group[individuo[meal][i], 5] / 100 * individuo['amounts'][meal][i]
            proteinas_cardapio +=  group[individuo[meal][i], 6] / 100 * individuo['amounts'][meal][i]
            gorduras_cardapio +=  group[individuo[meal][i], 7] / 100 * individuo['amounts'][meal][i]
            if group[individuo[meal][i], 8] == 1: # É fonte de carboidratos
                igs_fontes_de_carboidratos.append(group[individuo[meal][i], 9])

    
    media_igs = sum(igs_fontes_de_carboidratos) / len(igs_fontes_de_carboidratos)
    razao_ig = media_igs / 55

    erro_carboidratos = math.pow(round(carboidratos_paciente - carboidratos_cardapio), 2)
    erro_proteinas = math.pow(round(proteinas_paciente - proteinas_cardapio), 2)
    erro_gorduras = math.pow(round(gorduras_paciente - gorduras_cardapio), 2)
    erro = math.sqrt(erro_carboidratos + erro_proteinas + erro_gorduras)

    aptidao = 1 / (erro * razao_ig +  1)

    return aptidao, calorias_cardapio, carboidratos_cardapio, proteinas_cardapio, gorduras_cardapio, media_igs

def elitismo(populacao):
    sobrevivente = None
    melhor_aptidao = None
    for idx, individuo in enumerate(populacao):
        if melhor_aptidao is None or individuo['fitness'] > melhor_aptidao:
            melhor_aptidao = individuo['fitness']
            sobrevivente = idx
            
    return sobrevivente

def mutacao(populacao, probabilidade):
    for individuo in populacao:
        aleatorio = random.uniform(0,1)
        if aleatorio < probabilidade:
            # Escolhe grupos aleatóriamente
            rand_breakfast = randint(0, len(individuo['breakfast']) - 1)
            rand_lunch = randint(0, len(individuo['lunch']) - 1)            
            rand_snack = randint(0, len(individuo['snack']) - 1)            
            rand_dinner = randint(0, len(individuo['dinner']) - 1)
            
            new_breakfast_food = randint(0, len(groups['breakfast'][rand_breakfast]) - 1)
            new_lunch_food = randint(0, len(groups['lunch'][rand_lunch]) - 1)
            new_snack_food = randint(0, len(groups['snack'][rand_snack]) - 1)
            new_dinner_food = randint(0, len(groups['dinner'][rand_dinner]) - 1)
            
            individuo['breakfast'][rand_breakfast] = new_breakfast_food
            individuo['lunch'][rand_lunch] = new_lunch_food
            individuo['snack'][rand_snack] = new_snack_food
            individuo['dinner'][rand_dinner] = new_dinner_food
            
            # Mutação da Quantidade:
            individuo['amounts']['breakfast'][rand_breakfast] = random.uniform(5,50)
            individuo['amounts']['lunch'][rand_lunch] = random.uniform(5,50)
            individuo['amounts']['snack'][rand_snack] = random.uniform(5,50)
            individuo['amounts']['dinner'][rand_dinner] = random.uniform(5,50)

    return populacao


def crossover(populacao, pares): 
    idx = 0
    nova_populacao = []
    
    while idx < len(pares) - 1:
        progenitores = []
        progenitores.append(populacao[pares[idx]])
        progenitores.append(populacao[pares[idx+1]])
        filhos = [{'amounts':{}},{'amounts':{}}]

        for meal in groups:
            aleatorio = randint(0, len(progenitores[0][meal]))
            for idx_filho in range(2):
                if idx_filho == 0:
                    filhos[idx_filho][meal] = progenitores[0][meal][:aleatorio]
                    filhos[idx_filho][meal].extend(progenitores[1][meal][aleatorio:])
                    filhos[idx_filho]['amounts'][meal] = progenitores[0]['amounts'][meal][:aleatorio]
                    filhos[idx_filho]['amounts'][meal].extend(progenitores[1]['amounts'][meal][aleatorio:])
                else:
                    filhos[idx_filho][meal] = progenitores[1][meal][:aleatorio]
                    filhos[idx_filho][meal].extend(progenitores[0][meal][aleatorio:])
                    filhos[idx_filho]['amounts'][meal] = progenitores[1]['amounts'][meal][:aleatorio]
                    filhos[idx_filho]['amounts'][meal].extend(progenitores[0]['amounts'][meal][aleatorio:])
        nova_populacao.extend(filhos)
        idx += 2
    return nova_populacao

def tournament_selection(populacao):
    idx = 0
    pares = []
    p = populacao[:]
    while idx < len(populacao):
        aleatorio1 = random.randint(0, len(p)-1)
        aleatorio2 = random.randint(0, len(p)-1)
        
        candidato1 = p[aleatorio1]
        candidato2 = p[aleatorio2]
        
        pares.append(aleatorio1 if candidato1['fitness'] > candidato2['fitness'] else aleatorio2)
        idx += 1
    return pares

def algoritmo_genetico(nutrientes_paciente, individuos):
    tempo_inicial = time.time()
    MAX_STRIKES = 100
    MAX_INDIVIDUOS = individuos
    PROBABILIDADE_MUTACAO = 0.05
    populacao = gera_populacao_inicial(MAX_INDIVIDUOS)
    melhor_aptidao = None
    strike = 0
    geracao = 0
    sobrevivente = None
    while strike < MAX_STRIKES:
        
        # Avaliando a geração atual
        populacao = fitness(populacao, nutrientes_paciente)
        sobrevivente = populacao[elitismo(populacao)]
        atual_melhor_aptidao = sobrevivente['fitness']
        
        if (melhor_aptidao is None or atual_melhor_aptidao > melhor_aptidao):
            melhor_aptidao = atual_melhor_aptidao
            strike = 0
        else:
            strike += 1 
    
        pares = tournament_selection(populacao)
        populacao = crossover(populacao, pares)
        populacao = mutacao(populacao, PROBABILIDADE_MUTACAO)
        populacao.append(sobrevivente)
        geracao += 1
        tempo_final = time.time()
        tempo_total = tempo_final - tempo_inicial
    print('Aptidao Final: %f' % melhor_aptidao)
    print('Tempo total de execucao: %d min %d s' %
          (int(tempo_total / 60), int(tempo_total % 60)))
    resultado = sobrevivente
    return resultado

def gera_populacao_inicial(tamanho):
    populacao = []
    for i in range(tamanho):
        individuo = {
            'breakfast': [
                randint(0, len(breakfast_cereals)-1),
                randint(0, len(fruits_and_juices)-1),
                randint(0, len(baked_products)-1),
                randint(0, len(dairy_and_egg)-1),
            ],
            'lunch': [
                randint(0, len(cereals_grains_pasta)-1),
                randint(0, len(entree)-1),
                randint(0, len(side)-1),
                randint(0, len(fats_oils)-1),
                randint(0, len(drinks)-1),
                randint(0, len(sweets)-1),
            ],
            'snack': [
                randint(0, len(sweets)-1),
                randint(0, len(baked_products)-1),
                randint(0, len(snacks)-1),
            ],
            'dinner': [
                randint(0, len(cereals_grains_pasta)-1),
                randint(0, len(entree)-1),
                randint(0, len(side)-1),
                randint(0, len(fats_oils)-1),
                randint(0, len(drinks)-1),
                randint(0, len(sweets)-1),
            ], # Adicionadas quantidades de cada alimento:
            'amounts': {
                'breakfast': [
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                ],
                'lunch': [
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                ],
                'snack': [
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                ],
                'dinner': [
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                    random.uniform(5, 50),
                ],
            }
        }
        populacao.append(individuo)
    return populacao

# Estrutura para cálculo de nutrientes

TabelaNutrientesPacientes = pd.DataFrame(columns=[
    'Calorias',
    'Carboidratos',
    'Proteinas',
    'Gorduras'
])

formulas_homem = [
    [61.0, -33.7],
    [23.3, 514],
    [18.4, 581],
    [16.0, 545],
    [14.2, 593],
    [13.5, 514]
]

formulas_mulher = [
    [58.9, -23.1],
    [20.1, 507],
    [11.1, 761],
    [13.1, 558],
    [9.74, 694],
    [10.1, 569]
]

def calcula_nutrientes(paciente):
    global TabelaNutrientesPacientes
    TMB = calcula_TMB(paciente) # Calcula a Taxa Metabólica Basal
    NDC = calcula_NDC(paciente, TMB) # Calcula a Necessidade Diária de Calorias
    carboidratos, proteinas, gorduras = calcula_macros(NDC) # Calcula os macronutrientes
            
    df_nutrientes = pd.DataFrame({
        'Calorias': NDC,
        'Carboidratos': carboidratos,
        'Proteinas': proteinas,
        'Gorduras': gorduras
    }, index=[0])
        
    TabelaNutrientesPacientes = TabelaNutrientesPacientes.append(df_nutrientes, ignore_index = True)
    return TabelaNutrientesPacientes
        
def calcula_NDC(paciente, TMB):
    # Necessário adicionar nível de atividade física ao paciente
    nivel_atividade_fisica = paciente['NivelAtividadeFisica']
    
    if nivel_atividade_fisica == 1: # Leve
        return TMB * 1.4
    elif nivel_atividade_fisica == 2: # Moderada:
        return TMB * 1.7
    elif nivel_atividade_fisica == 3: # Intensa
        return TMB * 2
    else:
        raise Exception('Nivel de Atividade Fisica fora do intervalo!')

def calcula_macros(calorias):
    carboidratos = calorias * 0.55 / 4
    proteinas = calorias * 0.15 / 4
    gorduras = calorias * 0.3 / 9
    
    return carboidratos, proteinas, gorduras
        
def calcula_TMB(paciente):
    if int(paciente['Genero']) == 1: # Se for homem
        return calcula_nutrientes_homem(paciente)
    elif int(paciente['Genero']) == 2: # Se mulher
        return calcula_nutrientes_mulher(paciente)
    else:
        raise Exception('Genero nao definido!')
            
def calcula_nutrientes_homem(paciente):
    return define_e_calcula_formula(paciente, formulas_homem)
        
def calcula_nutrientes_mulher(paciente):
    return define_e_calcula_formula(paciente, formulas_mulher)

def define_e_calcula_formula(paciente, vetor_formulas):
    idade = paciente['Idade']
    peso = paciente['Peso']
    indice_formula = define_indice_formula(idade)
    formula = vetor_formulas[indice_formula]
    return formula[0] * peso + formula[1]
    
def define_indice_formula(idade):
    if 0 <= idade <= 3:
        return 0
    elif 3 < idade <= 10:
        return 1
    elif 10 < idade <= 18:
        return 2
    elif 18 < idade <= 30:
        return 3
    elif 30 < idade <= 60:
        return 4
    elif idade > 60:
        return 5
    else:
        raise Exception('Idade fora dos intervalos: ' + idade)

def print_menu(menu):
    for meal_name, meal_group in menu.items():
        if meal_name in ['breakfast', 'lunch', 'snack', 'dinner']:
            print(meal_name)
            for idx, meal in enumerate(meal_group):
                print(f'\t{groups[meal_name][idx][meal,2]}')
    
def create_menu_string(menu):
    menu_str = ''
    for meal_name, meal_group in menu.items():
        if meal_name in ['breakfast', 'lunch', 'snack', 'dinner']:
            menu_str += meal_name + '\n'
            for idx, meal in enumerate(meal_group):
                menu_str += '\t' + groups[meal_name][idx][meal,2] + '\n'
    
    return menu_str

def create_menu_json(menu):
    menu_dict = {
        'breakfast': [],
        'lunch': [],
        'snack': [],
        'dinner': [],
        'amounts': None
    }

    for meal_name, meal_group in menu.items():
        if meal_name in ['breakfast', 'lunch', 'snack', 'dinner']:
            for idx, meal in enumerate(meal_group):
                menu_dict[meal_name].append(groups[meal_name][idx][meal,2])

    menu_dict['amounts'] = menu['amounts']

    return menu_dict

