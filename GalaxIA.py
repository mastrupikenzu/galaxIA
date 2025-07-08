import pymssql

from cat.mad_hatter.decorators import tool, hook
from cat.log import log
from .dbfunction import get_sqlserver_connection, execute_query_return_string, call_stored_procedure_two_params


conn = None

#--------------Settings----------------
# @hook
# def agent_prompt_prefix(prefix, cat):
#     settings = cat.mad_hatter.get_plugin().load_settings()
#     prefix = settings["prompt_prefix"]

#     return prefix

# @tool(return_direct=True, examples=[
#     "reparto di C1500",
#     "posizione di C1510",
#     "reparto di R0500"])
# def get_machine_department(machine_name, cat):
#     """
#     Restituisce il reparto della macchina.     
#     Input è il nome della macchina
#     """
#     global conn
#     try:
#         if conn is None:
#             conn = get_sqlserver_connection()
#             log.info("Connessione al database stabilita con successo.")
#     except Exception as e:
#         log.error(f"Errore di connessione: {e}")
#         return f"Errore di connessione: {e}"
#     try:
#         result = execute_query_return_string(conn, f"SELECT Department FROM ScadaNode WHERE ReportDescription = '{machine_name}'")
#         if result is None:
#             return f"Reparto di {machine_name} non trovato"
#         else:
#             reparto = result[0]
#             return f"Il reparto di {machine_name} è {reparto}"
#     except Exception as ex:
#         log.error(f"Errore durante l'esecuzione della query: {ex}")
#         return f"Errore durante l'esecuzione della query: {ex}"    


@tool( return_direct=True, examples=[
    "OEE of C1500"
    "Performance of C1500"
    "Availability of C1500"
    "Quality of C1500"
    "OEE of V4890 for October"
    "Performance of T0810 over the last 2 months"
    "Quality of R0500"
    "Analyze OEE of C1510" 
     ])
def get_oee_last_year (machine_name, cat):
    """
    Retrieve the Overall Equipment Effectiveness (OEE), performance, availability, and quality data for a specified machine over the last 12 months.
The machine name consists of 5 characters: the first character is a letter (e.g., R, C, A) followed by four numbers. 
"""
     #test
    #return f"l'oee è 47,7 % per {machine_name} negli ultimi 12 mesi"
    global conn
    try:
        if conn is None:
            conn = get_sqlserver_connection()
            log.info("Connessione al database stabilita con successo.")
    except Exception as e:
        log.error(f"Errore di connessione: {e}")
        return f"Errore di connessione: {e}"
    try:
        # 3 = oee macchina
        result = call_stored_procedure_two_params(conn, 'Gal_HistOEE_MonthAVG_SEL', 3, machine_name)
        if not result:
            return f"Nessuna registrazione OEE per {machine_name} negli ultimi 12 mesi."
        mesi = [
            "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
            "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"
        ]
        righe = []
        righe.append(
                f"Negli ultimi 12 mesi l'OEE di {machine_name} è stato:"
            )
        for row in result:
            try:
                mese_num = int(row[6])
                mese_str = mesi[mese_num-1] if 1 <= mese_num <= 12 else str(row[6])
            except Exception:
                mese_str = str(row[6])
            oee = f"{float(row[2]):.0f}"
            quality = f"{float(row[3]):.0f}"
            performance = f"{float(row[4]):.0f}"
            availability = f"{float(row[5]):.0f}"
            year = str(row[7]).split('-')[0]  # Prende solo l'anno dalla data
            righe.append(
                f"Mese di {mese_str} {year}: OEE = {oee}, Disponibilità = {availability}, Performance = {performance}, Qualità = {quality}"
            )
        return "\n".join(righe)
    except Exception as ex:
        log.error(f"Errore durante l'esecuzione della query: {ex}")
        return f"Errore durante l'esecuzione della query: {ex}"
       
      
@tool( return_direct=True, examples=[
    "Speed of C1500"
    "How fast is C1510 running?"
    "Current speed of R0500"
    ])   
def get_machine_speed (machine_name, cat):
    """    
    Retrieve the current operating speed of a specified machine.
    If the speed is 0, it indicates the machine is correctly stopped.
    Input is the machine name."""
    global conn
    try:
        if conn is None:
            conn = get_sqlserver_connection()
            log.info("Connessione al database stabilita con successo.")
    except Exception as e:
        log.error(f"Errore di connessione: {e}")
        return f"Errore di connessione: {e}"
    try:

        result = execute_query_return_string(conn, f"""
                                             SELECT TOP (1)  [Descrizione],CAST(Valore AS DECIMAL(10,1)) AS Velocita,[Unità],FORMAT([Timestamp], 'dd/MM/yyyy') AS [Data],FORMAT([Timestamp], 'HH:mm') AS [Ora]
                                            FROM [GestioneImpianti].[dbo].[v_HistData]
                                            where ReportDescription='{machine_name}' and PerformanceMonitor=1 and [Timestamp] >= DATEADD(HOUR, -1, GETDATE()) order  by Timestamp desc 
                                             """                                             )
        if result is None:
            return f"Nessuna registrazione di velocità nell'ultima ora per {machine_name}"
        else:   
            descrizione = result[0]
            velocita = result[1]
            unita = result[2]
            data = result[3]
            ora = result[4]
            return f"La {descrizione} di {machine_name} è {velocita} {unita} (registrata il {data} alle {ora})"         
            return f"La velocità di {machine_name} è {result}"
    except Exception as ex:
        log.error(f"Errore durante l'esecuzione della query: {ex}")
        return f"Errore durante l'esecuzione della query: {ex}"
    