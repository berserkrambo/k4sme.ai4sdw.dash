from fipy.ngsi.entity import BaseEntity, BoolAttr, FloatAttr, TextAttr



ROUGHNESS_ESTIMATE_TYPE = 'RoughnessEstimate'

class RoughnessEstimateEntity(BaseEntity):
    type = ROUGHNESS_ESTIMATE_TYPE
    acceleration: FloatAttr
    roughness: FloatAttr