import streamlit as st
import pandas as pd
import random
import weakref
import streamlit.components.v1 as components


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
    modif_sagesse = 0
    
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
        if i == 'S': modif_sagesse = bonus
        
        signe = "+" if bonus > 0 else ""
        carac[i] = f"{val}({signe}{bonus})" if bonus != 0 else str(val)

    return carac, modif_constitution, modif_sagesse




def ajouter_raccourci_clavier():
    components.html("""
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        
        // --- 1. Raccourci GLOBAL : Touche 'P' pour Passer un Round ---
        // Ne fonctionne que si on N'EST PAS en train d'écrire dans un champ
        if (e.key.toLowerCase() === 'p') {
            if (doc.activeElement.tagName !== 'INPUT' && doc.activeElement.tagName !== 'TEXTAREA') {
                const buttons = doc.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText.includes('Passer un Round')) {
                        btn.click();
                    }
                });
            }
        }

        // --- 2. Raccourcis CONTEXTUELS : 'D' (Dégâts) et 'S' (Soins) ---
        // Ne fonctionnent QUE si on est dans un input (celui du montant PV)
        if (doc.activeElement.tagName === 'INPUT') {
            
            let keyword = null;
            if (e.key.toLowerCase() === 'd') keyword = 'Dégâts';
            if (e.key.toLowerCase() === 's') keyword = 'Soins';

            if (keyword) {
                // On cherche le bouton correspondant À CÔTÉ de l'input actif.
                // On remonte de quelques niveaux parents pour trouver le conteneur commun (le popover)
                let parent = doc.activeElement.parentElement;
                let foundBtn = null;
                
                // On remonte jusqu'à 6 niveaux max pour trouver le bouton voisin
                for(let i=0; i<6; i++) {
                    if(!parent) break;
                    
                    // On cherche le bouton dans ce parent
                    let potentialBtns = parent.querySelectorAll('button');
                    for(let btn of potentialBtns) {
                        if(btn.innerText.includes(keyword)) {
                            foundBtn = btn;
                            break;
                        }
                    }
                    if(foundBtn) break; // Trouvé !
                    parent = parent.parentElement; // Sinon on monte d'un cran
                }
                
                if(foundBtn) {
                    e.preventDefault(); // Empêche d'écrire la lettre 'd' ou 's' dans la case
                    foundBtn.click();
                }
            }
        }
    });
    </script>
    """, height=0, width=0)




class Effet:

    _instances = weakref.WeakSet()

    def __init__(self, duree_tours:int, nom:str, cible:Pnj):
        self.duree = duree_tours*3
        self.nom = nom
        self.effet = []
        Effet._instances.add(self)
        self.cible = cible
    
    def faire_effet(self):
        pass

    @classmethod
    def passer_round(cls):
        for effet in cls._instances:
            effet.duree -= 1
            if effet.duree <= 0:
                cls._instances.remove(effet)
            else:
                effet.faire_effet()




class AutreEffet(Effet):
    def __init__(self, duree:int, nom:str, description:str, cible:Pnj):
        super().__init__(duree, nom, cible)
        self.description = description
    



class Poison(Effet):

    def __init__(self, duree:int, nom:str, degats_p_round:int, cible:Pnj):
        super().__init__(duree, nom='Poison', cible=cible)
        self.degats_p_round = degats_p_round
    
    def faire_effet(self):
        self.cible.pv -= self.degats_p_round
        if self.cible.pv <= 0: 
            self.cible.pv = 0
            self.cible.vivant = False


class Paralysie(Effet):

    def __init__(self, duree:int, nom:str, cible:Pnj):
        super().__init__(duree, nom='Paralysie', cible=cible)
    

class Benediction(Effet):

    def __init__(self, duree:int, nom:str, cible:Pnj):
        super().__init__(duree, nom='Benediction', cible=cible)


class Invisibilité(Effet):

    def __init__(self, duree:int, nom:str, cible:Pnj):
        super().__init__(duree, nom='Invisibilité', cible=cible)











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
        self.equipement_classique = list(equip_classique[self.classe])
        self.po = self.po = self.niveau*random.randint(100, 300) if self.niveau <= 6 else self.niveau*random.randint(300, 700) if self.niveau <= 8 else self.niveau*random.randint(700, 1000) if self.niveau <= 10 else self.niveau*random.randint(2000, 2500)
        self.carac = {}
        self.jp = {}
        self.modif_constitution = 0
        self.modif_sagesse = 0
        self.pv = 0
        self.pv_max = 0
        self.vivant = True
        self.ca = 0
        self.effet = {}

    def trait_de_caractere(self, alignement:str):
        mapping = {
            'LL': ['Psychorigide', 'Veut être certain de n\'offenser personne', 'Dévoué à la garde', 'Honnête et fiable', 'Force tranquille', 'Amical et inspire le respect', 'Parano des chaotiques'],
            'LN': ['Inquiet d\'enfreindre les règles', 'Pragmatique', 'Impartial', 'Rieur', 'Parano des chaotiques'],
            'NL': ['Cherche à tempérer les plus loyaux que lui', 'déprimé face au chaos dans le monde', 'Suit les règles si ça l\'arrange'],
            'NN': ['Un bon coup un mauvais coup', 'Équilibre avant tout', 'Indépendant', 'Imprévisible'],
            'NC': ['Adore les jeux d\'argent', 'Libre penseur', 'Se moque de tout le monde', 'Imprévisible'],
            'CN': ['Chaotique mais bon', 'Rackette les plus faible mais a peur des plus fort', 'Imprudent'],
            'CC': ['Aime tabasser les enfants', 'Égoïste', 'Destructeur', 'Imprévisible et dangereux', 'Religieux fou']
        }
        traits = mapping.get(alignement, ['Neutre'])
        self.caractere = ' - '.join(random.sample(traits, min(2, len(traits))))

    def lancer_stats_completes(self):
        self.carac, self.modif_constitution, self.modif_sagesse = lancer_carac(self.classe)
        self.define_pv()
        self.define_equipement_rare()
        self.define_ca()
        self.trait_de_caractere(self.alignement)

    def define_pv(self):
        self.pv = lancer_pv(self.classe, self.niveau + 1 if self.niveau<=9 else 10, self.modif_constitution)
        if self.niveau>9: self.pv += (self.niveau - 9)*(1+self.modif_constitution)
        if self.modif_constitution:
            self.pv-= self.modif_constitution
        self.pv_max = self.pv


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


    def recevoir_effet(self, effet:str, durée_tours:str):
        #faire un dict de mapping
        effet = effet.lower().strip()
        mapping_effet = {'poison': Poison, 'autre': AutreEffet, 'paralysie': Paralysie, 'benediction': Benediction, 'invisibilité': Invisibilité}

        e = {effet: mapping_effet[effet](durée_tours, effet, self)}
        self.effet.update(e)

    
    def nettoyage_effet(self):
        self.effet = {nom: obj for nom, obj in self.effet.items() if obj.duree > 0}
    
    def perdre_pv(self, nb_degats:int):
        self.pv -= nb_degats
        if self.pv <= 0: 
            self.pv = 0
            self.vivant = False

    def gagner_pv(self, nb_pv_soignés):
        self.pv += nb_pv_soignés
        if self.pv > self.pv_max: self.pv = self.pv_max







# --- Sous-classes (avec la logique des JP incluse) ---
class Voleur(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'voleur')
        self.guilde = random.choice(['Specularium','Kelven'])
        self.alignement = random.choice(['CC','CN', 'NC', 'NN'])
        self.jp = {'Rayon mortel, poison':13, 'Baguette magique':14, 'Paralysie ou pétrification':13, 'Souffle du dragon':16, 'Sceptre, baton ou sort':15} if self.niveau <= 4 else {'Rayon mortel, poison':11, 'Baguette magique':12, 'Paralysie ou pétrification':11, 'Souffle du dragon':14, 'Sceptre, baton ou sort':13} if self.niveau <= 8 else {'Rayon mortel, poison':9, 'Baguette magique':10, 'Paralysie ou pétrification':9, 'Souffle du dragon':12, 'Sceptre, baton ou sort':11} if self.niveau <= 12 else {'Rayon mortel, poison':7, 'Baguette magique':8, 'Paralysie ou pétrification':7, 'Souffle du dragon':10, 'Sceptre, baton ou sort':9} if self.niveau <= 16 else {'Rayon mortel, poison':5, 'Baguette magique':6, 'Paralysie ou pétrification':5, 'Souffle du dragon':8, 'Sceptre, baton ou sort':7}

class Guerrier(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'guerrier')
        self.jp = {'Rayon mortel, poison':12, 'Baguette magique':13, 'Paralysie ou pétrification':14, 'Souffle du dragon':15, 'Sceptre, baton ou sort':16} if self.niveau <= 3 else {'Rayon mortel, poison':10, 'Baguette magique':11, 'Paralysie ou pétrification':12, 'Souffle du dragon':13, 'Sceptre, baton ou sort':14} if self.niveau <= 6 else {'Rayon mortel, poison':8, 'Baguette magique':9, 'Paralysie ou pétrification':10, 'Souffle du dragon':11, 'Sceptre, baton ou sort':12} if self.niveau <= 9 else {'Rayon mortel, poison':6, 'Baguette magique':7, 'Paralysie ou pétrification':8, 'Souffle du dragon':9, 'Sceptre, baton ou sort':10} if self.niveau <= 12 else {'Rayon mortel, poison':6, 'Baguette magique':6, 'Paralysie ou pétrification':7, 'Souffle du dragon':8, 'Sceptre, baton ou sort':9}

class Clerc(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'clerc')
        self.culte = 'Idriss' if self.alignement in ('NC','NN', 'NL') else 'Chardros' if self.alignement in ('CC', 'CN') else 'Balgor'
        self.jp = {'Rayon mortel, poison':11, 'Baguette magique':12, 'Paralysie ou pétrification':14, 'Souffle du dragon':16, 'Sceptre, baton ou sort':15} if self.niveau <= 4 else {'Rayon mortel, poison':9, 'Baguette magique':10, 'Paralysie ou pétrification':12, 'Souffle du dragon':14, 'Sceptre, baton ou sort':13} if self.niveau <= 8 else {'Rayon mortel, poison':7, 'Baguette magique':8, 'Paralysie ou pétrification':10, 'Souffle du dragon':12, 'Sceptre, baton ou sort':11} if self.niveau <= 12 else {'Rayon mortel, poison':6, 'Baguette magique':7, 'Paralysie ou pétrification':8, 'Souffle du dragon':10, 'Sceptre, baton ou sort':9} if self.niveau <= 16 else {'Rayon mortel, poison':5, 'Baguette magique':6, 'Paralysie ou pétrification':6, 'Souffle du dragon':8, 'Sceptre, baton ou sort':7}

class Mage(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'mage')
        self.jp = {'Rayon mortel, poison':13, 'Baguette magique':14, 'Paralysie ou pétrification':13, 'Souffle du dragon':16, 'Sceptre, baton ou sort':15} if self.niveau <= 5 else {'Rayon mortel, poison':11, 'Baguette magique':12, 'Paralysie ou pétrification':11, 'Souffle du dragon':14, 'Sceptre, baton ou sort':12} if self.niveau <= 10 else {'Rayon mortel, poison':9, 'Baguette magique':10, 'Paralysie ou pétrification':9, 'Souffle du dragon':12, 'Sceptre, baton ou sort':9} if self.niveau <= 15 else {'Rayon mortel, poison':7, 'Baguette magique':8, 'Paralysie ou pétrification':7, 'Souffle du dragon':10, 'Sceptre, baton ou sort':6} if self.niveau <= 20 else {'Rayon mortel, poison':5, 'Baguette magique':6, 'Paralysie ou pétrification':5, 'Souffle du dragon':8, 'Sceptre, baton ou sort':4}

class Nain(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'nain')
        self.jp = {'Rayon mortel, poison':8, 'Baguette magique':9, 'Paralysie ou pétrification':10, 'Souffle du dragon':13, 'Sceptre, baton ou sort':12} if self.niveau <= 3 else {'Rayon mortel, poison':6, 'Baguette magique':7, 'Paralysie ou pétrification':8, 'Souffle du dragon':10, 'Sceptre, baton ou sort':9} if self.niveau <= 6 else {'Rayon mortel, poison':4, 'Baguette magique':5, 'Paralysie ou pétrification':6, 'Souffle du dragon':7, 'Sceptre, baton ou sort':6} if self.niveau <= 9 else {'Rayon mortel, poison':2, 'Baguette magique':3, 'Paralysie ou pétrification':4, 'Souffle du dragon':4, 'Sceptre, baton ou sort':3}
        self.clan = random.choice(['Arche de jade', 'Poing sanglant', 'Forge de Roïd'])

class Elfe(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'elfe')
        self.jp = {'Rayon mortel, poison':12, 'Baguette magique':13, 'Paralysie ou pétrification':13, 'Souffle du dragon':15, 'Sceptre, baton ou sort':15} if self.niveau <= 3 else {'Rayon mortel, poison':8, 'Baguette magique':10, 'Paralysie ou pétrification':10, 'Souffle du dragon':11, 'Sceptre, baton ou sort':11} if self.niveau <= 6 else {'Rayon mortel, poison':4, 'Baguette magique':7, 'Paralysie ou pétrification':7, 'Souffle du dragon':7, 'Sceptre, baton ou sort':7} if self.niveau <= 9 else {'Rayon mortel, poison':2, 'Baguette magique':4, 'Paralysie ou pétrification':4, 'Souffle du dragon':3, 'Sceptre, baton ou sort':3}
        self.clan = random.choice(['Croix Verte', 'Trèfle Rouge', 'Flamme d\'Or'])

class Petite_gens(Pnj):
    def __init__(self, nom, niveau):
        super().__init__(nom, niveau, 'petite-gens')
        self.alignement = random.choice(['LL', 'LN', 'NL', 'NN'])
        self.jp = {'Rayon mortel, poison':8, 'Baguette magique':9, 'Paralysie ou pétrification':10, 'Souffle du dragon':13, 'Sceptre, baton ou sort':12} if self.niveau <= 3 else {'Rayon mortel, poison':5, 'Baguette magique':6, 'Paralysie ou pétrification':7, 'Souffle du dragon':8, 'Sceptre, baton ou sort':9} if self.niveau <= 6 else {'Rayon mortel, poison':2, 'Baguette magique':3, 'Paralysie ou pétrification':4, 'Souffle du dragon':5, 'Sceptre, baton ou sort':4}
        self.clan = random.choice(['Huttes Jumelles'])

def generer_pnj_objet(nom, niveau, classe):
    classe_map = {'voleur': Voleur, 'guerrier': Guerrier, 'clerc': Clerc, 'mage': Mage, 'nain': Nain, 'elfe': Elfe, 'petite-gens': Petite_gens}
    pnj = classe_map.get(classe, Guerrier)(nom, niveau)
    return pnj






#==========================================
# 3. INTERFACE STREAMLIT
# ==========================================


st.title("🛡️ Générateur de PNJ - D&D")


ajouter_raccourci_clavier()

col_time, col_info = st.columns([1, 4])
with col_time:
    # On fait passer un "Round" (la plus petite unité)
    if st.button("⏳ Passer un Round", type="primary", help="Fait avancer le temps de 1 Round."):
        
        # On utilise un set d'IDs (mémoire) pour ne pas traiter deux fois le même objet
        pnj_traites = set()
        
        # Fonction helper pour traiter une liste sans doublons
        def traiter_liste_pnj(liste_pnj):
            compteur_local = 0
            for pnj in liste_pnj:
                # Si on a déjà traité cet objet précis (id(pnj)), on passe
                if id(pnj) in pnj_traites:
                    continue
                
                # On marque cet objet comme traité
                pnj_traites.add(id(pnj))
                
                if pnj.vivant and hasattr(pnj, 'effet') and pnj.effet:
                    effets_actifs = list(pnj.effet.values())
                    for effet in effets_actifs:
                        effet.faire_effet() 
                        effet.duree -= 1 
                        compteur_local += 1
                    pnj.nettoyage_effet()
            return compteur_local

        # 1. Traitement des favoris
        compteur_effets = traiter_liste_pnj(st.session_state.favoris)
        
        # 2. Traitement des résultats temporaires
        if st.session_state.resultats_temporaires:
            for grp in st.session_state.resultats_temporaires:
                compteur_effets += traiter_liste_pnj(grp['pnjs'])
        
        if compteur_effets > 0:
            st.toast(f"Round terminé ! {compteur_effets} effets appliqués.", icon="⚔️")
        else:
            st.toast("Round terminé. Aucun effet actif.", icon="🕊️")
        
        st.rerun()

with col_info:
    st.info("ℹ️ **Rappel :** Utiliser **p** pour **passer un round**.")

st.divider()


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
        # Sécurisation des attributs pour l'export
        carac = p.carac if isinstance(p.carac, dict) else {}
        data_exp.append({
            "Nom": p.nom, "Classe": p.classe, "Niveau": p.niveau,
            "PV": p.pv, "PV_Max": getattr(p, 'pv_max', p.pv), 
            "CA": p.ca, "PO": p.po, "Alignement": p.alignement, "Caractère": p.caractere,
            "F": carac.get('F'), "I": carac.get('I'), "S": carac.get('S'),
            "D": carac.get('D'), "C": carac.get('C'), "Ch": carac.get('Ch'),
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
            # Récupération PV Max ou fallback sur PV actuels
            pnj.pv_max = int(r['PV_Max']) if 'PV_Max' in r else pnj.pv 
            
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

# Fonction centrale d'affichage d'une carte PNJ
def afficher_carte_pnj(hero, i, context_key):
    with st.container(border=True):
        # 1. En-tête et Statut
        col_titre, col_statut = st.columns([3, 1])
        
        with col_titre:
            # On divise le titre en 2 : Nom à gauche, Bouton modif à droite
            c_nom, c_edit = st.columns([5, 1])
            with c_nom:
                st.subheader(hero.nom)
            with c_edit:
                # Le petit bouton crayon qui ouvre un menu
                with st.popover("✏️", help="Modifier le nom"):
                    new_name = st.text_input("Nouveau nom", value=hero.nom, key=f"input_ren_{context_key}")
                    if st.button("Valider", key=f"btn_ren_{context_key}"):
                        hero.nom = new_name
                        st.rerun()
            
            st.caption(f"{hero.classe.capitalize()} Niv.{hero.niveau}")
            
        with col_statut:
            if hero.pv <= 0: st.markdown("💀 **MORT**")
            else: st.markdown("🟢 **VIVANT**")
        
        # 2. Détails RP
        details = f"⚖️ **Alignement :** {hero.alignement}"
        if getattr(hero, 'guilde', None): details += f"  \n🗡️ **Guilde :** {hero.guilde}"
        if getattr(hero, 'clan', None):   details += f"  \n🌲 **Clan :** {hero.clan}"
        if getattr(hero, 'culte', None):  details += f"  \n🙏 **Culte :** {hero.culte}"
        st.markdown(details)
        
        st.divider()

        # 3. Métriques
        # 3. Métriques (PV avec gestion manuelle)
        col_pv, col_ca, col_or = st.columns(3)
        
        # Colonne PV transformée
        with col_pv:
            st.metric("❤️ PV", f"{hero.pv}/{getattr(hero, 'pv_max', hero.pv)}")
            
            # Gestion manuelle des PV (Petit formulaire inline)
            # On utilise un popover (plus propre) ou un expander mini
            with st.popover("Modif. PV"):
                valeur_pv = st.number_input("Montant", min_value=0, value=0, key=f"input_pv_{context_key}")
                c_minus, c_plus = st.columns(2)
                if c_minus.button("➖ Dégâts", key=f"btn_degats_{context_key}"):
                    hero.perdre_pv(valeur_pv)
                    st.rerun()
                if c_plus.button("➕ Soins", key=f"btn_soins_{context_key}"):
                    hero.gagner_pv(valeur_pv)
                    st.rerun()

        col_ca.metric("🛡️ CA", hero.ca)
        col_or.metric("💰 Or", hero.po)
        
        # 4. Caractéristiques & Jets
        with st.expander("📊 Caractéristiques", expanded=False):
            sc = st.columns(6)
            for idx, k in enumerate(['F','I','S','D','C','Ch']):
                val = hero.carac.get(k) if isinstance(hero.carac, dict) else "?"
                sc[idx].markdown(f"<div style='text-align:center'><b>{k}</b><br><small>{val}</small></div>", unsafe_allow_html=True)
        
        with st.expander("🛡️ Jets de protection"):
            sj = st.columns(5)

            liste_jp = [
                ('Rayon mortel, poison', '☠️'),
                ('Baguette magique', '🪄'),
                ('Paralysie ou pétrification', '🗿'),
                ('Souffle du dragon', '🐲'),
                ('Sceptre, baton ou sort', '✨')
            ]
            for idx, (cle_exacte, icon) in enumerate(liste_jp):
                # On récupère la valeur avec la clé exacte
                valeur = hero.jp.get(cle_exacte, '-')
                sj[idx].markdown(f"<div style='text-align:center;font-size:12px'>{icon}<br><b>{valeur}</b></div>", unsafe_allow_html=True)
        
        with st.expander("🎒 Inventaire"):
            st.caption(f"Base: {hero.equipement_classique}")
            if hero.equipement_rare_offensif: st.info(f"⚔️ **Off:** {hero.equipement_rare_offensif}")
            if hero.equipement_rare_defensif: st.success(f"🛡️ **Def:** {hero.equipement_rare_defensif}")
            if hero.equipement_rare_general: st.warning(f"✨ **Obj:** {hero.equipement_rare_general}")

        # 5. GESTION DES EFFETS
        st.divider()
        st.markdown("🧪 **Effets Actifs**")
        
        if hasattr(hero, 'effet') and hero.effet:
            for nom_effet, obj_effet in list(hero.effet.items()):
                col_e1, col_e2 = st.columns([3, 1])
                # Affichage des rounds restants
                col_e1.text(f"• {nom_effet} (Reste: {obj_effet.duree} rounds)")
                if col_e2.button("🗑️", key=f"del_eff_{context_key}_{nom_effet}"):
                    del hero.effet[nom_effet]
                    st.rerun()
        else:
            st.caption("Aucun effet.")

        # Menu d'ajout d'effet
        with st.expander("➕ Ajouter un effet"):
            with st.form(key=f"form_effet_{context_key}"):
                # Choix du type
                choix_effet = st.selectbox("Type d'effet", ["Poison", "Autre", 'Invisibilité', 'Paralysie', 'Benediction'])
                
                # Saisie en TOURS (converti en rounds par la classe Effet)
                duree_tours = st.number_input("Durée (en Tours)", min_value=1, value=1, help="1 Tour = 3 Rounds")
                
                # Case Dégâts qui n'apparait (logiquement) que pour le Poison
                degats_input = 0
                if choix_effet == "Poison":
                    degats_input = st.number_input("Dégâts (par Round)", min_value=1, value=3, help='Ignorer si le sort ne fait pas de dégat')
                
                # Champs pour Autre
                st.caption("Si 'Autre' :")
                nom_custom = st.text_input("Nom de l'effet")
                desc_custom = st.text_input("Description")
                
                if st.form_submit_button("Appliquer"):
                    try:
                        if choix_effet == "Poison":
                            # On passe les dégâts choisis
                            nouvel_effet = Poison(duree=duree_tours, nom="Poison", degats_p_round=degats_input, cible=hero)
                            hero.effet["Poison"] = nouvel_effet

                        if choix_effet == "Invisibilité":
                            nouvel_effet = Invisibilité(duree=duree_tours, nom="Invisibilité", cible=hero)
                            hero.effet['Invisibilité'] = nouvel_effet

                        if choix_effet == 'Paralysie':
                            nouvel_effet = Paralysie(duree=duree_tours, nom="Paralysie", cible=hero)
                            hero.effet['Paralysie'] = nouvel_effet

                        if choix_effet == 'Benediction':
                            nouvel_effet = Benediction(duree=duree_tours, nom="Benediction", cible=hero)
                            hero.effet['Benediction'] = nouvel_effet


                        elif choix_effet == "Autre":
                            nom_final = nom_custom if nom_custom else "Inconnu"
                            nouvel_effet = AutreEffet(duree=duree_tours, nom=nom_final, description=desc_custom, cible=hero)
                            hero.effet[nom_final] = nouvel_effet
                        
                        st.toast(f"Effet ajouté ! (Durée : {duree_tours} tours)", icon="🧪")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur : {e}")

        st.divider()
        
        # 6. BOUTONS D'ACTION
        if "resultat" in context_key:
            if st.button("❤️ Sauvegarder", key=f"btn_save_{context_key}"):
                st.session_state.favoris.append(hero)
                st.toast("Sauvegardé !", icon="✅")
                st.rerun()
        else:
            if st.button("❌ Supprimer", key=f"btn_del_{context_key}"):
                st.session_state.favoris.pop(i)
                st.rerun()

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

# B. AFFICHAGE DES NOUVEAUX RÉSULTATS
if st.session_state.resultats_temporaires:
    for i_grp, grp in enumerate(st.session_state.resultats_temporaires):
        st.markdown(f"### {grp['titre']}")
        cols = st.columns(min(grp['quantite'], 3))
        for i_hero, hero in enumerate(grp['pnjs']):
            with cols[i_hero % 3]:
                afficher_carte_pnj(hero, i_hero, f"resultat_{i_grp}_{i_hero}_{hero.nom}")

# C. AFFICHAGE DES FAVORIS
if st.session_state.favoris:
    st.markdown("---")
    st.header(f"📂 PNJ Sauvegardés / Importés ({len(st.session_state.favoris)})")
    cols_fav = st.columns(3)
    for i, hero in enumerate(st.session_state.favoris):
        with cols_fav[i % 3]:
            afficher_carte_pnj(hero, i, f"fav_{i}_{hero.nom}")