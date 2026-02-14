#!/usr/bin/env python3
"""
Axelor XML Validator
Validates domain-models and object-views XML files against their respective XSD schemas.
Automatically detects file type and version from the XML content.

Usage: python axelor_validator.py <fichier.xml>
"""

import sys
import argparse
import re
from pathlib import Path
from lxml import etree
import requests


# XSD URLs templates
XSD_URLS = {
    'domain-models': 'https://axelor.com/xml/ns/domain-models/domain-models_{version}.xsd',
    'object-views': 'https://axelor.com/xml/ns/object-views/object-views_{version}.xsd'
}

# Namespaces
NAMESPACES = {
    'domain-models': 'http://axelor.com/xml/ns/domain-models',
    'object-views': 'http://axelor.com/xml/ns/object-views'
}


def detect_xml_type_and_version(xml_path):
    """
    Détecte le type de fichier XML (domain-models ou object-views) et sa version
    
    Args:
        xml_path: Chemin vers le fichier XML
    
    Returns:
        tuple: (xml_type, version) ou (None, None) si non détecté
    """
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher le namespace pour déterminer le type
        xml_type = None
        for type_name, namespace in NAMESPACES.items():
            if namespace in content:
                xml_type = type_name
                break
        
        if not xml_type:
            return None, None
        
        # Extraire la version depuis xsi:schemaLocation
        # Format: https://axelor.com/xml/ns/{type}/{type}_X.Y.xsd
        pattern = rf'{xml_type}_{type_name}_(\d+\.\d+)\.xsd'
        match = re.search(pattern, content)
        
        if match:
            version = match.group(1)
            return xml_type, version
        
        # Si pas trouvé dans schemaLocation, essayer de parser le XML
        tree = etree.parse(xml_path)
        root = tree.getroot()
        
        # Chercher dans l'attribut schemaLocation
        schema_location = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', '')
        
        pattern = rf'{xml_type}_(\d+\.\d+)\.xsd'
        match = re.search(pattern, schema_location)
        
        if match:
            version = match.group(1)
            return xml_type, version
        
        return xml_type, None
        
    except Exception as e:
        print(f"AVERTISSEMENT: Erreur lors de la détection du type/version: {e}")
        return None, None


def telecharger_xsd(xml_type, version, cache_dir=".cache"):
    """
    Télécharge le fichier XSD correspondant et le met en cache
    
    Args:
        xml_type: Type de fichier ('domain-models' ou 'object-views')
        version: Version du schéma (ex: '8.0', '7.4')
        cache_dir: Répertoire de cache
    
    Returns:
        Chemin vers le fichier XSD en cache ou None si erreur
    """
    cache_path = Path(cache_dir)
    cache_path.mkdir(exist_ok=True)
    
    # Construire l'URL du XSD
    xsd_url = XSD_URLS[xml_type].format(version=version)
    
    # Nom du fichier en cache
    filename = f"{xml_type}_{version}.xsd"
    fichier_cache = cache_path / filename
    
    # Télécharger si pas en cache
    if not fichier_cache.exists():
        print(f"Téléchargement du schéma XSD depuis {xsd_url}...")
        try:
            response = requests.get(xsd_url, timeout=10)
            response.raise_for_status()
            fichier_cache.write_bytes(response.content)
            print(f"Schéma téléchargé et mis en cache: {fichier_cache}")
        except requests.RequestException as e:
            print(f"ERREUR lors du téléchargement du XSD: {e}")
            print(f"   URL tentée: {xsd_url}")
            return None
    else:
        print(f"Utilisation du schéma en cache: {fichier_cache}")
    
    return str(fichier_cache)


def valider_xml(fichier_xml, fichier_xsd):
    """
    Valide un fichier XML contre un schéma XSD
    
    Args:
        fichier_xml: Chemin vers le fichier XML à valider
        fichier_xsd: Chemin vers le fichier XSD
    
    Returns:
        tuple: (is_valid, errors)
    """
    try:
        # Charger le schéma XSD
        with open(fichier_xsd, 'rb') as f:
            schema_doc = etree.parse(f)
            schema = etree.XMLSchema(schema_doc)
        
        # Charger le fichier XML
        with open(fichier_xml, 'rb') as f:
            xml_doc = etree.parse(f)
        
        # Valider
        is_valid = schema.validate(xml_doc)
        
        if is_valid:
            return True, []
        else:
            return False, schema.error_log
            
    except etree.XMLSyntaxError as e:
        return False, [f"Erreur de syntaxe XML: {e}"]
    except FileNotFoundError as e:
        return False, [f"Fichier introuvable: {e}"]
    except Exception as e:
        return False, [f"Erreur inattendue: {e}"]


def main():
    parser = argparse.ArgumentParser(
        description="Valide un fichier XML Axelor (domain-models ou object-views) contre son schéma XSD",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s Paiement.xml
  %(prog)s equipement-form.xml
  %(prog)s mon_domaine.xml --version 7.4
  %(prog)s ma_vue.xml --type object-views --version 8.0
        """
    )
    
    parser.add_argument(
        'fichier_xml',
        help='Chemin vers le fichier XML à valider'
    )
    
    parser.add_argument(
        '--type',
        choices=['domain-models', 'object-views'],
        help='Type de fichier XML (détecté automatiquement si non spécifié)'
    )
    
    parser.add_argument(
        '--version',
        help='Version du schéma (détectée automatiquement si non spécifié, ex: 8.0, 7.4)'
    )
    
    parser.add_argument(
        '--xsd',
        help='Chemin vers un fichier XSD local (ignore la détection automatique)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Ne pas mettre en cache le XSD téléchargé'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Affichage détaillé'
    )
    
    args = parser.parse_args()
    
    # Vérifier que le fichier XML existe
    if not Path(args.fichier_xml).exists():
        print(f"ERREUR: Le fichier '{args.fichier_xml}' n'existe pas")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"VALIDATION AXELOR XML")
    print(f"{'='*70}")
    print(f"Fichier: {args.fichier_xml}\n")
    
    # Déterminer le type et la version
    if args.xsd:
        # Utiliser le XSD local fourni
        fichier_xsd = args.xsd
        if not Path(fichier_xsd).exists():
            print(f"ERREUR: Le fichier XSD '{fichier_xsd}' n'existe pas")
            sys.exit(1)
        print(f"Utilisation du XSD local: {fichier_xsd}")
        xml_type = "custom"
        version = "local"
    else:
        # Détection automatique ou utilisation des paramètres
        if args.type and args.version:
            xml_type = args.type
            version = args.version
            print(f"Type spécifié: {xml_type}")
            print(f"Version spécifiée: {version}")
        else:
            print("Détection automatique du type et de la version...")
            xml_type, version = detect_xml_type_and_version(args.fichier_xml)

            if not xml_type:
                print("ERREUR: Impossible de détecter le type de fichier XML")
                print("   Le fichier doit être un domain-models ou object-views Axelor")
                print("   Vous pouvez spécifier le type avec --type et --version")
                sys.exit(1)

            print(f"Type détecté: {xml_type}")

            if not version:
                print("AVERTISSEMENT: Version non détectée dans le fichier")
                print("   Utilisation de la version par défaut: 8.0")
                version = "8.0"
            else:
                print(f"Version détectée: {version}")

        # Télécharger le XSD
        print()
        cache_dir = None if args.no_cache else ".cache"
        fichier_xsd = telecharger_xsd(xml_type, version, cache_dir)

        if not fichier_xsd:
            print("\nERREUR: Impossible de récupérer le schéma XSD")
            print("   Vérifiez votre connexion internet ou spécifiez un fichier XSD local avec --xsd")
            sys.exit(1)
    
    # Valider le fichier XML
    print(f"\n{'='*70}")
    print(f"VALIDATION EN COURS...")
    print(f"{'='*70}\n")

    is_valid, errors = valider_xml(args.fichier_xml, fichier_xsd)

    print(f"{'='*70}")
    print(f"RESULTAT DE LA VALIDATION")
    print(f"{'='*70}\n")

    if is_valid:
        print("SUCCES: Le fichier XML est CONFORME au schéma XSD\n")
        print(f"   Type: {xml_type}")
        print(f"   Version: {version}")
        print(f"   Aucune erreur détectée\n")
        print(f"{'='*70}")
        sys.exit(0)
    else:
        print("ECHEC: Le fichier XML N'EST PAS conforme au schéma XSD\n")
        print(f"   Type: {xml_type}")
        print(f"   Version: {version}")
        print(f"   Nombre d'erreurs: {len(errors)}\n")
        print(f"{'-'*70}\n")

        for i, error in enumerate(errors, 1):
            print(f"Erreur {i}/{len(errors)}:")
            # Handle both error objects and error strings
            if isinstance(error, str):
                print(f"   {error}")
            else:
                print(f"   Ligne {error.line}, Colonne {error.column}")
                print(f"   {error.message}")
                if hasattr(error, 'path') and error.path:
                    print(f"   Chemin: {error.path}")
            print()

        print(f"{'='*70}")
        sys.exit(1)


if __name__ == "__main__":
    main()
