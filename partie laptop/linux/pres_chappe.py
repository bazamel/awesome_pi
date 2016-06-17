# coding=utf-8

import socket

hote = "localhost"
port = 12800


def sendMessage(mess):
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))
    msg_a_envoyer = mess
    # Peut planter si vous tapez des caractères spéciaux
    msg_a_envoyer = msg_a_envoyer.encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)
    connexion_avec_serveur.close()



if __name__ == '__main__':
    sendMessage("right")
