<?php

$token = bin2hex(openssl_random_pseudo_bytes(16));
$username = $_GET['username'];
$id = $_GET['user_id'];
$mail = $_GET['email'];
$nom_serveur = "localhost";
$utilisateur = "root";
$mot_de_passe = "";
$nom_base_données = "pfe";
$con = mysqli_connect($nom_serveur, $utilisateur, $mot_de_passe, $nom_base_données);
$req ="UPDATE users SET jeton = '$token' WHERE email = '$mail';";
$res = mysqli_query($con,$req);
if ($res) {
    $subjet = "Accés à l'application";
    $mess = "Bonjour monsieur/madame , nous vous informons que l'accés à l'application vous est à nouveau autorisé, \nnous vous remercions pour votre fidélité";
    $from = "levyren38@gmail.com";
    $to = $mail;
    mail($to,$subjet,$mess);
    header("location:invalid_token.php");
} else {//si non
    $erreur = "ECHEC!!!!!!";
}