import sqlite3
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt

con = sqlite3.connect("Chinook_Sqlite.sqlite")

cursor = con.cursor()

def printAllTables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

def printSchema():
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    schema_info = cursor.fetchall()

def bestSellingTrack() -> list[Any]:
    cursor.execute("""SELECT t.name, il.Quantity FROM InvoiceLine il
                   JOIN Track t ON il.TrackId = t.TrackId
                   ORDER BY il.Quantity
                   LIMIT 10;""")
    bestTracks = cursor.fetchall()
    return bestTracks

def bestCountry() -> Any:
    cursor.execute("""SELECT BillingCountry FROM Invoice i
                   GROUP BY i.BillingCountry
                   HAVING MAX(i.Total)
                   ORDER BY i.Total DESC LIMIT 1;""")
    country = cursor.fetchone()
    return country

def topSalesEmployee() -> Any:
    cursor.execute("""
                   SELECT e.FirstName || ' ' ||  e.LastName as employee FROM Employee e
                    JOIN Customer c ON e.EmployeeId = c.SupportRepId
                    GROUP BY employee
                    HAVING MAX(c.SupportRepId)
                    LIMIT 1;
                   """)
    employee = cursor.fetchone()
    return employee

def main() -> None:
    tracks = bestSellingTrack()
    country = bestCountry()
    employee = topSalesEmployee()
    df = pd.DataFrame(tracks, columns=["Треки", "Количество"])
    plt.bar(df["Треки"], df["Количество"])
    plt.show()
    con.close()

if __name__ == '__main__':
    main()
