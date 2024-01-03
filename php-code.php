<?php
// Database configuration
$servername = "localhost"; // Replace with your MySQL server address
$username = "your_username"; // Replace with your MySQL username
$password = "your_password"; // Replace with your MySQL password
$dbname = "sensor_data_db"; // Replace with your database name
$table = "sensor_data"; // Replace with your table name

// Get the POST data from the ESP8266
$postdata = file_get_contents("php://input");

// Decode JSON data received from the ESP8266
$data = json_decode($postdata);

// Log received data for debugging
error_log("Received data: " . print_r($data, true));

if ($data !== null && isset($data->sensor_value)) {
    // Create connection to MySQL database
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Prepare and execute SQL query to insert sensor data into the table
    $sensor_value = $data->sensor_value;
    $sql = "INSERT INTO $table (sensor_value) VALUES ($sensor_value)";

    if ($conn->query($sql) === TRUE) {
        echo "Sensor data inserted successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    // Close the database connection
    $conn->close();
} else {
    echo "Invalid data received";
}
?>
