<?php

if (isset($_SESSION['email'])) {
    header('Location:admin_sign.php');
    exit();
}
?>

<!doctype html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="style/magi.css">
</head>
<body>
<?php
include_once ("header_manage.php");
?>
<section style="height: 400px; position: relative; background-color: #e1e1e1">
    <?php
    // Connexion à la base de données et requête pour récupérer les éléments
    $pdo = new PDO('mysql:host=localhost;dbname=pfe', 'root', '');
    $requete = $pdo->query("SELECT * FROM users WHERE jeton IS NOT NULL AND jeton != '';");
    $elements = $requete->fetchAll();

    // Nombre d'éléments à afficher par page
    $elements_par_page = 5;

    // Nombre total de pages
    $nombre_pages = ceil(count($elements) / $elements_par_page);

    // Récupérer le numéro de la page courante
    $page = isset($_GET['page']) ? $_GET['page'] : 1;

    // Calculer le premier élément à afficher
    $premier_element = ($page - 1) * $elements_par_page;

    // Récupérer les éléments de la page courante
    $elements_page = array_slice($elements, $premier_element, $elements_par_page);
    ?>

    <table style="height: 80%; background-color: #bdbeef">
        <thead>
        <tr>
            <th>Nom de l'utilisateur</th>
            <th>Prénom de l'utilisateur</th>
            <th>Pseudo</th>
            <th>Token</th>
            <th>Refuser l'accès</th>
        </tr>
        </thead>
        <tbody>
        <?php foreach ($elements_page as $element) : ?>
            <tr>
                <td><?= $element['email'] ?></td>
                <td><?= $element['nom'] ?></td>
                <td><?= $element['prenom'] ?></td>
                <td><?= $element['jeton'] ?></td>
                <td><a style="text-decoration: none; color: #589be7" href="revoke_token.php?id=<?= $element['user_id'] ?>&email=<?= $element['email'] ?>&nom_user=<?= $element['nom'] ?>">Supprimer le token</a></td>



            </tr>
        <?php endforeach; ?>
        </tbody>
    </table>

    <?php
    // Afficher les liens vers les autres pages
    echo '<div class="page" >';
    for ($i = 1; $i <= $nombre_pages; $i++) {
        if ($i == $page) {
            echo '<span class="curent_pg" >' . $i . '</span>';
        } else {
            echo '<a class="next_pg" href="?page=' . $i . '">' . $i . '</a>';
        }
    }
    echo '</div>';
    ?>

</section>
</body>
</html>