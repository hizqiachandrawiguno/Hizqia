<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz PPKS</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="kuis-end.css">
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
                            <a class="nav-link" href="pengaduan.php">Laporan</a>
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
                TERIMA KASIH TELAH MENGISI
            </h1>
            <h1 class="font1" style="margin-bottom: 75px;">
                KUISIONER KAMI
            </h1>
        </div>

        <!--Penjelasan-->
        
        <!--Button-->
        <a href="home.php" style="display: inline-block; text-decoration: none;">
            <button type="button" class="highlight mb-3" style="background-color: #82B6BD; transition: background-color 0.3s ease;" onmouseover="this.style.backgroundColor='#d9f1f1'" onmouseout="this.style.backgroundColor='#82B6BD'" >
                <p class="font3 buttoncard">Kembali Ke Beranda</p>
            </button>
        </a>
    </div>
</body>