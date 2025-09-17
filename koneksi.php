<?php 

// Konfigurasi koneksi ke database
$server = "localhost"; // Ganti sesuai dengan nama server database Anda
$username = "root"; // Ganti dengan username database Anda
$password = ""; // Ganti dengan password database Anda
$database = "ppks"; // Ganti dengan nama database yang ingin Anda gunakan

// Membuat koneksi
$koneksi = new mysqli($server, $username, $password, $database);

// Memeriksa koneksi
if ($koneksi->connect_error) {
    die("Koneksi gagal: " . $koneksi->connect_error);
}

// Ambil nilai dari formulir
$nama = $_POST['nama'];
$nim = $_POST['nim'];
$no1 = $_POST['no1'];
$no2 = $_POST['no2'];
$no3 = $_POST['no3'];
$no4 = $_POST['no4'];
$no5 = $_POST['no5'];
$no6 = $_POST['no6'];
$no7 = $_POST['no7'];
$no8 = $_POST['no8'];

// Kunci jawaban
$answers = array(
  'no1' => 'ss',
  'no2' => 'ss',
  'no3' => 'ss',
  'no4' => 'ss',
  'no5' => 'ss',
  'no6' => 'ss',
  'no7' => 'ss',
  'no8' => 'ss',

);

  $answers2 = array(
    'no1' => 's',
    'no2' => 's',
    'no3' => 's',
    'no4' => 's',
    'no5' => 's',
    'no6' => 's',
    'no7' => 's',
    'no8' => 's',
  );

  $answers3 = array(
    'no1' => 'ks',
    'no2' => 'ks',
    'no3' => 'ks',
    'no4' => 'ks',
    'no5' => 'ks',
    'no6' => 'ks',
    'no7' => 'ks',
    'no8' => 'ks',
  );

  $answers4 = array(
    'no1' => 'ts',
    'no2' => 'ts',
    'no3' => 'ts',
    'no4' => 'ts',
    'no5' => 'ts',
    'no6' => 'ts',
    'no7' => 'ts',
    'no8' => 'ts',
  );

// Hitung skor
$score = 0;
foreach ($answers as $key => $value) {
  if ($_POST[$key] == $value) {
    $score+=4;
  }
}

foreach ($answers2 as $key => $value) {
    if ($_POST[$key] == $value) {
      $score+=3;
    }
  }

  foreach ($answers3 as $key => $value) {
    if ($_POST[$key] == $value) {
      $score+=2;
    }
  }

foreach ($answers4 as $key => $value) {
    if ($_POST[$key] == $value) {
      $score+=1;
    }
  }

// Simpan ke database
$sql = "INSERT INTO question (nama, nim, no1, no2, no3, no4, no5, no6, no7, no8, score) VALUES ('$nama', '$nim', '$no1', '$no2', '$no3', '$no4', '$no5', '$no6', '$no7', '$no8', '$score')";

if ($koneksi->query($sql) === TRUE) {
    echo "<script>alert('Berhasil mengisi Quiz');
        window.location='kuis-end.php';</script>";
  } else {
    echo "Error: " . $sql . "<br>" . $koneksi->error;
  }

$koneksi->close();
?>