<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="kuis1.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
</head>

<body>
    <div class="container-fluid header text-center">
        
        <!--NavBar-->
        <nav class="navbar navbar-expand-lg">
            <div class="item container-fluid">
                <a class="navbar-brand" href="#">
                    <img src="Logoo.png" max-width="50%" height="auto">
                </a>
                    <ul class="navbar-nav font3">
                        <li class="nav-item jarakbutton">
                            <a class="nav-link " href="home.php">Beranda</a>
                        </li>
                        <li class="nav-item jarakbutton">
                            <a class="nav-link" href="Materi.php">Materi</a>
                        </li>
                        <li class="nav-item  jarakbutton" >
                            <a class="nav-link" href="pengaduan.php">Kontak</a>
                        </li>
                        <li class="nav-item jarakbutton1" style="background-color: #F0FAE0; transition: background-color 0.3s ease;" onmouseover="this.style.backgroundColor='#82B6BD'" onmouseout="this.style.backgroundColor='#F0FAE0'">
                            <a class="nav-link active" aria-current="page" href="kuis1.php">Kuisioner</a>
                        </li>
                    </ul>
            </div>
        </nav>

        <!--Heading-->
        <div class="text-center">
            <h1 class="font1 judul">
                KUISIONER PENCEGAHAN DAN PENANGANAN
            </h1>
            <h1 class="font1">
                KEKERASAN SEKSUAL
            </h1>
            <h6 class="font3 pt-1">
                Pilihlah salah satu dari pilihan berikut dan perlu diketahui bahwa anda
            </h6>
            <h6 class="font3">
                tidak akan bisa keluar dari kuisioner ini jika belum menyelesaikan kuisioner
            </h6>
        </div>

        <!--Penjelasan-->
        <div class="row text-center pt-5">
            <div class="col-sm-3">
                <h2 class="font4 container-fluid" style="background-color: #F0FAE0; max-width: 60px; height: 75px; padding-top: 22px;"> SS</h2>
                <h5>Sangat Setuju</h5>
            </div>
            <div class="col-sm-3">
                <h2 class="font4 container-fluid" style="background-color: #F0FAE0; max-width: 60px; height: 75px; padding-top: 22px;"> S</h2>
                <h5>Setuju</h5>
            </div>
            <div class="col-sm-3">
                <h2 class="font4 container-fluid" style="background-color: #F0FAE0; max-width: 60px; height: 75px; padding-top: 22px;"> KS</h2>
                <h5>Kurang Setuju</h5>
            </div>
            <div class="col-sm-3">
                <h2 class="font4 container-fluid" style="background-color: #F0FAE0; max-width: 60px; height: 75px; padding-top: 22px;">TS</h2>
                <h5>Tidak Setuju</h5>
            </div>
        </div>  
        
        <!--Button-->
        <a href="FormKuis.php" style="display: inline-block; text-decoration: none;">
            <button type="button" class="highlight mb-3" style="background-color: #82B6BD; transition: background-color 0.3s ease;" onmouseover="this.style.backgroundColor='#d9f1f1'" onmouseout="this.style.backgroundColor='#82B6BD'" >
                <p class="font3 buttoncard">Mulai Kuisioner</p>
            </button>
        </a>
    </div>
</body>