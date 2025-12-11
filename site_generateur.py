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

def lancer_carac():
    carac = {'F':0, 'I':0, 'S':0, 'D':0, 'C':0, 'Ch':0}
    modif_constitution = 0

    for i in carac:
        carac[i]= random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
        if carac[i] ==18: carac[i] = '18(+3)'
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
        self.equipement_rare_offensif = []
        self.equipement_rare_defensif = []
        self.equipement_rare_general = []
        self.equipement_classique = equip_classique[self.classe]
        self.po = self.niveau*random.randint(200, 1000)
        self.carac = 0
        self.modif_constitution = 0
        self.pv = 0
        self.ca = 0

    def lancer_carac(self):
        self.carac, self.modif_constitution = lancer_carac()

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

class Guerrier(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe='guerrier')

class Clerc(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe='clerc')
        self.culte = 'Balgor' if self.alignement in ('LL','LN') else 'Idriss' if self.alignement in ('NL', 'NN', 'NC') else 'Chardros'

class Mage(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'mage')

class Nain(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'nain')
        self.clan = random.choice(['Poing Sanglant','Arche de Jade', 'Forge de Roïd'])

class Elfe(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'elfe')
        self.clan = random.choice(['Croix Verte', 'Trèfle rouge', 'Flamme d\'or'])

class Petite_gens(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, classe = 'petite-gens')
        self.alignement = random.choice(['LL','LN','NL','NN'])
        self.clan = random.choice(['Huttes Jumelles'])


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
    
    return pnj

# ==========================================
# 3. INTERFACE STREAMLIT
# ==========================================

st.title("🛡️ Générateur de PNJ - D&D")

# --- SIDEBAR (Entrées utilisateur) ---
st.sidebar.header("Paramètres")

nb_pnj = st.sidebar.number_input("Nombre de PNJ à créer", min_value=1, max_value=20, value=1)
utiliser_nom_aleatoire = st.sidebar.checkbox("Générer des noms aléatoires ?", value=True)

if not utiliser_nom_aleatoire:
    nom_base = st.sidebar.text_input("Nom manuel (ou base)", "Inconnu")
else:
    nom_base = "Aléatoire"

niveau_choisi = st.sidebar.number_input("Niveau", min_value=1, max_value=20, value=1)
classe_choisie = st.sidebar.selectbox("Classe", classes_dispo)

st.write(f"### Résultat : {nb_pnj} {classe_choisie.capitalize()}(s) niveau {niveau_choisi}")
    
cols = st.columns(min(nb_pnj, 3))
    
for i in range(nb_pnj):
        
        # --- LOGIQUE DE NOM ---
        if utiliser_nom_aleatoire:
            # On appelle le générateur
            nom_final = generer_nom_fantasy(classe_choisie)
        else:
            # On garde ton ancienne logique manuelle
            nom_final = f"{nom_base} {i+1}" if nb_pnj > 1 else nom_base
        
        # Création du PNJ avec le nom final
        hero = generer_pnj_objet(nom_final, niveau_choisi, classe_choisie)
        
        # Affichage propre dans un "Container"
        with st.container(border=True):
            st.subheader(f"👤 {hero.nom}")
            
            # Attributs spéciaux selon classe (Polymorphisme visuel)
            details = f"Alignement : **{hero.alignement}**"
            if hasattr(hero, 'guilde'): details += f" | Guilde : **{hero.guilde}**"
            if hasattr(hero, 'culte'): details += f" | Culte : **{hero.culte}**"
            if hasattr(hero, 'clan'): details += f" | Clan : **{hero.clan}**"
            st.markdown(details)
            
            # Métriques clés
            c1, c2, c3 = st.columns(3)
            c1.metric("PV", hero.pv)
            c2.metric("CA", hero.ca)
            c3.metric("Or (PO)", hero.po)
            
            # Caractéristiques
            st.markdown("---")
            st.markdown("**Caractéristiques :**")
            st.code(str(hero.carac).replace("{", "").replace("}", "").replace("'", ""))
            
            # Equipement dans des menus déroulants pour gagner de la place
            with st.expander("⚔️ Équipement & Inventaire"):
                st.markdown(f"**Classique:** {hero.equipement_classique}")
                if hero.equipement_rare_offensif:
                    st.markdown(f"**🔴 Offensif Rare:** {hero.equipement_rare_offensif}")
                if hero.equipement_rare_defensif:
                    st.markdown(f"**🛡️ Défensif Rare:** {hero.equipement_rare_defensif}")
                if hero.equipement_rare_general:
                    st.markdown(f"**✨ Général Rare:** {hero.equipement_rare_general}")