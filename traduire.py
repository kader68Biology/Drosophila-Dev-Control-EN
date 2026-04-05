#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de traduction automatique FR → EN - Version 2.0 (En place)
Préserve les noms de fichiers dans les liens
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict

class TraducteurHTML:
    def __init__(self):
        self.translations = self._charger_translations()
        self.stats = {'fichiers_traites': 0, 'remplacements': 0, 'erreurs': 0}
        
    def _charger_translations(self) -> Dict[str, str]:
        return {
            # NAVIGATION
            "Accueil": "Home",
            "Cours": "Courses",
            "Vidéo": "Video",
            "Vidéos": "Videos",
            "Documents": "Documents",
            "Activités": "Activities",
            "Activité": "Activity",
            "Contact": "Contact",
            
            # TITRES
            "Aspect Génétique du Développement Embryonnaire": "Genetic Aspects of Embryonic Development",
            "Aspects Génétiques du Développement Embryonnaire": "Genetic Aspects of Embryonic Development",
            "Maîtrisez les mécanismes du développement chez": "Master the mechanisms of development in",
            "Maîtrisez les mécanismes moléculaires chez": "Master the molecular mechanisms in",
            "Génétique du Développement": "Developmental Genetics",
            
            # SECTIONS
            "Ressources Pédagogiques": "Educational Resources",
            "Ressources pédagogiques": "Educational Resources",
            "Documents de Cours": "Course Documents",
            "Activités Interactives": "Interactive Activities",
            "Annonce Importante": "Important Announcement",
            "Contact & Informations": "Contact & Information",
            "Annonce Bienvenue": "Welcome Announcement",
            "Vidéo d'Annonce": "Announcement Video",
            "Bienvenue dans le module": "Welcome to the Module",
            
            # UNIVERSITÉ
            "Université d'Oran 1": "University of Oran 1",
            "Université d'Oran 1 - Ahmed Ben Bella": "University of Oran 1 - Ahmed Ben Bella",
            "Faculté des Sciences de la Nature et de la Vie": "Faculty of Natural and Life Sciences",
            "Département de Biotechnologie": "Department of Biotechnology",
            "Niveau:": "Level:",
            "3ème année Licence": "3rd Year Bachelor's Degree",
            "3ème année Licence": "3rd Year Bachelor's Degree",
            "Année:": "Year:",
            "Enseignant:": "Instructor:",
            "Maître de Conférences": "Associate Professor",
            "Maître de Conférences en Biologie": "Associate Professor in Biology",
            "Tous droits réservés": "All rights reserved",
            
            # BOUTONS
            "Accéder aux Ressources": "Access Resources",
            "Accéder aux Ressources": "Access Resources",
            "Télécharger PDF": "Download PDF",
            "Télécharger": "Download",
            "Consulter": "View",
            "Consulter l'annonce": "Read Announcement",
            "Accéder": "Access",
            "Accéder aux TD": "Access Tutorials",
            "Bientôt disponible": "Coming Soon",
            "Bientôt disponible": "Coming Soon",
            "à venir": "coming soon",
            "à venir": "coming soon",
            "Envoyer un Message": "Send Message",
            "Via la messagerie de": "Via the",
            "la plateforme e-learning": "e-learning platform messaging",
            "Plateforme": "Platform",
            "Messagerie intégrée": "Integrated messaging",
            "En préparation": "In preparation",
            
            # CONTENU PÉDAGOGIQUE
            "Développement Embryonnaire": "Embryonic Development",
            "Régulation Maternelle": "Maternal Regulation",
            "Cycle de Vie & Segmentation": "Life Cycle & Segmentation",
            "Cycle de Vie": "Life Cycle",
            "Cycle de vie": "Life Cycle",
            "Cycle de vie Drosophila": "Drosophila Life Cycle",
            "Signalisation terminale": "Terminal signaling",
            "Signalisation terminale (Torso)": "Terminal signaling (Torso)",
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
            "Activation du récepteur": "Receptor activation",
            "Cascade Ras/MAPK": "Ras/MAPK cascade",
            "Axes Antéro-Postérieur et Dorso-Ventral": "Antero-Posterior and Dorso-Ventral Axes",
            "Système antérieur": "Anterior system",
            "Système antérieur (Bicoid)": "Anterior system (Bicoid)",
            "Système postérieur": "Posterior system",
            "Système postérieur (Nanos/Oskar)": "Posterior system (Nanos/Oskar)",
            "Système dorso-ventral": "Dorso-ventral system",
            "Système dorso-ventral (Dorsal)": "Dorso-ventral system (Dorsal)",
            "Cascade de segmentation": "Segmentation cascade",
            "Gènes homéotiques": "Homeotic genes",
            "Gènes homéotiques": "Homeotic genes",
            "Cours HTML Interactifs": "Interactive HTML Courses",
            "TD Interactifs": "Interactive Tutorials",
            "Contrôles Continus": "Continuous Assessment",
            "Contrôles Continus (CC)": "Continuous Assessment (CA)",
            "Présentations PPTX": "PowerPoint Presentations",
            "Support de cours": "Course support",
            "Support de cours L3": "L3 Course Support",
            "Schémas animés": "Animated diagrams",
            "Révisions examen": "Exam review",
            "Corrigés types": "Model answers",
            "Axes AP/DV": "AP/DV Axes",
            "TD & Exercices": "Tutorials & Exercises",
            "TD & Diagrammes": "Tutorials & Diagrams",
            "Diagrammes Interactifs": "Interactive Diagrams",
            "Diagrammes Drosophile": "Drosophila Diagrams",
            "Diagrammes AP": "AP Diagrams",
            "Ressources Visuelles": "Visual Resources",
            "Voir toutes les figures": "View all figures",
            "Cours Ovogenèse": "Oogenesis Course",
            "Cours Cycle de Vie": "Life Cycle Course",
            "Régulation maternelle, axes embryonnaires": "Maternal regulation, embryonic axes",
            "Développement & Segmentation": "Development & Segmentation",
            "Exercices pratiques": "Practical exercises",
            "Exercices et simulations interactives pour approfondir vos connaissances": 
                "Interactive exercises and simulations to deepen your knowledge",
            "Exercices, QCM, diagrammes dynamiques pour approfondir": 
                "Exercises, quizzes, dynamic diagrams to deepen knowledge",
            
            # DESCRIPTIONS
            "Mise en ligne des ressources pédagogiques": "Educational resources are now online",
            "Mise en ligne des ressources pédagogiques et informations pratiques": 
                "Educational resources and practical information are now online",
            "Besoin d'aide ou d'informations ?": "Need help or information?",
            "Téléchargez ou consultez les supports": "Download or view course materials",
            "Téléchargez ou consultez les supports au format PDF / HTML": 
                "Download or view materials in PDF / HTML format",
            "Téléchargez ou consultez en ligne": "Download or view online",
            "Supports de cours, PDF, TD interactifs": "Course materials, PDFs, interactive tutorials",
            "Supports de cours, PDF, TD interactifs — téléchargez ou consultez en ligne":
                "Course materials, PDFs, interactive tutorials — download or view online",
            "Accédez à l'ensemble des supports de cours,documents PDF et activités interactives":
                "Access all course materials, PDF documents, and interactive activities",
            "Accédez à l'ensemble des supports de cours, documents PDF et activités interactives":
                "Access all course materials, PDF documents, and interactive activities",
            
            # VIDÉO
            "Votre navigateur ne supporte pas la balise vidéo": "Your browser does not support the video tag",
            "Votre navigateur ne supporte pas la lecture vidéo": "Your browser does not support video playback",
            "Présentation du module et des ressources": "Module presentation and resources",
            "Présentation du module, objectifs et organisation des ressources":
                "Module presentation, objectives, and resource organization",
            "Découvrez dans cette vidéo :": "Discover in this video:",
            "Les objectifs pédagogiques du cours": "Course educational objectives",
            "Objectifs pédagogiques et compétences visées": "Educational objectives and targeted skills",
            "L'organisation des ressources en ligne": "Organization of online resources",
            "Organisation des ressources en ligne": "Organization of online resources",
            "Organisation des ressources en ligne (PDF, TD interactifs)": 
                "Organization of online resources (PDFs, interactive tutorials)",
            "Les modalités d'accès et d'évaluation": "Access and assessment methods",
            "Modalités d'évaluation": "Assessment methods",
            "Modalités d'évaluation (CC, examens)": "Assessment methods (CA, exams)",
            "Les recommandations pour réussir": "Recommendations for success",
            "Recommandations pour réussir en génétique du développement":
                "Recommendations for success in developmental genetics",
            
            # INSTRUCTIONS
            "Informations Générales": "General Information",
            "Informations Générales": "General Information",
            "Présentation du module": "Module presentation",
            "Planning": "Schedule",
            "Page d'accueil et tableau de bord du cours": "Homepage and course dashboard",
            "Contenu pédagogique": "Educational content",
            "Contenu pédagogique": "Educational content",
            "Chapitres, PDF, Vidéos, Interactifs": "Chapters, PDFs, Videos, Interactive content",
            "Chapitres, PDF, Vidéos, Interactifs": "Chapters, PDFs, Videos, Interactive content",
            "Profile de l'enseignant": "Instructor profile",
            "Coordonnées et formulaire de contact": "Contact information and form",
            "Coordonnées et formulaire de contact": "Contact information and form",
            
            # MESSAGES DIVERS
            "Site e-learning sur le développement embryonnaire de Drosophila melanogaster":
                "E-learning site on the embryonic development of Drosophila melanogaster",
            "Ce site présente le module": "This site presents the module",
            "pour les étudiants de L3 Biotechnologie à l'Université d'Oran 1":
                "for L3 Biotechnology students at the University of Oran 1",
            "Il est structuré pour ressembler à une plateforme LMS":
                "It is structured to resemble an LMS platform",
            "type Moodle": "Moodle-like",
            "afin de faciliter l'accès aux ressources": "to facilitate access to resources",
            "Navigation :": "Navigation:",
            "Utilisez la barre de menu pour accéder aux cours et contacts":
                "Use the menu bar to access courses and contacts",
            "Interactivité :": "Interactivity:",
            "Les fichiers HTML interactifs sont intégrés directement dans la page":
                "Interactive HTML files are embedded directly in the page",
            "via des iframes": "via iframes",
            "Vidéo :": "Video:",
            "La vidéo d'introduction est disponible sur la page d'accueil":
                "The introductory video is available on the homepage",
            "Téléchargement :": "Download:",
            "Les PDF s'ouvrent dans un nouvel onglet":
                "PDFs open in a new tab",
            "pour consultation ou téléchargement": "for viewing or downloading",
            "Accès": "Access",
            "Site web": "Website",
            "Email": "Email",
            "Lecture vidéo": "Video playback",
            "Introduction": "Introduction",
            "Dans un nouvel onglet": "In a new tab",
            "Sur la page d'accueil": "On the homepage",
            "Directement dans la page": "Directly in the page",
            "Via la messagerie de": "Via the",
            "Via la messagerie de la plateforme e-learning": "Via the e-learning platform messaging",
            
            # ÉLÉMENTS DE LISTE
            "Signalisation terminale (Torso)": "Terminal signaling (Torso)",
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
            "Activation du récepteur": "Receptor activation",
            "Cascade Ras/MAPK": "Ras/MAPK cascade",
            "Axes Antéro-Postérieur et Dorso-Ventral": "Antero-Posterior and Dorso-Ventral Axes",
            "Système antérieur (Bicoid)": "Anterior system (Bicoid)",
            "Système postérieur (Nanos/Oskar)": "Posterior system (Nanos/Oskar)",
            "Système dorso-ventral (Dorsal)": "Dorso-ventral system (Dorsal)",
            "CC1 - Ovogenèse & Axes": "CA1 - Oogenesis & Axes",
            "CC1 - Ovogenèse & Axes": "CA1 - Oogenesis & Axes",
            "CC2 - Segmentation": "CA2 - Segmentation",
            "Modèle d'annonce": "Announcement template",
            "Modèle de message": "Message template",
            
            # FOOTER & MÉTADONNÉES
            "fr": "en",
            "Drosophila Melanogaster developmental biology": 
                "Drosophila Melanogaster Developmental Biology",
            "Developmental Drosophila Genetic Control": "Developmental Drosophila Genetic Control",
            
            # ÉMOJIS ET SYMBOLES (préservation)
            "🧬 Aspect Génétique du Développement Embryonnaire": "🧬 Genetic Aspects of Embryonic Development",
            "🎓 Université d'Oran 1 - Ahmed Ben Bella": "🎓 University of Oran 1 - Ahmed Ben Bella",
            "📢 Annonce Importante": "📢 Important Announcement",
            "📖 Ressources Pédagogiques": "📖 Educational Resources",
            "📂 Documents de Cours": "📂 Course Documents",
            "🎥 Vidéo d'Annonce": "🎥 Announcement Video",
            "📌 Bienvenue dans le module": "📌 Welcome to the Module",
            "📬 Contact & Informations": "📬 Contact & Information",
            "👨‍🏫 Enseignant": "👨‍🏫 Instructor",
            "🏛️ Université": "🏛️ University",
            "💻 Plateforme": "💻 Platform",
            "📧 Contact": "📧 Contact",
            "📚 E-Learning": "📚 E-Learning",
            "📧 Contact": "📧 Contact",
            "📄 Télécharger PDF": "📄 Download PDF",
            "📑 Télécharger PDF": "📑 Download PDF",
            "📘 Télécharger PDF": "📘 Download PDF",
            "📁 Bientôt disponible": "📁 Coming Soon",
            "⏳ Bientôt disponible": "⏳ Coming Soon",
            "📊 En préparation": "📊 In preparation",
            "🔬 Développement Embryonnaire": "🔬 Embryonic Development",
            "🧬 Régulation Maternelle": "🧬 Maternal Regulation",
            "🔄 Cycle de Vie & Segmentation": "🔄 Life Cycle & Segmentation",
            "🎮 Cours HTML Interactifs": "🎮 Interactive HTML Courses",
            "🧪 TD Interactifs": "🧪 Interactive Tutorials",
            "📋 Contrôles Continus (CC)": "📋 Continuous Assessment (CA)",
            "📊 Présentations PPTX": "📊 PowerPoint Presentations",
            "→ TD2: Axes AP/DV": "→ TD2: AP/DV Axes",
            "→ TD4 Interactive": "→ TD4 Interactive",
            "→ OvoReg Final": "→ OvoReg Final",
            "→ Cycle de Vie (HTML)": "→ Life Cycle (HTML)",
            "→ Ovogenèse (HTML)": "→ Oogenesis (HTML)",
            "→ Diagrammes Drosophile": "→ Drosophila Diagrams",
            "→ Diagrammes AP": "→ AP Diagrams",
            "→ Figure 1: Cycle de Vie": "→ Figure 1: Life Cycle",
            "→ Figure 2: Ovariole": "→ Figure 2: Ovariole",
            "→ Figure 5: Axes Polarité": "→ Figure 5: Axis Polarity",
            "→ Voir toutes les figures": "→ View all figures",
        }
    
    def traduire_texte_securise(self, texte: str) -> str:
        """Traduit le texte sans toucher aux chemins de fichiers"""
        if not texte or not isinstance(texte, str):
            return texte
        
        # Ne pas traduire si c'est un chemin de fichier
        if any(ext in texte.lower() for ext in ['.html', '.htm', '.pdf', '.mp4', '.css', '.js', '.png', '.jpg']):
            # Mais traduire si c'est un mélange texte + chemin (rare)
            if not texte.startswith(('http', 'mailto', 'tel:', '/', './', '../')):
                pass  # Continuer la traduction
            else:
                return texte
        
        resultat = texte
        for francais, anglais in sorted(self.translations.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = re.escape(francais)
            resultat = re.sub(pattern, anglais, resultat, flags=re.IGNORECASE)
        
        return resultat
    
    def traduire_fichier(self, chemin: Path):
        """Traduit un fichier en place"""
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            original = contenu
            nb_remplacements = 0
            
            # 1. Traduire <title>
            def traduire_title(match):
                titre = match.group(1)
                traduit = self.traduire_texte_securise(titre)
                return f'<title>{traduit}</title>'
            
            contenu = re.sub(r'<title>(.*?)</title>', traduire_title, contenu, flags=re.IGNORECASE | re.DOTALL)
            
            # 2. Traduire texte entre balises (sauf dans <script> et <style>)
            def traduire_balise(match):
                balise_ouvrante = match.group(1)
                texte = match.group(2)
                balise_fermante = match.group(3)
                
                # Ignorer script et style
                if balise_ouvrante.lower() in ['<script', '<style']:
                    return match.group(0)
                
                traduit = self.traduire_texte_securise(texte)
                return f'{balise_ouvrante}{traduit}{balise_fermante}'
            
            # Pattern simple: capture tout entre > et <
            contenu = re.sub(r'(</?[a-zA-Z][^>]*>)([^<]*?)(</[a-zA-Z][^>]*>)', traduire_balise, contenu)
            
            # 3. Traduire attributs alt, title (PAS href/src)
            def traduire_attr(match):
                nom = match.group(1).lower()
                quote = match.group(2)
                val = match.group(3)
                
                if nom in ['alt', 'title', 'placeholder']:
                    traduit = self.traduire_texte_securise(val)
                    return f'{match.group(1)}={quote}{traduit}{quote}'
                return match.group(0)
            
            contenu = re.sub(r'\b(alt|title|placeholder)=([\'"])(.*?)\2', traduire_attr, contenu, flags=re.IGNORECASE)
            
            # 4. Corriger lang
            contenu = re.sub(r'<html([^>]*)lang=["\']fr["\']', r'<html\1lang="en"', contenu, flags=re.IGNORECASE)
            
            # 5. Traduire commentaires
            def traduire_commentaire(match):
                return f'<!--{self.traduire_texte_securise(match.group(1))}-->'
            
            contenu = re.sub(r'<!--(.*?)-->', traduire_commentaire, contenu, flags=re.DOTALL)
            
            # Sauvegarder
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            # Compter les changements
            if contenu != original:
                nb_remplacements = sum(1 for fr in self.translations.keys() if fr.lower() in original.lower())
            
            self.stats['fichiers_traites'] += 1
            self.stats['remplacements'] += nb_remplacements
            
            print(f"✅ {chemin.name} ({nb_remplacements} traductions)")
            return True
            
        except Exception as e:
            self.stats['erreurs'] += 1
            print(f"❌ Erreur {chemin}: {e}")
            return False
    
    def traiter_dossier(self, dossier: Path):
        """Traite tous les fichiers HTML du dossier"""
        extensions = {'.html', '.htm', '.css', '.js', '.md'}
        
        for chemin in dossier.rglob('*'):
            if chemin.is_file() and chemin.suffix.lower() in extensions:
                self.traduire_fichier(chemin)
    
    def afficher_stats(self):
        """Affiche les statistiques finales"""
        print("\n" + "=" * 50)
        print("RÉSULTATS")
        print("=" * 50)
        print(f"Fichiers traités: {self.stats['fichiers_traites']}")
        print(f"Remplacements: {self.stats['remplacements']}")
        print(f"Erreurs: {self.stats['erreurs']}")
        print("=" * 50)


def main():
    print("=" * 50)
    print("TRADUCTION FR → EN (En place)")
    print("Préservation des liens href/src")
    print("=" * 50)
    
    # Dossier courant par défaut
    dossier = Path('.').resolve()
    
    print(f"Dossier: {dossier}")
    print("-" * 50)
    
    traducteur = TraducteurHTML()
    traducteur.traiter_dossier(dossier)
    traducteur.afficher_stats()
    
    print("\n💡 Les liens sont conservés (ex: annonce_bienvenue.html)")


if __name__ == "__main__":
    main()
