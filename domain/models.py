from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

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
    activo = Column(Boolean)
    rol = relationship("Rol", back_populates="usuarios")
    ventas = relationship("Sale", back_populates="usuario")

class Platform(Base):
    __tablename__ = "platform"
    id_plataforma = Column(Integer, primary_key=True, index=True)
    nombre_plataforma = Column(String)
    videojuegos = relationship("Videojuego", back_populates="plataforma")

class Genre(Base):
    __tablename__ = "genre"
    id_genero = Column(Integer, primary_key=True, index=True)
    nombre_genero = Column(String)
    videojuegos = relationship("Videojuego", back_populates="genero")

class Videojuego(Base):
    __tablename__ = "videogame"
    id_juego = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    id_plataforma = Column(Integer, ForeignKey("platform.id_plataforma"))
    id_genero = Column(Integer, ForeignKey("genre.id_genero"))
    precio = Column(Numeric)
    stock_local = Column(Integer)
    stock_global = Column(Integer)
    es_historico = Column(Boolean)
    imagen = Column(String)
    
    plataforma = relationship("Platform", back_populates="videojuegos")
    genero = relationship("Genre", back_populates="videojuegos")

class Sale(Base):
    __tablename__ = "sale"
    id_venta = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, server_default=func.now())
    total = Column(Numeric)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    
    usuario = relationship("Usuario", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    id_detalle = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("sale.id_venta"))
    id_juego = Column(Integer, ForeignKey("videogame.id_juego"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric)
    
    venta = relationship("Sale", back_populates="detalles")