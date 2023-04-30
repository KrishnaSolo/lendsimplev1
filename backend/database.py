from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

mock_data = {
    "properties": [
        {
            "id": 1,
            "name": "Welland Vale Project",
            "description": "Welland Vale is a 3 home luxury development project currently being managed by heartwood.",
            "address": "St. Catharines, ON",
            "type": "Lending",
            "investmentNeeded": 100000,
            "investmentGained": 25000,
            "minInvestment": 50,
            "closingDate": "2023-04-25",
            "image": "wellandVale.png",
            "detailedDescription": "Participate in the ownership of a newly constructed 2-unit multifamily homes in St. Catharines, ON. \n\n Participate in the ownership of a newly constructed 2-unit multifamily homes in St. Catharines, ON. Participate in the ownership of a newly constructed 2-unit multifamily homes in St. Catharines, ON. Participate in the ownership of a newly constructed 2-unit multifamily homes in St. Catharines, ON.",
            "realizedMOIC": 2.0,
            "realizedIRR": 66,
            "projectTimeline": 2.1,
            "projectROIC": 139,
            "highlights": [
                "Features 3 residential units comprising of one bedroom studio houses.",
                "Sought-after building in a popular location suggests consistent occupancy.",
                "Constructed in 2020. Constructed by 76 Contruction Management",
                "Aimed to be built for the modern small homes sought out for new home owners",
                "Plaster on lathe, inlaid oak flooring, cast iron tubs and wood panel doors were all installed.",
                "Built with both stone and wood to have a unique design for these properties",
            ],
            "locationScore": {"transit": 80, "walking": 85, "biking": 94},
            "investmentType": {
                "type": "Core",
                "detailedDescription": "Participate in the ownership of a newly constructed plaza in Simcoe, ON. \n\n Participate in the ownership of a newly constructed plaza in Simcoe, ON. Participate in the ownership of a newly constructed plaza in Simcoe, ON. Participate in the ownership of a newly constructed plaza in Simcoe, ON. Participate in the ownership of a newly constructed plaza in Simcoe, ON.",
                "target": "For investors looking to generate stable income with very low risk.",
            },
        },
        {
            "id": 3,
            "name": "Cedar Park Plaza",
            "description": "The Cedar Park Plaza is a ~58,000 sq. ft commercial development consisting of 35+ retail stores & offices.",
            "address": "Simcoe, ON",
            "type": "Lending",
            "investmentNeeded": 100000,
            "investmentGained": 35000,
            "minInvestment": 55,
            "closingDate": "2023-05-23",
            "image": "cedarPark.jpg",
            "detailedDescription": "Participate in the ownership of a newly constructed homes in Pelham, ON. \n\n Participate in the ownership of a newly constructed homes in Pelham, ON. Participate in the ownership of a newly constructed homes in Pelham, ON. Participate in the ownership of a newly constructed homes in Pelham, ON. Participate in the ownership of a newly constructed homes in Pelham, ON.",
            "realizedMOIC": 2.2,
            "realizedIRR": 71,
            "projectTimeline": 3.4,
            "projectROIC": 241,
            "highlights": [
                "Features 10 commercial units for sale in 58,000sq. ft. lot",
                "Sought-after building in a popular location suggests consistent occupancy.",
                "Started Constructed in 2019. Constructed by 76 Contruction Management",
                "Aimed to be built for new homes in the area that need business to follow",
                "Consists of office spaces to businesses to open, but also large building for stores",
            ],
            "locationScore": {"transit": 90, "walking": 81, "biking": 88},
            "investmentType": {
                "type": "Core",
                "define": "A Core investment usually requires very little management from owners and are usually occupied with tenants on long-term leases. Core investments are typically acquired and held. This type of investing is as close as one can get to passive investing when buying properties directly.",
                "target": "For investors looking to generate stable income with very low risk.",
            },
        },
        {
            "id": 2,
            "name": "River Road Estates",
            "description": "The Pelham Development is a 2 homes luxury development led by the Heartwood team. All homes were Pre-sold at $1.8M.",
            "address": "Pelham, ON",
            "type": "Lending",
            "investmentNeeded": 100000,
            "investmentGained": 65000,
            "minInvestment": 40,
            "closingDate": "2023-04-23",
            "image": "riverRoad.png",
            "detailedDescription": "Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor. \n\n Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor.Participate in the ownership of a newly renovated and fully occupied 19-unit multifamily apartment building in the Vancouver-Broadway Corridor.",
            "realizedMOIC": 1.9,
            "realizedIRR": 35,
            "projectTimeline": 3.8,
            "projectROIC": 133,
            "highlights": [
                "Features 2 pre sold luxury residentails homes featuring a 2 bedroom 1 level house",
                "Isolated homes, not near any motorways with large property value",
                "Started Constructed in 2020. Constructed by 76 Contruction Management",
                "Aimed to be built for owners that need a place away from the city",
                "Consists to large open areas in front and behind the house for various uses",
                "Containes natural terrain surrounding the house to build a natural feel",
            ],
            "locationScore": {"transit": 70, "walking": 89, "biking": 89},
            "investmentType": {
                "type": "Core",
                "define": "A Core investment usually requires very little management from owners and are usually occupied with tenants on long-term leases. Core investments are typically acquired and held. This type of investing is as close as one can get to passive investing when buying properties directly.",
                "target": "For investors looking to generate stable income with very low risk.",
            },
        },
    ]
}


def init_db(app):
    if os.environ.get("ENVIRONMENT") == "PRODUCTION":
        # Google Cloud SQL database configuration
        db_user = os.environ.get("CLOUD_SQL_USERNAME")
        db_password = os.environ.get("CLOUD_SQL_PASSWORD")
        db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
        db_socket_dir = os.environ.get("DB_SOCKET_DIR")
        cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

        db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@/{db_name}?host={db_socket_dir}/{cloud_sql_connection_name}"
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    else:
        # Local development database configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.session.close_all()
        db.engine.dispose()
        db.drop_all()
        db.create_all()
        from backend.data_local_loader import insert_example_data

        insert_example_data(mock_data)
