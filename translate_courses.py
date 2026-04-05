#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de traduction complète des cours PDF et HTML - FR → EN
Auteur: Assistant IA
Date: 2026-04-05
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TranslationStats:
    html_files: int = 0
    pdf_files: int = 0
    text_segments: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class CourseTranslator:
    def __init__(self):
        self.stats = TranslationStats()
        
        # Dictionnaire scientifique complet pour la biologie du développement
        self.scientific_terms = self._load_scientific_dictionary()
        self.common_phrases = self._load_common_phrases()
        
    def _load_scientific_dictionary(self) -> Dict[str, str]:
        """Charge le dictionnaire de termes scientifiques"""
        return {
            # Termes généraux de biologie
            "embryon": "embryo",
            "embryonnaire": "embryonic",
            "développement": "development",
            "développemental": "developmental",
            "développementale": "developmental",
            "génétique": "genetics",
            "génétiques": "genetic",
            "moléculaire": "molecular",
            "moléculaires": "molecular",
            "cellule": "cell",
            "cellulaire": "cellular",
            "cellulaires": "cellular",
            "tissu": "tissue",
            "tissus": "tissues",
            "organe": "organ",
            "organes": "organs",
            "organisme": "organism",
            "organismes": "organisms",
            
            # Drosophila spécifique
            "drosophile": "Drosophila",
            "drosophila": "Drosophila",
            "mouche": "fly",
            "mouches": "flies",
            "mouche du vinaigre": "vinegar fly",
            "fruit fly": "fruit fly",
            "métamorphose": "metamorphosis",
            "cycle de vie": "life cycle",
            "stade": "stage",
            "stades": "stages",
            "larve": "larva",
            "larves": "larvae",
            "pupaison": "pupariation",
            "pupe": "pupa",
            "pupes": "pupae",
            "imago": "adult",
            "adulte": "adult",
            "adultes": "adults",
            "oeuf": "egg",
            "oeufs": "eggs",
            "ovocyte": "oocyte",
            "ovocytes": "oocytes",
            "ovule": "ovum",
            "ovules": "ova",
            "spermatozoïde": "sperm",
            "spermatozoïdes": "sperm",
            "fécondation": "fertilization",
            "zigote": "zygote",
            "blastoderme": "blastoderm",
            "blastodermique": "blastodermic",
            "gastrulation": "gastrulation",
            "germe": "germ",
            "ligne germinale": "germ line",
            "cellules germinales": "germ cells",
            
            # Ovogenèse et axes
            "ovogenèse": "oogenesis",
            "ovariole": "ovariole",
            "ovarioles": "ovarioles",
            "ovaire": "ovary",
            "ovaires": "ovaries",
            "follicule": "follicle",
            "follicules": "follicles",
            "cellules nourricières": "nurse cells",
            "cellule nourricière": "nurse cell",
            "ovocyte I": "primary oocyte",
            "ovocyte II": "secondary oocyte",
            "vitellogenèse": "vitellogenesis",
            "vitelline": "vitelline",
            "membrane vitelline": "vitelline membrane",
            "chorion": "chorion",
            "coque": "shell",
            "pôle animal": "animal pole",
            "pôle végétal": "vegetal pole",
            "pôle antérieur": "anterior pole",
            "pôle postérieur": "posterior pole",
            "axe antéro-postérieur": "anteroposterior axis",
            "axe dorso-ventral": "dorsoventral axis",
            "axe gauche-droite": "left-right axis",
            "polarité": "polarity",
            "gradient": "gradient",
            "gradients": "gradients",
            "morphogène": "morphogen",
            "morphogènes": "morphogens",
            "champ morphogénétique": "morphogenetic field",
            
            # Segmentation
            "segmentation": "segmentation",
            "segment": "segment",
            "segments": "segments",
            "parasegment": "parasegment",
            "parasegments": "parasegments",
            "métamère": "metamere",
            "métamères": "metameres",
            "somitogenèse": "somitogenesis",
            "cascade de segmentation": "segmentation cascade",
            "gènes de segmentation": "segmentation genes",
            "gène gap": "gap gene",
            "gènes gap": "gap genes",
            "gène pair-rule": "pair-rule gene",
            "gènes pair-rule": "pair-rule genes",
            "gène de polarité segmentaire": "segment polarity gene",
            "gènes de polarité segmentaire": "segment polarity genes",
            "engrailed": "engrailed",
            "wingless": "wingless",
            "hedgehog": "hedgehog",
            "patched": "patched",
            "hunchback": "hunchback",
            "krüppel": "krüppel",
            "knirps": "knirps",
            "giant": "giant",
            "even-skipped": "even-skipped",
            "ftz": "ftz",
            "runt": "runt",
            "hairy": "hairy",
            
            # Gènes homéotiques
            "gène homéotique": "homeotic gene",
            "gènes homéotiques": "homeotic genes",
            "sélecteur de segment": "segment selector",
            "sélecteurs de segment": "segment selectors",
            "complexe bithorax": "bithorax complex",
            "complexe antennapedia": "antennapedia complex",
            "homéoboîte": "homeobox",
            "homéodomaine": "homeodomain",
            "antennapedia": "antennapedia",
            "bithorax": "bithorax",
            "ultrabithorax": "ultrabithorax",
            "abdominal-A": "abdominal-A",
            "abdominal-B": "abdominal-B",
            "labial": "labial",
            "proboscipedia": "proboscipedia",
            "deformed": "deformed",
            "sex combs reduced": "sex combs reduced",
            
            # Signalisation
            "signalisation": "signaling",
            "voie de signalisation": "signaling pathway",
            "voies de signalisation": "signaling pathways",
            "cascade de signalisation": "signaling cascade",
            "récepteur": "receptor",
            "récepteurs": "receptors",
            "ligand": "ligand",
            "ligands": "ligands",
            "activation": "activation",
            "inhibition": "inhibition",
            "voie Ras/MAPK": "Ras/MAPK pathway",
            "cascade Ras/MAPK": "Ras/MAPK cascade",
            "voie JAK/STAT": "JAK/STAT pathway",
            "voie Wnt": "Wnt pathway",
            "voie Hedgehog": "Hedgehog pathway",
            "voie Notch": "Notch pathway",
            "voie TGF-β": "TGF-β pathway",
            "voie BMP": "BMP pathway",
            "facteur de transcription": "transcription factor",
            "facteurs de transcription": "transcription factors",
            "expression génique": "gene expression",
            "régulation de l'expression": "expression regulation",
            "promoteur": "promoter",
            "enhancer": "enhancer",
            "silencieur": "silencer",
            "élément cis-régulateur": "cis-regulatory element",
            "éléments cis-régulateurs": "cis-regulatory elements",
            
            # Systèmes maternels spécifiques
            "système antérieur": "anterior system",
            "système postérieur": "posterior system",
            "système terminal": "terminal system",
            "système dorso-ventral": "dorsoventral system",
            "bicoid": "bicoid",
            "nanos": "nanos",
            "oskar": "oskar",
            "staufen": "staufen",
            "torso": "torso",
            "torso-like": "torso-like",
            "trunk": "trunk",
            "pipe": "pipe",
            "nudel": "nudel",
            "gdl": "gdl",
            "easter": "easter",
            "snake": "snake",
            "gd": "gd",
            "dorsal": "dorsal",
            "cactus": "cactus",
            "pelle": "pelle",
            "tube": "tube",
            "localisation": "localization",
            "transport": "transport",
            "déterminant": "determinant",
            "déterminants": "determinants",
            "ARNm": "mRNA",
            "ARN messager": "messenger RNA",
            "traduction": "translation",
            "synthèse protéique": "protein synthesis",
            
            # Terminologie pédagogique
            "cours": "course",
            "cours magistral": "lecture",
            "travaux dirigés": "tutorials",
            "TD": "tutorials",
            "exercice": "exercise",
            "exercices": "exercises",
            "pratique": "practical",
            "pratiques": "practicals",
            "contrôle continu": "continuous assessment",
            "CC": "CA",
            "examen": "exam",
            "examen final": "final exam",
            "évaluation": "evaluation",
            "note": "grade",
            "notes": "grades",
            "crédit": "credit",
            "crédits": "credits",
            "syllabus": "syllabus",
            "programme": "curriculum",
            "objectif": "objective",
            "objectifs": "objectives",
            "compétence": "skill",
            "compétences": "skills",
            "apprentissage": "learning",
            "enseignement": "teaching",
            "pédagogie": "pedagogy",
            "pédagogique": "pedagogical",
            "pédagogiques": "pedagogical",
            
            # Structure du cours
            "chapitre": "chapter",
            "chapitres": "chapters",
            "partie": "part",
            "parties": "parts",
            "section": "section",
            "sections": "sections",
            "introduction": "introduction",
            "conclusion": "conclusion",
            "résumé": "summary",
            "bibliographie": "bibliography",
            "références": "references",
            "figure": "figure",
            "figures": "figures",
            "tableau": "table",
            "tableaux": "tables",
            "schéma": "diagram",
            "schémas": "diagrams",
            "illustration": "illustration",
            "illustrations": "illustrations",
            "légende": "caption",
            "légendes": "captions",
        }
    
    def _load_common_phrases(self) -> Dict[str, str]:
        """Charge les phrases courantes du cours"""
        return {
            # Phrases d'introduction
            "Dans ce chapitre, nous allons étudier": "In this chapter, we will study",
            "Nous allons voir que": "We will see that",
            "Il est important de noter que": "It is important to note that",
            "Il faut souligner que": "It should be emphasized that",
            "On observe que": "We observe that",
            "On constate que": "We find that",
            "Comme nous l'avons vu": "As we have seen",
            "Comme mentionné précédemment": "As previously mentioned",
            "Dans la section précédente": "In the previous section",
            "Dans la partie suivante": "In the following part",
            
            # Phrases de description
            "La figure ci-dessus montre": "The figure above shows",
            "La figure ci-dessous illustre": "The figure below illustrates",
            "Comme le montre la figure": "As shown in the figure",
            "Cette figure représente": "This figure represents",
            "Le schéma suivant présente": "The following diagram presents",
            "Cette illustration démontre": "This illustration demonstrates",
            
            # Phrases explicatives
            "Cela signifie que": "This means that",
            "En d'autres termes": "In other words",
            "Autrement dit": "In other words",
            "C'est-à-dire que": "That is to say",
            "Par conséquent": "Consequently",
            "Par conséquent,": "Therefore,",
            "En conséquence": "As a result",
            "De ce fait": "As a result",
            "Ainsi,": "Thus,",
            "C'est pourquoi": "That is why",
            "En effet,": "Indeed,",
            "En effet": "Indeed",
            "En fait,": "In fact,",
            "En fait": "In fact",
            "Notons que": "Note that",
            "Remarquons que": "Let us note that",
            "Il est à noter que": "It should be noted that",
            
            # Phrases de transition
            "Premièrement,": "First,",
            "Deuxièmement,": "Second,",
            "Troisièmement,": "Third,",
            "En premier lieu": "First",
            "En second lieu": "Second",
            "Enfin,": "Finally,",
            "Pour conclure": "To conclude",
            "En conclusion": "In conclusion",
            "Pour résumer": "To summarize",
            "En résumé": "In summary",
            "D'une part": "On one hand",
            "D'autre part": "On the other hand",
            "Par ailleurs": "Furthermore",
            "De plus,": "Moreover,",
            "En outre,": "Furthermore,",
            "En outre": "Furthermore",
            "Cependant,": "However,",
            "Néanmoins,": "Nevertheless,",
            "Toutefois,": "However,",
            "Bien que": "Although",
            "Malgré": "Despite",
            "Grâce à": "Thanks to",
            "En raison de": "Due to",
            "À cause de": "Because of",
            
            # Phrases de définition
            "On définit": "We define",
            "On appelle": "We call",
            "Par définition": "By definition",
            "Il s'agit de": "It is about",
            "Cela correspond à": "This corresponds to",
            "Cela représente": "This represents",
            
            # Phrases de processus
            "Ce processus permet de": "This process allows",
            "Ce mécanisme conduit à": "This mechanism leads to",
            "Cette étape consiste à": "This step consists of",
            "Il en résulte que": "It follows that",
            "On aboutit à": "We end up with",
            "Cela aboutit à": "This results in",
            
            # Questions et exercices
            "Question :": "Question:",
            "Questions :": "Questions:",
            "Exercice :": "Exercise:",
            "Exercices :": "Exercises:",
            "Problème :": "Problem:",
            "Problèmes :": "Problems:",
            "À compléter :": "To complete:",
            "À remplir :": "To fill in:",
            "Réponse :": "Answer:",
            "Réponses :": "Answers:",
            "Solution :": "Solution:",
            "Solutions :": "Solutions:",
            "Indice :": "Hint:",
            "Indices :": "Hints:",
            
            # Instructions
            "Cliquez sur": "Click on",
            "Sélectionnez": "Select",
            "Choisissez": "Choose",
            "Identifiez": "Identify",
            "Nommez": "Name",
            "Décrivez": "Describe",
            "Expliquez": "Explain",
            "Analysez": "Analyze",
            "Comparez": "Compare",
            "Distinguez": "Distinguish",
            "Illustrez": "Illustrate",
            "Représentez": "Represent",
            "Schématisez": "Diagram",
            "Localisez": "Locate",
            "Indiquez": "Indicate",
            "Précisez": "Specify",
            "Justifiez votre réponse": "Justify your answer",
            "Donnez un exemple": "Give an example",
            "Citez un exemple": "Cite an example",
        }
    
    def translate_html_file(self, input_path: Path, output_path: Optional[Path] = None) -> bool:
        """
        Traduit un fichier HTML en préservant la structure et les liens
        """
        try:
            if output_path is None:
                output_path = input_path
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            translation_count = 0
            
            # 1. Traduire le contenu textuel entre balises (sauf dans les balises elles-mêmes)
            def translate_tag_content(match):
                before = match.group(1)  # Balise ouvrante
                text = match.group(2)    # Contenu texte
                after = match.group(3)   # Balise fermante
                
                # Ne pas traduire dans script ou style
                if before.lower().startswith(('<script', '<style')):
                    return match.group(0)
                
                # Traduire le texte
                translated_text = self._translate_text(text)
                nonlocal translation_count
                if translated_text != text:
                    translation_count += 1
                
                return f'{before}{translated_text}{after}'
            
            # Pattern pour capturer le texte entre balises HTML
            content = re.sub(
                r'(<[^>]+>)([^<]*)(</[^>]+>)',
                translate_tag_content,
                content,
                flags=re.DOTALL
            )
            
            # 2. Traduire les attributs alt, title, placeholder (pas href/src/action)
            def translate_attribute(match):
                attr_name = match.group(1).lower()
                quote = match.group(2)
                attr_value = match.group(3)
                
                if attr_name in ['alt', 'title', 'placeholder', 'aria-label', 'aria-placeholder']:
                    translated = self._translate_text(attr_value)
                    nonlocal translation_count
                    if translated != attr_value:
                        translation_count += 1
                    return f'{match.group(1)}={quote}{translated}{quote}'
                return match.group(0)
            
            content = re.sub(
                r'\b(alt|title|placeholder|aria-label|aria-placeholder)=([\'"])(.*?)\2',
                translate_attribute,
                content,
                flags=re.IGNORECASE
            )
            
            # 3. Traduire les commentaires HTML
            def translate_comment(match):
                comment_text = match.group(1)
                translated = self._translate_text(comment_text)
                return f'<!--{translated}-->'
            
            content = re.sub(r'<!--(.*?)-->', translate_comment, content, flags=re.DOTALL)
            
            # 4. Mettre à jour l'attribut lang
            content = re.sub(
                r'<html([^>]*)lang=["\']fr["\']',
                r'<html\1lang="en"',
                content,
                flags=re.IGNORECASE
            )
            content = re.sub(
                r'<html([^>]*)xml:lang=["\']fr["\']',
                r'<html\1xml:lang="en"',
                content,
                flags=re.IGNORECASE
            )
            
            # Sauvegarder
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats.html_files += 1
            self.stats.text_segments += translation_count
            
            print(f"✅ HTML traduit: {input_path.name} ({translation_count} segments)")
            return True
            
        except Exception as e:
            self.stats.errors.append(f"HTML {input_path}: {str(e)}")
            print(f"❌ Erreur HTML {input_path.name}: {e}")
            return False
    
    def translate_pdf_file(self, input_path: Path, output_path: Optional[Path] = None) -> bool:
        """
        Traduit un fichier PDF en créant un fichier texte annoté côte à côte
        Note: La traduction directe de PDF est complexe, on crée donc un fichier HTML bilingue
        """
        try:
            if output_path is None:
                output_path = input_path.with_suffix('.en.html')
            
            # Extraire le texte du PDF si possible (nécessite pdftotext)
            extracted_text = self._extract_pdf_text(input_path)
            
            if extracted_text:
                # Créer un document HTML bilingue
                html_content = self._create_bilingual_pdf_html(input_path.name, extracted_text)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"✅ PDF traité: {input_path.name} → {output_path.name}")
            else:
                # Créer un simple résumé traduit
                summary = self._translate_pdf_filename(input_path.name)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{summary}</title>
</head>
<body>
    <h1>{summary}</h1>
    <p>This is the English version of the PDF document.</p>
    <p>Original file: {input_path.name}</p>
    <p>Please refer to the original PDF for the complete content.</p>
</body>
</html>""")
                
                print(f"⚠️  PDF traité (sans extraction): {input_path.name}")
            
            self.stats.pdf_files += 1
            return True
            
        except Exception as e:
            self.stats.errors.append(f"PDF {input_path}: {str(e)}")
            print(f"❌ Erreur PDF {input_path.name}: {e}")
            return False
    
    def _extract_pdf_text(self, pdf_path: Path) -> Optional[str]:
        """Tente d'extraire le texte d'un PDF"""
        try:
            # Essayer avec pdftotext (poppler-utils)
            result = subprocess.run(
                ['pdftotext', '-layout', str(pdf_path), '-'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            
            # Alternative: essayer avec PyPDF2 si disponible
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text if text.strip() else None
            except ImportError:
                pass
            
            return None
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None
    
    def _create_bilingual_pdf_html(self, filename: str, french_text: str) -> str:
        """Crée un document HTML bilingue à partir du texte PDF"""
        # Traduire le texte par paragraphes
        paragraphs = french_text.split('\n\n')
        translated_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                translated = self._translate_text(para)
                translated_paragraphs.append({
                    'fr': para.strip(),
                    'en': translated
                })
        
        # Générer le HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._translate_pdf_filename(filename)}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .bilingual-block {{
            background: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .french {{
            color: #666;
            border-left: 4px solid #ccc;
            padding-left: 15px;
            margin-bottom: 10px;
            font-style: italic;
        }}
        .english {{
            color: #333;
            border-left: 4px solid #2c7bb6;
            padding-left: 15px;
            font-weight: 500;
        }}
        .label {{
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
            opacity: 0.7;
        }}
        .download-link {{
            display: inline-block;
            background: #2c7bb6;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }}
        .download-link:hover {{
            background: #1a5490;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 {self._translate_pdf_filename(filename)}</h1>
        <p>Bilingual version / Version bilingue</p>
    </div>
    
    <p><a href="{filename}" class="download-link">⬇️ Download Original PDF / Télécharger le PDF original</a></p>
    
    <hr style="margin: 30px 0;">
    
    <h2>📖 Document Content / Contenu du document</h2>
"""
        
        for block in translated_paragraphs[:50]:  # Limiter à 50 paragraphes
            html += f"""
    <div class="bilingual-block">
        <div class="label">🇫🇷 Original</div>
        <div class="french">{self._escape_html(block['fr'])}</div>
        <div class="label">🇬🇧 English</div>
        <div class="english">{self._escape_html(block['en'])}</div>
    </div>
"""
        
        if len(translated_paragraphs) > 50:
            html += f"""
    <p style="text-align: center; color: #666; margin: 30px 0;">
        ... and {len(translated_paragraphs) - 50} more paragraphs / 
        et {len(translated_paragraphs) - 50} paragraphes supplémentaires
    </p>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def _translate_pdf_filename(self, filename: str) -> str:
        """Traduit le nom de fichier PDF pour le titre"""
        translations = {
            "Cours1_Synthese_Drosophila": "Course1_Synthesis_Drosophila",
            "Cours1_Synthese_Session2": "Course1_Synthesis_Session2",
            "cours_drosophila": "course_drosophila",
            "cours_drosophila_ovogenese": "course_drosophila_oogenesis",
            "Synthese": "Synthesis",
            "Session": "Session",
            "ovogenese": "oogenesis",
        }
        
        result = filename
        for fr, en in translations.items():
            result = result.replace(fr, en)
        
        return result
    
    def _translate_text(self, text: str) -> str:
        """Traduit un texte en utilisant les dictionnaires"""
        if not text or not isinstance(text, str):
            return text
        
        # Ne pas traduire les chemins de fichiers
        if text.strip().startswith(('http://', 'https://', 'mailto:', 'tel:', 
                                    './', '../', '/', '#', 'data:', 'javascript:')):
            return text
        
        # Ne pas traduire si c'est principalement du code
        if len(re.findall(r'[{}[\]();=<>]', text)) > len(text) * 0.1:
            return text
        
        result = text
        
        # 1. Traduire les phrases courantes (priorité haute)
        for fr_phrase, en_phrase in sorted(self.common_phrases.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = re.escape(fr_phrase)
            result = re.sub(pattern, en_phrase, result, flags=re.IGNORECASE)
        
        # 2. Traduire les termes scientifiques
        for fr_term, en_term in sorted(self.scientific_terms.items(), key=lambda x: len(x[0]), reverse=True):
            # Utiliser word boundaries pour éviter les remplacements partiels
            pattern = r'\b' + re.escape(fr_term) + r'\b'
            result = re.sub(pattern, en_term, result, flags=re.IGNORECASE)
        
        # 3. Corrections post-traduction
        result = self._post_process_translation(result)
        
        return result
    
    def _post_process_translation(self, text: str) -> str:
        """Corrections post-traduction"""
        # Capitaliser les noms propres scientifiques si au début de phrase
        text = re.sub(r'([.!?]\s+)drosophila', r'\1Drosophila', text, flags=re.IGNORECASE)
        text = re.sub(r'^drosophila', 'Drosophila', text, flags=re.IGNORECASE)
        
        # Corriger les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        # Corriger les espaces avant la ponctuation
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        
        return text.strip()
    
    def _escape_html(self, text: str) -> str:
        """Échappe les caractères HTML spéciaux"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))
    
    def process_directory(self, input_dir: Path, output_dir: Optional[Path] = None):
        """Traite tous les fichiers d'un répertoire"""
        if output_dir is None:
            output_dir = input_dir
        
        print("=" * 70)
        print("🚀 TRADUCTION DES COURS PDF ET HTML - FR → EN")
        print("=" * 70)
        print(f"📂 Dossier source: {input_dir}")
        print(f"📂 Dossier sortie: {output_dir}")
        print("-" * 70)
        
        # Traiter les fichiers HTML
        html_files = list(input_dir.rglob('*.html')) + list(input_dir.rglob('*.htm'))
        print(f"\n📄 Fichiers HTML trouvés: {len(html_files)}")
        
        for html_file in html_files:
            rel_path = html_file.relative_to(input_dir)
            out_path = output_dir / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            self.translate_html_file(html_file, out_path)
        
        # Traiter les fichiers PDF
        pdf_files = list(input_dir.rglob('*.pdf'))
        print(f"\n📕 Fichiers PDF trouvés: {len(pdf_files)}")
        
        for pdf_file in pdf_files:
            rel_path = pdf_file.relative_to(input_dir)
            out_path = (output_dir / rel_path).with_suffix('.en.html')
            out_path.parent.mkdir(parents=True, exist_ok=True)
            self.translate_pdf_file(pdf_file, out_path)
        
        # Générer le rapport
        self._generate_report(output_dir)
        
        print("\n" + "=" * 70)
        print("✅ TRADUCTION TERMINÉE")
        print(f"📊 HTML: {self.stats.html_files}, PDF: {self.stats.pdf_files}")
        print(f"📝 Segments traduits: {self.stats.text_segments}")
        if self.stats.errors:
            print(f"⚠️  Erreurs: {len(self.stats.errors)}")
        print("=" * 70)
    
    def _generate_report(self, output_dir: Path):
        """Génère un rapport de traduction"""
        report = {
            'date': '2026-04-05',
            'statistics': {
                'html_files': self.stats.html_files,
                'pdf_files': self.stats.pdf_files,
                'text_segments': self.stats.text_segments,
                'errors_count': len(self.stats.errors),
                'errors': self.stats.errors
            },
            'dictionaries': {
                'scientific_terms': len(self.scientific_terms),
                'common_phrases': len(self.common_phrases)
            }
        }
        
        # Sauvegarder JSON
        json_path = output_dir / 'translation_report.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Sauvegarder Markdown
        md_path = output_dir / 'TRANSLATION_REPORT.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Translation Report - Course Materials FR → EN\n\n")
            f.write("**Date:** 2026-04-05\n\n")
            f.write("## Statistics\n\n")
            f.write(f"- **HTML files translated:** {self.stats.html_files}\n")
            f.write(f"- **PDF files processed:** {self.stats.pdf_files}\n")
            f.write(f"- **Text segments translated:** {self.stats.text_segments}\n")
            f.write(f"- **Errors:** {len(self.stats.errors)}\n\n")
            
            if self.stats.errors:
                f.write("## Errors\n\n")
                for error in self.stats.errors:
                    f.write(f"- {error}\n")
            
            f.write("\n## Dictionaries Used\n\n")
            f.write(f"- Scientific terms: {len(self.scientific_terms)} entries\n")
            f.write(f"- Common phrases: {len(self.common_phrases)} entries\n\n")
            
            f.write("## Sample Translations\n\n")
            f.write("| French | English |\n")
            f.write("|--------|---------|\n")
            sample_terms = list(self.scientific_terms.items())[:20]
            for fr, en in sample_terms:
                f.write(f"| {fr} | {en} |\n")
        
        print(f"\n📊 Rapport généré: {md_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Traduit les cours PDF et HTML du FR vers EN'
    )
    parser.add_argument(
        'input',
        nargs='?',
        default='.',
        help='Dossier contenant les fichiers à traduire (défaut: courant)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Dossier de sortie (défaut: même que input)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Affiche les statistiques sans traduire'
    )
    
    args = parser.parse_args()
    
    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve() if args.output else input_dir
    
    if args.dry_run:
        # Mode simulation: compter les fichiers
        html_files = list(input_dir.rglob('*.html')) + list(input_dir.rglob('*.htm'))
        pdf_files = list(input_dir.rglob('*.pdf'))
        print(f"📄 HTML files to translate: {len(html_files)}")
        print(f"📕 PDF files to process: {len(pdf_files)}")
        for f in html_files[:5]:
            print(f"  - {f.relative_to(input_dir)}")
        for f in pdf_files:
            print(f"  - {f.relative_to(input_dir)}")
        return
    
    translator = CourseTranslator()
    translator.process_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
