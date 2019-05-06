from database import db

class ClinicModel(db.Model):
    __tablename__ = 'clinics'

    id = db.Column(db.Integer, primary_key = True)
    cnpj = db.Column(db.String(), unique=True, nullable = False)
    description = db.Column(db.String(), nullable = False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.query(UserModel.id == self.id).delete()
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'cnpj': self.cnpj,
            'description': self.description
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_cnpj(cls, cnpj):
        return cls.query.filter_by(cnpj = cnpj).first()