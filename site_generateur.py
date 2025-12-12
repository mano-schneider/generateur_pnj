import streamlit as st
import random


# --- MOTEUR DE GÉNÉRATION DE NOMS ---
def generer_nom_fantasy(classe_pnj):
    # On définit des sonorités par "race/ambiance"
    syllabes = {
        'humain': { # Pour Voleur, Guerrier, Mage, Clerc
            'debut': ['Al', 'Breg', 'Cal', 'Dar', 'El', 'Fen', 'Gor', 'Hald', 'Jar', 'Kel', 'Lor', 'Mar', 'Nor', 'Or', 'Pol', 'Quen', 'Rad', 'Sten', 'Tor', 'Val'],
            'fin': ['aric', 'on', 'en', 'or', 'an', 'in', 'is', 'us', 'ath', 'el', 'win', 'ard', 'ric', 'mond', 'gard']
        },
        'elfe': {
            'debut': ['Ael', 'Cael', 'Elar', 'Faen', 'Gala', 'Ilan', 'Laer', 'Mael', 'Nael', 'Paer', 'Rael', 'Sae', 'Tael', 'Vaer'],
            'fin': ['a', 'as', 'ian', 'ion', 'iar', 'or', 'wyn', 'fiel', 'thil', 'luan', 'niel']
        },
        'nain': {
            'debut': ['Bal', 'Bof', 'Dor', 'Dwal', 'Far', 'Gil', 'Gim', 'Kil', 'Mor', 'Nal', 'Nor', 'Oin', 'Thor', 'Thra', 'Ung'],
            'fin': ['in', 'ur', 'ar', 'or', 'ik', 'ok', 'al', 'ol', 'im', 'am', 'ir']
        },
        'petite-gens': {
            'debut': ['Bil', 'Bung', 'Dro', 'Fro', 'Mer', 'Mil', 'Per', 'Pip', 'Sam', 'Tol', 'Wil'],
            'fin': ['bo', 'do', 'go', 'lo', 'mo', 'po', 'to', 'wise', 'ac', 'ic']
        }
    }

    # 1. On détermine la race
    classe_pnj = classe_pnj.lower()
    if classe_pnj in ['elfe']:
        categorie = 'elfe'
    elif classe_pnj in ['nain']:
        categorie = 'nain'
    elif classe_pnj in ['petite-gens']:
        categorie = 'petite-gens'
    else:
        categorie = 'humain'

    # 2. Construction du nom
    partie_1 = random.choice(syllabes[categorie]['debut'])
    partie_2 = random.choice(syllabes[categorie]['fin'])
    
    return partie_1 + partie_2




# ==========================================
# 1. DONNÉES & CONFIGURATION
# ==========================================

st.set_page_config(page_title="Générateur PNJ D&D", page_icon="🐉", layout="wide")

classes_dispo = ['voleur','guerrier','mage','clerc','nain','elfe','petite-gens']

# --- dictionnaires d'équipement ---
equip_off_niv_1_a_6 = {
    'voleur':['épée courte +1', 'arbalète + 1', 'baguette de foudre 5 dé 6 1 charge', 'parchemin de projectile magique 1 charge', '1 carreau de sommeil', 'un carreau enflammé (+3 dégats)'], 
    'guerrier':['espadon +1', 'arc long +1', 'potion de force (+2 force)'], 
    'mage':['dague +1', 'fronde +1', 'baguette de paralysie 1 charge'], 
    'clerc':['épieu +1', 'fronde +1', 'parchemin de controle des morts vivants 1 charge'], 
    'nain':['hache +1', 'arc long +1', 'potion de force (+2 force)'], 
    'elfe':['épée longue +1', 'arc court +1', 'potion de dextérité (+2 dextérité)'], 
    'petite-gens':['épée courte +1', 'arc court +1', 'parchemin de controle de la nature 1 charge']
}

equip_def_niv_1_a_6 = {
    'voleur':['bouclier +1', 'armure de cuir +1', 'parchemin de bouclier 2 charges'], 
    'guerrier':['bouclier +1', 'armure de plaque +1', 'parchemin de bouclier 2 charges', 'anneau protection +1'], 
    'mage':['bouclier +1', 'armure de cotte +1', 'parchemin de bouclier 2 charges', 'anneau de protection +1'], 
    'clerc':['bouclier +1', 'armure de cotte +1', 'parchemin de bouclier 2 charges', 'amulette de protection contre le mal'], 
    'nain':['bouclier +1', 'armure de plaque +1', 'parchemin de bouclier 2 charges', 'bracelet de protection +1'], 
    'elfe':['bouclier +1', 'armure de plaque +1', 'parchemin de bouclier 2 charges'], 
    'petite-gens':['bouclier +1', 'armure de plaque +1', 'parchemin de bouclier 2 charges']
}

equip_gen_niv_1_a_6 = {
    'voleur':['anneau d\'invisibilité', 'potion de forme gazeuse', 'potion de soins mineurs', 'potions de soins majeurs'], 
    'guerrier':['potion de rapidité', 'potion de croissance', 'potion de soins majeurs', 'potions de soins mineurs'], 
    'mage':['potion de soins majeurs', 'potions de soins mineurs'], 
    'clerc':['potion de soins majeurs', 'potions de soins mineurs'], 
    'nain':['potion de soins majeurs', 'potions de soins mineurs', 'baguette de détection des métaux précieux'], 
    'elfe':['potion de soins majeurs', 'potions de soins mineurs', 'parchemin de boule de feu 5dé6 1 charge'], 
    'petite-gens':['potion de soins majeurs', 'potions de soins mineurs', 'parchemin de langage des plantes']
}

equip_off_niv_7_ou_plus = {
    'voleur':[ 'épée courte +2 empoisonnée (2dégats par round pendant 10 rounds)', 'arbalette +2', '3 carreaux de sommeil', '3 carreaux empoisonnés', '3 carreaux enflammés'], 
    'guerrier': ['espadon +2 enflammé (+1dé6 dégats de feu)', 'arc long +2', '2 flèche de glace', 'flèche à tête chercheuse (+3 pour toucher)', 'espadon +1', 'parchemin de bénédiction 1 charge (+2+2)'], 
    'mage':['dague +2 sommeil', 'dague +2', 'fronde +2', 'anneau de Djinn radieux', 'baguette de paralysie 2 charges'], 
    'clerc':['épieux +1 maudit (-1-1 si la cible rate jdp)', 'épieux +2', 'fronde +2','parchemin de confusion 1 charge'], 
    'nain':['hache +2', 'arc long +2', '2 flèches empoisonnées', 'hâche +1 enflammée'], 
    'elfe':['épée longue +2', 'épée longue +1 de glace', 'arc court +2', 'baguette de foudre 7dé6 2charges'], 
    'petite-gens':['arc court +2', 'épée courte +2', 'épée courte +1 vampirique', 'parchemin de controle de la nature 3 charges']
}

equip_def_niv_7_ou_plus = {
    'voleur':['anneau d\'invisiblité', 'armure de cuir +2', 'bouclier +2', 'anneau de vol', 'amulette de protection contre le mal'], 
    'guerrier':['anneau d\'invisiblité', 'armure de plaque +2', 'bouclier +2', 'potion de résistance (5 dégats absorbés sur chaque coup)'], 
    'mage':['anneau d\'invisiblité', 'armure de cotte +2', 'bouclier +2', 'anneau de vol'], 
    'clerc':['anneau d\'invisiblité', 'amulette de protection contre le mal sur 5 metres', 'armure de cotte +2', 'bouclier +2'], 
    'nain':['anneau d\'invisiblité', 'armure de plaque +2', 'bouclier +2', 'anneau de vol'], 
    'elfe':['anneau d\'invisiblité', 'armure de plaque +2', 'bouclier +2', 'anneau de vol'], 
    'petite-gens':['anneau d\'invisiblité', 'armure de plaque +2', 'bouclier +2', 'anneau de vol']
}

equip_gen_niv_7_ou_plus = {
    'voleur':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale', 'potion de rapidité'], 
    'guerrier':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale','potion de rapidité'], 
    'mage':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale','potion de rapidité'], 
    'clerc':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale','potion de rapidité'], 
    'nain':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale','potion de rapidité'], 
    'elfe':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale','potion de rapidité'], 
    'petite-gens':['2 potions de soins mineurs', '2 potions de soins majeurs','potion de soins ultimes', 'potion de guérison totale','potion de rapidité']
}

equip_classique = {
    'voleur':['armure de cuir', 'épée courte', 'arbalète', 'bouclier'], 
    'guerrier':['armure de plaque', 'bouclier', 'arc long', 'espadon'], 
    'mage':['armure de cottes', 'dague', 'fronde', 'bouclier'], 
    'clerc':['armure de cottes', 'épieu', 'bouclier', 'fronde'], 
    'nain':['hache', 'arc long', 'bouclier', 'armure de plaque'], 
    'elfe':['épée longue', 'arc court', 'armure de plaque', 'bouclier'], 
    'petite-gens':['armure de plaque', 'épée courte', 'bouclier', 'arc court']
}

# Reconstitution des dictionnaires assemblés
equip_par_classe_niv_1_a_6 = {
    'voleur':[equip_def_niv_1_a_6['voleur'], equip_gen_niv_1_a_6['voleur'], equip_off_niv_1_a_6['voleur']],
    'guerrier':[equip_def_niv_1_a_6['guerrier'], equip_gen_niv_1_a_6['guerrier'], equip_off_niv_1_a_6['guerrier']],
    'mage':[equip_def_niv_1_a_6['mage'], equip_gen_niv_1_a_6['mage'], equip_off_niv_1_a_6['mage']],
    'clerc':[equip_def_niv_1_a_6['clerc'], equip_gen_niv_1_a_6['clerc'], equip_off_niv_1_a_6['clerc']],
    'nain':[equip_def_niv_1_a_6['nain'], equip_gen_niv_1_a_6['nain'], equip_off_niv_1_a_6['nain']],
    'elfe':[equip_def_niv_1_a_6['elfe'], equip_gen_niv_1_a_6['elfe'], equip_off_niv_1_a_6['elfe']],
    'petite-gens':[equip_def_niv_1_a_6['petite-gens'], equip_gen_niv_1_a_6['petite-gens'], equip_off_niv_1_a_6['petite-gens']]
}

equip_par_classe_niv_7_ou_plus = {
    'voleur':[equip_def_niv_7_ou_plus['voleur'], equip_gen_niv_7_ou_plus['voleur'], equip_off_niv_7_ou_plus['voleur']],
    'guerrier':[equip_def_niv_7_ou_plus['guerrier'], equip_gen_niv_7_ou_plus['guerrier'], equip_off_niv_7_ou_plus['guerrier']],
    'mage':[equip_def_niv_7_ou_plus['mage'], equip_gen_niv_7_ou_plus['mage'], equip_off_niv_7_ou_plus['mage']],
    'clerc':[equip_def_niv_7_ou_plus['clerc'], equip_gen_niv_7_ou_plus['clerc'], equip_off_niv_7_ou_plus['clerc']],
    'nain':[equip_def_niv_7_ou_plus['nain'], equip_gen_niv_7_ou_plus['nain'], equip_off_niv_7_ou_plus['nain']],
    'elfe':[equip_def_niv_7_ou_plus['elfe'], equip_gen_niv_7_ou_plus['elfe'], equip_off_niv_7_ou_plus['elfe']],
    'petite-gens':[equip_def_niv_7_ou_plus['petite-gens'], equip_gen_niv_7_ou_plus['petite-gens'], equip_off_niv_7_ou_plus['petite-gens']]
}


# ==========================================
# 2. LOGIQUE MÉTIER
# ==========================================

def lancer_pv(classe:str, nb_dés:int, modificateur=0):
    resultat=0
    classe = classe.lower().strip()
    for i in range(nb_dés):
        if classe in ('voleur', 'mage'):
            resultat += (random.randint(1,4) + modificateur)
        elif classe in ('guerrier', 'nain'):
            resultat += (random.randint(1,8) + modificateur)
        elif classe in ('clerc', 'elfe', 'petite-gens'):
            resultat += (random.randint(1,6) + modificateur)
    if resultat <= 0:
        resultat = 1
    return resultat


def lancers_bonus(classe:str, carac:dict):
    """
    classe : classe du pnj
    carac : carac du pnj déjà tirés

    renvoie les carac modifiées avec le dé bonus
    """
    mapping_lancers_bonus = {
        'voleur': lambda c : c.update({'D':c['D']+random.randint(1,4)}),
        'guerrier': lambda c : c.update({'F':c['F']+random.randint(1,4)}),
        'mage': lambda c : c.update({'I':c['I']+random.randint(1,4)}),
        'clerc': lambda c : c.update({'S':c['S']+random.randint(1,4)}),
        'nain': lambda c : c.update({'F':c['F']+random.randint(1,2), 'C':c['C']+random.randint(1,2)}),
        'elfe': lambda c : c.update({'I': c['I']+random.randint(1,2), 'S':c['S']+random.randint(1,2)}),
        'petite-gens': lambda c : c.update({'C':c['C']+random.randint(1,2), 'Ch':c['Ch']+random.randint(1,2)})
    }
    mapping_lancers_bonus[classe](carac)
    return carac

def lancer_carac(classe:str):
    carac = {'F':0, 'I':0, 'S':0, 'D':0, 'C':0, 'Ch':0}
    modif_constitution = 0

    for i in carac:
        carac[i]= random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
        
    carac = lancers_bonus(classe, carac)
    for i in carac:
        if carac[i] ==22: carac[i] = '22(+5)'
        elif carac[i] >= 20: carac[i] = f'{str(carac[i])}(+4)'
        elif carac[i] >= 18: carac[i] = f'{str(carac[i])}(+3)'
        elif carac[i] >= 16: carac[i] = f'{str(carac[i])}(+2)'
        elif carac[i] >= 14: carac[i] = f'{str(carac[i])}(+1)'
        elif carac[i]<= 4: carac[i] = f'{str(carac[i])}(-3)'
        elif carac[i] <= 6: carac[i] = f'{str(carac[i])}(-2)'
        elif carac[i] <= 8: carac[i] = f'{str(carac[i])}(-1)'
        else: carac[i] = str(carac[i])
    try:
        if int(carac['C'].split('(')[0]) >= 14 or int(carac['C'].split('(')[0]) <= 8:
            temporaire = carac['C'].split('(')[1]
            modif_propre = temporaire.replace(')', '')
            modif_constitution = int(modif_propre)
    except:
        pass
    return carac, modif_constitution

class Pnj:
    def __init__(self, nom:str, niveau:int, classe:str):
        self.nom = nom
        self.niveau = niveau
        self.classe = classe
        self.alignement = random.choice(['LL', 'LN', 'NL', 'NN', 'NC', 'CN', 'CC'])
        self.caractere = ''
        self.equipement_rare_offensif = []
        self.equipement_rare_defensif = []
        self.equipement_rare_general = []
        self.equipement_classique = equip_classique[self.classe]
        self.po = self.niveau*random.randint(100, 300) if self.niveau <= 6 else self.niveau*random.randint(300, 700) if self.niveau <= 8 else self.niveau*random.randint(700, 1000)
        self.carac = 0
        self.jp = 0
        self.modif_constitution = 0
        self.pv = 0
        self.ca = 0

    def trait_de_caractere(self, alignement:str):
        mapping_trait_de_caractere= {
            'LL': ['Psychorigide', 'Veut être certain de n\'offenser personne', 'Dévoué à la garde', 'Honnête et fiable', 'Force tranquille', 'Amical et inspire le respect', 'Parano des chaotiques'],
            'LN': ['Inquiet d\'enfreindre les règles', 'Pragmatique', 'Impartial', 'Rieur', 'Parano des chaotiques'],
            'NL': ['Cherche à tempérer les plus loyaux que lui', 'déprimé face au chaos dans le monde', 'Suit les règles si ça l\'arrange'],
            'NN': ['Un bon coup un mauvais coup', 'Équilibre avant tout', 'Indépendant', 'Imprévisible'],
            'NC': ['Adore les jeux d\'argent', 'Libre penseur', 'Se moque de tout le monde', 'Imprévisible'],
            'CN': ['Chaotique mais bon', 'Rackette les plus faible mais a peur des plus fort', 'Imprudent'],
            'CC': ['Aime tabasser les enfants', 'Égoïste', 'Destructeur', 'Imprévisible et dangereux', 'Religieux fou']
        }
        self.caractere = random.sample(mapping_trait_de_caractere[alignement], 2)

 



    def lancer_carac(self):
        self.carac, self.modif_constitution = lancer_carac(self.classe)

    def define_pv(self):
        if not self.carac:
            self.lancer_carac()
        self.pv = lancer_pv(self.classe, self.niveau + 1 if self.niveau<=9 else 10, self.modif_constitution)
        if self.niveau>9:
            niveaux_en_plus = self.niveau - 9
            self.pv += niveaux_en_plus*(1+self.modif_constitution)

    def define_equipement_rare(self):
        chance = {'off' : random.randint(1,100), 'def' : random.randint(1,100), 'gen' : random.randint(1,100)}
        
        # Sélection des listes selon niveau
        if self.niveau <= 6:
            source = equip_par_classe_niv_1_a_6[self.classe]
            nb_items = 2
        else:
            source = equip_par_classe_niv_7_ou_plus[self.classe]
            nb_items = 3

        if chance['off'] <= 20:
             self.equipement_rare_offensif.extend(random.sample(source[2], nb_items))
        if chance['def'] <= 20:           
             self.equipement_rare_defensif.extend(random.sample(source[0], nb_items))
        if chance['gen'] <= 20:
             self.equipement_rare_general.extend(random.sample(source[1], nb_items))

        
        self.equipement_rare_offensif = ' - '.join(self.equipement_rare_offensif)
        self.equipement_rare_defensif = ' - '.join(self.equipement_rare_defensif)
        self.equipement_rare_general = ' - '.join(self.equipement_rare_general)
        self.equipement_classique = ' - '.join(self.equipement_classique)

    def define_ca(self):
        # Base CA
        base_ca = {'guerrier':3, 'nain':3, 'clerc':4, 'mage':4, 'elfe':2, 'petite-gens':2, 'voleur':6}
        self.ca = base_ca.get(self.classe, 9)


        # On découpe la string créée dans define_equipement_rare
        if self.equipement_rare_defensif:
            objets = self.equipement_rare_defensif.split(' - ')
            for i in objets:
                if '+' in i:
                    try:
                        # On cherche le chiffre après le +
                        valeur = int(i.split('+')[1].split()[0]) # .split()[0] gère les textes après le chiffre
                        self.ca -= valeur
                    except:
                        continue # Si ça foire, on ignore l'objet au lieu de crasher

# --- Sous-classes ---
class Voleur(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe='voleur')
        self.guilde = random.choice(['Specularium','Kelven','Luln','Selenica'])
        self.alignement = random.choice(['CC','CN','NC','NN'])
        self.jp = {
    'Rayon mortel, poison':13,
    'Baguette magique':14,
    'Paralysie ou pétrification':13,
    'Souffle du dragon':16,
    'Sceptre, baton ou sort':15
} if self.niveau <= 4 else {
    'Rayon mortel, poison':11,
    'Baguette magique':12,
    'Paralysie ou pétrification':11,
    'Souffle du dragon':14,
    'Sceptre, baton ou sort':13
} if self.niveau <= 8 else {
    'Rayon mortel, poison':9,
    'Baguette magique':10,
    'Paralysie ou pétrification':9,
    'Souffle du dragon':12,
    'Sceptre, baton ou sort':11
} if self.niveau <= 12 else {
    'Rayon mortel, poison':7,
    'Baguette magique':8,
    'Paralysie ou pétrification':7,
    'Souffle du dragon':10,
    'Sceptre, baton ou sort':9
} if self.niveau <= 16 else {
    'Rayon mortel, poison':5,
    'Baguette magique':6,
    'Paralysie ou pétrification':5,
    'Souffle du dragon':8,
    'Sceptre, baton ou sort':7
}

class Guerrier(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe='guerrier')
        self.jp = {
    'Rayon mortel, poison':12,
    'Baguette magique':13,
    'Paralysie ou pétrification':14,
    'Souffle du dragon':15,
    'Sceptre, baton ou sort':16
} if self.niveau <= 3 else {
    'Rayon mortel, poison':10,
    'Baguette magique':11,
    'Paralysie ou pétrification':12,
    'Souffle du dragon':13,
    'Sceptre, baton ou sort':14
} if self.niveau <= 6 else {
    'Rayon mortel, poison':8,
    'Baguette magique':9,
    'Paralysie ou pétrification':10,
    'Souffle du dragon':11,
    'Sceptre, baton ou sort':12
} if self.niveau <= 9 else {
    'Rayon mortel, poison':6,
    'Baguette magique':7,
    'Paralysie ou pétrification':8,
    'Souffle du dragon':9,
    'Sceptre, baton ou sort':10
} if self.niveau <= 12 else {
    'Rayon mortel, poison':6,
    'Baguette magique':6,
    'Paralysie ou pétrification':7,
    'Souffle du dragon':8,
    'Sceptre, baton ou sort':9
}

class Clerc(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe='clerc')
        self.culte = 'Balgor' if self.alignement in ('LL','LN') else 'Idriss' if self.alignement in ('NL', 'NN', 'NC') else 'Chardros'
        self.jp = {
    'Rayon mortel, poison':11,
    'Baguette magique':12,
    'Paralysie ou pétrification':14,
    'Souffle du dragon':16,
    'Sceptre, baton ou sort':15
} if self.niveau <= 4 else {
    'Rayon mortel, poison':9,
    'Baguette magique':10,
    'Paralysie ou pétrification':12,
    'Souffle du dragon':14,
    'Sceptre, baton ou sort':13
} if self.niveau <= 8 else {
    'Rayon mortel, poison':7,
    'Baguette magique':8,
    'Paralysie ou pétrification':10,
    'Souffle du dragon':12,
    'Sceptre, baton ou sort':11
} if self.niveau <= 12 else {
    'Rayon mortel, poison':6,
    'Baguette magique':7,
    'Paralysie ou pétrification':8,
    'Souffle du dragon':10,
    'Sceptre, baton ou sort':9
} if self.niveau <= 16 else {
    'Rayon mortel, poison':5,
    'Baguette magique':6,
    'Paralysie ou pétrification':6,
    'Souffle du dragon':8,
    'Sceptre, baton ou sort':7
}
        
class Mage(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'mage')
        self.jp = {
    'Rayon mortel, poison':13,
    'Baguette magique':14,
    'Paralysie ou pétrification':13,
    'Souffle du dragon':16,
    'Sceptre, baton ou sort':15
} if self.niveau <= 5 else {
    'Rayon mortel, poison':11,
    'Baguette magique':12,
    'Paralysie ou pétrification':11,
    'Souffle du dragon':14,
    'Sceptre, baton ou sort':12
} if self.niveau <= 10 else {
    'Rayon mortel, poison':9,
    'Baguette magique':10,
    'Paralysie ou pétrification':9,
    'Souffle du dragon':12,
    'Sceptre, baton ou sort':9
} if self.niveau <= 15 else {
    'Rayon mortel, poison':7,
    'Baguette magique':8,
    'Paralysie ou pétrification':7,
    'Souffle du dragon':10,
    'Sceptre, baton ou sort':6
} if self.niveau <= 20 else {
    'Rayon mortel, poison':5,
    'Baguette magique':6,
    'Paralysie ou pétrification':5,
    'Souffle du dragon':8,
    'Sceptre, baton ou sort':4
}

class Nain(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'nain')
        self.clan = random.choice(['Poing Sanglant','Arche de Jade', 'Forge de Roïd'])
        self.jp = {
    'Rayon mortel, poison':8,
    'Baguette magique':9,
    'Paralysie ou pétrification':10,
    'Souffle du dragon':13,
    'Sceptre, baton ou sort':12
} if self.niveau <= 3 else {
    'Rayon mortel, poison':6,
    'Baguette magique':7,
    'Paralysie ou pétrification':8,
    'Souffle du dragon':10,
    'Sceptre, baton ou sort':9
} if self.niveau <= 6 else {
    'Rayon mortel, poison':4,
    'Baguette magique':5,
    'Paralysie ou pétrification':6,
    'Souffle du dragon':7,
    'Sceptre, baton ou sort':6
} if self.niveau <= 9 else {
    'Rayon mortel, poison':2,
    'Baguette magique':3,
    'Paralysie ou pétrification':4,
    'Souffle du dragon':4,
    'Sceptre, baton ou sort':3
} 

class Elfe(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'elfe')
        self.clan = random.choice(['Croix Verte', 'Trèfle rouge', 'Flamme d\'or'])
        self.jp = {
    'Rayon mortel, poison':12,
    'Baguette magique':13,
    'Paralysie ou pétrification':13,
    'Souffle du dragon':15,
    'Sceptre, baton ou sort':15
} if self.niveau <= 3 else {
    'Rayon mortel, poison':8,
    'Baguette magique':10,
    'Paralysie ou pétrification':10,
    'Souffle du dragon':11,
    'Sceptre, baton ou sort':11
} if self.niveau <= 6 else {
    'Rayon mortel, poison':4,
    'Baguette magique':7,
    'Paralysie ou pétrification':7,
    'Souffle du dragon':7,
    'Sceptre, baton ou sort':7
} if self.niveau <= 9 else {
    'Rayon mortel, poison':2,
    'Baguette magique':4,
    'Paralysie ou pétrification':4,
    'Souffle du dragon':3,
    'Sceptre, baton ou sort':3
} 

class Petite_gens(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'petite-gens')
        self.alignement = random.choice(['LL','LN','NL','NN'])
        self.clan = random.choice(['Huttes Jumelles'])
        self.jp = {
    'Rayon mortel, poison':8,
    'Baguette magique':9,
    'Paralysie ou pétrification':10,
    'Souffle du dragon':13,
    'Sceptre, baton ou sort':12
} if self.niveau <= 3 else {
    'Rayon mortel, poison':5,
    'Baguette magique':6,
    'Paralysie ou pétrification':7,
    'Souffle du dragon':8,
    'Sceptre, baton ou sort':9
} if self.niveau <= 6 else {
    'Rayon mortel, poison':2,
    'Baguette magique':3,
    'Paralysie ou pétrification':4,
    'Souffle du dragon':5,
    'Sceptre, baton ou sort':4
} 

def generer_pnj_objet(nom, niveau, classe):
    # Factory function qui retourne l'objet au lieu d'afficher
    classe_map = {
        'voleur': Voleur, 'guerrier': Guerrier, 'clerc': Clerc,
        'mage': Mage, 'nain': Nain, 'elfe': Elfe, 'petite-gens': Petite_gens
    }
    
    # Création de l'instance
    pnj_class = classe_map.get(classe)
    pnj = pnj_class(nom, niveau)
    
    # Lancers de dés
    pnj.lancer_carac()
    pnj.define_pv()
    pnj.define_equipement_rare()
    pnj.define_ca()
    pnj.trait_de_caractere(pnj.alignement)
    
    return pnj


# ==========================================
# 3. INTERFACE STREAMLIT (MODE "PANIER")
# ==========================================

st.title("🛡️ Générateur de PNJ - D&D")

# --- Initialisation de la mémoire (Le Panier) ---
if 'file_attente' not in st.session_state:
    st.session_state.file_attente = []

# --- SIDEBAR (Configuration) ---
st.sidebar.header("1. Configurer un groupe")

# On utilise un formulaire pour ne pas recharger la page à chaque changement de chiffre
with st.sidebar.form("config_form"):
    classe_choisie = st.selectbox("Classe", classes_dispo)
    niveau_choisi = st.number_input("Niveau", 1, 20, 1)
    nb_pnj = st.number_input("Quantité", 1, 20, 1)
    
    # Options supplémentaires
    utiliser_nom_aleatoire = st.checkbox("Noms aléatoires ?", value=True)
    if not utiliser_nom_aleatoire:
        nom_base = st.text_input("Nom de base", "Inconnu")
    else:
        nom_base = "Aléatoire"

    # Bouton d'ajout
    bouton_ajout = st.form_submit_button("➕ Ajouter ce groupe")

if bouton_ajout:
    # On ajoute la commande dans la mémoire
    st.session_state.file_attente.append({
        'classe': classe_choisie,
        'niveau': niveau_choisi,
        'quantite': nb_pnj,
        'nom_base': nom_base,
        'auto_nom': utiliser_nom_aleatoire
    })
    st.success(f"Ajouté : {nb_pnj} {classe_choisie}(s) Niv.{niveau_choisi}")

# --- SIDEBAR (Affichage du Panier) ---
st.sidebar.markdown("---")
st.sidebar.header("2. File d'attente")

if len(st.session_state.file_attente) == 0:
    st.sidebar.info("Aucun groupe préparé.")
else:
    # On affiche la liste des commandes
    for i, cmd in enumerate(st.session_state.file_attente):
        st.sidebar.text(f"{i+1}. {cmd['quantite']}x {cmd['classe']} (Niv.{cmd['niveau']})")
    
    # Bouton pour vider si on s'est trompé
    if st.sidebar.button("🗑️ Tout effacer"):
        st.session_state.file_attente = []
        st.rerun()

# --- ZONE PRINCIPALE (Génération) ---

# Le bouton pour lancer tout ce qu'il y a dans la file d'attente
if st.button("🎲 GÉNÉRER TOUTE LA LISTE", type="primary"):
    
    if not st.session_state.file_attente:
        st.error("Ajoute d'abord des groupes dans la barre latérale !")
    
    else:
        # On boucle sur chaque groupe de la file d'attente
        for cmd in st.session_state.file_attente:
            
            st.markdown(f"### ⚔️ Groupe : {cmd['quantite']} {cmd['classe'].capitalize()}(s) Niveau {cmd['niveau']}")
            
            # Création des colonnes pour ce groupe spécifique
            cols = st.columns(min(cmd['quantite'], 3))
            
            # On boucle pour créer le nombre de PNJ demandé dans ce groupe
            for i in range(cmd['quantite']):
                
                # Gestion du nom
                if cmd['auto_nom']:
                    nom_final = generer_nom_fantasy(cmd['classe'])
                else:
                    nom_final = f"{cmd['nom_base']} {i+1}" if cmd['quantite'] > 1 else cmd['nom_base']
                
                # Création
                hero = generer_pnj_objet(nom_final, cmd['niveau'], cmd['classe'])
                
                # Affichage
                # On utilise cols[i % 3] pour remplir les colonnes grille par grille
                # Affichage
                with cols[i % 3].container(border=True):
                    st.subheader(f"👤 {hero.nom}")
                    
                    # Détails (Alignement, Guilde...)
                    st.info(f"🧠 **{hero.caractere}**")
                    details = f"Alignement : **{hero.alignement}**"
                    if hasattr(hero, 'guilde'): details += f" | Guilde : **{hero.guilde}**"
                    if hasattr(hero, 'culte'): details += f" | Culte : **{hero.culte}**"
                    if hasattr(hero, 'clan'): details += f" | Clan : **{hero.clan}**"
                    st.markdown(details)
                    
                    # Métriques principales (PV, CA, PO)
                    c1, c2, c3 = st.columns(3)
                    c1.metric("❤️ PV", hero.pv)
                    c2.metric("🛡️ CA", hero.ca)
                    c3.metric("💰 PO", hero.po)
                    
                    st.divider() # Petite ligne de séparation
                    
                    # ---  CARACTÉRISTIQUES EN COLONNES ---
                    with st.expander("📊 Caractéristiques", expanded=True): 
                        # expanded=True permet de le laisser ouvert par défaut (change en False pour fermer)
                        
                        s1, s2, s3, s4, s5, s6 = st.columns(6)
                        
                        # On affiche chaque stat dans sa petite colonne
                        # hero.carac est un dictionnaire {'F': '18(+3)', ...}
                        s1.markdown(f"**FOR**<br>{hero.carac['F']}", unsafe_allow_html=True)
                        s2.markdown(f"**INT**<br>{hero.carac['I']}", unsafe_allow_html=True)
                        s3.markdown(f"**SAG**<br>{hero.carac['S']}", unsafe_allow_html=True)
                        s4.markdown(f"**DEX**<br>{hero.carac['D']}", unsafe_allow_html=True)
                        s5.markdown(f"**CON**<br>{hero.carac['C']}", unsafe_allow_html=True)
                        s6.markdown(f"**CHA**<br>{hero.carac['Ch']}", unsafe_allow_html=True)

                    # --- INVENTAIRE ---
                    with st.expander("🎒 Inventaire"):
                        if hero.equipement_classique:
                            st.write(f"**Base:** {hero.equipement_classique}")
                        
                        # On affiche seulement si la liste n'est pas vide
                        if hero.equipement_rare_offensif: 
                            st.info(f"⚔️ **Off:** {hero.equipement_rare_offensif}")
                        
                        if hero.equipement_rare_defensif: 
                            st.success(f"🛡️ **Def:** {hero.equipement_rare_defensif}")
                        
                        if hero.equipement_rare_general: 
                            st.warning(f"✨ **Obj:** {hero.equipement_rare_general}")
                    
                    # --- JETS DE PROTECTION ---
                    with st.expander("🛡️ Jets de Protection"):
                        
                        # Sécurité : on vérifie si le dico 'jp' existe
                        if hasattr(hero, 'jp'):
                            
                            c1, c2, c3, c4, c5 = st.columns(5)
                            
                            # Fonction locale pour afficher joliment (Icône + Label court + Valeur)
                            def afficher_stat(colonne, icone, label_court, cle_dico):
                                valeur = hero.jp.get(cle_dico, "-")
                                # On utilise du HTML pour centrer et grossir le chiffre
                                colonne.markdown(f"""
                                    <div style="text-align: center;">
                                        <div style="font-size: 20px;">{icone}</div>
                                        <div style="font-size: 10px; color: grey;">{label_court}</div>
                                        <div style="font-size: 22px; font-weight: bold;">{valeur}</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                            # --- MAPPING ---
                            # On associe tes clés longues à l'affichage colonne
                            
                            # 1. Mort / Poison
                            afficher_stat(c1, "☠️", "R.Mort/Poison", 'Rayon mortel, poison')
                            
                            # 2. Baguettes
                            afficher_stat(c2, "🪄", "Baguettes", 'Baguette magique')
                            
                            # 3. Paralysie
                            afficher_stat(c3, "🗿", "Paralysie", 'Paralysie ou pétrification')
                            
                            # 4. Souffle
                            afficher_stat(c4, "🐲", "Souffle", 'Souffle du dragon')
                            
                            # 5. Sorts
                            afficher_stat(c5, "✨", "Sorts", 'Sceptre, baton ou sort')
                            
                        else:
                            st.warning("Pas de jets de protection définis.")