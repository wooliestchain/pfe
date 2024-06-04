<!doctype html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="style/admin_sign.css">
</head>
<body>
<main>
    <form action="#" method="post">
        <label for="email">Entrer votre email: </label><br>
        <input type="email" name="email" placeholder="Entrer votre adresse mail" autocomplete="off"><br>
        <label for="password">Entrer votre mot de passe: </label><br>
        <input type="password" name="password" minlength="5" placeholder="Entrer votre mot de passe" autocomplete="off" ><br>

        <?php
        if (isset($_POST['valider'])) {
            if (isset($_POST['email']) && isset($_POST['password'])) {
                $email = $_POST['email'];
                $pass = $_POST['password'];

                $nom_serveur = "localhost";
                $utilisateur = "root";
                $mot_de_passe = "";
                $nom_base_données = "saas";
                $dsn = "mysql:host=$nom_serveur;dbname=$nom_base_données;charset=utf8mb4";

                try {
                    $pdo = new PDO($dsn, $utilisateur, $mot_de_passe);
                    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                    $stmt = $pdo->prepare("INSERT INTO admin (admin_email, admin_mdp) VALUES (:email, :pass)");
                    $stmt->execute(array(':email' => $email, ':pass' => $pass));
                    $count = $stmt->rowCount();
                    if ($count > 0) {
                        header("location:admin_manage.php");
                        $_SESSION['email'] = $email;
                    } else {
                        $erreur = "ECHEC!!!!!!";
                    }
                } catch(PDOException $e) {
                    echo "Erreur : " . $e->getMessage();
                }
            }
        }
        ?>

        <input type="submit" value="S'inscire" name="valider"><br>
        <h4>Déja inscrit ? <a href="admin_log.php">Connectez-vous ici</a></h4>
        <?php
        /*
        if(isset($_POST['valider'])){
            if(isset($_POST['email']) && isset($_POST['password']) && isset($_POST['confirm_password'])){
                $email = $_POST['email'];
                $pass = $_POST ['password'];
                $con_pass = $_POST['confirm_password'];
                if($pass == $con_pass) {


                    $nom_serveur = "localhost";
                    $utilisateur = "root";
                    $mot_de_passe = "";
                    $nom_base_données = "saas";
                    $con = mysqli_connect($nom_serveur, $utilisateur, $mot_de_passe, $nom_base_données);
                    $req ="INSERT INTO admin (admin_email, admin_mdp) VALUES ($email, $pass)";
                    $res = mysqli_query($con,$req);
                    if ($res) {
                        header("location:admin_manage.php");
                        $_SESSION['email'] = $email;
                    } else {//si non
                        $erreur = "ECHEC!!!!!!";
                    }
                }else{
                    echo "Les mots de passes ne correspondent pas";
                }

            }
        }
*/
        ?>
    </form>
</main>
</body>
<script>
    function checkPassword() {
        var password = document.getElementById("password");
        var confirm_password = document.getElementById("confirm_password");

        if (password.value != confirm_password.value) {
            confirm_password.setCustomValidity("Les mots de passe ne correspondent pas");
        } else {
            confirm_password.setCustomValidity('');
        }
    }
</script>
</html>