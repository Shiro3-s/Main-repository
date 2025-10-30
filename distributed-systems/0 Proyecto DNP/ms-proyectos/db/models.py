from pydantic import BaseModel
from typing import Optional

class Proyecto(BaseModel):
    codigo_bpin: str
    nombre_proyecto: str
    desc_proyecto: Optional[str]
    objetivo_general: Optional[str]
    objetivos_especificos: Optional[str]
    justificacion: Optional[str]
    fecha_inicio_proyecto: Optional[str]
    fecha_fin_prevista: Optional[str]
    fecha_fin_registrada: Optional[str]
    id_estado_proyecto: Optional[int]
    id_fase_proyecto: Optional[int]
    poblacion_beneficiaria: Optional[int]
    id_tipo_poblacion: Optional[int]
    valor_total_proyecto: Optional[float]
    id_programa: Optional[int]
    id_sector: Optional[int]
    id_ods: Optional[int]
    id_region: Optional[int]
    id_entidad_ejecutora: Optional[int]
    id_tipo_entidad: Optional[int]
    id_nivel_gobierno: Optional[int]
    id_estado: Optional[int]
    id_tipo_estado: Optional[int]

class Hito(BaseModel):
    id_hito: int
    nombre_hito: str
    desc_hito: Optional[str]
    fecha_programada: Optional[str]
    fecha_real: Optional[str]
    porcentaje_completado: Optional[float]
    responsable_hito: Optional[str]
    id_estado: Optional[int]
    id_tipo_estado: Optional[int]
    codigo_bpin: str

class Contrato(BaseModel):
    id_contrato: int
    numero_contrato: str
    objeto_contrato: Optional[str]
    contratista: Optional[str]
    valor_contrato: Optional[float]
    fecha_inicio_contrato: Optional[str]
    fecha_fin_contrato: Optional[str]
    id_estado: Optional[int]
    id_tipo_estado: Optional[int]
    id_tipo_contratacion: Optional[int]
    codigo_bpin: str

class Riesgo(BaseModel):
    id_riesgo: int
    codigo_bpin: str
    probabilidad: Optional[float]
    estrategia_mitigacion: Optional[str]
    responsable_seguimiento: Optional[str]
    fecha_identificacion: Optional[str]
    id_impacto: Optional[int]

class Impacto(BaseModel):
    id_impacto: int
    nombre_impacto: str
    desc_impacto: Optional[str]

class NivelRiesgo(BaseModel):
    id_nivel_riesgo: int
    nombre_nivel: str
    desc_nivel: Optional[str]

class AvanceFisico(BaseModel):
    id_avance_fisico: int
    fecha_reporte: Optional[str]
    periodo_reporte: Optional[str]
    porcentaje_avance_acumulado: Optional[float]
    porcentaje_avance_periodo: Optional[float]
    desc_actividades: Optional[str]
    productos_entregados: Optional[str]
    metas_cumplidas: Optional[int]
    dificultades_presentadas: Optional[str]
    acciones_correctivas: Optional[str]
    responsable_reporte: Optional[str]
    codigo_bpin: str

class FaseProyecto(BaseModel):
    id_fase_proyecto: int
    nombre_fase_proyecto: str
    desc_fase_proyecto: Optional[str]