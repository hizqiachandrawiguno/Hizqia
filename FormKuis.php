<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz</title>
    <link rel="icon" href="logo Woah.png">
    <link rel="stylesheet" href="FormKuis.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
</head>
<body>
    <form action="Kuis.php" method="post">
        <h2 class="text1 font2" style="padding-top: 100px;">Silahkan isi Data</h2>
        <input type="text" class="text2 font3 input1" style="padding-top: 13px;" name="nama" placeholder="Nama Mahasiswa" id="nama" required>
        <input type="text" class="text2 font3 input2" name="nim" placeholder="NIM" id="nim" required>
        <button type="submit" class="font6 button" style="padding-top: 10px;" value="Mulai Kuis">Mulai Kuis</button>
    </form>
</body>
</html>