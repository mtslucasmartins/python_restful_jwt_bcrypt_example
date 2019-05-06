import bcrypt
from database import db

from models.clinic import ClinicModel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), index=True, unique=True, nullable=False)
    username = db.Column(db.String(), index=True, unique=True, nullable=False)
    fullname = db.Column(db.String(), index=False, unique=False, nullable=False)
    password = db.Column(db.String(), index=False, unique=False, nullable=False)
    
    fk_clinics_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    clinic = db.relationship('ClinicModel', foreign_keys='UserModel.fk_clinics_id')

    def save(self):
        try:
            if ClinicModel.find_by_cnpj(self.clinic.cnpj) is None:
                db.session.add(self.clinic)
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise Exception('Algo deu errado inserindo usuário.')
            

    def delete(self):
        db.session.query(UserModel.id == self.id).delete()
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'fullname': self.fullname,
            'clinic': self.clinic.json()
        }

    @classmethod
    def count_all(cls, authorized_user=None):
        query = db.session.query(cls)
        if authorized_user is not None:
            query = query.filter(cls.fk_clinics_id == authorized_user.clinic.id)
        return query.count()

    @classmethod
    def find_all(cls, offset=None, limit=None, authorized_user=None):
        query = db.session.query(cls)
        if authorized_user is not None:
            query = query.filter(cls.fk_clinics_id == authorized_user.clinic.id)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def find_by_id(cls, id, authorized_user=None):
        query = db.session.query(cls).filter(cls.id == id)
        if authorized_user is not None:
            query.filter(cls.fk_clinics_id == authorized_user.clinic.id)
        return query.first()

    @classmethod
    def find_by_email(cls, email, authorized_user=None):
        query = db.session.query(cls).filter(cls.email == email)
        if authorized_user is not None:
            query.filter(cls.fk_clinics_id == authorized_user.clinic.id)
        return query.first()

    @classmethod
    def find_by_username(cls, email, authorized_user=None):
        return query.filter_by(username = username).first()

    @staticmethod
    def generate_hash(password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')

    @staticmethod
    def verify_hash(password, hash):
        return bcrypt.checkpw(password.encode('utf8'), hash.encode('utf8'))


# db.Index('users_id_idx', db.func.lower(db.metadata.tables['users'].c.id))
# db.Index('users_email_idx', db.func.lower(db.metadata.tables['users'].c.email))
# db.Index('users_username_idx', db.func.lower(db.metadata.tables['users'].c.username))