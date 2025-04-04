from comun.extensions import db


class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
        }