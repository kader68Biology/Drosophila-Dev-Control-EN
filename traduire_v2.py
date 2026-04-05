#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de traduction automatique FR → EN pour Drosophila-Dev-Control-EN
Version 2.0 - Ne traduit PAS les noms de fichiers dans les liens (préserve les références)
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List
from html.parser import HTMLParser

class TraducteurHTML:
    def __init__(self):
        self.translations = self._charger_translations()
        self.stats = {'fichiers_traites': 0, 'remplacements': 0, 'erreurs': 0}
        
    def _charger_translations(self) -> Dict[str, str]:
        """Dictionnaire de traduction - contenu textuel uniquement"""
        return {
            # ===== NAVIGATION =====
            "Accueil": "Home",
            "Cours": "Courses",
            "Vidéo": "Video",
            "Vidéos": "Videos",
            "Documents": "Documents",
            "Activités": "Activities",
            "Activité": "Activity",
            "Contact": "Contact",
            
            # ===== TITRES =====
            "Aspect Génétique du Développement Embryonnaire": "Genetic Aspects of Embryonic Development",
            "Aspects Génétiques du Développement Embryonnaire": "Genetic Aspects of Embryonic Development",
            "Maîtrisez les mécanismes du développement chez": "Master the mechanisms of development in",
            "Maîtrisez les mécanismes moléculaires chez": "Master the molecular mechanisms in",
            "Génétique du Développement": "Developmental Genetics",
            
            # ===== SECTIONS =====
            "Ressources Pédagogiques": "Educational Resources",
            "Ressources pédagogiques": "Educational Resources",
            "Documents de Cours": "Course Documents",
            "Activités Interactives": "Interactive Activities",
            "Annonce Importante": "Important Announcement",
            "Contact & Informations": "Contact & Information",
            "Contact & Information": "Contact & Information",
            "Annonce Bienvenue": "Welcome Announcement",
            "Vidéo d'Annonce": "Announcement Video",
            "Bienvenue dans le module": "Welcome to the Module",
            
            # ===== UNIVERSITÉ =====
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
            
            # ===== BOUTONS =====
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
            
            # ===== CONTENU PÉDAGOGIQUE =====
            "Développement Embryonnaire": "Embryonic Development",
            "Régulation Maternelle": "Maternal Regulation",
            "Cycle de Vie & Segmentation": "Life Cycle & Segmentation",
            "Cycle de Vie": "Life Cycle",
            "Cycle de vie": "Life Cycle",
            "Cycle de vie Drosophila": "Drosophila Life Cycle",
            "Signalisation terminale": "Terminal signaling",
            "Signalisation terminale (Torso)": "Terminal signaling (Torso)",
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
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
            
            # ===== DESCRIPTIONS =====
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
            
            # ===== VIDÉO =====
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
            
            # ===== INSTRUCTIONS =====
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
            
            # ===== MESSAGES DIVERS =====
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
            
            # ===== ÉLÉMENTS DE LISTE =====
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et mise en place des axes": "Oogenesis and axis establishment",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
            "Ovogenèse et structure de l'œuf": "Oogenesis and egg structure",
            "Gènes homéotiques": "Homeotic genes",
            "Gènes homéotiques": "Homeotic genes",
            "CC1 - Ovogenèse & Axes": "CA1 - Oogenesis & Axes",
            "CC1 - Ovogenèse & Axes": "CA1 - Oogenesis & Axes",
            "CC2 - Segmentation": "CA2 - Segmentation",
            "Corrigés types": "Model answers",
            
            # ===== FOOTER & MÉTADONNÉES =====
            "fr": "en",
            "Drosophila Melanogaster developmental biology": 
                "Drosophila Melanogaster Developmental Biology",
            "Developmental Drosophila Genetic Control": "Developmental Drosophila Genetic Control",
        }
    
    def traduire_texte_securise(self, texte: str, est_dans_lien: bool = False) -> str:
        """
        Traduit le texte en évitant de toucher aux noms de fichiers dans les liens
        """
        if not texte or not isinstance(texte, str):
            return texte
            
        # Si on est dans un lien (href/src), on ne traduit que si ce n'est pas un chemin de fichier
        if est_dans_lien:
            # Ne pas traduire les chemins de fichiers (contenant .html, .pdf, .mp4, etc.)
            if any(ext in texte.lower() for ext in ['.html', '.htm', '.pdf', '.mp4', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif']):
                return texte
            # Ne pas traduire les URLs absolues
            if texte.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                return texte
        
        # Trier par longueur décroissante pour éviter les remplacements partiels
        termes = sorted(self.translations.keys(), key=len, reverse=True)
        
        resultat = texte
        for francais in termes:
            anglais = self.translations[francais]
            # Remplacement avec préservation de la casse pour les acronymes
            pattern = re.escape(francais)
            resultat = re.sub(pattern, anglais, resultat, flags=re.IGNORECASE)
        
        return resultat
    
    def traduire_fichier_html(self, chemin_entree: Path, chemin_sortie: Path):
        """Traduit un fichier HTML en préservant les liens et noms de fichiers"""
        try:
            with open(chemin_entree, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            original = contenu
            nb_remplacements = 0
            
            # 1. Traduire les balises <title>
            def traduire_title(match):
                titre = match.group(1)
                traduit = self.traduire_texte_securise(titre)
                nonlocal nb_remplacements
                if titre != traduit:
                    nb_remplacements += 1
                return f'<title>{traduit}</title>'
            
            contenu = re.sub(r'<title>(.*?)</title>', traduire_title, contenu, flags=re.IGNORECASE | re.DOTALL)
            
            # 2. Traduire le texte entre balises (hors attributs)
            def traduire_texte_balise(match):
                avant = match.group(1)
                texte = match.group(2)
                apres = match.group(3)
                
                # Ne pas traduire si c'est du code JavaScript ou CSS
                if avant.lower() in ['<script', '<style']:
                    return match.group(0)
                
                traduit = self.traduire_texte_securise(texte)
                if texte != traduit:
                    nonlocal nb_remplacements
                    nb_remplacements += len([k for k in self.translations.keys() if k.lower() in texte.lower()])
                return f'{avant}{traduit}{apres}'
            
            # Pattern pour capturer le texte entre balises HTML
            contenu = re.sub(
                r'(</?[a-zA-Z][^>]*>)([^<]*)(</[a-zA-Z][^>]*>)',
                traduire_texte_balise,
                contenu
            )
            
            # 3. Traduire les attributs alt et title (pas href/src !)
            def traduire_attribut_safe(match):
                attr_name = match.group(1).lower()
                quote = match.group(2)
                valeur = match.group(3)
                
                if attr_name in ['alt', 'title', 'placeholder', 'aria-label']:
                    traduit = self.traduire_texte_securise(valeur)
                    if valeur != traduit:
                        nonlocal nb_remplacements
                        nb_remplacements += 1
                    return f'{match.group(1)}={quote}{traduit}{quote}'
                return match.group(0)
            
            contenu = re.sub(
                r'\b(alt|title|placeholder|aria-label)=([\'"])(.*?)\2',
                traduire_attribut_safe,
                contenu,
                flags=re.IGNORECASE
            )
            
            # 4. Corriger l'attribut lang
            contenu = re.sub(r'<html([^>]*)lang=["\']fr["\']', r'<html\1lang="en"', contenu, flags=re.IGNORECASE)
            contenu = re.sub(r'xml:lang=["\']fr["\']', 'xml:lang="en"', contenu, flags=re.IGNORECASE)
            
            # 5. Traduire les commentaires HTML
            def traduire_commentaire(match):
                commentaire = match.group(1)
                traduit = self.traduire_texte_securise(commentaire)
                return f'<!--{traduit}-->'
            
            contenu = re.sub(r'<!--(.*?)-->', traduire_commentaire, contenu, flags=re.DOTALL)
            
            # Sauvegarder
            chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
            with open(chemin_sortie, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            self.stats['fichiers_traites'] += 1
            self.stats['remplacements'] += nb_remplacements
            
            print(f"✅ {chemin_entree.name} → {chemin_sortie.name} ({nb_remplacements} traductions)")
            return True
            
        except Exception as e:
            self.stats['erreurs'] += 1
            print(f"❌ Erreur sur {chemin_entree}: {e}")
            return False
    
    def traduire_fichier_css(self, chemin_entree: Path, chemin_sortie: Path):
        """Traduit les commentaires CSS et les chaînes de caractères content"""
        try:
            with open(chemin_entree, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Traduire les commentaires CSS
            def traduire_commentaire_css(match):
                commentaire = match.group(1)
                traduit = self.traduire_texte_securise(commentaire)
                return f'/*{traduit}*/'
            
            contenu = re.sub(r'/\*(.*?)\*/', traduire_commentaire_css, contenu, flags=re.DOTALL)
            
            # Traduire les content: "..." (pseudo-éléments)
            def traduire_content(match):
                avant = match.group(1)
                texte = match.group(2)
                apres = match.group(3)
                traduit = self.traduire_texte_securise(texte)
                return f'{avant}{traduit}{apres}'
            
            contenu = re.sub(
                r'(content:\s*["\'])(.*?)(["\'])',
                traduire_content,
                contenu
            )
            
            chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
            with open(chemin_sortie, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            self.stats['fichiers_traites'] += 1
            print(f"✅ {chemin_entree.name} → {chemin_sortie.name} (CSS traduit)")
            return True
            
        except Exception as e:
            self.stats['erreurs'] += 1
            print(f"❌ Erreur CSS sur {chemin_entree}: {e}")
            return False
    
    def traduire_fichier_js(self, chemin_entree: Path, chemin_sortie: Path):
        """Traduit les chaînes de caractères dans les fichiers JS"""
        try:
            with open(chemin_entree, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Traduire les chaînes entre guillemets simples ou doubles
            def traduire_chaine_js(match):
                quote = match.group(1)
                texte = match.group(2)
                
                # Ne pas traduire si c'est une clé d'objet ou un nom de variable
                if texte.isidentifier() and len(texte) < 30:
                    return match.group(0)
                
                traduit = self.traduire_texte_securise(texte)
                return f'{quote}{traduit}{quote}'
            
            # Chaînes entre guillemets doubles
            contenu = re.sub(r'"((?:[^"\\]|\\.)*)"', traduire_chaine_js, contenu)
            # Chaînes entre guillemets simples
            contenu = re.sub(r"'((?:[^'\\]|\\.)*)'", traduire_chaine_js, contenu)
            
            chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
            with open(chemin_sortie, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            self.stats['fichiers_traites'] += 1
            print(f"✅ {chemin_entree.name} → {chemin_sortie.name} (JS traduit)")
            return True
            
        except Exception as e:
            self.stats['erreurs'] += 1
            print(f"❌ Erreur JS sur {chemin_entree}: {e}")
            return False
    
    def traduire_markdown(self, chemin_entree: Path, chemin_sortie: Path):
        """Traduit les fichiers Markdown"""
        try:
            with open(chemin_entree, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Traduire tout sauf les blocs de code et URLs
            lignes = contenu.split('\n')
            resultat = []
            dans_bloc_code = False
            
            for ligne in lignes:
                # Détecter les blocs de code
                if ligne.strip().startswith('```'):
                    dans_bloc_code = not dans_bloc_code
                    resultat.append(ligne)
                    continue
                
                if dans_bloc_code:
                    resultat.append(ligne)
                    continue
                
                # Ne pas traduire les liens Markdown [texte](url) mais traduire le texte
                def traduire_lien_md(match):
                    texte = match.group(1)
                    url = match.group(2)
                    traduit = self.traduire_texte_securise(texte)
                    return f'[{traduit}]({url})'
                
                ligne = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', traduire_lien_md, ligne)
                
                # Traduire le reste de la ligne
                ligne = self.traduire_texte_securise(ligne)
                resultat.append(ligne)
            
            contenu = '\n'.join(resultat)
            
            chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
            with open(chemin_sortie, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            self.stats['fichiers_traites'] += 1
            print(f"✅ {chemin_entree.name} → {chemin_sortie.name} (Markdown traduit)")
            return True
            
        except Exception as e:
            self.stats['erreurs'] += 1
            print(f"❌ Erreur Markdown sur {chemin_entree}: {e}")
            return False
    
    def copier_fichier_binaire(self, chemin_entree: Path, chemin_sortie: Path):
        """Copie les fichiers binaires sans modification"""
        import shutil
        try:
            chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(chemin_entree, chemin_sortie)
            print(f"📁 Copié: {chemin_entree.name}")
            return True
        except Exception as e:
            print(f"❌ Erreur copie {chemin_entree}: {e}")
            return False
    
    def traiter_dossier(self, dossier_source: Path, dossier_sortie: Path):
        """Traite récursivement tous les fichiers du dossier"""
        extensions_html = {'.html', '.htm'}
        extensions_css = {'.css'}
        extensions_js = {'.js'}
        extensions_md = {'.md', '.markdown'}
        extensions_texte = {'.txt', '.json', '.xml'}
        extensions_binaires = {'.pdf', '.mp4', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot'}
        
        for chemin_entree in dossier_source.rglob('*'):
            if chemin_entree.is_dir():
                continue
            
            # Calculer le chemin relatif et de sortie
            rel_path = chemin_entree.relative_to(dossier_source)
            chemin_sortie = dossier_sortie / rel_path
            
            extension = chemin_entree.suffix.lower()
            
            if extension in extensions_html:
                self.traduire_fichier_html(chemin_entree, chemin_sortie)
            elif extension in extensions_css:
                self.traduire_fichier_css(chemin_entree, chemin_sortie)
            elif extension in extensions_js:
                self.traduire_fichier_js(chemin_entree, chemin_sortie)
            elif extension in extensions_md:
                self.traduire_markdown(chemin_entree, chemin_sortie)
            elif extension in extensions_texte:
                self.traduire_fichier_html(chemin_entree, chemin_sortie)  # Traiter comme HTML simple
            else:
                # Considérer comme binaire
                self.copier_fichier_binaire(chemin_entree, chemin_sortie)
    
    def generer_rapport(self, dossier_sortie: Path):
        """Génère un rapport de traduction"""
        rapport = {
            'date': '2026-04-05',
            'statistiques': self.stats,
            'dictionnaire': {
                'nombre_entrees': len(self.translations),
                'entrees': self.translations
            }
        }
        
        # JSON
        json_path = dossier_sortie / 'rapport_traduction.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        # Markdown
        md_path = dossier_sortie / 'RAPPORT_TRADUCTION.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Rapport de Traduction FR → EN\n\n")
            f.write("**Date:** 2026-04-05\n\n")
            f.write("## Statistiques\n\n")
            f.write(f"- **Fichiers traités:** {self.stats['fichiers_traites']}\n")
            f.write(f"- **Remplacements effectués:** {self.stats['remplacements']}\n")
            f.write(f"- **Erreurs:** {self.stats['erreurs']}\n\n")
            f.write("## Important\n\n")
            f.write("⚠️ **Les noms de fichiers dans les liens (href, src) ont été préservés** ")
            f.write("pour éviter les erreurs de référencement. Seul le contenu textuel visible ")
            f.write("a été traduit.\n\n")
            f.write("## Dictionnaire de traduction utilisé\n\n")
            f.write("| Français | English |\n")
            f.write("|----------|---------|\n")
            for fr, en in sorted(self.translations.items())[:50]:  # Limiter à 50 pour lisibilité
                f.write(f"| {fr} | {en} |\n")
            f.write(f"\n... et {len(self.translations) - 50} autres entrées.\n")
        
        print(f"\n📊 Rapport généré: {json_path}")
        return rapport


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Traduit le contenu FR → EN en préservant les noms de fichiers dans les liens'
    )
    parser.add_argument('source', nargs='?', default='.', help='Dossier source')
    parser.add_argument('-o', '--output', default='./traduction_en', help='Dossier de sortie')
    parser.add_argument('--in-place', action='store_true', help='Traduire en place')
    
    args = parser.parse_args()
    
    dossier_source = Path(args.source).resolve()
    dossier_sortie = dossier_source if args.in_place else Path(args.output).resolve()
    
    print("=" * 70)
    print("🚀 TRADUCTION FR → EN (Version 2.0 - Préservation des liens)")
    print("=" * 70)
    print(f"📂 Source: {dossier_source}")
    print(f"📂 Sortie: {dossier_sortie}")
    print("⚠️  Les noms de fichiers dans href/src sont PRÉSERVÉS")
    print("-" * 70)
    
    traducteur = TraducteurHTML()
    traducteur.traiter_dossier(dossier_source, dossier_sortie)
    
    print("-" * 70)
    rapport = traducteur.generer_rapport(dossier_sortie)
    
    print("=" * 70)
    print("✅ TRADUCTION TERMINÉE")
    print(f"📊 {traducteur.stats['fichiers_traites']} fichiers traités")
    print(f"📝 {traducteur.stats['remplacements']} remplacements effectués")
    if traducteur.stats['erreurs'] > 0:
        print(f"⚠️  {traducteur.stats['erreurs']} erreur(s)")
    print("=" * 70)
    print("\n💡 Les liens vers les fichiers français sont conservés.")
    print("   Exemple: href='annonce_bienvenue.html' reste inchangé")
    print("   mais le texte affiché 'Annonce Bienvenue' devient 'Welcome Announcement'")


if __name__ == "__main__":
    main()
