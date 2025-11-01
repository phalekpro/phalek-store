#!/usr/bin/env python3
"""
Serveur HTTP simple pour Phalek Store
Lance l'application sur http://localhost:4000 et http://192.168.x.x:4000
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from datetime import datetime
import socket

class PhalekHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personnalisé avec gestion des routes"""
    
    def log_message(self, format, *args):
        """Log personnalisé avec timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} - {format % args}")
    
    def end_headers(self):
        """Ajouter les headers CORS pour le développement"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        """Gestion personnalisée des routes"""
        # Nettoyer le path
        path = self.path.split('?')[0]  # Enlever les query parameters
        
        # Routes principales
        routes = {
            '/': '/index.html',
            '/upb-presence': '/upb-presence.html',
            '/seph-saveur': '/seph-saveur.html', 
            '/evaluation-numerique': '/evaluation-numerique.html'
        }
        
        # Vérifier si c'est une route connue
        if path in routes:
            filepath = routes[path]
            self.serve_html_file(filepath)
            return
        
        # Gestion des téléchargements
        if path.startswith('/downloads/'):
            filename = path.split('/')[-1]
            filepath = f'downloads/{filename}'
            if os.path.exists(filepath):
                self.serve_file_download(filepath, filename)
            else:
                self.send_error(404, f"Fichier non trouvé: {filename}")
            return
        
        # Pour tous les autres cas, servir normalement
        super().do_GET()
    
    def serve_html_file(self, filepath):
        """Servir un fichier HTML"""
        try:
            with open('.' + filepath, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(os.path.getsize('.' + filepath)))
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, f"File not found: {filepath}")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def serve_file_download(self, filepath, filename):
        """Servir un fichier en forçant le téléchargement"""
        try:
            with open(filepath, 'rb') as file:
                self.send_response(200)
                
                # Déterminer le type MIME
                if filename.endswith('.apk'):
                    self.send_header('Content-Type', 'application/vnd.android.package-archive')
                elif filename.endswith('.zip'):
                    self.send_header('Content-Type', 'application/zip')
                else:
                    self.send_header('Content-Type', 'application/octet-stream')
                
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Content-Length', str(os.path.getsize(filepath)))
                self.end_headers()
                
                # Envoyer le fichier
                self.wfile.write(file.read())
                
        except FileNotFoundError:
            self.send_error(404, f"Fichier non trouvé: {filename}")
        except Exception as e:
            self.send_error(500, f"Erreur serveur: {str(e)}")

def get_local_ip():
    """Récupère l'adresse IP locale (192.168.x.x)"""
    try:
        # Créer une connexion socket pour déterminer l'IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Adresse IP non disponible"

def check_downloads_files():
    """Vérifier que les fichiers de téléchargement existent"""
    required_files = [
        'downloads/UPB_presence.apk',
        'downloads/UPB_Presence_Final_Installer.zip'
    ]
    
    print("🔍 Vérification des fichiers de téléchargement...")
    for filepath in required_files:
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # Taille en MB
            print(f"✅ {filepath} - {file_size:.1f} MB")
        else:
            print(f"❌ Fichier manquant: {filepath}")

def start_server(port=4000):
    """Démarre le serveur HTTP"""
    try:
        # Récupérer l'IP locale
        local_ip = get_local_ip()
        
        # Vérifier les fichiers
        check_downloads_files()
        
        # Créer le handler
        handler = PhalekHTTPRequestHandler
        
        # Configurer le server
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("🚀 " + "="*70)
            print("   PHALEK STORE - Serveur de développement")
            print("="*70)
            print(f"📂 Répertoire : {os.getcwd()}")
            print(f"🌐 URL locale (PC) : http://localhost:{port}")
            print(f"📱 URL réseau (Mobile) : http://{local_ip}:{port}")
            print(f"🔗 UPB Présence : http://{local_ip}:{port}/upb-presence")
            print(f"🔗 Seph Saveur : http://{local_ip}:{port}/seph-saveur")
            print(f"🔗 Évaluation Numérique : http://{local_ip}:{port}/evaluation-numerique")
            print("")
            print("📥 Téléchargements disponibles :")
            print("   - UPB_presence.apk (Android)")
            print("   - UPB_Presence_Final_Installer.zip (Windows)")
            print("")
            print("📱 Pour accéder depuis votre mobile :")
            print(f"   1. Connectez-vous au même WiFi que ce PC")
            print(f"   2. Ouvrez le navigateur sur votre mobile")
            print(f"   3. Tapez : http://{local_ip}:{port}")
            print("")
            print("⏹️  Arrêt : Ctrl+C")
            print("="*70)
            
            # Ouvrir automatiquement le navigateur
            try:
                webbrowser.open(f'http://localhost:{port}')
                print("✅ Navigateur ouvert automatiquement sur localhost")
            except:
                print("ℹ️  Ouvrez manuellement votre navigateur")
            
            print("🔄 Serveur démarré avec succès!")
            print("-"*70)
            
            # Démarrer le serveur
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48 or e.errno == 10048:  # Address already in use
            print(f"❌ Le port {port} est déjà utilisé!")
            print("💡 Solutions possibles :")
            print("   1. Attendez que l'autre processus se termine")
            print("   2. Utilisez un autre port : python server.py 8080")
        else:
            print(f"❌ Erreur : {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
        print("👋 À bientôt sur Phalek Store!")
        return True
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False

def main():
    """Fonction principale"""
    # Récupérer le port depuis les arguments
    port = 4000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if not (1024 <= port <= 65535):
                print("❌ Le port doit être entre 1024 et 65535")
                return
        except ValueError:
            print("❌ Le port doit être un nombre valide")
            return
    
    print(f"🐍 Démarrage du serveur Phalek Store sur le port {port}...")
    start_server(port)

if __name__ == "__main__":
    main()