<!DOCTYPE html>
<html>
<head>
    <title>Acceuil</title>
    <style type="text/css">
        body{
            background-color: #7e7b7b;
            backdrop-filter: blur(10px);
            background-image: url("style/images/indew_back.jpg");
            background-size: cover;
        }
        .container {
            backdrop-filter: blur(10px);
            display: flex;
            justify-content: space-between;
            width: 420px;
            margin: 20px auto;
        }

        .card {
            margin-top: 150px;
            height: 250px;
            width: 250px;
            margin-right: 30px;
            background-color: #fff;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
            border-radius: 5px;
            padding: 20px;
            box-sizing: border-box;
        }

        .card h2 {
            margin: 0;
            font-size: 20px;
            color: #333;
        }

        .card p {
            font-size: 22px;
            color: #333333;
            text-align: center;
            margin-top: 30%;
        }

        .card.admin {
            background-color: #f44336;
            transition: 1s;
        }
        .card.admin:hover{
            background-color: #ee8282;

        }

        .card.util {
            background-color: #4caf50;
            transition: 1s;
        }
        .card.util:hover{
            background-color: #42de77;

        }

        .card.admin h2 {
            color: #fff;
            text-align: center;
        }

        .card.util h2 {
            color: #fff;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <a style="text-decoration: none" href="admin_log.php">
    <div class="card admin">
        <h2>Administration</h2>
        <p>Admin, Bonjour</p>
    </div></a>

    <a style="text-decoration: none" href="user_log.php"><div class="card util">
        <h2>Utilisation</h2>
        <p>User, Bonjour</p>
    </div></a>
</div>
</body>
</html>
