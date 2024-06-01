<?php
// Récupérer l'email de l'utilisateur depuis l'URL
$email = $_GET['email'];

// Vérifier que l'email est fourni
if ($email === null) {
    die("Email non fourni.");
}

// Informations de connexion à la base de données
$nom_serveur = "localhost";
$utilisateur = "root";
$mot_de_passe = "";
$nom_base_données = "pfe";

// Connexion à la base de données
$con = mysqli_connect($nom_serveur, $utilisateur, $mot_de_passe, $nom_base_données);

// Vérification de la connexion
if (mysqli_connect_errno()) {
    die("Échec de la connexion à la base de données : " . mysqli_connect_error());
}

// Requête pour récupérer les informations de l'utilisateur
$user_query = "SELECT email, nom, prenom, role FROM users WHERE email = ?";
$user_stmt = mysqli_prepare($con, $user_query);
mysqli_stmt_bind_param($user_stmt, "s", $email);
mysqli_stmt_execute($user_stmt);
$user_result = mysqli_stmt_get_result($user_stmt);

// Vérifier si l'utilisateur existe
if ($user_row = mysqli_fetch_assoc($user_result)) {
    $nom = htmlspecialchars($user_row['nom']);
    $prenom = htmlspecialchars($user_row['prenom']);
    $role = htmlspecialchars($user_row['role']);
} else {
    die("Utilisateur non trouvé.");
}

// Requête pour récupérer les 5 derniers logs de l'utilisateur
$log_query = "SELECT log_id, email, date, time FROM log_entry WHERE email = ? ORDER BY log_id DESC LIMIT 5";
$log_stmt = mysqli_prepare($con, $log_query);
mysqli_stmt_bind_param($log_stmt, "s", $email);
mysqli_stmt_execute($log_stmt);
$log_result = mysqli_stmt_get_result($log_stmt);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Informations de l'Utilisateur</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>
<?php
include_once ("header_manage.php");
?>
<h1>Informations de l'Utilisateur</h1>
<p><strong>Email :</strong> <?= htmlspecialchars($email) ?></p>
<p><strong>Nom :</strong> <?= $nom ?></p>
<p><strong>Prénom :</strong> <?= $prenom ?></p>
<p><strong>Rôle :</strong> <?= $role ?></p>

<h2>5 Derniers Logs</h2>
<table>
    <thead>
    <tr>
        <th>ID</th>
        <th>Email</th>
        <th>Date</th>
        <th>Heure</th>
    </tr>
    </thead>
    <tbody>
    <?php while ($log_row = mysqli_fetch_assoc($log_result)): ?>
        <tr>
            <td><?= htmlspecialchars($log_row['log_id']) ?></td>
            <td><?= htmlspecialchars($log_row['email']) ?></td>
            <td><?= htmlspecialchars($log_row['date']) ?></td>
            <td><?= htmlspecialchars($log_row['time']) ?></td>
        </tr>
    <?php endwhile; ?>
    </tbody>
</table>

<?php
// Fermeture de la connexion
mysqli_close($con);
?>
</body>
</html>
