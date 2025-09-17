<?php
$conn = mysqli_connect("localhost", "root", "", "ppks");

function report($data) {
    global $conn;

    $nama = strtolower(stripslashes($data["nama"]));
    $nim = mysqli_real_escape_string($conn, $data["nim"]);
    $laporan = mysqli_real_escape_string($conn, $data["laporan"]);

    $result = mysqli_query($conn, "SELECT nama FROM report WHERE nama='$nama'");
    if(mysqli_fetch_assoc($result)){
        echo "<script>alert('Laporan sudah terkirim');</script>";
        return false;
    }


    mysqli_query($conn, "INSERT INTO report VALUES('', '$nim', '$nama', '$laporan')");
    return mysqli_affected_rows($conn);

}
?>