USE Medical_Screening;

LOAD DATA INFILE '/var/lib/mysql-files/Address.csv'
INTO TABLE Address
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Address_ID, Country, City, Street, Zip_Code);

LOAD DATA INFILE '/var/lib/mysql-files/Patient.csv'
INTO TABLE Patient
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Patient_ID, First_Name, Last_Name, Date_of_Birth, Gender, Phone_Number, Email, Age, Address_ID);

LOAD DATA INFILE '/var/lib/mysql-files/Doctor.csv'
INTO TABLE Doctor
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Doctor_ID, First_Name, Last_Name, Date_of_Birth, Gender, Phone_Number, Email, Work_Experience, Age, Address_ID);

LOAD DATA INFILE '/var/lib/mysql-files/Hospital.csv'
INTO TABLE Hospital
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Hospital_ID, Hospital_Name, Capacity, Address_ID);

LOAD DATA INFILE '/var/lib/mysql-files/Hospital_Specializations.csv'
INTO TABLE Hospital_Specializations
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Specialization_ID, Hospital_ID, Specialization);

LOAD DATA INFILE '/var/lib/mysql-files/Appointment.csv'
INTO TABLE Appointment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Appointment_ID, Doctor_ID, Patient_ID, Status, Appointment_Date);

LOAD DATA INFILE '/var/lib/mysql-files/Medical_History.csv'
INTO TABLE Medical_History
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(History_ID, Patient_ID, Past_Diseases, Past_Surgeries, Chronic_Conditions, Date_of_last_checkup);

LOAD DATA INFILE '/var/lib/mysql-files/Medical_Screening_Test.csv'
INTO TABLE Medical_Screening_Test
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Test_ID, Test_Name, Result_Time, Cost);

LOAD DATA INFILE '/var/lib/mysql-files/Medical_Screening_Result.csv'
INTO TABLE Medical_Screening_Result
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Result_ID, Test_Name, Result, Test_ID, Patient_ID);