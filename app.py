from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, BigInteger, String, Float, Boolean, Date, Enum, Text, ForeignKey, DateTime, func, desc, text, DECIMAL
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

import uvicorn

DATABASE = 'mysql+pymysql://root:qwerty@localhost:3307/Medical_Screening'
engine = create_engine(DATABASE, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# Models Definitions
# -----------------------------
class Address(Base):
    __tablename__ = 'Address'
    Address_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    City = Column(String(100))
    Street = Column(String(255))
    Zip_Code = Column(String(20))

class Patient(Base):
    __tablename__ = 'Patient'
    Patient_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    Gender = Column(Enum('Male', 'Female', 'Other'))
    Phone_Number = Column(String(20))
    Email = Column(String(255))

class Doctor(Base):
    __tablename__ = 'Doctor'
    Doctor_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    First_Name = Column(String(100))
    Last_Name = Column(String(100))
    Gender = Column(Enum('Male', 'Female', 'Other'))
    Work_Experience = Column(String(10))

class Hospital(Base):
    __tablename__ = 'Hospital'
    Hospital_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Hospital_Name = Column(String(255))
    Capacity = Column(BigInteger)
    Phone_Number = Column(String(15))
    Email = Column(String(100))
    Address_ID = Column(BigInteger, ForeignKey('Address.Address_ID', ondelete="CASCADE", onupdate="CASCADE"))

class Appointment(Base):
    __tablename__ = 'Appointment'
    Appointment_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Doctor_ID = Column(BigInteger, ForeignKey('Doctor.Doctor_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Patient_ID = Column(BigInteger, ForeignKey('Patient.Patient_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Status = Column(Enum('Scheduled', 'Completed', 'Cancelled'))
    Appointment_Date = Column(Date)

class MedicalHistory(Base):
    __tablename__ = 'Medical_History'
    History_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Patient_ID = Column(BigInteger, ForeignKey('Patient.Patient_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Date_of_last_checkup = Column(Date)

class MedicalNotes(Base):
    __tablename__ = 'Medical_Notes'
    Note_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Patient_ID = Column(BigInteger, ForeignKey('Patient.Patient_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Note = Column(String(255))
    Type = Column(String(255))

class Payment(Base):
    __tablename__ = 'Payment'
    Payment_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Patient_ID = Column(BigInteger, ForeignKey('Patient.Patient_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Amount = Column(DECIMAL(10, 2))
    Payment_Date = Column(Date)
    Status = Column(String(50))

class MedicalScreeningTest(Base):
    __tablename__ = 'Medical_Screening_Test'
    Test_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Test_Name = Column(String(255))
    Cost = Column(Float)
    Payment_ID = Column(BigInteger, ForeignKey('Payment.Payment_ID', ondelete="CASCADE", onupdate="CASCADE"))

class RequiredSupplies(Base):
    __tablename__ = 'Required_Supplies'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Test_ID = Column(BigInteger, ForeignKey('Medical_Screening_Test.Test_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Supply_Name = Column(String(255))

class MedicalScreeningResult(Base):
    __tablename__ = 'Medical_Screening_Result'
    Result_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Test_Name = Column(String(255))
    Result = Column(String(255))
    Test_ID = Column(BigInteger, ForeignKey('Medical_Screening_Test.Test_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Patient_ID = Column(BigInteger, ForeignKey('Patient.Patient_ID', ondelete="CASCADE", onupdate="CASCADE"))

class SupplyOrder(Base):
    __tablename__ = 'Supply_Order'
    Order_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Test_ID = Column(BigInteger, ForeignKey('Medical_Screening_Test.Test_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Hospital_ID = Column(BigInteger, ForeignKey('Hospital.Hospital_ID', ondelete="CASCADE", onupdate="CASCADE"))
    Order_Date = Column(Date)
    Status = Column(String(50))

class Pharmacy(Base):
    __tablename__ = 'Pharmacy'
    Pharmacy_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Order_ID = Column(BigInteger, ForeignKey('Supply_Order.Order_ID', ondelete="CASCADE", onupdate="CASCADE"))

class CreditCardCompany(Base):
    __tablename__ = 'Credit_Card_Company'
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    Company_Name = Column(String(255))
    Payment_ID = Column(BigInteger, ForeignKey('Payment.Payment_ID', ondelete="CASCADE", onupdate="CASCADE"))


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# -----------------------------
# Routes and Forms
# -----------------------------

# Homepage with links to forms
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 1. Adding a new Medical Note (Add Form)
@app.get("/medical_note/add", response_class=HTMLResponse)
async def add_medical_note_form(request: Request):
    return templates.TemplateResponse("medical_note_add.html", {"request": request})

@app.post("/medical_note/add")
async def add_medical_note(
    Patient_ID: int = Form(...),
    Note: str = Form(...),
    Type: str = Form(...)
):
    session = SessionLocal()
    try:
        # Check if the patient exists
        patient = session.query(Patient).filter(Patient.Patient_ID == Patient_ID).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Add the medical note
        new_note = MedicalNotes(
            Patient_ID=Patient_ID,
            Note=Note,
            Type=Type
        )
        session.add(new_note)
        session.commit()
        session.refresh(new_note)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    return RedirectResponse("/", status_code=303)


# 2. Updating an Appointment Status (Update Form)
@app.get("/appointment/update", response_class=HTMLResponse)
async def update_appointment_form(request: Request):
    return templates.TemplateResponse("appointment_update.html", {"request": request})

@app.post("/appointment/update")
async def update_appointment(Appointment_ID: int = Form(...), Status: str = Form(...)):
    session = SessionLocal()
    try:
        appointment = session.query(Appointment).filter(Appointment.Appointment_ID == Appointment_ID).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        appointment.Status = Status
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    return RedirectResponse("/", status_code=303)

# 3. Deleting a Required Supply record (Delete Form)
@app.get("/required_supplies/delete", response_class=HTMLResponse)
async def delete_required_supplies_form(request: Request):
    return templates.TemplateResponse("required_supplies_delete.html", {"request": request})

@app.post("/required_supplies/delete")
async def delete_required_supplies(ID: int = Form(...)):
    session = SessionLocal()
    try:
        required_supply = session.query(RequiredSupplies).filter(RequiredSupplies.ID == ID).first()
        if not required_supply:
            raise HTTPException(status_code=404, detail="Required Supply not found")
        session.delete(required_supply)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    return RedirectResponse("/", status_code=303)

# reports

@app.get("/report/appointment", response_class=HTMLResponse)
def appointment_report_form(request: Request):
    return templates.TemplateResponse("report_appointment.html", {"request": request, "appointment": None})

@app.get("/report/appointment/{appointment_id}", response_class=HTMLResponse)
def appointment_report(appointment_id: int, request: Request):
    session = SessionLocal()
    appointment = session.execute(text("""
        SELECT 
            a.Appointment_ID, 
            a.Appointment_Date,
            CONCAT(d.First_Name, ' ', d.Last_Name) AS Doctor_Name,
            p.First_Name AS Patient_First_Name,
            p.Last_Name AS Patient_Last_Name
        FROM Appointment a
        JOIN Doctor d ON a.Doctor_ID = d.Doctor_ID
        JOIN Patient p ON a.Patient_ID = p.Patient_ID
        WHERE a.Appointment_ID = :id
    """), {"id": appointment_id}).fetchone()
    session.close()
    return templates.TemplateResponse("report_appointment.html", {"request": request, "appointment": appointment})

@app.get("/report/medical_notes", response_class=HTMLResponse)
def medical_notes_report_form(request: Request):
    return templates.TemplateResponse("report_medical_notes.html", {"request": request, "notes": None})

@app.get("/report/medical_notes/{patient_id}", response_class=HTMLResponse)
def medical_notes_report(patient_id: int, request: Request):
    session = SessionLocal()
    notes = session.execute(text("""
        SELECT 
            n.Note_ID, n.Note, n.Type, n.Patient_ID,
            p.First_Name, p.Last_Name
        FROM Medical_Notes n
        JOIN Patient p ON n.Patient_ID = p.Patient_ID
        WHERE n.Patient_ID = :id
    """), {"id": patient_id}).fetchall()
    session.close()
    return templates.TemplateResponse("report_medical_notes.html", {"request": request, "notes": notes})

@app.get("/report/result", response_class=HTMLResponse)
def result_report_form(request: Request):
    return templates.TemplateResponse("report_result.html", {"request": request, "result": None})

@app.get("/report/result/{result_id}", response_class=HTMLResponse)
def result_report(result_id: int, request: Request):
    session = SessionLocal()
    row = session.execute(text("""
        SELECT
          r.Result_ID,
          r.Test_Name,
          r.Result,
          p.First_Name,
          p.Last_Name
        FROM Medical_Screening_Result AS r
        JOIN Patient AS p ON r.Patient_ID = p.Patient_ID
        WHERE r.Result_ID = :id
    """), {"id": result_id}).fetchone()
    session.close()

    return templates.TemplateResponse(
        "report_result.html",
        {"request": request, "result": row}
    )

@app.get("/tests", response_class=HTMLResponse)
def display_tests(request: Request):
    results = test_operations()
    return templates.TemplateResponse("tests.html", {"request": request, "results": results})

@app.get("/tests/operations")
def test_operations():
    session = SessionLocal()
    results = {}

    try:
        # O1: Schedule the appointment
        results['O1_schedule_appointment'] = {}
        before = session.execute(text("SELECT COUNT(*) FROM Appointment")).scalar()
        session.execute(text("""
            INSERT INTO Appointment (Doctor_ID, Patient_ID, Status, Appointment_Date)
            VALUES (2, 5, 'Scheduled', '2025-05-30')
        """))
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM Appointment")).scalar()
        results['O1_schedule_appointment']['passed'] = after == before + 1

        # O3: Submit a test order
        results['O3_submit_test_order'] = {}
        before_tests = session.execute(text("SELECT COUNT(*) FROM Medical_Screening_Test")).scalar()
        before_supplies = session.execute(text("SELECT COUNT(*) FROM Required_Supplies")).scalar()
        session.execute(text("""
            INSERT INTO Payment (Patient_ID, Amount, Payment_Date, Status)
            VALUES (5, 100.00, CURDATE(), 'Pending')
        """))
        pay_id = session.execute(text("SELECT MAX(Payment_ID) FROM Payment")).scalar()
        session.execute(text("""
            INSERT INTO Medical_Screening_Test (Test_Name, Cost, Payment_ID)
            VALUES ('Blood Panel', 100.00, :pid)
        """), {"pid": pay_id})
        test_id = session.execute(text("SELECT MAX(Test_ID) FROM Medical_Screening_Test")).scalar()
        session.execute(text("""
            INSERT INTO Required_Supplies (Test_ID, Supply_Name)
            VALUES (:tid, 'Syringe')
        """), {"tid": test_id})
        session.commit()
        after_tests = session.execute(text("SELECT COUNT(*) FROM Medical_Screening_Test")).scalar()
        after_supplies = session.execute(text("SELECT COUNT(*) FROM Required_Supplies")).scalar()
        results['O3_submit_test_order']['passed'] = after_tests == before_tests + 1 and after_supplies == before_supplies + 1

        # O5: Enter test results
        results['O5_enter_test_results'] = {}
        session.execute(text("""
            INSERT INTO Medical_Screening_Result (Test_Name, Result, Test_ID, Patient_ID)
            VALUES ('Blood Panel', 'Normal', :tid, 5)
        """), {"tid": test_id})
        session.commit()
        new_result = session.execute(text("SELECT Result FROM Medical_Screening_Result WHERE Test_ID = :tid"), {"tid": test_id}).scalar()
        results['O5_enter_test_results']['passed'] = new_result == 'Normal'

        # O6: Bill the patient
        results['O6_bill_patient'] = {}
        payment_status = session.execute(text("SELECT Status FROM Payment WHERE Payment_ID = :pid"), {"pid": pay_id}).scalar()
        results['O6_bill_patient']['passed'] = payment_status == 'Pending'

        # O7: Retrieve patient history
        results['O7_retrieve_patient_history'] = {}
        history_rows = session.execute(text("SELECT * FROM Medical_Notes WHERE Patient_ID = 5")).fetchall()
        results['O7_retrieve_patient_history']['passed'] = len(history_rows) > 0

        # O8: Update patient history
        results['O8_update_patient_history'] = {}
        result_data = session.execute(text("""
            SELECT Result, Patient_ID FROM Medical_Screening_Result
            WHERE Test_ID = :tid ORDER BY Result_ID DESC LIMIT 1
        """), {"tid": test_id}).fetchone()

        if result_data:
            note_text = result_data.Result
            patient_id = result_data.Patient_ID
            session.execute(text("""
                INSERT INTO Medical_Notes (Patient_ID, Note, Type)
                VALUES (:pid, :note, 'Medical_Treatment')
            """), {"pid": patient_id, "note": note_text})
            session.commit()
            found = session.execute(text("""
                SELECT COUNT(*) FROM Medical_Notes
                WHERE Patient_ID = :pid AND Note = :note
            """), {"pid": patient_id, "note": note_text}).scalar()
            results['O8_update_patient_history']['note_added'] = found > 0
            results['O8_update_patient_history']['passed'] = found > 0
        else:
            results['O8_update_patient_history'] = {
                "error": "No recent result found"
            }

        # O9: Allow patients to view history
        results['O9_view_patient_history'] = {}
        result_rows = session.execute(text("SELECT * FROM Medical_Notes WHERE Patient_ID = 5")).fetchall()
        results['O9_view_patient_history']['passed'] = len(result_rows) > 0

        # Form 1: Add Medical Note
        results['form_add_medical_note'] = {}
        before = session.execute(text("SELECT COUNT(*) FROM Medical_Notes WHERE Patient_ID = 5")).scalar()
        session.execute(text("""
            INSERT INTO Medical_Notes (Patient_ID, Note, Type)
            VALUES (5, 'Test Note from Form Test', 'Allergies')
        """))
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM Medical_Notes WHERE Patient_ID = 5")).scalar()
        results['form_add_medical_note']['passed'] = after == before + 1

        # Form 2: Update Appointment Status
        results['form_update_appointment'] = {}
        appointment_id = 4
        session.execute(text("UPDATE Appointment SET Status = 'Completed' WHERE Appointment_ID = :id"), {"id": appointment_id})
        session.commit()
        updated_status = session.execute(text("SELECT Status FROM Appointment WHERE Appointment_ID = :id"), {"id": appointment_id}).scalar()
        results['form_update_appointment']['passed'] = updated_status == 'Completed'

        # Form 3: Delete Required Supply
        results['form_delete_required_supply'] = {}
        supply_id = 1
        session.execute(text("DELETE FROM Required_Supplies WHERE ID = :id"), {"id": supply_id})
        session.commit()
        confirm = session.execute(text("SELECT COUNT(*) FROM Required_Supplies WHERE ID = :id"), {"id": supply_id}).scalar()
        results['form_delete_required_supply']['passed'] = confirm == 0

        # Report 1: Appointment Report
        results['report_appointment'] = {}
        appt_id = 4
        row = session.execute(text("""
            SELECT a.Appointment_ID, a.Appointment_Date,
                   CONCAT(d.First_Name, ' ', d.Last_Name) AS Doctor_Name,
                   p.First_Name AS Patient_First_Name,
                   p.Last_Name AS Patient_Last_Name
            FROM Appointment a
            JOIN Doctor d ON a.Doctor_ID = d.Doctor_ID
            JOIN Patient p ON a.Patient_ID = p.Patient_ID
            WHERE a.Appointment_ID = :id
        """), {"id": appt_id}).fetchone()
        results['report_appointment']['passed'] = row is not None

        # Report 2: Medical Notes Report
        results['report_medical_notes'] = {}
        notes = session.execute(text("SELECT * FROM Medical_Notes WHERE Patient_ID = 5")).fetchall()
        results['report_medical_notes']['passed'] = len(notes) > 0

        # Report 3: Result Report
        results['report_result'] = {}
        last_result_id = 3
        result = session.execute(text("""
            SELECT r.Result_ID, r.Test_Name, r.Result,
               p.First_Name, p.Last_Name
            FROM Medical_Screening_Result r
            JOIN Patient p ON r.Patient_ID = p.Patient_ID
            WHERE r.Result_ID = :rid
        """), {"rid": last_result_id}).fetchone()
        results['report_result']['passed'] = result is not None

    except Exception as e:
        session.rollback()
        results['error'] = str(e)
    finally:
        session.close()

    return results

@app.get("/tests/reset", response_class=HTMLResponse)
def reset_tests(request: Request):
    session = SessionLocal()
    cleanup_results = {}
    try:
        # O1: Remove the appointment inserted in the test (assumes Appointment_Date '2025-05-30' and Patient_ID = 5)
        session.execute(text("DELETE FROM Appointment WHERE Appointment_Date = '2025-05-30' AND Patient_ID = 5"))
        cleanup_results['O1_schedule_appointment_reset'] = True

        # O3: Remove the Payment, Medical_Screening_Test and Required_Supplies inserted during test order submission
        session.execute(text("DELETE FROM Payment WHERE Payment_Date = CURDATE() AND Patient_ID = 5"))
        session.execute(text("DELETE FROM Medical_Screening_Test WHERE Test_Name = 'Blood Panel'"))
        session.execute(text("DELETE FROM Required_Supplies WHERE Supply_Name = 'Syringe'"))
        cleanup_results['O3_submit_test_order_reset'] = True

        # O5: Remove the test result inserted
        session.execute(text("DELETE FROM Medical_Screening_Result WHERE Test_Name = 'Blood Panel' AND Patient_ID = 5"))
        cleanup_results['O5_enter_test_results_reset'] = True

        # O8: Remove Medical Notes added (assumes Type = 'Medical_Treatment')
        session.execute(text("DELETE FROM Medical_Notes WHERE Type = 'Medical_Treatment' AND Patient_ID = 5"))
        cleanup_results['O8_update_patient_history_reset'] = True

        # Cleanup for form: Add Medical Note
        session.execute(text("""
            DELETE FROM Medical_Notes
            WHERE Patient_ID = 5
              AND Note = 'Test Note from Form Test'
              AND Type = 'Allergies'
        """))

        # Cleanup for form: Update Appointment Status (revert to 'Scheduled')
        session.execute(text("""
            UPDATE Appointment
            SET Status = 'Scheduled'
            WHERE Appointment_ID = 4 AND Status = 'Completed'
        """))

        # Cleanup for form: Delete Required Supply (restore a dummy record if missing)
        if session.execute(text("SELECT COUNT(*) FROM Required_Supplies WHERE ID = 1")).scalar() == 0:
            # Ensure there is a dummy screening test to reference; insert one if needed.
            dummy_test_id = session.execute(text("SELECT Test_ID FROM Medical_Screening_Test WHERE Test_Name = 'Test Dummy'")).scalar()
            if not dummy_test_id:
                session.execute(text("""
                    INSERT INTO Medical_Screening_Test (Test_Name, Cost)
                    VALUES ('Test Dummy', 0.0)
                """))
                dummy_test_id = session.execute(text("SELECT MAX(Test_ID) FROM Medical_Screening_Test")).scalar()
            session.execute(text("""
                INSERT INTO Required_Supplies (Test_ID, Supply_Name)
                VALUES (:tid, 'Dummy Supply')
            """), {"tid": dummy_test_id})

        session.commit()
    except Exception as e:
        session.rollback()
        cleanup_results['error'] = str(e)
    finally:
        session.close()
    return templates.TemplateResponse("tests.html", {"request": request, "results": cleanup_results})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)