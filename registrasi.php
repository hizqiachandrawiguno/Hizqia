<?php
require 'functions.php';
if (isset($_POST['register'])){
    if(registrasi($_POST) > 0 ){
        echo "<script>alert('Berhasil membuat akun');
        window.location='login.php';</script>";
    } else {
        echo mysqli_error($conn);
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
    <title>Form Registrasi</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="style-regist.css" />
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-6 padding-tombol">
                <div class="justify-content-center">
                    <br>
                    <img src="Logoo.png" width="15%">
                    <p>
                        ______________________________________________________________________________
                    </p>
    <h1 class="text-start font2">Daftar</h1>
    <p class="font1">
    Bergabung dengan kami untuk kemudahan akses anda
    </p>
        <form action="" method="post">
            <table>
                <div class="form-group form-p font1">
                    <input type="NIM" class="form-control form-size tmbol" placeholder="NIM" name="nim" required>
                </div>
                <br>
                <div class="form-group form-p font1">
                    <input type="text" class="form-control form-size tmbol"  placeholder="Nama" name="nama" required>
                </div>
                <br>
                <div class="form-group form-p font1">
                    <input type="text" class="form-control form-size tmbol" placeholder="E-mail" name="email" required>
                </div>
                <br>
                <div class="form-group form-p font1">
                    <input type="Password" class="form-control form-size tmbol" placeholder="Password" name="password" required>
                </div>
                <br>
                <div class="form-group form-p font1">
                    <input type="Password" class="form-control form-size tmbol"  placeholder="Konfirmasi Password" name="password2" required>
                </div>
            </table>
            <br>
            <input class="tombol font1" type="submit" name="register" value="Daftar">
            <br>
            <br>
            <center class="font1">
            Sudah memiliki akun?
            <a style="color:black;" href="login.php">Masuk</a>
            </center>
        </form>
        </div>
    </div>
    <div class="col gambar">
    </div>
    </div>
    </div>
</body>
</html>