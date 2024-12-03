from colorama import Fore, Style, init

class EntityVisualizerConsole:
    
    def __init__(self) -> None:
        # Initialiser colorama pour la gestion des couleurs dans la console
        init(autoreset=True)
    
    def run(self, text, matched_results):
        # Couleur pour les malwares
        MALWARE_COLOR = Fore.YELLOW
        
        print("\n=== Résultats de la correspondance ===\n")
        
        for result in matched_results:
            print(f"\nFichier PDF: {result['pdf_file']}")
            
            for match in result.get('matches', []):
                print(f"\n- Malware STIX: {match['stix_malware']}")
                print(f"- Malware PDF: {match['pdf_malware']}")
                print(f"- Score: {match['score']}%")
                
                # Pour chaque occurrence trouvée
                for context in match.get('context', []):
                    print("\nContexte:")
                    output = (
                        context['before'] +
                        MALWARE_COLOR + context['match'] + Style.RESET_ALL +
                        context['after']
                    )
                    print(output)
                    print("-" * 80)  # Séparateur pour plus de lisibilité

    def visualize_matches(self, text, matched_results):
        visualizer = EntityVisualizerConsole()
        visualizer.run(text, matched_results)
