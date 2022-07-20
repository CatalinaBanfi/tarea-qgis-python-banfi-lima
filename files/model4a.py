"""
Model exported as python.
Name : modelo4a
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_wlds', 'fix_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Interseccion', 'interseccion', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Corregir geometrías - idiomas
        alg_params = {
            'INPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/clean.shp',
            'OUTPUT': parameters['Fix_wlds']
        }
        outputs['CorregirGeometrasIdiomas'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_wlds'] = outputs['CorregirGeometrasIdiomas']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Estadísticas por categorías
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersecci_n_d36207f8_da61_4d05_b5e3_e6e9b230431d',
            'OUTPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/output/languages_by_country.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EstadsticasPorCategoras'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Corregir geometrías - countries
        alg_params = {
            'INPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['CorregirGeometrasCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['CorregirGeometrasCountries']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Intersección
        alg_params = {
            'INPUT': outputs['CorregirGeometrasIdiomas']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['CorregirGeometrasCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Interseccion']
        }
        outputs['Interseccin'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Interseccion'] = outputs['Interseccin']['OUTPUT']
        return results

    def name(self):
        return 'modelo4a'

    def displayName(self):
        return 'modelo4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4a()
