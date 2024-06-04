<?php
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

// Déterminer la page actuelle
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 5; // Nombre de résultats par page
$offset = ($page - 1) * $limit;

// Requête pour récupérer le nombre total d'entrées
$total_query = "SELECT COUNT(*) as total FROM log_entry";
$total_result = mysqli_query($con, $total_query);
$total_row = mysqli_fetch_assoc($total_result);
$total_entries = $total_row['total'];
$total_pages = ceil($total_entries / $limit);

// Requête pour récupérer les entrées avec pagination
$query = "SELECT log_id, email, date, time FROM log_entry ORDER BY log_id DESC LIMIT $limit OFFSET $offset";
$result = mysqli_query($con, $query);

if (!$result) {
    die("Erreur de requête : " . mysqli_error($con));
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Journal des Entrées</title>
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
<h1>Journal des Entrées</h1>
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
    <?php while ($row = mysqli_fetch_assoc($result)): ?>
        <tr>
            <td><?= htmlspecialchars($row['log_id']) ?></td>
            <td><a href="users_info.php?email=<?= urlencode($row['email']) ?>"><?= htmlspecialchars($row['email']) ?></a></td>
            <td><?= htmlspecialchars($row['date']) ?></td>
            <td><?= htmlspecialchars($row['time']) ?></td>
        </tr>
    <?php endwhile; ?>
    </tbody>
</table>

<div>
    <p>Page <?= $page ?> sur <?= $total_pages ?></p>
    <?php if ($page > 1): ?>
        <a href="?page=<?= $page - 1 ?>">Précédente</a>
    <?php endif; ?>

    <?php if ($page < $total_pages): ?>
        <a href="?page=<?= $page + 1 ?>">Suivante</a>
    <?php endif; ?>
</div>

<?php
// Fermeture de la connexion
mysqli_close($con);
?>
</body>
</html>
