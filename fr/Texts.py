# fr
hp = 'PV'
mp = 'PM'
attack_stat = 'Attaque'
defense_stat = 'Défense'
base = 'Base'
plain = 'Plaine'
desert = 'Désert'
snow = 'Neige'
forest = 'Forêt'
mountain = 'Montagne'
volcano = 'Volcan'

attack = 'Attaque'
magic = 'Magie'
inventory = 'Inventaire'
leave = 'Abandon'
back = 'Retour'
attack_1 = 'Attaque 1'
attack_2 = 'Attaque 2'
attack_3 = 'Attaque 3'
attack_4 = 'Attaque 4'
magic_1 = 'Soin'
magic_2 = 'Bouclier'
magic_3 = 'Boost Déf.'
magic_4 = 'Boost Att.'
confirm = 'Confirmer'
use = 'Utiliser'
quantity = 'Quantité'

resume = 'REPRENDRE'
settings = 'PARAMETRES'
save = 'SAUVEGARDER'
quit_game = 'QUITTER'

select_action = "Sélectionnez une action."
select_attack = "Sélectionnez une attaque."
select_spell = "Sélectionnez un sort."
select_object = "Sélectionnez un objet."
description_attack = "Attaque 1 :|Coup d'épée basique. Inflige {} dégâts.|||Attaque 2 :|Fait saigner l'ennemi pendant 4 tours. Inflige {} dégâts. Total : {}.||Attaque 3 :|Attaque brutale. Inflige {} dégâts. Vous inflige en retour {} dégâts.||Attaque 4 :|Attaque spéciale. Basée en plus grande partie sur l'environnement de l'ennemi. Inflige {} dégâts."
description_magic = "Soin. Régénère 20% des PV max.|(+{})|Coût : 10 PM||Bouclier magique. Tous les dégâts subits lors de ce tour seront divisé par 1,5.|Coût : 10 PM||Boost de défense. Augmente la défense de base de {}. (Max : 1, 3)|Coût : 20 PM||Boost d'attaque. Augmente l'attaque de base de {}. (Max : 1, 3)|Coût : 25 PM"
description_object = [["Potion Soin (Minuscule)", 'Régénère 10 PV.|({})'],
                      ["Potion Soin (Petite)", "Régénère 20 PV.|({})"],
                      ["Potion Soin (Moyenne)", "Régénère 50 PV.|({})"],
                      ["Potion Soin (Grande)", "Régénère 100 PV.|({})"],
                      ["Potion Soin (Géante)", "Régénère tous les PV.|({})"],
                      #  5-9
                      ["Potion Mana (Minuscule)", "Régénère 5 PM."],
                      ["Potion Mana (Petite)", "Régénère 10 PM."],
                      ["Potion Mana (Moyenne)", "Régénère 15 PM."],
                      ["Potion Mana (Grande)", "Régénère 25 PM."],
                      ["Potion Mana (Géante)", "Régénère tous les PM."],
                      #  10-14
                      ["Boost Attaque Plaine", "Augmente l'attaque spéciale contre les ennemis d'environnement Plaine.||+15% × Attaque de base|(+{})"],
                      ["Boost Défense Plaine", "Augmente la défense spéciale contre les ennemis d'environnement Plaine.||+15% × Défense de base|(+{})"],
                      ["Boost Attaque Désert", "Augmente l'attaque spéciale contre les ennemis d'environnement Désert.||+15% × Attaque de base|(+{})"],
                      ["Boost Défense Désert", "Augmente la défense spéciale contre les ennemis d'environnement Désert.||+15% × Défense de base|(+{})"],
                      ["Boost Attaque Neige", "Augmente l'attaque spéciale contre les ennemis d'environnement Neige.||+15% × Attaque de base|(+{})"],
                      #  15-19
                      ["Boost Défense Neige", "Augmente la défense spéciale contre les ennemis d'environnement Neige.||+15% × Défense de base|(+{})"],
                      ["Boost Attaque Forêt", "Augmente l'attaque spéciale contre les ennemis d'environnement Forêt.||+15% × Attaque de base|(+{})"],
                      ["Boost Défense Forêt", "Augmente la défense spéciale contre les ennemis d'environnement Forêt.||+15% × Défense de base|(+{})"],
                      ["Boost Attaque Montagne", "Augmente l'attaque spéciale contre les ennemis d'environnement Montagne.||+15% × Attaque de base|(+{})"],
                      ["Boost Défense Montagne", "Augmente la défense spéciale contre les ennemis d'environnement Montagne.||+15% × Défense de base|(+{})"],
                      #  20-24
                      ["Boost Attaque Volcan", "Augmente l'attaque spéciale contre les ennemis d'environnement Volcan.||+15% × Attaque de base|(+{})"],
                      ["Boost Défense Volcan", "Augmente la défense spéciale contre les ennemis d'environnement Volcan.||+15% × Défense de base|(+{})"],
                      ["Boost Attaque Spéciale", "Augmente l'attaque spéciale contre les ennemis de tous les environnements.||+4% × Attaque de base|(+{})"],
                      ["Boost Défense Spéciale", "Augmente la défense spéciale contre les ennemis de tous les environnements.||+4% × Défense de base|(+{})"],
                      ["Boost Stats Spéciales", "Augmente l'attaque et la défense spéciales contre les ennemis de tous les environnements.||+3% × Attaque de base|(+{})|+3% × Défense de base|(+{})"],
                      #  25-29
                      ["Boost Stats Base",
                       "Augmente l'attaque et la défense de base.||+8% × Attaque de base|+8% × Défense de base"],
                      ["Boost PV max", "Augmente vos PV max.||+50|Max : +100"],
                      ["Boost PM max", "Augmente vos PM max.||+15|Max : +30"],
                      ["Boost Probabilité Critique", "Augmente la probabilité de réaliser un coup critique.||+5%"],
                      ["Boost Multiplicateur Critique", "Augmente le multiplicateur de dégâts en cas de coup critique.||+0,1"],
                      #  30-34
                      ["", "Diminue l'attaque de {}.||-10%|Min : "],
                      ["", ""],
                      ["", ""],
                      ["", ""],
                      ["", ""],
                      #  35
                      ["Boost Durée Attaque 2",
                       "Augmente d'un tour la durée de l'attaque 2. (Ne s'applique pas aux attaques déjà lancées."]]
