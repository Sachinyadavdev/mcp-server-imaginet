from typing import List, Dict, Any, Optional
from core.db import get_db_connection
from core.utils import serialize_sql_row

def analyze_eod_reports(employee_name: Optional[str] = None, date_filter: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Analyze End of Day (EOD) reports. Automatically maps employee ID to their Name 
    and brings in the associated project information for context.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT e.id, e.date, h.employee_name, e.description, p.name as project_name 
                FROM tbl_eod_report e
                LEFT JOIN tbl_hr_master h ON e.employee_id = h.ID
                LEFT JOIN tbl_project_master p ON e.project_id = p.id
                WHERE 1=1
            '''
            params = []
            if employee_name:
                sql += ' AND h.employee_name LIKE %s'
                params.append(f"%{employee_name}%")
            if date_filter:
                sql += ' AND e.date = %s'
                params.append(date_filter)
                
            sql += ' ORDER BY e.date DESC LIMIT %s'
            params.append(limit)
            
            cursor.execute(sql, tuple(params))
            return [serialize_sql_row(row) for row in cursor.fetchall()]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

def analyze_leave_history(employee_name: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get Employee Leave Records heavily joined with Employee Name.
    Retrieves the actual reason, subject, and timeframe.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT l.id, h.employee_name, l.leave_from_date, l.leave_to_date, 
                       l.leave_subject, l.leave_reason, l.leave_status
                FROM tbl_leave l
                LEFT JOIN tbl_hr_master h ON l.employee_id = h.ID
                WHERE 1=1
            '''
            params = []
            if employee_name:
                sql += ' AND h.employee_name LIKE %s'
                params.append(f"%{employee_name}%")
                
            sql += ' ORDER BY l.leave_from_date DESC LIMIT %s'
            params.append(limit)
            
            cursor.execute(sql, tuple(params))
            return [serialize_sql_row(row) for row in cursor.fetchall()]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

def analyze_attendance_records(employee_name: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get daily attendance data joined with Employee Name and shift working hours.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT a.id, a.date, h.employee_name, a.start_time, a.end_time, 
                       a.working_hours, a.attendance_status
                FROM tbl_attendance_data a
                LEFT JOIN tbl_hr_master h ON a.employee_id = h.ID
                WHERE 1=1
            '''
            params = []
            if employee_name:
                sql += ' AND h.employee_name LIKE %s'
                params.append(f"%{employee_name}%")
                
            sql += ' ORDER BY a.date DESC LIMIT %s'
            params.append(limit)
            
            cursor.execute(sql, tuple(params))
            return [serialize_sql_row(row) for row in cursor.fetchall()]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

def get_database_schema() -> Dict[str, Any]:
    """
    Get the full database schema (all tables and columns) from the live server.
    """
    conn = get_db_connection()
    schema = {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            for t in tables:
                t_name = list(t.values())[0]
                cursor.execute(f"DESCRIBE {t_name}")
                columns = cursor.fetchall()
                schema[t_name] = [f"{col['Field']} ({col['Type']})" for col in columns]
        return schema
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def run_select_query(sql_query: str) -> List[Dict[str, Any]]:
    """
    Run a custom SQL SELECT query for advanced, dynamic analytics.
    """
    if not sql_query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE", "EXPLAIN")):
         return [{"error": "Security Restriction: Only SELECT, SHOW, or DESCRIBE queries are permitted."}]
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            return [serialize_sql_row(row) for row in cursor.fetchall()]
    except Exception as e:
        return [{"error": f"SQL Error: {str(e)}"}]
    finally:
        conn.close()

def get_system_summary() -> Dict[str, Any]:
    """Get a quick high-level summary of the company ERP data."""
    conn = get_db_connection()
    summary = {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT count(*) as total FROM tbl_hr_master")
            summary["Total Employees"] = cursor.fetchone()["total"]
            
            cursor.execute("SELECT count(*) as total FROM tbl_project_master")
            summary["Total Projects"] = cursor.fetchone()["total"]
            
            cursor.execute("SELECT count(*) as total FROM tbl_client_master")
            summary["Total Clients"] = cursor.fetchone()["total"]
            
            cursor.execute("SELECT count(*) as total FROM tbl_invoice_master")
            summary["Total Invoices"] = cursor.fetchone()["total"]
        return summary
    except Exception as e:
         return {"error": str(e)}
    finally:
        conn.close()
