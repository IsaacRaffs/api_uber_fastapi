"""
Objetivo: Criar uma API de App de Corridas (Uber)

Recurso/Objeto: Corrida
- Atributos: origem, destino, distancia(km), valor(R$ 6,65 + R$ 2/km),
- Atributos: estado('Requisitada', 'Em Andamento', 'Finalizado')
"""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from ulid import ulid
from fastapi.encoders import jsonable_encoder


app = FastAPI()


class Corrida(BaseModel):
    id: str | None
    origem: str
    destino: str
    distancia: float
    valor: float
    estado: str


corridas: list[Corrida] = [
    Corrida(id=str(ulid()), origem='timbre', destino='morro', distancia=450, valor=209, estado="Requisitada"),
    Corrida(id=str(ulid()), origem='mangue', destino='cupuaçu', distancia=255, valor=129, estado="Requisitada"),
    Corrida(id=str(ulid()), origem='osasco', destino='macau', distancia=300, valor=190, estado="Em Andamento"),
    Corrida(id=str(ulid()), origem='zona rural', destino='ministro', distancia=30, valor=210, estado="Finalizado"),
]


@app.get('/corrida')
async def listar_corridas() -> list[Corrida]:
    return corridas


@app.get('/corrida/{estado}')
async def corrida_filtrar_estado(estado: str):
    list = []
    for corrida in corridas:
        if corrida.estado.upper().split() == estado.upper().split():
            list.append(corrida)
    return jsonable_encoder(list)
    raise HTTPException(status_code=404, detail='Corrida não localizada!')


@app.post('/corrida')
async def criar_corrida(corre: Corrida) -> Corrida:
    u_corrida = Corrida(id=str(ulid()), origem=corre.origem, destino=corre.destino, distancia=corre.distancia, valor=2 * corre.distancia + 6.65, estado='requisitada')
    corridas.append(u_corrida)
    return u_corrida


@app.post('/corrida/iniciar/{id}')
async def iniciar_corrida(id: str):
    for corrida in corridas:
        if corrida.id == id:
            if corrida.estado.upper().split() != "requisitada".upper().split():
                raise HTTPException(status_code=400, detail="A corrida deve ter sido requisitada para ser iniciada.")
            corrida = "em andamento".estado.upper().split() 
            return corrida
    raise HTTPException(status_code=404, detail="Corrida não encontrada!")


@app.post('/corrida/finalizar/{id}')
async def finalizar_corrida(id: str):
    for corrida in corridas:
        if corrida.id == id:
            if corrida.estado.upper().split() != "em endamento".upper().split():
                raise HTTPException(status_code=400, detail="A corrida deve ter estar em andamento para ser finalizada.")
            corrida = "finalizado".estado.upper().split() 
            return corrida
    raise HTTPException(status_code=404, detail="Corrida não encontrada!")


@app.put('/corrida/{id}')
async def corrida_alterar(id: str, corrida: Corrida):
    for corre in corridas:
        if id == corre.id and ('requisitada'.upper().split() == corre.estado.upper().split() or 'em andamento'.upper().split() == corre.estado.upper().split()):
            corre.origem = corrida.origem
            corre.destino = corrida.destino
            corre.distancia = corrida.distancia
            corre.valor = corrida.valor
            corre.estado = corrida.estado
            return corre
        else:
            return HTTPException(status_code=400, detail="A corrida deve ter sido requisitada ou estar em andamento")
    raise HTTPException(status_code=404, detail='Corrida não localizada!')


@app.delete('/corrida/{id}')
async def corrida_remover(id: str):
    for corrida in corridas:
        if corrida.id == id and 'requisitada'.upper().split() == corrida.estado.upper().split():
            corridas.remove(corrida)
            return Response(status_code=204)

    return HTTPException(status_code=404, detail="A corrida deve ter sido requisitada")