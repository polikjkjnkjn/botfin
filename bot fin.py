from pyfacebook import Api
import random
import time
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Logique pour vérifier la Webhook
        return "Webhook OK", 200
    elif request.method == 'POST':
        # Logique pour gérer les messages Messenger
        return "Message received", 200

if __name__ == "__main__":
    app.run()

# Créez une instance de l'API Facebook en utilisant votre jeton d'accès
# Assurez-vous d'avoir généré un jeton d'accès valide avec les autorisations nécessaires pour accéder à l'API Messenger
api = Api(app_id='3728603687421120', app_secret='70c8f9c7874a427649abdc1623567931', access_token='EAA0ZCJTJMBMABO9ZCnS2xVeriWZCoFN2vcBvCb4WZCcfx3kZBgNGZCNUzmOwFEwGedFu5kefwfrr0bhaZBb7970Bgp2fcSinvSmXxSmpqBowJK9AMwrZAzEZCzgijfD9ZAMyXNxdoHAy42dBxSx1tDiuJUQcZCjx1CUGZBgihgsdRALbOZBltw0ZBPWFYVXlObDHOOM2g4Fcw8rha7XgZDZD')

# ID Facebook de Hallik T'Challa
hallik_user_id = '100091759061987'

# Liste des services offerts par votre entreprise, y compris la création de code Python
services = [
    "Saisie de documents",
    "Recherche d'épreuves",
    "Téléchargement de films, séries ou mangas",
    "Création de code Python",
    "Création d'exposé",
    "Traduction de documents",
    "Transcription de fichiers audio ou vidéo",
    "Révision et correction de documents"
]

# Fonction de temporisation
def wait_time():
    time.sleep(2)  # Patienter pendant 2 secondes

# Fonction pour récupérer le nom de l'utilisateur
def get_user_name(sender_id):
    user_info = api.get_user_info(sender_id)
    return user_info.get("name", "Utilisateur inconnu")

# Fonction pour notifier Hallik T'Challa du service demandé
def notify_hallik_service(user_name, service_requested):
    hallik_notification = f"Nouvelle demande de service de {user_name} :\nService : {service_requested}"
    api.send_text(hallik_user_id, hallik_notification)

# Fonction pour simuler un délai
def simulate_delay(seconds):
    time.sleep(seconds)

# Fonction pour traiter les réponses inattendues de l'utilisateur
def handle_unexpected_response(message):
    # Réponse en cas de message inattendu
    unexpected_message = "Désolé, je ne comprends pas. Veuillez choisir parmi les options disponibles."
    api.send_text(message.sender_id, unexpected_message)

# Fonction pour répondre aux messages
def reply_message(message):
    # Récupérer le nom de l'utilisateur
    user_name = get_user_name(message.sender_id)

    # Logique pour générer la réponse en fonction du message reçu
    if message.text.lower() in ["bonjour", "salut", "cc"]:
        # Construction de la réponse avec le nom de l'utilisateur et la liste des services
        response_message = f"Bonjour {user_name} ! Merci d'avoir visité notre page. Voici les services que nous proposons :\n"
        response_message += "\n".join(services)
        response_message += "\n\nVeuillez mentionner le service que vous souhaitez pour plus d'informations."

        # Envoyer la réponse
        api.send_text(message.sender_id, response_message)
        wait_time()  # Attendre quelques instants
    else:
        service_requested = message.text.capitalize()

        # Vérifier si le service demandé est dans la liste des services
        if service_requested in services:
            # Envoyer un message à Hallik T'Challa avec les détails du client et du service
            notify_hallik_service(user_name, service_requested)

            # Obtenir le prix du service de Hallik T'Challa
            price = random.randint(1000, 5000)  # Prix aléatoire entre 1000 et 5000 FCFA
            
            # Construction de la réponse pour l'utilisateur avec le prix
            response_message = f"Merci {user_name} pour votre demande de {service_requested}."
            response_message += f"\n\nLe prix pour ce service est de : {price} FCFA"
            response_message += "\n\nVeuillez choisir un mode de paiement :"
            response_message += "\n1. Perfect Money"
            response_message += "\n2. Mobile Money (MTN MoMo)"

            # Envoyer la réponse à l'utilisateur
            api.send_text(message.sender_id, response_message)
            wait_time()  # Attendre quelques instants
        else:
            # Si le service n'est pas reconnu
            handle_unexpected_response(message)

# Fonction pour traiter les réponses du client après avoir choisi un mode de paiement
def handle_payment_choice(message):
    user_name = get_user_name(message.sender_id)
    if "perfect money" in message.text.lower():
        # Si le client choisit Perfect Money
        # Demander la devise (EUR ou USD)
        currency_message = "Veuillez choisir la devise :\n1. EUR\n2. USD"
        api.send_text(message.sender_id, currency_message)
    elif "mobile money" in message.text.lower():
        # Si le client choisit Mobile Money
        # Envoyer un message pour demander le réseau (MTN ou Moov)
        network_message = "Veuillez choisir votre réseau Mobile Money :\n1. MTN\n2. Moov"
        api.send_text(message.sender_id, network_message)
    else:
        # Si le choix n'est pas valide
        handle_unexpected_response(message)

# Fonction pour traiter les réponses du client après avoir choisi le réseau Mobile Money
def handle_mobile_money_network(message):
    user_name = get_user_name(message.sender_id)
    if "mtn" in message.text.lower():
        # Si le client choisit MTN
        hallik_message = f"Numéro MTN MoMo de {user_name} : 1"
        api.send_text(hallik_user_id, hallik_message)
        payment_message = f"Merci {user_name} pour votre choix. Veuillez effectuer le paiement sur le numéro MTN MoMo suivant : +229 95958177 Veuillez mettre l'id de la transaction"
        api.send_text(message.sender_id, payment_message)
    elif "moov" in message.text.lower():
        # Si le client choisit Moov
        hallik_message = f"Numéro Moov Cash de {user_name} : 2"
        api.send_text(hallik_user_id, hallik_message)
        payment_message = f"Merci {user_name} pour votre choix. Veuillez effectuer le paiement sur le numéro Moov Cash suivant : +229 96823067 Veuillez mettre l'id de la transaction"
        api.send_text(message.sender_id, payment_message)
    else:
        # Si le choix n'est pas valide
        handle_unexpected_response(message)

# Fonction pour traiter les réponses du client après avoir choisi la devise pour Perfect Money
def handle_perfect_money_currency(message):
    user_name = get_user_name(message.sender_id)
    if "eur" in message.text.lower():
        # Si le client choisit EUR
        hallik_message = f"Numéro Perfect Money (EUR) de {user_name} : 3"
        api.send_text(hallik_user_id, hallik_message)
        payment_message = f"Merci {user_name} pour votre choix. Veuillez effectuer le paiement à l'adresse Perfect Money (EUR) suivante : E40108094"
        api.send_text(message.sender_id, payment_message)
    elif "usd" in message.text.lower():
        # Si le client choisit USD
        hallik_message = f"Numéro Perfect Money (USD) de {user_name} : 4"
        api.send_text(hallik_user_id, hallik_message)
        payment_message = f"Merci {user_name} pour votre choix. Veuillez effectuer le paiement à l'adresse Perfect Money (USD) suivante : U41740343"
        api.send_text(message.sender_id, payment_message)
    else:
        # Si le choix n'est pas valide
        handle_unexpected_response(message)

# Fonction pour traiter les réponses du client après confirmation du paiement
def handle_payment_confirmation(message):
    user_name = get_user_name(message.sender_id)
    if "oui" in message.text.lower() or "prêt" in message.text.lower():
        # Si le client confirme le paiement
        confirmation_message = f"Merci {user_name} pour votre paiement. Votre service sera traité sous peu."
        api.send_text(message.sender_id, confirmation_message)
        # Envoyer un message à Hallik T'Challa pour confirmer le paiement
        hallik_confirmation = f"Confirmation de paiement pour {user_name}."
        hallik_confirmation += "\nLe service peut maintenant être traité."
        api.send_text(hallik_user_id, hallik_confirmation)
    elif "non" in message.text.lower():
        # Si le client annule le paiement
        cancel_message = f"Le paiement a été annulé. Veuillez nous contacter si vous avez d'autres questions."
        api.send_text(message.sender_id, cancel_message)
    else:
        # Si la réponse n'est pas claire
        unclear_message = "Je ne comprends pas votre réponse. Veuillez répondre avec 'oui' ou 'non'."
        api.send_text(message.sender_id, unclear_message)

# Boucle pour recevoir et traiter les messages entrants
while True:
    # Récupérer les messages entrants
    messages = api.get_messages()

    # Parcourir les messages et répondre à chacun d'eux
    for message in messages:
        # Vérifier si le message est une réponse après avoir choisi un mode de paiement
        if "perfect money" in message.text.lower() or "mobile money" in message.text.lower():
            handle_payment_choice(message)
        elif "mtn" in message.text.lower() or "moov" in message.text.lower():
            handle_mobile_money_network(message)
        elif "eur" in message.text.lower() or "usd" in message.text.lower():
            handle_perfect_money_currency(message)
        elif "prêt" in message.text.lower():
            handle_payment_confirmation(message)
        else:
            # Appeler la fonction de réponse pour chaque message
            reply_message(message)

        # Vérifier si Hallik T'Challa envoie un message
        hallik_messages = api.get_messages(hallik_user_id)
        for hallik_message in hallik_messages:
            # Vérifier si Hallik envoie le mot "prêt"
            if "prêt" in hallik_message.text.lower():
                # Si Hallik T'Challa confirme que le service est prêt
                # Envoyer un message au client que le service est accompli et demander le mode de paiement
                payment_message = f"Bonjour {user_name}, le service que vous avez demandé est prêt !"
                payment_message += "\n\nVeuillez choisir un mode de paiement :"
                payment_message += "\n1. Perfect Money"
                payment_message += "\n2. Mobile Money (MTN MoMo)"
                api.send_text(message.sender_id, payment_message)
                wait_time()  # Attendre quelques instants
 # Vérifier si de nouveaux messages sont arrivés toutes les secondes
    time.sleep(1)
