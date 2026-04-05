#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de traduction complète des cours PDF et HTML - FR → EN
Version 3.0 - Avec traduction PDF avancée et termes spécifiques au cours
Auteur: Assistant IA
Date: 2026-04-05
"""

import os
import re
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TranslationStats:
    html_files: int = 0
    pdf_files: int = 0
    pdf_pages_translated: int = 0
    text_segments: int = 0
    scientific_terms_found: Set[str] = field(default_factory=set)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return {
            'html_files': self.html_files,
            'pdf_files': self.pdf_files,
            'pdf_pages_translated': self.pdf_pages_translated,
            'text_segments': self.text_segments,
            'scientific_terms_found': list(self.scientific_terms_found),
            'errors_count': len(self.errors),
            'errors': self.errors
        }


class CourseTranslator:
    def __init__(self):
        self.stats = TranslationStats()
        
        # Dictionnaires de traduction
        self.scientific_terms = self._load_scientific_dictionary()
        self.specific_course_terms = self._load_course_specific_terms()
        self.common_phrases = self._load_common_phrases()
        self.abbreviations = self._load_abbreviations()
        
        # Combiner tous les termes scientifiques
        self.all_terms = {**self.scientific_terms, **self.specific_course_terms}
        
    def _load_scientific_dictionary(self) -> Dict[str, str]:
        """Dictionnaire scientifique général de biologie du développement"""
        return {
            # === TERMINOLOGIE GÉNÉRALE ===
            "embryon": "embryo",
            "embryonnaire": "embryonic",
            "embryonnaires": "embryonic",
            "développement": "development",
            "développemental": "developmental",
            "développementale": "developmental",
            "développementaux": "developmental",
            "génétique": "genetics",
            "génétiques": "genetic",
            "moléculaire": "molecular",
            "moléculaires": "molecular",
            "cellule": "cell",
            "cellules": "cells",
            "cellulaire": "cellular",
            "cellulaires": "cellular",
            "tissu": "tissue",
            "tissus": "tissues",
            "organe": "organ",
            "organes": "organs",
            "organisme": "organism",
            "organismes": "organisms",
            "biologie": "biology",
            "biologique": "biological",
            "biologiques": "biological",
            
            # === DROSOPHILA SPÉCIFIQUE ===
            "drosophile": "Drosophila",
            "drosophila": "Drosophila",
            "mouche": "fly",
            "mouches": "flies",
            "mouche du vinaigre": "vinegar fly",
            "mouche des fruits": "fruit fly",
            "métamorphose": "metamorphosis",
            "cycle de vie": "life cycle",
            "cycles de vie": "life cycles",
            "stade": "stage",
            "stades": "stages",
            "stade larvaire": "larval stage",
            "stade pupal": "pupal stage",
            "stade embryonnaire": "embryonic stage",
            "larve": "larva",
            "larves": "larvae",
            "larvaire": "larval",
            "larvaires": "larval",
            "pupaison": "pupariation",
            "pupe": "pupa",
            "pupes": "pupae",
            "pupal": "pupal",
            "imago": "adult",
            "adulte": "adult",
            "adultes": "adults",
            "oeuf": "egg",
            "oeufs": "eggs",
            "ovocyte": "oocyte",
            "ovocytes": "oocytes",
            "ovocyte I": "primary oocyte",
            "ovocyte II": "secondary oocyte",
            "ovule": "ovum",
            "ovules": "ova",
            "spermatozoïde": "sperm",
            "spermatozoïdes": "sperm",
            "spermatogenèse": "spermatogenesis",
            "fécondation": "fertilization",
            "zigote": "zygote",
            "blastoderme": "blastoderm",
            "blastodermique": "blastodermic",
            "blastodermiques": "blastodermic",
            "gastrulation": "gastrulation",
            "germe": "germ",
            "ligne germinale": "germ line",
            "lignes germinales": "germ lines",
            "cellules germinales": "germ cells",
            "cellule germinale": "germ cell",
            "plasmique": "plasmic",
            "plasme germinal": "germ plasm",
            "plasme": "plasm",
            
            # === OVOGENÈSE ET REPRODUCTION ===
            "ovogenèse": "oogenesis",
            "ovariole": "ovariole",
            "ovarioles": "ovarioles",
            "ovaire": "ovary",
            "ovaires": "ovaries",
            "follicule": "follicle",
            "follicules": "follicles",
            "cellule folliculaire": "follicle cell",
            "cellules folliculaires": "follicle cells",
            "cellules nourricières": "nurse cells",
            "cellule nourricière": "nurse cell",
            "chambre ovarienne": "egg chamber",
            "chambres ovariennes": "egg chambers",
            "pédicelle": "stalk",
            "pédicelles": "stalks",
            "germarium": "germarium",
            "vitellogenèse": "vitellogenesis",
            "vitelline": "vitelline",
            "membrane vitelline": "vitelline membrane",
            "chorion": "chorion",
            "coque": "shell",
            "coques": "shells",
            "réticulum endoplasmique": "endoplasmic reticulum",
            "appareil de Golgi": "Golgi apparatus",
            "mitochondries": "mitochondria",
            "mitochondrie": "mitochondrion",
            "ribosomes": "ribosomes",
            "ribosome": "ribosome",
            
            # === AXES ET POLARITÉ ===
            "pôle animal": "animal pole",
            "pôles animaux": "animal poles",
            "pôle végétal": "vegetal pole",
            "pôles végétaux": "vegetal poles",
            "pôle antérieur": "anterior pole",
            "pôles antérieurs": "anterior poles",
            "pôle postérieur": "posterior pole",
            "pôles postérieurs": "posterior poles",
            "pôle dorsal": "dorsal pole",
            "pôle ventral": "ventral pole",
            "axe antéro-postérieur": "anteroposterior axis",
            "axes antéro-postérieurs": "anteroposterior axes",
            "axe A-P": "A-P axis",
            "axe dorso-ventral": "dorsoventral axis",
            "axes dorso-ventraux": "dorsoventral axes",
            "axe D-V": "D-V axis",
            "axe gauche-droite": "left-right axis",
            "polarité": "polarity",
            "polarités": "polarities",
            "gradient": "gradient",
            "gradients": "gradients",
            "gradient de concentration": "concentration gradient",
            "morphogène": "morphogen",
            "morphogènes": "morphogens",
            "champ morphogénétique": "morphogenetic field",
            "champs morphogénétiques": "morphogenetic fields",
            "positionnement": "positioning",
            "positionnements": "positionings",
            "localisation": "localization",
            "localisations": "localizations",
            "asymétrie": "asymmetry",
            "asymétries": "asymmetries",
            "asymétrique": "asymmetric",
            "asymétriques": "asymmetric",
            "symétrie": "symmetry",
            "symétrique": "symmetric",
            "symétriques": "symmetric",
            
            # === SEGMENTATION ===
            "segmentation": "segmentation",
            "segment": "segment",
            "segments": "segments",
            "segmenté": "segmented",
            "segmentée": "segmented",
            "segmentés": "segmented",
            "segmentées": "segmented",
            "parasegment": "parasegment",
            "parasegments": "parasegments",
            "parasegmenté": "parasegmental",
            "métamère": "metamere",
            "métamères": "metameres",
            "métamérisation": "metamerism",
            "somitogenèse": "somitogenesis",
            "cascade de segmentation": "segmentation cascade",
            "cascades de segmentation": "segmentation cascades",
            "gènes de segmentation": "segmentation genes",
            "gène de segmentation": "segmentation gene",
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
            "even skipped": "even-skipped",
            "ftz": "ftz",
            "fushi tarazu": "fushi tarazu",
            "runt": "runt",
            "hairy": "hairy",
            "paired": "paired",
            "sloppy paired": "sloppy paired",
            "odd-skipped": "odd-skipped",
            "odd skipped": "odd-skipped",
            "stripe": "stripe",
            "stripes": "stripes",
            "expression en bandes": "striped expression",
            "bandes": "stripes",
            "bande": "stripe",
            "frontière de parasegment": "parasegment boundary",
            "frontières de parasegment": "parasegment boundaries",
            
            # === GÈNES HOMÉOTIQUES ===
            "gène homéotique": "homeotic gene",
            "gènes homéotiques": "homeotic genes",
            "homéose": "homeosis",
            "homéotique": "homeotic",
            "homéotiques": "homeotic",
            "sélecteur de segment": "segment selector",
            "sélecteurs de segment": "segment selectors",
            "gène sélecteur": "selector gene",
            "gènes sélecteurs": "selector genes",
            "identité segmentaire": "segmental identity",
            "identités segmentaires": "segmental identities",
            "complexe bithorax": "bithorax complex",
            "complexe BX-C": "BX-C complex",
            "complexe antennapedia": "antennapedia complex",
            "complexe ANT-C": "ANT-C complex",
            "homéoboîte": "homeobox",
            "homéoboîtes": "homeoboxes",
            "homéodomaine": "homeodomain",
            "homéodomaines": "homeodomains",
            "protéine homéotique": "homeotic protein",
            "protéines homéotiques": "homeotic proteins",
            "facteur de transcription homéotique": "homeotic transcription factor",
            "facteurs de transcription homéotiques": "homeotic transcription factors",
            "antennapedia": "antennapedia",
            "bithorax": "bithorax",
            "ultrabithorax": "ultrabithorax",
            "Ubx": "Ubx",
            "abdominal-A": "abdominal-A",
            "Abd-A": "Abd-A",
            "abdominal-B": "abdominal-B",
            "Abd-B": "Abd-B",
            "labial": "labial",
            "Lab": "Lab",
            "proboscipedia": "proboscipedia",
            "Pb": "Pb",
            "deformed": "deformed",
            "Dfd": "Dfd",
            "sex combs reduced": "sex combs reduced",
            "Scr": "Scr",
            "antennapedia": "antennapedia",
            "Antp": "Antp",
            
            # === VOIES DE SIGNALISATION ===
            "signalisation": "signaling",
            "signalisations": "signalings",
            "voie de signalisation": "signaling pathway",
            "voies de signalisation": "signaling pathways",
            "cascade de signalisation": "signaling cascade",
            "cascades de signalisation": "signaling cascades",
            "transduction du signal": "signal transduction",
            "transductions du signal": "signal transductions",
            "récepteur": "receptor",
            "récepteurs": "receptors",
            "récepteur tyrosine kinase": "receptor tyrosine kinase",
            "récepteurs tyrosine kinase": "receptor tyrosine kinases",
            "RTK": "RTK",
            "ligand": "ligand",
            "ligands": "ligands",
            "activation": "activation",
            "activations": "activations",
            "inhibition": "inhibition",
            "inhibitions": "inhibitions",
            "inhibiteur": "inhibitor",
            "inhibiteurs": "inhibitors",
            "activateur": "activator",
            "activateurs": "activators",
            "voie Ras/MAPK": "Ras/MAPK pathway",
            "voies Ras/MAPK": "Ras/MAPK pathways",
            "cascade Ras/MAPK": "Ras/MAPK cascade",
            "cascades Ras/MAPK": "Ras/MAPK cascades",
            "voie JAK/STAT": "JAK/STAT pathway",
            "voie Wnt": "Wnt pathway",
            "voie Hedgehog": "Hedgehog pathway",
            "voie Notch": "Notch pathway",
            "voie TGF-β": "TGF-β pathway",
            "voie BMP": "BMP pathway",
            "voie de signalisation TGF-β": "TGF-β signaling pathway",
            "protéine kinase": "protein kinase",
            "protéines kinases": "protein kinases",
            "phosphorylation": "phosphorylation",
            "déphosphorylation": "dephosphorylation",
            "cascade de phosphorylation": "phosphorylation cascade",
            
            # === FACTEURS DE TRANSCRIPTION ===
            "facteur de transcription": "transcription factor",
            "facteurs de transcription": "transcription factors",
            "TF": "TF",
            "expression génique": "gene expression",
            "expressions géniques": "gene expressions",
            "régulation de l'expression": "expression regulation",
            "régulations de l'expression": "expression regulations",
            "promoteur": "promoter",
            "promoteurs": "promoters",
            "enhancer": "enhancer",
            "enhancers": "enhancers",
            "élément cis-régulateur": "cis-regulatory element",
            "éléments cis-régulateurs": "cis-regulatory elements",
            "élément cis-régulateur distal": "distal cis-regulatory element",
            "silencieur": "silencer",
            "silencieurs": "silencers",
            "insulateur": "insulator",
            "insulateurs": "insulators",
            "boîte promotrice": "promoter box",
            "site de liaison": "binding site",
            "sites de liaison": "binding sites",
            "domaine de liaison à l'ADN": "DNA-binding domain",
            "domaines de liaison à l'ADN": "DNA-binding domains",
            "activation transcriptionnelle": "transcriptional activation",
            "répression transcriptionnelle": "transcriptional repression",
            
            # === SYSTÈMES MATERNELS ===
            "système antérieur": "anterior system",
            "systèmes antérieurs": "anterior systems",
            "système postérieur": "posterior system",
            "systèmes postérieurs": "posterior systems",
            "système terminal": "terminal system",
            "systèmes terminaux": "terminal systems",
            "système dorso-ventral": "dorsoventral system",
            "systèmes dorso-ventraux": "dorsoventral systems",
            "bicoid": "bicoid",
            "Bcd": "Bcd",
            "nanos": "nanos",
            "Nos": "Nos",
            "oskar": "oskar",
            "Osk": "Osk",
            "staufen": "staufen",
            "Stau": "Stau",
            "torso": "torso",
            "Tor": "Tor",
            "torso-like": "torso-like",
            "Tsl": "Tsl",
            "trunk": "trunk",
            "Trk": "Trk",
            "pipe": "pipe",
            "nudel": "nudel",
            "gdl": "gdl",
            "Gdl": "Gdl",
            "easter": "easter",
            "Ea": "Ea",
            "snake": "snake",
            "Snk": "Snk",
            "gd": "gd",
            "Gdl": "Gdl",
            "dorsal": "dorsal",
            "Dl": "Dl",
            "cactus": "cactus",
            "Cact": "Cact",
            "pelle": "pelle",
            "pll": "pll",
            "tube": "tube",
            "transport": "transport",
            "transport actif": "active transport",
            "diffusion": "diffusion",
            "diffusions": "diffusions",
            "déterminant cytoplasmique": "cytoplasmic determinant",
            "déterminants cytoplasmiques": "cytoplasmic determinants",
            "déterminant de polarité": "polarity determinant",
            "déterminants de polarité": "polarity determinants",
            "ARNm": "mRNA",
            "ARN messager": "messenger RNA",
            "ARN": "RNA",
            "traduction": "translation",
            "traductions": "translations",
            "synthèse protéique": "protein synthesis",
            "synthèses protéiques": "protein syntheses",
            "localisation de l'ARNm": "mRNA localization",
            "localisations de l'ARNm": "mRNA localizations",
            "stabilisation de l'ARNm": "mRNA stabilization",
            "dégradation de l'ARNm": "mRNA degradation",
            "transport de l'ARNm": "mRNA transport",
            "granule de germe": "germ granule",
            "granules de germe": "germ granules",
            "nuage de polarité": "polar plasm",
            "nuage périnucléaire": "perinuclear cloud",
            "corps de Balbiani": "Balbiani body",
            
            # === MOUVEMENTS ET MIGRATIONS ===
            "migration cellulaire": "cell migration",
            "migrations cellulaires": "cell migrations",
            "invagination": "invagination",
            "invaginations": "invaginations",
            "involution": "involution",
            "épibolie": "epiboly",
            "convergence": "convergence",
            "extension": "extension",
            "convergence et extension": "convergence and extension",
            "mouvement morphogénétique": "morphogenetic movement",
            "mouvements morphogénétiques": "morphogenetic movements",
            "repliement": "folding",
            "repliements": "foldings",
            "constriction": "constriction",
            "constrictions": "constrictions",
            "cinétose": "kinesis",
            "chimiotactisme": "chemotaxis",
            
            # === STRUCTURES EMBRYONNAIRES ===
            "feuillet germinatif": "germ layer",
            "feuillets germinatifs": "germ layers",
            "ectoderme": "ectoderm",
            "ectodermique": "ectodermal",
            "mésoderme": "mesoderm",
            "mésodermique": "mesodermal",
            "endoderme": "endoderm",
            "endodermique": "endodermal",
            "ectomesoderme": "ectomesoderm",
            "arc entérique": "intestinal arch",
            "squelette": "skeleton",
            "système nerveux": "nervous system",
            "tube nerveux": "neural tube",
            "plaque neurale": "neural plate",
            "crête neurale": "neural crest",
            "sillon neurale": "neural groove",
            "lèvre dorsale": "dorsal lip",
            "organisateur": "organizer",
            "centre organisateur": "organizer center",
            "champ céphalique": "cephalic field",
            
            # === MOLÉCULES ET PROTÉINES ===
            "protéine": "protein",
            "protéines": "proteins",
            "glycoprotéine": "glycoprotein",
            "glycoprotéines": "glycoproteins",
            "protéine mère": "maternal protein",
            "protéines mères": "maternal proteins",
            "protéine zygotique": "zygotic protein",
            "protéines zygotiques": "zygotic proteins",
            "protéine de choc thermique": "heat shock protein",
            "protéines de choc thermique": "heat shock proteins",
            "HSP": "HSP",
            "chaperon moléculaire": "molecular chaperone",
            "chaperons moléculaires": "molecular chaperones",
            "facteur de croissance": "growth factor",
            "facteurs de croissance": "growth factors",
            "facteur de croissance épithélial": "epidermal growth factor",
            "EGF": "EGF",
            "récepteur EGF": "EGF receptor",
            "FGF": "FGF",
            "facteur de croissance des fibroblastes": "fibroblast growth factor",
            "TGF-β": "TGF-β",
            "facteur de transformation bêta": "transforming growth factor beta",
            "BMP": "BMP",
            "protéine morphogénétique osseuse": "bone morphogenetic protein",
            "Shh": "Shh",
            "sonic hedgehog": "sonic hedgehog",
            "Wnt": "Wnt",
            "wingless-related": "wingless-related",
            "Notch": "Notch",
            "Delta": "Delta",
            "Serrate": "Serrate",
            "Jagged": "Jagged",
            
            # === MÉTHODOLOGIE ===
            "microscopie": "microscopy",
            "microscope": "microscope",
            "microscopes": "microscopes",
            "microscopique": "microscopic",
            "microscopiques": "microscopic",
            "immunofluorescence": "immunofluorescence",
            "immunohistochimie": "immunohistochemistry",
            "hybridation in situ": "in situ hybridization",
            "ISH": "ISH",
            "marquage": "labeling",
            "marquages": "labelings",
            "sonde": "probe",
            "sondes": "probes",
            "anticorps": "antibody",
            "anticorps monoclonal": "monoclonal antibody",
            "anticorps polyclonal": "polyclonal antibody",
            "clonage moléculaire": "molecular cloning",
            "séquençage": "sequencing",
            "séquençage ADN": "DNA sequencing",
            "PCR": "PCR",
            "réaction en chaîne de la polymérase": "polymerase chain reaction",
            "génie génétique": "genetic engineering",
            "transformation génétique": "genetic transformation",
            "transgénèse": "transgenesis",
            "organisme transgénique": "transgenic organism",
            "organismes transgéniques": "transgenic organisms",
            "lignée transgénique": "transgenic line",
            "lignées transgéniques": "transgenic lines",
            "mutant": "mutant",
            "mutants": "mutants",
            "mutation": "mutation",
            "mutations": "mutations",
            "allèle": "allele",
            "allèles": "alleles",
            "allèle sauvage": "wild-type allele",
            "allèle mutant": "mutant allele",
            "phénotype": "phenotype",
            "phénotypes": "phenotypes",
            "génotype": "genotype",
            "génotypes": "genotypes",
            "phénotype sauvage": "wild-type phenotype",
            "phénotype mutant": "mutant phenotype",
            "souche": "strain",
            "souches": "strains",
            "souche sauvage": "wild-type strain",
            "lignée": "line",
            "lignées": "lines",
            
            # === ANATOMIE DROSOPHILA ===
            "cuticule": "cuticle",
            "cuticules": "cuticles",
            "endocuticule": "endocuticle",
            "exocuticule": "exocuticle",
            "épicuticule": "epicuticle",
            "chitine": "chitin",
            "sclérite": "sclerite",
            "sclérites": "sclerites",
            "tergite": "tergite",
            "tergites": "tergites",
            "sternite": "sternite",
            "sternites": "sternites",
            "pleure": "pleuron",
            "pleures": "pleura",
            "appendice": "appendage",
            "appendices": "appendages",
            "patte": "leg",
            "pattes": "legs",
            "aile": "wing",
            "ailes": "wings",
            "haltere": "haltere",
            "halteres": "halteres",
            "antenne": "antenna",
            "antennes": "antennae",
            "mandibule": "mandible",
            "mandibules": "mandibles",
            "maxille": "maxilla",
            "maxilles": "maxillae",
            "labium": "labium",
            "clypéo-labrum": "clypeo-labrum",
            "tête": "head",
            "thorax": "thorax",
            "abdomen": "abdomen",
            "segment thoracique": "thoracic segment",
            "segments thoraciques": "thoracic segments",
            "segment abdominal": "abdominal segment",
            "segments abdominaux": "abdominal segments",
            "segment céphalique": "cephalic segment",
            "segments céphaliques": "cephalic segments",
            
            # === PHYSIOLOGIE ===
            "métabolisme": "metabolism",
            "métabolique": "metabolic",
            "métaboliques": "metabolic",
            "respiration": "respiration",
            "respiratoire": "respiratory",
            "respiratoires": "respiratory",
            "circulation": "circulation",
            "circulatoire": "circulatory",
            "circulatoires": "circulatory",
            "système immunitaire": "immune system",
            "immunité": "immunity",
            "immunitaire": "immune",
            "développement post-embryonnaire": "post-embryonic development",
            "développement post-embryonnaires": "post-embryonic developments",
        }
    
    def _load_course_specific_terms(self) -> Dict[str, str]:
        """Termes spécifiques au cours de Dr. Allouche - L3 Génétique Oran"""
        return {
            # === NOMENCLATURE SPÉCIFIQUE AU COURS ===
            "cours magistral": "lecture",
            "cours magistraux": "lectures",
            "travaux dirigés": "tutorials",
            "travail dirigé": "tutorial",
            "TD": "tutorials",
            "T.D.": "tutorials",
            "session de TD": "tutorial session",
            "séance de TD": "tutorial session",
            "séances de TD": "tutorial sessions",
            "contrôle continu": "continuous assessment",
            "contrôles continus": "continuous assessments",
            "CC": "CA",
            "C.C.": "C.A.",
            "examen": "exam",
            "examens": "exams",
            "examen final": "final exam",
            "examen partiel": "midterm exam",
            "session principale": "main session",
            "session de rattrapage": "remedial session",
            "rattrapage": "remedial exam",
            "note": "grade",
            "notes": "grades",
            "moyenne": "average",
            "moyennes": "averages",
            "coefficient": "coefficient",
            "coefficients": "coefficients",
            "crédit": "credit",
            "crédits": "credits",
            "unité d'enseignement": "teaching unit",
            "unités d'enseignement": "teaching units",
            "UE": "TU",
            "semestre": "semester",
            "semestres": "semesters",
            "année universitaire": "academic year",
            "licence": "bachelor's degree",
            "master": "master's degree",
            "doctorat": "doctorate",
            "thèse": "thesis",
            "thèses": "theses",
            "soutenance": "defense",
            "soutenances": "defenses",
            
            # === STRUCTURE PÉDAGOGIQUE ===
            "programme": "curriculum",
            "programmes": "curricula",
            "syllabus": "syllabus",
            "syllabuses": "syllabi",
            "objectif pédagogique": "learning objective",
            "objectifs pédagogiques": "learning objectives",
            "compétence visée": "targeted skill",
            "compétences visées": "targeted skills",
            "apprentissage": "learning",
            "apprentissages": "learnings",
            "enseignement": "teaching",
            "enseignements": "teachings",
            "pédagogie": "pedagogy",
            "pédagogique": "pedagogical",
            "pédagogiques": "pedagogical",
            "didactique": "didactic",
            "didactiques": "didactics",
            "évaluation": "evaluation",
            "évaluations": "evaluations",
            "formative": "formative",
            "sommative": "summative",
            "diagnostique": "diagnostic",
            "certificative": "certificative",
            
            # === RESSOURCES PÉDAGOGIQUES ===
            "support de cours": "course material",
            "supports de cours": "course materials",
            "polycopié": "handout",
            "polycopiés": "handouts",
            "diapositive": "slide",
            "diapositives": "slides",
            "présentation PowerPoint": "PowerPoint presentation",
            "présentations PowerPoint": "PowerPoint presentations",
            "schéma explicatif": "explanatory diagram",
            "schémas explicatifs": "explanatory diagrams",
            "schéma animé": "animated diagram",
            "schémas animés": "animated diagrams",
            "vidéo pédagogique": "educational video",
            "vidéos pédagogiques": "educational videos",
            "capsule vidéo": "video capsule",
            "capsules vidéo": "video capsules",
            "ressource en ligne": "online resource",
            "ressources en ligne": "online resources",
            "ressource numérique": "digital resource",
            "ressources numériques": "digital resources",
            "plateforme d'apprentissage": "learning platform",
            "plateformes d'apprentissage": "learning platforms",
            "LMS": "LMS",
            "environnement numérique de travail": "digital work environment",
            "ENT": "DWE",
            "e-learning": "e-learning",
            "mooc": "MOOC",
            "moocs": "MOOCs",
            
            # === ACTIVITÉS PRATIQUES ===
            "travail pratique": "practical work",
            "travaux pratiques": "practical works",
            "TP": "PW",
            "T.P.": "P.W.",
            "séance pratique": "practical session",
            "séances pratiques": "practical sessions",
            "manipulation": "experiment",
            "manipulations": "experiments",
            "expérimentation": "experimentation",
            "expérimentations": "experimentations",
            "protocole expérimental": "experimental protocol",
            "protocoles expérimentaux": "experimental protocols",
            "protocole": "protocol",
            "protocoles": "protocols",
            "technique": "technique",
            "techniques": "techniques",
            "méthode": "method",
            "méthodes": "methods",
            "méthodologie": "methodology",
            "méthodologies": "methodologies",
            "guide méthodologique": "methodological guide",
            "guides méthodologiques": "methodological guides",
            
            # === EXERCICES ET ÉVALUATIONS ===
            "exercice d'application": "application exercise",
            "exercices d'application": "application exercises",
            "exercice dirigé": "guided exercise",
            "exercices dirigés": "guided exercises",
            "problème à résoudre": "problem to solve",
            "problèmes à résoudre": "problems to solve",
            "étude de cas": "case study",
            "études de cas": "case studies",
            "QCM": "MCQ",
            "question à choix multiples": "multiple choice question",
            "questions à choix multiples": "multiple choice questions",
            "question ouverte": "open question",
            "questions ouvertes": "open questions",
            "question fermée": "closed question",
            "questions fermées": "closed questions",
            "réponse courte": "short answer",
            "réponses courtes": "short answers",
            "dissertation": "essay",
            "dissertations": "essays",
            "compte-rendu": "report",
            "comptes-rendus": "reports",
            "analyse critique": "critical analysis",
            "analyses critiques": "critical analyses",
            
            # === INTERACTIONS ET COMMUNICATION ===
            "forum de discussion": "discussion forum",
            "forums de discussion": "discussion forums",
            "chat": "chat",
            "messagerie instantanée": "instant messaging",
            "visioconférence": "video conference",
            "visioconférences": "video conferences",
            "webinaire": "webinar",
            "webinaires": "webinars",
            "séance de questions-réponses": "Q&A session",
            "séances de questions-réponses": "Q&A sessions",
            "heures de bureau": "office hours",
            "tutorat": "tutoring",
            "accompagnement pédagogique": "pedagogical support",
            "accompagnements pédagogiques": "pedagogical supports",
            
            # === DOCUMENTATION SPÉCIFIQUE ===
            "annonce bienvenue": "welcome announcement",
            "annonces bienvenue": "welcome announcements",
            "message de bienvenue": "welcome message",
            "messages de bienvenue": "welcome messages",
            "présentation du module": "module introduction",
            "présentations des modules": "module introductions",
            "descriptif du cours": "course description",
            "descriptifs des cours": "course descriptions",
            "guide de l'étudiant": "student guide",
            "guides de l'étudiant": "student guides",
            "guide de l'enseignant": "instructor guide",
            "guides de l'enseignant": "instructor guides",
            "plan de cours": "course plan",
            "plans de cours": "course plans",
            "calendrier pédagogique": "academic calendar",
            "calendriers pédagogiques": "academic calendars",
            "bibliographie commentée": "annotated bibliography",
            "bibliographies commentées": "annotated bibliographies",
            "webographie": "webography",
            "webographies": "webographies",
            "lien utile": "useful link",
            "liens utiles": "useful links",
            
            # === NIVEAUX ET PRÉREQUIS ===
            "niveau L1": "L1 level",
            "niveau L2": "L2 level",
            "niveau L3": "L3 level",
            "niveau M1": "M1 level",
            "niveau M2": "M2 level",
            "niveau doctorat": "PhD level",
            "prérequis": "prerequisite",
            "prérequis": "prerequisites",
            "préalable": "prior knowledge",
            "préalables": "prior knowledge",
            "connaissance requise": "required knowledge",
            "connaissances requises": "required knowledge",
            "notion de base": "basic concept",
            "notions de base": "basic concepts",
            "notion fondamentale": "fundamental concept",
            "notions fondamentales": "fundamental concepts",
            "compétence préalable": "prior skill",
            "compétences préalables": "prior skills",
            
            # === SPÉCIALITÉS ORAN ===
            "département de biotechnologie": "Department of Biotechnology",
            "département de biologie": "Department of Biology",
            "faculté des sciences": "Faculty of Sciences",
            "faculté des sciences de la nature et de la vie": "Faculty of Natural and Life Sciences",
            "université d'Oran 1": "University of Oran 1",
            "université d'Oran 1 Ahmed Ben Bella": "University of Oran 1 Ahmed Ben Bella",
            "université d'Oran": "University of Oran",
            "maître de conférences": "Associate Professor",
            "maître de conférences en biologie": "Associate Professor in Biology",
            "doctorant": "PhD student",
            "doctorants": "PhD students",
            "thésard": "doctoral candidate",
            "thésards": "doctoral candidates",
            "chercheur": "researcher",
            "chercheurs": "researchers",
            "laboratoire de recherche": "research laboratory",
            "laboratoires de recherche": "research laboratories",
            "équipe de recherche": "research team",
            "équipes de recherche": "research teams",
            "projet de recherche": "research project",
            "projets de recherche": "research projects",
        }
    
    def _load_common_phrases(self) -> Dict[str, str]:
        """Phrases courantes dans les documents pédagogiques"""
        return {
            # === INTRODUCTIONS ===
            "Dans ce chapitre, nous allons étudier": "In this chapter, we will study",
            "Dans ce cours, nous allons voir": "In this course, we will examine",
            "Dans cette partie, nous allons analyser": "In this section, we will analyze",
            "Dans cette section, nous allons comprendre": "In this section, we will understand",
            "Nous allons voir que": "We will see that",
            "Nous allons démontrer que": "We will demonstrate that",
            "Nous allons étudier": "We will study",
            "Nous allons analyser": "We will analyze",
            "Nous allons comprendre": "We will understand",
            "Nous allons examiner": "We will examine",
            "Nous allons explorer": "We will explore",
            "Nous allons découvrir": "We will discover",
            "Nous allons apprendre": "We will learn",
            "Nous verrons que": "We will see that",
            "Nous verrons comment": "We will see how",
            "Nous verrons pourquoi": "We will see why",
            
            # === OBSERVATIONS ET FAITS ===
            "Il est important de noter que": "It is important to note that",
            "Il est essentiel de comprendre que": "It is essential to understand that",
            "Il est crucial de remarquer que": "It is crucial to notice that",
            "Il faut souligner que": "It should be emphasized that",
            "Il convient de mentionner que": "It is worth mentioning that",
            "Il est intéressant d'observer que": "It is interesting to observe that",
            "On observe que": "We observe that",
            "On constate que": "We find that",
            "On remarque que": "We notice that",
            "On note que": "We note that",
            "On peut voir que": "We can see that",
            "On peut observer que": "We can observe that",
            "On peut remarquer que": "We can notice that",
            "Il apparaît que": "It appears that",
            "Il semble que": "It seems that",
            "Il est clair que": "It is clear that",
            "Il est évident que": "It is evident that",
            "Il est manifeste que": "It is manifest that",
            
            # === RÉFÉRENCES AU CONTENU ===
            "Comme nous l'avons vu": "As we have seen",
            "Comme nous l'avons vu précédemment": "As we have seen previously",
            "Comme mentionné précédemment": "As previously mentioned",
            "Comme indiqué précédemment": "As previously indicated",
            "Comme nous l'avons mentionné": "As we have mentioned",
            "Comme nous l'avons indiqué": "As we have indicated",
            "Dans la section précédente": "In the previous section",
            "Dans le chapitre précédent": "In the previous chapter",
            "Dans la partie précédente": "In the previous part",
            "Dans la partie suivante": "In the following part",
            "Dans la section suivante": "In the following section",
            "Dans le chapitre suivant": "In the following chapter",
            "Comme nous le verrons": "As we will see",
            "Comme nous le verrons plus tard": "As we will see later",
            "Nous y reviendrons": "We will return to this",
            "Nous y reviendrons plus tard": "We will return to this later",
            
            # === DESCRIPTIONS DE FIGURES ===
            "La figure ci-dessus montre": "The figure above shows",
            "La figure ci-dessous illustre": "The figure below illustrates",
            "La figure suivante représente": "The following figure represents",
            "La figure précédente montrait": "The previous figure showed",
            "Comme le montre la figure": "As shown in the figure",
            "Comme l'illustre la figure": "As illustrated in the figure",
            "Cette figure représente": "This figure represents",
            "Cette figure montre": "This figure shows",
            "Cette figure illustre": "This figure illustrates",
            "Cette figure démontre": "This figure demonstrates",
            "Cette figure présente": "This figure presents",
            "Le schéma suivant présente": "The following diagram presents",
            "Le schéma ci-dessus montre": "The diagram above shows",
            "Le schéma ci-dessous illustre": "The diagram below illustrates",
            "Cette illustration démontre": "This illustration demonstrates",
            "Cette illustration montre": "This illustration shows",
            "Cette image représente": "This image represents",
            "Le tableau suivant présente": "The following table presents",
            "Le tableau ci-dessus montre": "The table above shows",
            "Le tableau ci-dessous indique": "The table below indicates",
            "Ces données montrent que": "These data show that",
            "Ces résultats montrent que": "These results show that",
            "Ces observations montrent que": "These observations show that",
            
            # === EXPLICATIONS ET CLARIFICATIONS ===
            "Cela signifie que": "This means that",
            "Cela veut dire que": "This means that",
            "Cela implique que": "This implies that",
            "Cela suggère que": "This suggests that",
            "Cela indique que": "This indicates that",
            "Cela montre que": "This shows that",
            "Cela démontre que": "This demonstrates that",
            "Cela prouve que": "This proves that",
            "En d'autres termes": "In other words",
            "Autrement dit": "In other words",
            "C'est-à-dire que": "That is to say",
            "C'est à dire que": "That is to say",
            "C'est-à-dire": "that is",
            "C'est à dire": "that is",
            "Plus précisément": "More precisely",
            "Plus exactement": "More exactly",
            "Pour être plus précis": "To be more precise",
            "Pour préciser": "To specify",
            "Pour clarifier": "To clarify",
            "Pour illustrer": "To illustrate",
            "Par exemple": "For example",
            "Prenons l'exemple de": "Let us take the example of",
            "Prenons comme exemple": "Let us take as an example",
            "À titre d'exemple": "As an example",
            "Par illustration": "By way of illustration",
            
            # === CONSÉQUENCES ET RÉSULTATS ===
            "Par conséquent": "Consequently",
            "Par conséquent,": "Therefore,",
            "En conséquence": "As a result",
            "En conséquence,": "As a result,",
            "De ce fait": "As a result",
            "De ce fait,": "As a result,",
            "De fait": "In fact",
            "De fait,": "In fact,",
            "Ainsi,": "Thus,",
            "Ainsi": "Thus",
            "C'est pourquoi": "That is why",
            "C'est la raison pour laquelle": "That is the reason why",
            "C'est pour cette raison que": "That is why",
            "En effet,": "Indeed,",
            "En effet": "Indeed",
            "En fait,": "In fact,",
            "En fait": "In fact",
            "Notons que": "Note that",
            "Remarquons que": "Let us note that",
            "Observons que": "Let us observe that",
            "Soulignons que": "Let us emphasize that",
            "Précisons que": "Let us specify that",
            "Précisons également que": "Let us also specify that",
            "Il est à noter que": "It should be noted that",
            "Il est à remarquer que": "It should be noted that",
            "Il est intéressant de noter que": "It is interesting to note that",
            "Il est important de remarquer que": "It is important to notice that",
            
            # === TRANSITIONS ===
            "Premièrement,": "First,",
            "Premièrement": "First",
            "Deuxièmement,": "Second,",
            "Deuxièmement": "Second",
            "Troisièmement,": "Third,",
            "Troisièmement": "Third",
            "Quatrièmement,": "Fourth,",
            "Quatrièmement": "Fourth",
            "Cinquièmement,": "Fifth,",
            "Cinquièmement": "Fifth",
            "En premier lieu": "First",
            "En second lieu": "Second",
            "En troisième lieu": "Third",
            "En quatrième lieu": "Fourth",
            "En cinquième lieu": "Fifth",
            "Enfin,": "Finally,",
            "Enfin": "Finally",
            "Pour finir": "To conclude",
            "Pour terminer": "To finish",
            "Pour conclure": "To conclude",
            "En conclusion": "In conclusion",
            "En guise de conclusion": "By way of conclusion",
            "Pour résumer": "To summarize",
            "En résumé": "In summary",
            "Pour synthétiser": "To synthesize",
            "En synthèse": "In synthesis",
            "D'une part": "On one hand",
            "D'autre part": "On the other hand",
            "D'une part... d'autre part": "On one hand... on the other hand",
            "Par ailleurs": "Furthermore",
            "Par ailleurs,": "Furthermore,",
            "De plus,": "Moreover,",
            "De plus": "Moreover",
            "En outre,": "Furthermore,",
            "En outre": "Furthermore",
            "En plus": "In addition",
            "Qui plus est": "What's more",
            "Cependant,": "However,",
            "Cependant": "However",
            "Néanmoins,": "Nevertheless,",
            "Néanmoins": "Nevertheless",
            "Toutefois,": "However,",
            "Toutefois": "However",
            "Pourtant,": "Yet,",
            "Pourtant": "Yet",
            "Malgré cela": "Despite this",
            "En dépit de cela": "Despite this",
            "Bien que": "Although",
            "Bien que...": "Although...",
            "Même si": "Even if",
            "Quoique": "Although",
            "Malgré": "Despite",
            "En dépit de": "Despite",
            "Grâce à": "Thanks to",
            "Grâce à...": "Thanks to...",
            "En raison de": "Due to",
            "En raison de...": "Due to...",
            "À cause de": "Because of",
            "À cause de...": "Because of...",
            "Du fait de": "Because of",
            "Suite à": "Following",
            "À la suite de": "As a result of",
            
            # === DÉFINITIONS ===
            "On définit": "We define",
            "On définit... comme": "We define... as",
            "On appelle": "We call",
            "On appelle...": "We call...",
            "Par définition": "By definition",
            "Il s'agit de": "It is about",
            "Il s'agit d'un": "It is a",
            "Il s'agit d'une": "It is a",
            "Cela correspond à": "This corresponds to",
            "Cela représente": "This represents",
            "Cela constitue": "This constitutes",
            "Cela forme": "This forms",
            "On peut définir": "We can define",
            "On peut définir... comme": "We can define... as",
            "Définissons": "Let us define",
            "Définissons... comme": "Let us define... as",
            
            # === PROCESSUS ET MÉCANISMES ===
            "Ce processus permet de": "This process allows",
            "Ce processus permet": "This process allows",
            "Ce mécanisme conduit à": "This mechanism leads to",
            "Ce mécanisme permet": "This mechanism allows",
            "Cette étape consiste à": "This step consists of",
            "Cette étape permet de": "This step allows",
            "Cette phase consiste à": "This phase consists of",
            "Cette phase permet de": "This phase allows",
            "Il en résulte que": "It follows that",
            "Il en découle que": "It follows that",
            "On aboutit à": "We end up with",
            "On obtient ainsi": "We thus obtain",
            "Cela aboutit à": "This results in",
            "Cela conduit à": "This leads to",
            "Cela mène à": "This leads to",
            "Cela entraîne": "This entails",
            "Cela provoque": "This causes",
            "Cela engendre": "This generates",
            "Cela donne lieu à": "This gives rise to",
            "Cela se traduit par": "This translates into",
            "Cela se manifeste par": "This manifests itself by",
            
            # === QUESTIONS ET EXERCICES ===
            "Question :": "Question:",
            "Questions :": "Questions:",
            "Question principale :": "Main question:",
            "Questions principales :": "Main questions:",
            "Exercice :": "Exercise:",
            "Exercices :": "Exercises:",
            "Exercice d'application :": "Application exercise:",
            "Exercices d'application :": "Application exercises:",
            "Problème :": "Problem:",
            "Problèmes :": "Problems:",
            "Problème à résoudre :": "Problem to solve:",
            "Problèmes à résoudre :": "Problems to solve:",
            "À compléter :": "To complete:",
            "À remplir :": "To fill in:",
            "À faire :": "To do:",
            "À réaliser :": "To carry out:",
            "Réponse :": "Answer:",
            "Réponses :": "Answers:",
            "Solution :": "Solution:",
            "Solutions :": "Solutions:",
            "Solution proposée :": "Proposed solution:",
            "Solutions proposées :": "Proposed solutions:",
            "Indice :": "Hint:",
            "Indices :": "Hints:",
            "Conseil :": "Tip:",
            "Conseils :": "Tips:",
            "Aide :": "Help:",
            "Aides :": "Helps:",
            
            # === INSTRUCTIONS POUR ÉTUDIANTS ===
            "Cliquez sur": "Click on",
            "Cliquez ici": "Click here",
            "Sélectionnez": "Select",
            "Sélectionnez...": "Select...",
            "Choisissez": "Choose",
            "Choisissez...": "Choose...",
            "Identifiez": "Identify",
            "Identifiez...": "Identify...",
            "Nommez": "Name",
            "Nommez...": "Name...",
            "Décrivez": "Describe",
            "Décrivez...": "Describe...",
            "Expliquez": "Explain",
            "Expliquez...": "Explain...",
            "Analysez": "Analyze",
            "Analysez...": "Analyze...",
            "Comparez": "Compare",
            "Comparez...": "Compare...",
            "Distinguez": "Distinguish",
            "Distinguez...": "Distinguish...",
            "Différenciez": "Differentiate",
            "Différenciez...": "Differentiate...",
            "Illustrez": "Illustrate",
            "Illustrez...": "Illustrate...",
            "Représentez": "Represent",
            "Représentez...": "Represent...",
            "Schématisez": "Diagram",
            "Schématisez...": "Diagram...",
            "Localisez": "Locate",
            "Localisez...": "Locate...",
            "Indiquez": "Indicate",
            "Indiquez...": "Indicate...",
            "Précisez": "Specify",
            "Précisez...": "Specify...",
            "Justifiez votre réponse": "Justify your answer",
            "Justifiez vos réponses": "Justify your answers",
            "Donnez un exemple": "Give an example",
            "Donnez des exemples": "Give examples",
            "Citez un exemple": "Cite an example",
            "Citez des exemples": "Cite examples",
            "Proposez une explication": "Propose an explanation",
            "Proposez des explications": "Propose explanations",
            "Formulez une hypothèse": "Formulate a hypothesis",
            "Formulez des hypothèses": "Formulate hypotheses",
            "Vérifiez votre réponse": "Check your answer",
            "Vérifiez vos réponses": "Check your answers",
            "Corrigez si nécessaire": "Correct if necessary",
            
            # === REMARQUES ET NOTES ===
            "Remarque :": "Note:",
            "Remarques :": "Notes:",
            "Note :": "Note:",
            "Notes :": "Notes:",
            "Important :": "Important:",
            "Attention :": "Warning:",
            "Attention !": "Warning!",
            "Précaution :": "Caution:",
            "Rappel :": "Reminder:",
            "Rappels :": "Reminders:",
            "Exemple :": "Example:",
            "Exemples :": "Examples:",
            "Contre-exemple :": "Counter-example:",
            "Contre-exemples :": "Counter-examples:",
            "Exception :": "Exception:",
            "Exceptions :": "Exceptions:",
            "Cas particulier :": "Special case:",
            "Cas particuliers :": "Special cases:",
            "Cas général :": "General case:",
            "Limitation :": "Limitation:",
            "Limitations :": "Limitations:",
            "Hypothèse :": "Hypothesis:",
            "Hypothèses :": "Hypotheses:",
            "Condition :": "Condition:",
            "Conditions :": "Conditions:",
            "Prérequis :": "Prerequisites:",
        }
    
    def _load_abbreviations(self) -> Dict[str, str]:
        """Abréviations et acronymes spécifiques"""
        return {
            # Abréviations scientifiques
            "ARNm": "mRNA",
            "ARN": "RNA",
            "ADN": "DNA",
            "ARNt": "tRNA",
            "ARNr": "rRNA",
            "PCR": "PCR",
            "RT-PCR": "RT-PCR",
            "qPCR": "qPCR",
            "RT-qPCR": "RT-qPCR",
            "ISH": "ISH",
            "FISH": "FISH",
            "GFP": "GFP",
            "EGFP": "EGFP",
            "RFP": "RFP",
            "YFP": "YFP",
            "CFP": "CFP",
            "HSP": "HSP",
            "HSP70": "HSP70",
            "HSP90": "HSP90",
            "RTK": "RTK",
            "MAPK": "MAPK",
            "ERK": "ERK",
            "JNK": "JNK",
            "p38": "p38",
            "PI3K": "PI3K",
            "AKT": "AKT",
            "mTOR": "mTOR",
            "NF-κB": "NF-κB",
            "TGF-β": "TGF-β",
            "BMP": "BMP",
            "FGF": "FGF",
            "EGF": "EGF",
            "VEGF": "VEGF",
            "Wnt": "Wnt",
            "Shh": "Shh",
            "Hh": "Hh",
            "Notch": "Notch",
            "Delta": "Delta",
            "Jagged": "Jagged",
            
            # Abréviations pédagogiques
            "L1": "L1",
            "L2": "L2",
            "L3": "L3",
            "M1": "M1",
            "M2": "M2",
            "L1-S1": "L1-S1",
            "L1-S2": "L1-S2",
            "L2-S3": "L2-S3",
            "L2-S4": "L2-S4",
            "L3-S5": "L3-S5",
            "L3-S6": "L3-S6",
            "S1": "S1",
            "S2": "S2",
            "S3": "S3",
            "S4": "S4",
            "S5": "S5",
            "S6": "S6",
            "ECTS": "ECTS",
            "CM": "CM",
            "TD": "TD",
            "TP": "PW",
            "CC": "CA",
            "DS": "MT",
            "EX": "FE",
        }
    
    def translate_html_file(self, input_path: Path, output_path: Optional[Path] = None) -> bool:
        """Traduit un fichier HTML en préservant la structure et les liens"""
        try:
            if output_path is None:
                output_path = input_path
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            translation_count = 0
            
            # Suivre les termes trouvés
            found_terms = set()
            
            # 1. Traduire le contenu textuel entre balises
            def translate_tag_content(match):
                before = match.group(1)
                text = match.group(2)
                after = match.group(3)
                
                # Ne pas traduire dans script ou style
                if before.lower().startswith(('<script', '<style')):
                    return match.group(0)
                
                translated_text, count, terms = self._translate_text_advanced(text)
                nonlocal translation_count, found_terms
                translation_count += count
                found_terms.update(terms)
                
                return f'{before}{translated_text}{after}'
            
            content = re.sub(
                r'(</?[a-zA-Z][^>]*>)([^<]*)(</[a-zA-Z][^>]*>)',
                translate_tag_content,
                content,
                flags=re.DOTALL
            )
            
            # 2. Traduire les attributs alt, title, placeholder
            def translate_attribute(match):
                attr_name = match.group(1).lower()
                quote = match.group(2)
                attr_value = match.group(3)
                
                if attr_name in ['alt', 'title', 'placeholder', 'aria-label', 'aria-placeholder']:
                    translated, count, terms = self._translate_text_advanced(attr_value)
                    nonlocal translation_count, found_terms
                    translation_count += count
                    found_terms.update(terms)
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
                translated, count, terms = self._translate_text_advanced(match.group(1))
                nonlocal translation_count, found_terms
                translation_count += count
                found_terms.update(terms)
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
                r'xml:lang=["\']fr["\']',
                'xml:lang="en"',
                content,
                flags=re.IGNORECASE
            )
            
            # Sauvegarder
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats.html_files += 1
            self.stats.text_segments += translation_count
            self.stats.scientific_terms_found.update(found_terms)
            
            print(f"✅ HTML: {input_path.name} ({translation_count} traductions, {len(found_terms)} termes scientifiques)")
            return True
            
        except Exception as e:
            self.stats.errors.append(f"HTML {input_path}: {str(e)}")
            print(f"❌ Erreur HTML {input_path.name}: {e}")
            return False
    
    def _translate_text_advanced(self, text: str) -> Tuple[str, int, Set[str]]:
        """
        Traduction avancée avec comptage et détection de termes
        Retourne: (texte_traduit, nombre_traductions, termes_trouvés)
        """
        if not text or not isinstance(text, str):
            return text, 0, set()
        
        # Ne pas traduire les chemins de fichiers
        if text.strip().startswith(('http://', 'https://', 'mailto:', 'tel:', 
                                    './', '../', '/', '#', 'data:', 'javascript:')):
            return text, 0, set()
        
        # Ne pas traduire si c'est principalement du code
        if len(re.findall(r'[{}[\]();=<>]', text)) > len(text) * 0.1:
            return text, 0, set()
        
        result = text
        count = 0
        found_terms = set()
        
        # 1. Traduire les phrases courantes (priorité haute)
        for fr_phrase, en_phrase in sorted(self.common_phrases.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = re.compile(re.escape(fr_phrase), re.IGNORECASE)
            matches = list(pattern.finditer(result))
            if matches:
                count += len(matches)
                result = pattern.sub(en_phrase, result)
        
        # 2. Traduire les termes scientifiques avec détection
        for fr_term, en_term in sorted(self.all_terms.items(), key=lambda x: len(x[0]), reverse=True):
            # Utiliser word boundaries pour les mots complets
            pattern = re.compile(r'\b' + re.escape(fr_term) + r'\b', re.IGNORECASE)
            matches = list(pattern.finditer(result))
            if matches:
                count += len(matches)
                found_terms.add(f"{fr_term} → {en_term}")
                result = pattern.sub(en_term, result)
        
        # 3. Post-traitement
        result = self._post_process_translation(result)
        
        return result, count, found_terms
    
    def _post_process_translation(self, text: str) -> str:
        """Corrections post-traduction"""
        # Capitaliser Drosophila si au début de phrase
        text = re.sub(r'([.!?]\s+)drosophila', r'\1Drosophila', text, flags=re.IGNORECASE)
        text = re.sub(r'^drosophila', 'Drosophila', text, flags=re.IGNORECASE)
        
        # Corriger les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        # Corriger les espaces avant la ponctuation
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        
        # Corriger les espaces après les parenthèses ouvrantes et avant les fermantes
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        
        return text.strip()
    
    def translate_pdf_to_html(self, input_path: Path, output_path: Optional[Path] = None) -> bool:
        """
        Traduit un PDF en créant une version HTML entièrement traduite
        avec le texte français remplacé par l'anglais (pas bilingue)
        """
        try:
            if output_path is None:
                output_path = input_path.with_suffix('.en.html')
            
            print(f"📖 Traitement PDF: {input_path.name}...")
            
            # Extraire le texte du PDF
            extracted_text = self._extract_pdf_text_advanced(input_path)
            
            if not extracted_text:
                # Fallback: créer un résumé basique
                return self._create_basic_pdf_summary(input_path, output_path)
            
            # Traduire le contenu extrait
            translated_content = []
            total_pages = 0
            
            for page_num, page_text in enumerate(extracted_text, 1):
                total_pages += 1
                
                # Diviser en paragraphes
                paragraphs = page_text.split('\n\n')
                translated_paragraphs = []
                
                for para in paragraphs:
                    if para.strip():
                        translated, count, terms = self._translate_text_advanced(para.strip())
                        translated_paragraphs.append(translated)
                        self.stats.text_segments += count
                        self.stats.scientific_terms_found.update(terms)
                
                translated_content.append({
                    'page': page_num,
                    'paragraphs': translated_paragraphs
                })
            
            # Générer le HTML traduit
            html_content = self._create_translated_pdf_html(input_path.name, translated_content)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.stats.pdf_files += 1
            self.stats.pdf_pages_translated += total_pages
            
            print(f"✅ PDF traduit: {input_path.name} → {output_path.name} ({total_pages} pages)")
            return True
            
        except Exception as e:
            self.stats.errors.append(f"PDF {input_path}: {str(e)}")
            print(f"❌ Erreur PDF {input_path.name}: {e}")
            return False
    
    def _extract_pdf_text_advanced(self, pdf_path: Path) -> Optional[List[str]]:
        """Extrait le texte du PDF page par page"""
        texts = []
        
        # Essayer avec pdftotext (meilleure option)
        try:
            # Extraire avec layout préservé
            result = subprocess.run(
                ['pdftotext', '-layout', '-enc', 'UTF-8', str(pdf_path), '-'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Séparer par pages (pdftotext insère des sauts de page)
                pages = result.stdout.split('\f')
                for page in pages:
                    if page.strip():
                        texts.append(page.strip())
                return texts if texts else None
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Alternative: PyMuPDF (fitz) si disponible
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(pdf_path))
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text.strip():
                    texts.append(text.strip())
            doc.close()
            return texts if texts else None
        except ImportError:
            pass
        
        # Dernière alternative: PyPDF2
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text and text.strip():
                        texts.append(text.strip())
            return texts if texts else None
        except ImportError:
            pass
        
        return None
    
    def _create_translated_pdf_html(self, filename: str, translated_content: List[Dict]) -> str:
        """Crée un document HTML avec le contenu PDF traduit en anglais"""
        
        # Traduire le nom de fichier pour le titre
        title = self._translate_filename(filename)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.2em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .header .meta {{
            margin-top: 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .page-marker {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 10px 20px;
            margin: 30px 0 20px 0;
            font-weight: 600;
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.85em;
        }}
        
        .paragraph {{
            margin-bottom: 20px;
            text-align: justify;
            text-indent: 30px;
        }}
        
        .paragraph:first-of-type {{
            text-indent: 0;
        }}
        
        .paragraph:first-of-type::first-letter {{
            font-size: 3em;
            float: left;
            line-height: 1;
            margin-right: 10px;
            color: #667eea;
            font-weight: 700;
        }}
        
        .highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 500;
        }}
        
        .term {{
            color: #764ba2;
            font-weight: 600;
        }}
        
        .download-section {{
            background: #f8f9fa;
            padding: 30px 40px;
            border-top: 1px solid #e9ecef;
            text-align: center;
        }}
        
        .download-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px 40px;
            text-align: center;
            font-size: 0.9em;
        }}
        
        .footer a {{
            color: #a8edea;
            text-decoration: none;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
            .download-section {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 {title}</h1>
            <div class="subtitle">English Translation / Traduction Anglaise</div>
            <div class="meta">Original document: {filename} | {len(translated_content)} pages</div>
        </div>
        
        <div class="content">
"""
        
        for page_data in translated_content:
            html += f'            <div class="page-marker">Page {page_data["page"]}</div>\n'
            
            for i, para in enumerate(page_data['paragraphs']):
                if para.strip():
                    # Appliquer des mises en forme pour les termes importants
                    formatted_para = self._format_scientific_terms(para)
                    html += f'            <p class="paragraph">{formatted_para}</p>\n'
        
        html += f"""        </div>
        
        <div class="download-section">
            <a href="{filename}" class="download-btn" download>⬇️ Download Original PDF</a>
            <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                This is an automated translation. For the authoritative version, please refer to the original French document.
            </p>
        </div>
        
        <div class="footer">
            <p>Generated by Course Translator | Dr. Abdelkader Allouche - University of Oran 1</p>
            <p>© 2024-2025 - Educational Resources</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _format_scientific_terms(self, text: str) -> str:
        """Met en évidence les termes scientifiques importants"""
        # Liste de termes à mettre en évidence
        important_terms = [
            'Drosophila', 'embryonic', 'development', 'gene', 'genes', 'protein', 
            'proteins', 'signaling', 'pathway', 'transcription', 'factor', 'mRNA',
            'oogenesis', 'segmentation', 'homeotic', 'morphogen', 'gradient',
            'anterior', 'posterior', 'dorsal', 'ventral', 'axis', 'polarity',
            'Bicoid', 'Nanos', 'Oskar', 'Torso', 'Dorsal', 'Hunchback', 'Krüppel'
        ]
        
        for term in important_terms:
            # Remplacer par une version stylisée (mais éviter les doubles)
            pattern = r'\b(' + re.escape(term) + r')\b(?!</span>)'
            text = re.sub(pattern, r'<span class="term">\1</span>', text, flags=re.IGNORECASE)
        
        return text
    
    def _create_basic_pdf_summary(self, input_path: Path, output_path: Path) -> bool:
        """Crée un résumé basique si l'extraction de texte échoue"""
        title = self._translate_filename(input_path.name)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; }}
        .content {{ margin-top: 30px; }}
        .btn {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>English version of the course document</p>
    </div>
    <div class="content">
        <p>This document is a PDF file that requires direct translation of its content.</p>
        <p>Please download the original PDF below:</p>
        <a href="{input_path.name}" class="btn" download>Download Original PDF</a>
        <p style="margin-top: 30px; color: #666;">
            <strong>Note:</strong> The full text extraction was not possible for this PDF. 
            Please refer to the original French document for complete content.
        </p>
    </div>
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self.stats.pdf_files += 1
        print(f"⚠️  PDF (résumé basique): {input_path.name}")
        return True
    
    def _translate_filename(self, filename: str) -> str:
        """Traduit le nom de fichier pour le titre"""
        translations = {
            "Cours1_Synthese_Drosophila": "Course 1: Drosophila Synthesis",
            "Cours1_Synthese_Session2": "Course 1: Session 2 Synthesis",
            "cours_drosophila": "Drosophila Course",
            "cours_drosophila_ovogenese": "Drosophila Oogenesis Course",
            "Synthese": "Synthesis",
            "Session": "Session",
            "ovogenese": "Oogenesis",
            "20260302": "March 2, 2026",
        }
        
        result = filename.replace('.pdf', '').replace('_', ' ')
        for fr, en in translations.items():
            result = result.replace(fr, en)
        
        return result.strip()
    
    def process_directory(self, input_dir: Path, output_dir: Optional[Path] = None):
        """Traite tous les fichiers du répertoire"""
        if output_dir is None:
            output_dir = input_dir
        
        print("=" * 80)
        print("🚀 TRADUCTION COMPLÈTE DES COURS - VERSION 3.0")
        print("=" * 80)
        print(f"📂 Dossier source: {input_dir}")
        print(f"📂 Dossier sortie: {output_dir}")
        print(f"📚 Dictionnaire: {len(self.all_terms)} termes scientifiques + {len(self.common_phrases)} phrases")
        print("-" * 80)
        
        # Traiter les fichiers HTML
        html_files = list(input_dir.rglob('*.html')) + list(input_dir.rglob('*.htm'))
        html_files = [f for f in html_files if not f.name.endswith('.en.html')]
        print(f"\n📄 Fichiers HTML à traduire: {len(html_files)}")
        
        for html_file in sorted(html_files):
            rel_path = html_file.relative_to(input_dir)
            out_path = output_dir / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            self.translate_html_file(html_file, out_path)
        
        # Traiter les fichiers PDF
        pdf_files = list(input_dir.rglob('*.pdf'))
        print(f"\n📕 Fichiers PDF à traduire: {len(pdf_files)}")
        
        for pdf_file in sorted(pdf_files):
            rel_path = pdf_file.relative_to(input_dir)
            out_path = (output_dir / rel_path).with_suffix('.en.html')
            out_path.parent.mkdir(parents=True, exist_ok=True)
            self.translate_pdf_to_html(pdf_file, out_path)
        
        # Générer le rapport
        self._generate_report(output_dir)
        
        print("\n" + "=" * 80)
        print("✅ TRADUCTION TERMINÉE")
        print(f"📊 HTML: {self.stats.html_files} | PDF: {self.stats.pdf_files} ({self.stats.pdf_pages_translated} pages)")
        print(f"📝 Segments traduits: {self.stats.text_segments}")
        print(f"🔬 Termes scientifiques trouvés: {len(self.stats.scientific_terms_found)}")
        if self.stats.errors:
            print(f"⚠️  Erreurs: {len(self.stats.errors)}")
        print("=" * 80)
    
    def _generate_report(self, output_dir: Path):
        """Génère un rapport détaillé"""
        report = {
            'date': datetime.now().isoformat(),
            'statistics': self.stats.to_dict(),
            'dictionaries': {
                'scientific_terms': len(self.scientific_terms),
                'course_specific_terms': len(self.specific_course_terms),
                'common_phrases': len(self.common_phrases),
                'total_entries': len(self.all_terms) + len(self.common_phrases)
            }
        }
        
        # JSON
        json_path = output_dir / 'translation_report_v3.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Markdown détaillé
        md_path = output_dir / 'TRANSLATION_REPORT_V3.md'
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Translation Report V3 - Complete Course Translation\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            f.write("## 📊 Statistics\n\n")
            f.write(f"- **HTML files translated:** {self.stats.html_files}\n")
            f.write(f"- **PDF files processed:** {self.stats.pdf_files}\n")
            f.write(f"- **PDF pages translated:** {self.stats.pdf_pages_translated}\n")
            f.write(f"- **Text segments translated:** {self.stats.text_segments}\n")
            f.write(f"- **Scientific terms found:** {len(self.stats.scientific_terms_found)}\n")
            f.write(f"- **Errors:** {len(self.stats.errors)}\n\n")
            
            if self.stats.scientific_terms_found:
                f.write("## 🔬 Scientific Terms Detected (Sample)\n\n")
                f.write("| French Term | English Translation |\n")
                f.write("|-------------|---------------------|\n")
                for term in sorted(self.stats.scientific_terms_found)[:50]:
                    f.write(f"| {term} |\n")
                if len(self.stats.scientific_terms_found) > 50:
                    f.write(f"\n*... and {len(self.stats.scientific_terms_found) - 50} more terms*\n")
            
            if self.stats.errors:
                f.write("\n## ⚠️ Errors\n\n")
                for error in self.stats.errors:
                    f.write(f"- {error}\n")
            
            f.write("\n## 📚 Dictionary Coverage\n\n")
            f.write(f"- General scientific terms: {len(self.scientific_terms)}\n")
            f.write(f"- Course-specific terms: {len(self.specific_course_terms)}\n")
            f.write(f"- Common phrases: {len(self.common_phrases)}\n")
            f.write(f"- **Total entries:** {len(self.all_terms) + len(self.common_phrases)}\n\n")
            
            f.write("## 🎯 Specific Course Coverage\n\n")
            f.write("This translation includes specialized terminology for:\n")
            f.write("- Drosophila developmental biology\n")
            f.write("- Oogenesis and axis formation\n")
            f.write("- Segmentation genes and homeotic genes\n")
            f.write("- Maternal effect genes (Bicoid, Nanos, Oskar, Torso, Dorsal)\n")
            f.write("- Signaling pathways (Ras/MAPK, TGF-β, Wnt, Notch)\n")
            f.write("- L3 Genetics course structure (Oran University)\n")
        
        print(f"\n📊 Rapport généré: {md_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Traduit complètement les cours PDF et HTML FR → EN (V3)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Traduire en place
  python3 translate_courses_v3.py .
  
  # Vers un dossier séparé
  python3 translate_courses_v3.py . -o ../translated
  
  # Mode simulation
  python3 translate_courses_v3.py --dry-run .
        """
    )
    parser.add_argument('input', nargs='?', default='.', help='Dossier source')
    parser.add_argument('-o', '--output', help='Dossier de sortie')
    parser.add_argument('--dry-run', action='store_true', help='Simulation uniquement')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve() if args.output else input_dir
    
    if args.dry_run:
        html_files = list(input_dir.rglob('*.html')) + list(input_dir.rglob('*.htm'))
        pdf_files = list(input_dir.rglob('*.pdf'))
        print(f"📄 HTML files: {len(html_files)}")
        print(f"📕 PDF files: {len(pdf_files)}")
        for f in html_files[:5]:
            print(f"  HTML: {f.relative_to(input_dir)}")
        for f in pdf_files[:5]:
            print(f"  PDF: {f.relative_to(input_dir)}")
        return
    
    translator = CourseTranslator()
    translator.process_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
