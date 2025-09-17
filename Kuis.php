<?php

// Ambil nilai dari formulir
$nama = $_POST['nama'];
$nim = $_POST['nim'];

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="kuis.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
</head> 
<body>
    
    <form action="koneksi.php" method="post">
        <input type="text" id="nama" value="<?php echo $nama?>"  name="nama" placeholder="Nama Mahasiswa" hidden>
            <input type="text" id="nim" name="nim" value="<?php echo $nim?>" placeholder="NIM" hidden>
    <div class="bg1 container">
        <!--Nomor 1-->
        <div class="container bg2">
            <h2 class="font2 nomor container">01</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Apakah website dapat mendorong dialog terbuka dan mendukung antara mahasiswa terkait isu-isu kekerasan seksual?
            </h6>
            <div class="radio-group">
                <label for="pt21" class="radio">
                    <input type="radio" value="ss" name="no1" id="pt21" required>
                    SS
                    <span></span>
                </label>
                <label for="pt22" class="radio">
                    <input type="radio" value="s" name="no1" id="pt22" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt23" class="radio">
                    <input type="radio" value="ks" name="no1" id="pt23" required>
                    KS
                    <span></span>
                </label>
                <label for="pt24" class="radio">
                    <input type="radio" value="ts" name="no1" id="pt24" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
        <!--Nomor 2-->
        <div class="container bg2">
            <h2 class="font2 nomor container">02</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Apakah penggunaan website PPKS dapat membantu meningkatkan kesadaran mahasiswa tentang pencegahan dan penanganan kekerasan seksual?
            </h6>
            <div class="radio-group">
                <label for="pt29" class="radio">
                    <input type="radio" value="ss" name="no2" id="pt29" required>
                    SS
                    <span></span>
                </label>
                <label for="pt30" class="radio">
                    <input type="radio" value="s" name="no2" id="pt30" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt31" class="radio">
                    <input type="radio" value="ks" name="no2" id="pt31" required>
                    KS
                    <span></span>
                </label>
                <label for="pt32" class="radio">
                    <input type="radio" value="ts" name="no2" id="pt32" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
        <!--Nomor 3-->
        <div class="container bg2">
            <h2 class="font2 nomor container">03</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Apakah merendahkan, menghina, dan mengancam termasuk kedalam kekerasan seksual?
            </h6>
            <div class="radio-group">
                <label for="pt33" class="radio">
                    <input type="radio" value="ss" name="no3" id="pt33" required>
                    SS
                    <span></span>
                </label>
                <label for="pt34" class="radio">
                    <input type="radio" value="s" name="no3" id="pt34" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt35" class="radio">
                    <input type="radio" value="ks" name="no3" id="pt35" required>
                    KS
                    <span></span>
                </label>
                <label for="pt36" class="radio">
                    <input type="radio" value="ts" name="no3" id="pt36" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
        <!--Nomor 4-->
        <div class="container bg2">
            <h2 class="font2 nomor container">04</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Apakah website ini dapat membantu para korban kekerasan seksual sebagai pusat dukungan bagi mereka?
            </h6>
            <div class="radio-group">
                <label for="pt37" class="radio">
                    <input type="radio" value="ss" name="no4" id="pt37" required>
                    SS
                    <span></span>
                </label>
                <label for="pt38" class="radio">
                    <input type="radio" value="s" name="no4" id="pt38" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt39" class="radio">
                    <input type="radio" value="ks" name="no4" id="pt39" required>
                    KS
                    <span></span>
                </label>
                <label for="pt40" class="radio">
                    <input type="radio" value="ts" name="no4" id="pt40" required>
                    TS
                    <span></span>
                </label>
            </div>
        <!--Nomor 5-->
        <div class="container bg2">
            <h2 class="font2 nomor container">05</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Warna tertentu tidak dapat membantu meredakan kecemasan dan trauma bagi korban dan penyintas yang membaca konten website?
            </h6>
            <div class="radio-group">
                <label for="pt1" class="radio">
                    <input type="radio" value="ss" name="no5" id="pt1" required>
                    SS
                    <span></span>
                </label>
                <label for="pt2" class="radio">
                    <input type="radio" value="s" name="no5" id="pt2" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt3" class="radio">
                    <input type="radio" value="ks" name="no5" id="pt3" required>
                    KS
                    <span></span>
                </label>
                <label for="pt4" class="radio">
                    <input type="radio" value="ts" name="no5" id="pt4" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
        <!--Nomor 6-->
        <div class="container bg2">
            <h2 class="font2 nomor container">06</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Seberapa penting pemilihan warna pada website PPKS dan pencegahan kekerasan seksual dapat memengaruhi pemahaman materi bagi korban dan penyintas?
            </h6>
            <div class="radio-group">
                <label for="pt9" class="radio">
                    <input type="radio" value="ss" name="no6" id="pt9" required>
                    SS
                    <span></span>
                </label>
                <label for="pt10" class="radio">
                    <input type="radio" value="s" name="no6" id="pt10" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt11" class="radio">
                    <input type="radio" value="ks" name="no6" id="pt11" required>
                    KS
                    <span></span>
                </label>
                <label for="pt12" class="radio">
                    <input type="radio" value="ts" name="no6" id="pt12" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
        <!--Nomor 7-->
        <div class="container bg2">
            <h2 class="font2 nomor container">07</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Menurut anda, Apakah pemilihan warna pada website meningkatkan minat Anda terhadap materi yang dibaca?
            </h6>
            <div class="radio-group">
                <label for="pt13" class="radio">
                    <input type="radio" value="ss" name="no7" id="pt13" required>
                    SS
                    <span></span>
                </label>
                <label for="pt14" class="radio">
                    <input type="radio" value="s" name="no7" id="pt14" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt15" class="radio">
                    <input type="radio" value="ks" name="no7" id="pt15" required>
                    KS
                    <span></span>
                </label>
                <label for="pt16" class="radio">
                    <input type="radio" value="ts" name="no7" id="pt16" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
        <!--Nomor 8-->
        <div class="container bg2">
            <h2 class="font2 nomor container">08</h2>
            <h6 class="font1 pt-3 text1 pb-3">
                Apakah warna dapat digunakan untuk membangun rasa aman dan kepercayaan bagi korban dan penyintas yang mengunjungi website?
            </h6>
            <div class="radio-group">
                <label for="pt17" class="radio">
                    <input type="radio" value="ss" name="no8" id="pt17" required>
                    SS
                    <span></span>
                </label>
                <label for="pt18" class="radio">
                    <input type="radio" value="s" name="no8" id="pt18" required>
                    <p style="padding-left: 7px;">S</p>
                    <span></span>
                </label>
                <label for="pt19" class="radio">
                    <input type="radio" value="ks" name="no8" id="pt19" required>
                    KS
                    <span></span>
                </label>
                <label for="pt20" class="radio">
                    <input type="radio" value="ts" name="no8" id="pt20" required>
                    TS
                    <span></span>
                </label>
            </div>
        </div>
            <!--Tombol Submit-->
            <button type="submit" class="container submit" name="simpan" style="background-color: #82B6BD; transition: background-color 0.3s ease;" onmouseover="this.style.backgroundColor='#5B7C81'" onmouseout="this.style.backgroundColor='#82B6BD'">
                <h4 class="font2">SERAHKAN KUIS</h4>
            </button>
        </div>
    </div>
</form>
</body>