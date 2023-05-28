from app import db
from datetime import datetime

cartificate_group = db.Table(
    'certificate_group',
    db.Column('certificate_id', db.Integer, db.ForeignKey('certificates.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)


class SQLCertificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    expiration = db.Column(db.Integer, unique=False, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime)
    # updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True))
    expirated_at = db.Column(db.DateTime(timezone=True))
    groups = db.relationship('SQLGroup', secondary=cartificate_group, backref=db.backref('certificados', lazy='dynamic'))


class SQLGroup(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    # created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(timezone=True))
    # updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True))
