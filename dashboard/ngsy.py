from fipy.ngsi.entity import BaseEntity, BoolAttr, FloatAttr





class AI4SDW_services(BaseEntity):
    type = 'ai4sdw_service'
    area_crossed: BoolAttr
    fall_pred: BoolAttr
    risk_leve: FloatAttr