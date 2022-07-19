"""
Model exported as python.
Name : modelo3
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Popd2000', 'popd2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Guardar objetos vectoriales en archivo
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Estadistica_zonal_5fa625aa_6f46_46a9_ae4a_fb9bcb452e63',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/output/rasterstatics.gpkg',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GuardarObjetosVectorialesEnArchivo'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Guardar registro en archivo
        alg_params = {
            'OUTPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/output/raster_stata.csv',
            'USE_HTML': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GuardarRegistroEnArchivo'] = processing.run('native:savelog', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Guardar objetos vectoriales en archivo
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Estadistica_zonal_5fa625aa_6f46_46a9_ae4a_fb9bcb452e63',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/output/raster_statics.gpkg',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GuardarObjetosVectorialesEnArchivo'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Estadísticas de zona
        alg_params = {
            'COLUMN_PREFIX': 'popd2000',
            'INPUT': 'Estadistica_zonal_c8d485a0_4f0c_4c1e_b34e_7fa868d02f36',
            'INPUT_RASTER': 'popd_2000AD_0fdcf75c_7398_4061_8fa3_ee6bff263ca8',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Popd2000']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Popd2000'] = outputs['EstadsticasDeZona']['OUTPUT']
        return results

    def name(self):
        return 'modelo3'

    def displayName(self):
        return 'modelo3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo3()
