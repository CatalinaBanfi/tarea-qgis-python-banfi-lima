"""
Model exported as python.
Name : modelo1
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc', 'AUTOINC', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo', 'fix.geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        # Corregir geometrías
        alg_params = {
            'INPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/langa/langa.shp',
            'OUTPUT': parameters['Fixgeo']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos clone
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Cadena
            'FORMULA': '"NAME_PROP"',
            'INPUT': 'menor_a_11_e2e59278_7b99_43cc_b719_245d3eee1cab',
            'OUTPUT': parameters['Field_calc']
        }
        outputs['CalculadoraDeCamposClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['CalculadoraDeCamposClone']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s)
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculado_700dd975_e378_44ba_9587_6cc8f33365ee',
            'OUTPUT': parameters['Wldsout']
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entero
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incrementado_81c51bfe_63df_4568_b888_0225bddfe225',
            'OUTPUT': parameters['Length']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Filtro de entidad
        alg_params = {
            'INPUT': 'Calculado_8076269b_ce95_46ff_9a5a_ee36032d6f82',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FiltroDeEntidad'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FiltroDeEntidad']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Agregar campo que auto-incrementa 
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['CorregirGeometras']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc']
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']
        return results

    def name(self):
        return 'modelo1'

    def displayName(self):
        return 'modelo1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo1()
