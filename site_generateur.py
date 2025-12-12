import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. DONNÉES & CONFIGURATION
# ==========================================

st.set_page_config(page_title="Générateur PNJ D&D", page_icon="🐉", layout="wide")

# Initialisation des états (Mémoire)
if 'favoris' not in st.session_state: st.session_state.favoris = []
if 'file_attente' not in st.session_state: st.session_state.file_attente = []
if 'resultats_temporaires' not in st.session_state: st.session_state.resultats_temporaires = []

classes_dispo = ['voleur','guerrier','mage','clerc','nain','elfe','petite-gens']

# --- DICTIONNAIRES D'ÉQUIPEMENT ---
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

# Assemblage des dictionnaires
equip_par_classe_niv_1_a_6 = {k: [equip_def_niv_1_a_6.get(k,[]), equip_gen_niv_1_a_6.get(k,[]), equip_off_niv_1_a_6.get(k,[])] for k in classes_dispo}
equip_par_classe_niv_7_ou_plus = {k: [equip_def_niv_7_ou_plus.get(k,[]), equip_gen_niv_7_ou_plus.get(k,[]), equip_off_niv_7_ou_plus.get(k,[])] for k in classes_dispo}


# ==========================================
# 2. LOGIQUE MÉTIER
# ==========================================

def generer_nom_fantasy(classe_pnj):
    syllabes = {
        'humain': {'debut': ['Al', 'Breg', 'Cal', 'Dar', 'El', 'Fen', 'Gor', 'Hald'], 'fin': ['aric', 'on', 'en', 'or', 'an', 'in', 'us']},
        'elfe': {'debut': ['Ael', 'Cael', 'Elar', 'Faen', 'Gala', 'Ilan'], 'fin': ['a', 'as', 'ian', 'ion', 'wyn', 'thil']},
        'nain': {'debut': ['Bal', 'Bof', 'Dor', 'Dwal', 'Thor', 'Thra'], 'fin': ['in', 'ur', 'ar', 'or', 'ik', 'ok']},
        'petite-gens': {'debut': ['Bil', 'Bung', 'Dro', 'Fro', 'Mer', 'Pip'], 'fin': ['bo', 'do', 'go', 'lo', 'mo', 'wise']}
    }
    classe_pnj = classe_pnj.lower()
    cat = 'elfe' if 'elfe' in classe_pnj else 'nain' if 'nain' in classe_pnj else 'petite-gens' if 'petite' in classe_pnj else 'humain'
    return random.choice(syllabes[cat]['debut']) + random.choice(syllabes[cat]['fin'])

def lancer_pv(classe:str, nb_dés:int, modificateur=0):
    resultat=0
    classe = classe.lower().strip()
    for i in range(nb_dés):
        if classe in ('voleur', 'mage'): resultat += (random.randint(1,4) + modificateur)
        elif classe in ('guerrier', 'nain'): resultat += (random.randint(1,8) + modificateur)
        elif classe in ('clerc', 'elfe', 'petite-gens'): resultat += (random.randint(1,6) + modificateur)
    if resultat <= 0: resultat = 1
    return resultat

def lancers_bonus(classe:str, carac:dict):
    mapping = {
        'voleur': lambda c : c.update({'D':c['D']+random.randint(1,4)}),
        'guerrier': lambda c : c.update({'F':c['F']+random.randint(1,4)}),
        'mage': lambda c : c.update({'I':c['I']+random.randint(1,4)}),
        'clerc': lambda c : c.update({'S':c['S']+random.randint(1,4)}),
        'nain': lambda c : c.update({'F':c['F']+random.randint(1,2), 'C':c['C']+random.randint(1,2)}),
        'elfe': lambda c : c.update({'I': c['I']+random.randint(1,2), 'S':c['S']+random.randint(1,2)}),
        'petite-gens': lambda c : c.update({'C':c['C']+random.randint(1,2), 'Ch':c['Ch']+random.randint(1,2)})
    }
    mapping.get(classe, lambda c: None)(carac)
    return carac

def lancer_carac(classe:str):
    carac = {k:0 for k in ['F','I','S','D','C','Ch']}
    for i in carac: carac[i] = sum(random.randint(1,6) for _ in range(3))
        
    carac = lancers_bonus(classe, carac)
    modif_constitution = 0
    
    for i in carac:
        val = carac[i]
        bonus = 0
        if val == 22: bonus = 5
        elif val >= 20: bonus = 4
        elif val >= 18: bonus = 3
        elif val >= 16: bonus = 2
        elif val >= 14: bonus = 1
        elif val <= 3: bonus = -3
        elif val <= 5: bonus = -2
        elif val <= 8: bonus = -1

        if i == 'C': modif_constitution = bonus
        
        signe = "+" if bonus > 0 else ""
        carac[i] = f"{val}({signe}{bonus})" if bonus != 0 else str(val)

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
        self.equipement_classique = list(equip_classique[self.classe]) # Copie liste
        self.po = self.niveau*random.randint(100, 300)
        self.carac = {}
        self.jp = {}
        self.modif_constitution = 0
        self.pv = 0
        self.ca = 0

    def trait_de_caractere(self, alignement:str):
        mapping = {
            'LL': ['Psychorigide', 'Dévoué', 'Honnête'], 'LN': ['Pragmatique', 'Impartial'],
            'NL': ['Tempéré', 'Déprimé'], 'NN': ['Indépendant', 'Imprévisible'],
            'NC': ['Libre penseur', 'Joueur'], 'CN': ['Bon vivant', 'Imprudent'],
            'CC': ['Égoïste', 'Destructeur']
        }
        traits = mapping.get(alignement, ['Neutre'])
        self.caractere = ' - '.join(random.sample(traits, min(2, len(traits))))

    def lancer_stats_completes(self):
        self.carac, self.modif_constitution = lancer_carac(self.classe)
        self.define_pv()
        self.define_equipement_rare()
        self.define_ca()
        self.trait_de_caractere(self.alignement)

    def define_pv(self):
        self.pv = lancer_pv(self.classe, self.niveau + 1 if self.niveau<=9 else 10, self.modif_constitution)
        if self.niveau>9: self.pv += (self.niveau - 9)*(1+self.modif_constitution)

    def define_equipement_rare(self):
        source = equip_par_classe_niv_1_a_6[self.classe] if self.niveau <= 6 else equip_par_classe_niv_7_ou_plus[self.classe]
        nb_items = 2 if self.niveau <= 6 else 3
        
        chance = {k: random.randint(1,100) for k in ['off','def','gen']}
        if chance['off'] <= 20: self.equipement_rare_offensif.extend(random.sample(source[2], nb_items))
        if chance['def'] <= 20: self.equipement_rare_defensif.extend(random.sample(source[0], nb_items))
        if chance['gen'] <= 20: self.equipement_rare_general.extend(random.sample(source[1], nb_items))
        
        self.equipement_rare_offensif = ' - '.join(self.equipement_rare_offensif)
        self.equipement_rare_defensif = ' - '.join(self.equipement_rare_defensif)
        self.equipement_rare_general = ' - '.join(self.equipement_rare_general)
        self.equipement_classique = ' - '.join(self.equipement_classique)

    def define_ca(self):
        base_ca = {'guerrier':3, 'nain':3, 'clerc':4, 'mage':4, 'elfe':2, 'petite-gens':2, 'voleur':6}
        self.ca = base_ca.get(self.classe, 9)
        if self.equipement_rare_defensif:
            for i in self.equipement_rare_defensif.split(' - '):
                if '+' in i:
                    try: self.ca -= int(i.split('+')[1].split()[0])
                    except: continue

# --- Sous-classes (avec la logique des JP incluse) ---
class Voleur(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'voleur')
        self.guilde = random.choice(['Specularium','Kelven'])
        if self.niveau<=4: self.jp={'Mort':13,'Baguettes':14,'Paralysie':13,'Souffle':16,'Sorts':15}
        elif self.niveau<=8: self.jp={'Mort':11,'Baguettes':12,'Paralysie':11,'Souffle':14,'Sorts':13}
        else: self.jp={'Mort':9,'Baguettes':10,'Paralysie':9,'Souffle':12,'Sorts':11}

class Guerrier(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'guerrier')
        if self.niveau<=3: self.jp={'Mort':12,'Baguettes':13,'Paralysie':14,'Souffle':15,'Sorts':16}
        elif self.niveau<=6: self.jp={'Mort':10,'Baguettes':11,'Paralysie':12,'Souffle':13,'Sorts':14}
        else: self.jp={'Mort':8,'Baguettes':9,'Paralysie':10,'Souffle':11,'Sorts':12}

class Clerc(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'clerc')
        self.culte = 'Idriss'
        if self.niveau<=4: self.jp={'Mort':11,'Baguettes':12,'Paralysie':14,'Souffle':16,'Sorts':15}
        elif self.niveau<=8: self.jp={'Mort':9,'Baguettes':10,'Paralysie':12,'Souffle':14,'Sorts':13}
        else: self.jp={'Mort':7,'Baguettes':8,'Paralysie':10,'Souffle':12,'Sorts':11}

class Mage(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'mage')
        if self.niveau<=5: self.jp={'Mort':13,'Baguettes':14,'Paralysie':13,'Souffle':16,'Sorts':15}
        elif self.niveau<=10: self.jp={'Mort':11,'Baguettes':12,'Paralysie':11,'Souffle':14,'Sorts':12}
        else: self.jp={'Mort':9,'Baguettes':10,'Paralysie':9,'Souffle':12,'Sorts':9}

class Nain(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'nain')
        if self.niveau<=3: self.jp={'Mort':8,'Baguettes':9,'Paralysie':10,'Souffle':13,'Sorts':12}
        elif self.niveau<=6: self.jp={'Mort':6,'Baguettes':7,'Paralysie':8,'Souffle':10,'Sorts':9}
        else: self.jp={'Mort':4,'Baguettes':5,'Paralysie':6,'Souffle':7,'Sorts':6}

class Elfe(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'elfe')
        if self.niveau<=3: self.jp={'Mort':12,'Baguettes':13,'Paralysie':13,'Souffle':15,'Sorts':15}
        elif self.niveau<=6: self.jp={'Mort':8,'Baguettes':10,'Paralysie':10,'Souffle':11,'Sorts':11}
        else: self.jp={'Mort':4,'Baguettes':7,'Paralysie':7,'Souffle':7,'Sorts':7}

class Petite_gens(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'petite-gens')
        if self.niveau<=3: self.jp={'Mort':8,'Baguettes':9,'Paralysie':10,'Souffle':13,'Sorts':12}
        elif self.niveau<=6: self.jp={'Mort':5,'Baguettes':6,'Paralysie':7,'Souffle':8,'Sorts':9}
        else: self.jp={'Mort':2,'Baguettes':3,'Paralysie':4,'Souffle':5,'Sorts':4}

def generer_pnj_objet(nom, niveau, classe):
    classe_map = {'voleur': Voleur, 'guerrier': Guerrier, 'clerc': Clerc, 'mage': Mage, 'nain': Nain, 'elfe': Elfe, 'petite-gens': Petite_gens}
    pnj = classe_map.get(classe, Guerrier)(nom, niveau)
    return pnj

# ==========================================
# 3. INTERFACE STREAMLIT
# ==========================================

st.title("🛡️ Générateur de PNJ - D&D")

# --- SIDEBAR: Config & Panier ---
st.sidebar.header("1. Configurer un groupe")
with st.sidebar.form("config_form"):
    classe = st.selectbox("Classe", classes_dispo)
    niveau = st.number_input("Niveau", 1, 20, 1)
    quantite = st.number_input("Quantité", 1, 20, 1)
    auto_nom = st.checkbox("Noms aléatoires ?", True)
    nom_base = st.text_input("Nom de base", "Inconnu") if not auto_nom else "Auto"
    
    if st.form_submit_button("➕ Ajouter ce groupe"):
        st.session_state.file_attente.append({
            'classe': classe, 'niveau': niveau, 'quantite': quantite,
            'nom_base': nom_base, 'auto_nom': auto_nom
        })
        st.success("Ajouté !")

st.sidebar.markdown("---")
st.sidebar.header(f"2. File d'attente ({len(st.session_state.file_attente)})")
if st.session_state.file_attente:
    for i, cmd in enumerate(st.session_state.file_attente):
        st.sidebar.text(f"{cmd['quantite']}x {cmd['classe']} (Niv.{cmd['niveau']})")
    if st.sidebar.button("🗑️ Vider File"):
        st.session_state.file_attente = []
        st.rerun()

# --- SIDEBAR: Favoris & Import/Export ---
st.sidebar.markdown("---")
st.sidebar.header(f"❤️ Favoris ({len(st.session_state.favoris)})")

# Export CSV
if st.session_state.favoris:
    data_exp = []
    for p in st.session_state.favoris:
        data_exp.append({
            "Nom": p.nom, "Classe": p.classe, "Niveau": p.niveau,
            "PV": p.pv, "CA": p.ca, "PO": p.po, "Alignement": p.alignement, "Caractère": p.caractere,
            "F": p.carac.get('F'), "I": p.carac.get('I'), "S": p.carac.get('S'),
            "D": p.carac.get('D'), "C": p.carac.get('C'), "Ch": p.carac.get('Ch'),
            "Eq_Base": p.equipement_classique,
            "Eq_Rare_Off": p.equipement_rare_offensif, "Eq_Rare_Def": p.equipement_rare_defensif, "Eq_Rare_Gen": p.equipement_rare_general
        })
    csv = pd.DataFrame(data_exp).to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("📥 Télécharger CSV", csv, "mes_pnj.csv", "text/csv")
    if st.sidebar.button("🗑️ Vider Favoris"):
        st.session_state.favoris = []
        st.rerun()

# Import CSV
st.sidebar.markdown("---")
st.sidebar.header("📂 Recharger")
fichier = st.sidebar.file_uploader("CSV", type=["csv"])
if fichier and st.sidebar.button("Valider Import"):
    try:
        df = pd.read_csv(fichier)
        for _, r in df.iterrows():
            pnj = generer_pnj_objet(r['Nom'], int(r['Niveau']), r['Classe'])
            pnj.pv, pnj.ca, pnj.po, pnj.alignement = int(r['PV']), int(r['CA']), int(r['PO']), r['Alignement']
            if pd.notna(r['Caractère']): pnj.caractere = r['Caractère']
            pnj.carac = {'F':str(r['F']), 'I':str(r['I']), 'S':str(r['S']), 'D':str(r['D']), 'C':str(r['C']), 'Ch':str(r['Ch'])}
            pnj.equipement_classique = str(r['Eq_Base'])
            pnj.equipement_rare_offensif = str(r['Eq_Rare_Off']) if pd.notna(r['Eq_Rare_Off']) else ""
            pnj.equipement_rare_defensif = str(r['Eq_Rare_Def']) if pd.notna(r['Eq_Rare_Def']) else ""
            pnj.equipement_rare_general = str(r['Eq_Rare_Gen']) if pd.notna(r['Eq_Rare_Gen']) else ""
            st.session_state.favoris.append(pnj)
        st.success("Rechargé !")
        st.rerun()
    except Exception as e: st.sidebar.error(f"Erreur: {e}")

# ==========================================
# 4. ZONE PRINCIPALE (GÉNÉRATION & AFFICHAGE)
# ==========================================

# A. BOUTON DE GÉNÉRATION
if st.button("🎲 GÉNÉRER TOUT", type="primary"):
    st.session_state.resultats_temporaires = []
    if not st.session_state.file_attente: st.error("Ajoute des groupes !")
    else:
        for cmd in st.session_state.file_attente:
            groupe = {'titre': f"⚔️ {cmd['quantite']} {cmd['classe']} Niv.{cmd['niveau']}", 'quantite': cmd['quantite'], 'pnjs': []}
            for i in range(cmd['quantite']):
                nom = generer_nom_fantasy(cmd['classe']) if cmd['auto_nom'] else f"{cmd['nom_base']} {i+1}"
                hero = generer_pnj_objet(nom, cmd['niveau'], cmd['classe'])
                hero.lancer_stats_completes()
                groupe['pnjs'].append(hero)
            st.session_state.resultats_temporaires.append(groupe)

# B. AFFICHAGE DES NOUVEAUX RÉSULTATS (TEMPORAIRES)
if st.session_state.resultats_temporaires:
    for i_grp, grp in enumerate(st.session_state.resultats_temporaires):
        st.markdown(f"### {grp['titre']}")
        cols = st.columns(min(grp['quantite'], 3))
        for i_hero, hero in enumerate(grp['pnjs']):
            with cols[i_hero % 3].container(border=True):
                st.subheader(hero.nom)
                st.info(f"🧠 {hero.caractere}")
                
                # --- AJOUT : DÉTAILS RP (Alignement, Clan, Guilde...) ---
                details = f"⚖️ **Alignement :** {hero.alignement}"
                # On vérifie dynamiquement si l'attribut existe pour l'afficher
                if getattr(hero, 'guilde', None): details += f"  \n🗡️ **Guilde :** {hero.guilde}"
                if getattr(hero, 'clan', None):   details += f"  \n🌲 **Clan :** {hero.clan}"
                if getattr(hero, 'culte', None):  details += f"  \n🙏 **Culte :** {hero.culte}"
                st.markdown(details)
                # -------------------------------------------------------

                c1, c2, c3 = st.columns(3)
                c1.metric("❤️ PV", hero.pv); c2.metric("🛡️ CA", hero.ca); c3.metric("💰 Or", hero.po)
                
                with st.expander("📊 Caractéristiques", expanded=True):
                    sc = st.columns(6)
                    for idx, k in enumerate(['F','I','S','D','C','Ch']):
                        sc[idx].markdown(f"<div style='text-align:center'><b>{k}</b><br><small>{hero.carac.get(k)}</small></div>", unsafe_allow_html=True)
                
                with st.expander("🛡️ Jets de protection"):
                    sj = st.columns(5)
                    for idx, (k, icon) in enumerate([('Mort','☠️'),('Baguettes','🪄'),('Paralysie','🗿'),('Souffle','🐲'),('Sorts','✨')]):
                        sj[idx].markdown(f"<div style='text-align:center;font-size:12px'>{icon}<br><b>{hero.jp.get(k,'-')}</b></div>", unsafe_allow_html=True)
                
                with st.expander("🎒 Inventaire"):
                    st.caption(f"Base: {hero.equipement_classique}")
                    if hero.equipement_rare_offensif: st.info(f"⚔️ **Off:** {hero.equipement_rare_offensif}")
                    if hero.equipement_rare_defensif: st.success(f"🛡️ **Def:** {hero.equipement_rare_defensif}")
                    if hero.equipement_rare_general: st.warning(f"✨ **Obj:** {hero.equipement_rare_general}")
                
                st.divider()
                
                stable_key = f"btn_save_{i_grp}_{i_hero}_{hero.nom}"
                if st.button("❤️ Sauvegarder", key=stable_key):
                    st.session_state.favoris.append(hero)
                    st.toast("Sauvegardé !", icon="✅")
                    st.rerun()

# C. AFFICHAGE DES PNJ SAUVEGARDÉS / IMPORTÉS (PERMANENTS)
if st.session_state.favoris:
    st.markdown("---")
    st.header(f"📂 PNJ Sauvegardés / Importés ({len(st.session_state.favoris)})")
    
    cols_fav = st.columns(3)
    
    for i, hero in enumerate(st.session_state.favoris):
        with cols_fav[i % 3].container(border=True):
            st.subheader(f"⭐ {hero.nom}")
            st.caption(f"{hero.classe.capitalize()} Niv.{hero.niveau}")
            st.info(f"🧠 {hero.caractere}")
            
            # --- AJOUT : DÉTAILS RP (Alignement, Clan, Guilde...) ---
            details = f"⚖️ **Alignement :** {hero.alignement}"
            if getattr(hero, 'guilde', None): details += f"  \n🗡️ **Guilde :** {hero.guilde}"
            if getattr(hero, 'clan', None):   details += f"  \n🌲 **Clan :** {hero.clan}"
            if getattr(hero, 'culte', None):  details += f"  \n🙏 **Culte :** {hero.culte}"
            st.markdown(details)
            # -------------------------------------------------------
            
            c1, c2, c3 = st.columns(3)
            c1.metric("❤️ PV", hero.pv); c2.metric("🛡️ CA", hero.ca); c3.metric("💰 Or", hero.po)
            
            with st.expander("📊 Caractéristiques", expanded=False):
                sc = st.columns(6)
                for idx, k in enumerate(['F','I','S','D','C','Ch']):
                    sc[idx].markdown(f"<div style='text-align:center'><b>{k}</b><br><small>{hero.carac.get(k)}</small></div>", unsafe_allow_html=True)
            
            with st.expander("🛡️ Jets de protection"):
                sj = st.columns(5)
                for idx, (k, icon) in enumerate([('Mort','☠️'),('Baguettes','🪄'),('Paralysie','🗿'),('Souffle','🐲'),('Sorts','✨')]):
                    sj[idx].markdown(f"<div style='text-align:center;font-size:12px'>{icon}<br><b>{hero.jp.get(k,'-')}</b></div>", unsafe_allow_html=True)
            
            with st.expander("🎒 Inventaire"):
                st.caption(f"Base: {hero.equipement_classique}")
                if hero.equipement_rare_offensif: st.info(f"⚔️ **Off:** {hero.equipement_rare_offensif}")
                if hero.equipement_rare_defensif: st.success(f"🛡️ **Def:** {hero.equipement_rare_defensif}")
                if hero.equipement_rare_general: st.warning(f"✨ **Obj:** {hero.equipement_rare_general}")
            
            st.divider()
            
            if st.button("❌ Supprimer", key=f"del_fav_{i}_{hero.nom}"):
                st.session_state.favoris.pop(i)
                st.rerun()