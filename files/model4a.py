"""
Model exported as python.
Name : modelo4
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
import processing


class Modelo4(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        pass

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Estadísticas por categorías
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersecci_n_5cafccc7_7b4a_4305_a46a_0001a329f185',
            'OUTPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/output/lenguajes_por_pais.gpkg',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EstadsticasPorCategoras'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo4'

    def displayName(self):
        return 'modelo4'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4()
