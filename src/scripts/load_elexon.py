from src.database.insert_data import InsertToDatabase
from src.utils.sessions import elexon_session
from src.loaders.elexon.indo import load_indo
from src.loaders.elexon.agws import load_agws
from src.loaders.elexon.fuelhh import load_fuelhh
from src.loaders.elexon.ndf import load_ndf
from src.loaders.elexon.ndfd import load_ndfd

def main():
    session = elexon_session()
    db = InsertToDatabase()

    try:
        print("########## INDO ##########")
        load_indo(
            start_date = "2023-08-01T00:30:00Z",
            end_date = "2026-08-01T00:00:00Z",
            db = db,
            hour_window = 14 * 24,
            session = session
        )

        print("########## AGWS ##########")
        load_agws(
            start_date = "2023-08-01T02:30:00Z",
            end_date = "2026-08-01T02:00:00Z",
            db = db,
            hour_window = 7 * 24,
            session = session 
        )

        print("########## FUELHH ##########")
        load_fuelhh(
            start_date = "2023-08-01T00:30:00Z",
            end_date = "2026-08-01T00:00:00Z",
            db = db,
            hour_window = 7 * 24,
            session = session
        )

        print("########## NDF ##########")
        load_ndf(
            start_date = "2023-08-01T00:30:00Z",
            end_date = "2026-08-01T00:00:00Z",
            db = db,
            session = session
        )

        print("########## NDFD ##########")
        load_ndfd(
            start_date = "2023-08-01T00:00:00Z",
            end_date = "2026-08-01T00:00:00Z",
            db = db,
            session = session
        )

    finally:
        db.close()

if __name__ == "__main__":
    main()