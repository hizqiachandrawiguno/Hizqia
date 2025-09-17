<?php
require 'functions.php';

if(isset($_POST['login'])){
    $email = $_POST['email'];
    $password = $_POST['password'];

    $result = mysqli_query($conn, "SELECT * FROM registrasi WHERE email = '$email'");

    if(mysqli_num_rows($result)===1){
        $row = mysqli_fetch_assoc($result);
        if (password_verify($password, $row['password'])){
            header("Location:home.php");
            exit;
        }

        $error = true;

    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="css/bootstrap.css" rel="stylesheet" />
    <link href="js/bootstrap.min.js" rel="stylesheet" />
    <link href="js/popper.min.js" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" />
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js" integrity="sha384-zYPOMqeu1DAVkHiLqWBUTcbYfZ8osu1Nd6Z89ify25QV9guujx43ITvfi12/QExE" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.min.js" integrity="sha384-Y4oOpwW3duJdCWv5ly8SCFYWqFDsfob/3GkgExXKV4idmbt98QcxXYs9UoXAB7BZ" crossorigin="anonymous"></script>
    <title>Form Login</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <div class="login-container">
        <div class="login-form">
            <div class="container">
                    <img src="Logoo.png " width="13%">
                    <p>
                        _________________________________________________________________________________________
                    </p>
    <h1 class="text-start font2">Selamat Datang</h1>
    <p class="font1">
    Lebih Cepat Lebih Baik
    </p>
    <form action="" method="post">
        <table>
            <div class="form-group form-p font1">
                <input type="E-mail" class="form-control form-size" id="exampleInputEmail1" placeholder="E-mail" name="email" required>
            </div>
            <br>
    <div class="form-group form-p font1">
    <input type="Password" class="form-control form-size" id="exampleInputPassword1" placeholder="Password" name="password" required>
</div>
</table>
<br>
<input class="tombol font1" type="submit" name="login" value="Masuk"><br><br>
<center class="font1">
Belum memiliki akun?
<a style="color:black;" href="registrasi.php">Daftar</a>
</center>
</form>
</div>
</div>
<div class="login-wallpaper"></div> <!-- Wallpaper -->
</div>
</body>
</html>