import datetime
from backend.application import db


class VirusSpreadRecord(db.Model):
    NOT_GIVEN = "not_given"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120), nullable=False)
    province = db.Column(db.String(120), nullable=False, default=NOT_GIVEN)
    cases_confirmed = db.Column(db.Integer, nullable=True)
    cases_deaths = db.Column(db.Integer, nullable=True)
    cases_recovered = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    __table_name__ = "virus_spread_record"
    __table_args__ = (
        db.UniqueConstraint("country", "province", "created_at", name="country_province_uc"),
    )

    def __repr__(self):
        return f"{self.country}, {self.province}"


class VirusDailyStatRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cases_confirmed = db.Column(db.Integer, nullable=True)
    cases_deaths = db.Column(db.Integer, nullable=True)
    cases_recovered = db.Column(db.Integer, nullable=True)
    cases_confirmed_new = db.Column(db.Integer, nullable=True)
    cases_deaths_new = db.Column(db.Integer, nullable=True)
    cases_recovered_new = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    __table_name__ = "virus_daily_stat_record"
