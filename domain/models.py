from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.types import Numeric as Decimal # O simplemente usa Numeric
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Rol(Base):
    __tablename__ = "rol"
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String)
    usuarios = relationship("Usuario", back_populates="rol")

class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True)
    contrasena = Column(String)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"))
    rol = relationship("Rol", back_populates="usuarios")

class Videojuego(Base):
    __tablename__ = "videojuego"
    id_juego = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio = Column(Decimal)
    stock = Column(Integer)

class Venta(Base):
    __tablename__ = "venta"
    id_venta = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    total = Column(Decimal)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    id_detalle = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta.id_venta"))
    id_juego = Column(Integer, ForeignKey("videojuego.id_juego"))
    cantidad = Column(Integer)
    precio_unitario = Column(Decimal)