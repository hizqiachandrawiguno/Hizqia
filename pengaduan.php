<?php
require 'laporan.php';
if (isset($_POST['report'])){
    if(report($_POST) > 0 ){
        echo "<script>alert('Laporan sudah terkirim');
        window.location='home.html';</script>";
    } else {
        echo mysqli_error($conn);
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pengaduan</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="pengaduan.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
</head>
<body>
    <!--Heading-->
    <div class="container-fluid header ">
        <nav class="navbar navbar-expand-lg">
            <div class="item container-fluid">
                <a class="navbar-brand" href="#">
                    <img src="Logoo.png" max-width="50%" height="auto">
                </a>
                    <ul class="navbar-nav font3">
                        <li class="nav-item jarakbutton">
                            <a class="nav-link  font3"  href="home.php">Beranda</a>
                        </li>
                        <li class="nav-item jarakbutton">
                            <a class="nav-link font3" href="Materi.php">Materi</a>
                        </li>
                        <li class="nav-item  jarakbutton" >
                            <a class="nav-link active font3" aria-current="page" href="pengaduan.php">Laporan</a>
                        </li>
                        <li class="nav-item jarakbutton1" style="background-color: #82B6BD; transition: background-color 0.3s ease;" onmouseover="this.style.backgroundColor='#6b9fa6'" onmouseout="this.style.backgroundColor='#82B6BD'">
                            <a class="nav-link font3" href="kuis1.php">Kuisioner</a>
                        </li>
                    </ul>
            </div>
        </nav>

        <!--isi-->
        <form action="" method="post">
        <div class="mt-5 pb-5">
            <h1 class="font1 text-center">
                Laporan Pengaduan
            </h1> 
            <p class="font3 text-center batas1">
                Bila anda mengalami atau melihat kekerasan seksual di sekitar anda,
            </p>
            <p class="font3 text-center batas2">
                jangan ragu untuk ajukan pengaduan melalui kami
            </p>
            <div class="container kolom mb-5">
                <div class="pt-4">
                    <p>Nama Mahasiswa</p>
                    <input type="text" placeholder="Tulis Namamu" class="kolom1" name="nama" required>
                </div>
                <div class="pt-3">
                    <p>Nomor Induk Mahasiswa</p>
                    <input type="text" placeholder="Nomor Induk Mahasiswa" class="kolom2" name="nim" required>
                </div>
                <div class="pt-3">
                    <p>Kolom Aduan</p>
                    <textarea type="text" placeholder="Tulis Aduanmu disini" class="kolom3" name="laporan" required></textarea>
                </div>
                <div>
                    <button type="submit" class="container laporan" name="report">Laporkan</button>
                    <a href="https://api.whatsapp.com/send?phone=085174383862" target="_blank">
                    <button class="btn-floating whatsapp" >
                        <i class="bi bi-whatsapp" ></i>
                    </button>
                    </a>
                </div>
            </div>
        </div>
    </div>
    </form>
    <!--footer-->
    <div class="container-fluid px-5 py-3 mx-0 footer" style="background-color: #82B6BD ; color: #2C2C2C;">

        <!-- Row -->'
            <div class="row jarak4">
            <!-- Kiri -->
                <div class="col-sm-5 font3">
                    <img src="Logoo.png" style="width: 20%">
                    <div>
                        <p>Website ini kami bangun untuk memudahkan, membantu, serta menggencarkan pemahaman kepada seluruh masyarakat kampus mengenai Pencegahan dan Penanganan Kekerasan Seksual
                        </p>
                    </div>
                </div>
  
                <!-- Tengah -->
                <div class="col-sm-3 font3">
                    <p><span style="font-weight:bold; color: #767676;">Layanan Lainnya</span>
                        <div>
                    <a class="nav-link" href="Materi.php" style="margin-bottom: 5px;">Materi</a>
                    <a class="nav-link" href="kuis1.php" style="margin-bottom: 5px;">Kuisioner</a>
                    <a class="nav-link" href="pengaduan.php" style="margin-bottom: 5px;">Laporan</a>
                    <a class="nav-link" href="tentang-kami.php" >Tentang</a>
                    </div>
                </div>
  
                <!-- Kanan -->
                <div class="col-sm-3 font3">
                    <p><span style="font-weight:bold; color: #767676;">Ikuti Sosial Media</span>
                        <div>
                            <a style="color:#2C2C2C;" class="nav-link" href="#" span class="btn-label" ><i class="bi bi-instagram" style="font-size: 30px;"></i>
                            </a>
                        </div>
                </div>
            </div>                 
    </div>
   


    <!--bottom text-->
    <div class="container-fluid px-5 py-3 mx-0 footer" style="background-color: #F0FAE0 ; color: #2C2C2C;">
        <p class="text-left mx-1 palingbawah">@2024 Satgas PPKS | Terms and Condition</p>
    </div>
</body>