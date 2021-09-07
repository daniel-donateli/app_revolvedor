
class Revolvedor:
  def __init__(self, id, nome) -> None:
    self.id = id
    self.nome = nome
    self.medidas = []
  
  def add_medida(self, hora, t1, t2, t3, t4, t5, media, ligado, motivo):
    medida = _Medida()
    medida.hora = hora
    medida.temperaturas = [t1, t2, t3, t4, t5]
    medida.media = media
    medida.ligado = ligado
    medida.motivo = motivo
    self.medidas.append(medida)


class _Medida:
  pass