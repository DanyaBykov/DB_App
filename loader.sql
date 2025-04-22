# DROP DATABASE IF EXISTS Medical_Screening;
CREATE DATABASE IF NOT EXISTS Medical_Screening;
USE Medical_Screening;

CREATE TABLE IF NOT EXISTS Address (
    Address_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Country VARCHAR(100),
    City VARCHAR(100),
    Street VARCHAR(255),
    Zip_Code VARCHAR(20)
)ENGINE = innodb COMMENT ="Address Table";

CREATE TABLE IF NOT EXISTS Patient (
    Patient_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Date_of_Birth DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    Phone_Number VARCHAR(20),
    Email VARCHAR(255),
    Age INT,
    Address_ID BIGINT UNSIGNED,
    FOREIGN KEY (`Address_ID`) REFERENCES `Address`(`Address_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Patient Table";


CREATE TABLE IF NOT EXISTS Doctor (
    Doctor_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Date_of_Birth DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    Phone_Number VARCHAR(20),
    Email VARCHAR(255),
    Work_Experience INT,
    Age INT,
    Address_ID BIGINT UNSIGNED,
    FOREIGN KEY (`Address_ID`) REFERENCES `Address`(`Address_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Doctor Table";

CREATE TABLE IF NOT EXISTS Hospital (
    Hospital_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Hospital_Name VARCHAR(255),
    Capacity INT,
    Address_ID BIGINT UNSIGNED,
    FOREIGN KEY (`Address_ID`) REFERENCES `Address`(`Address_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Hospital Table";

CREATE TABLE IF NOT EXISTS Hospital_Specializations (
    Specialization_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Hospital_ID BIGINT UNSIGNED,
    Specialization VARCHAR(255),
    FOREIGN KEY (`Hospital_ID`) REFERENCES `Hospital`(`Hospital_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Hospital Specialization Table";

CREATE TABLE IF NOT EXISTS Appointment (
    Appointment_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Doctor_ID BIGINT UNSIGNED,
    Patient_ID BIGINT UNSIGNED,
    Status ENUM('Scheduled', 'Completed', 'Cancelled'),
    Appointment_Date DATE,
    FOREIGN KEY (`Doctor_ID`) REFERENCES `Doctor`(`Doctor_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`Patient_ID`) REFERENCES `Patient`(`Patient_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Appointment Table";

CREATE TABLE IF NOT EXISTS Medical_History (
    History_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Patient_ID BIGINT UNSIGNED,
    Past_Diseases TEXT,
    Past_Surgeries TEXT,
    Chronic_Conditions TEXT,
    Date_of_last_checkup DATE,
    FOREIGN KEY (`Patient_ID`) REFERENCES `Patient`(`Patient_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Medical History Table";

CREATE TABLE IF NOT EXISTS Medical_Screening_Test (
    Test_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Test_Name VARCHAR(255),
    Result_Time VARCHAR(50),
    Cost DOUBLE
)ENGINE = INNODB COMMENT = "Medical Screening Test Table";

CREATE TABLE IF NOT EXISTS Medical_Screening_Result (
    Result_ID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Test_Name VARCHAR(255),
    Result VARCHAR(255),
    Test_ID BIGINT UNSIGNED,
    Patient_ID BIGINT UNSIGNED,
    FOREIGN KEY (`Test_ID`) REFERENCES `Medical_Screening_Test`(`Test_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`Patient_ID`) REFERENCES `Patient`(`Patient_ID`) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = INNODB COMMENT = "Medical Screening Result Table";
