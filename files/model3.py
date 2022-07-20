#########################################################################################
#########################################################################################

"""
Model exported as python.
Name : modelo3
Group : 
With QGIS : 32208
"""

#########################################################################################
#########################################################################################

#En este script, seleccionamos distintos rasters y les sacamos informacion para poder armar una tabla.
#Contamos con datos de elevacion, poblacion y landquality (archivo que generamos del model2)
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

##################################################################
# Create new model3
##################################################################

class Modelo3(QgsProcessingAlgorithm):

    #Agregamos los rasters
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo_3', 'fix_geo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Popd1800', 'popd1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Popd1900', 'popd1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Popd2000', 'popd2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}
##################################################################
# Corregir geometrias
##################################################################
        alg_params = {
            'INPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shx',
            'OUTPUT': parameters['Fix_geo_3']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo_3'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

##################################################################
# Quitar campos
##################################################################
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Geometr_as_corregidas_7635a498_a661_4b89_9737_b9aa9d949988',
            'OUTPUT': parameters['Drop_fields_3']
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}   
        
##################################################################
# Estadisticas de zona por raster
##################################################################
        
    # landquality
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Campos_restantes_ab67611e_24e1_40ef_ac3f_ce096f92e095',
            'INPUT_RASTER': 'landquality_fc714d1e_9304_4ce9_8fa1_5f399ffcbe0e',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media a nivel pais
            'OUTPUT': parameters['Landq']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        
        # popd1800
        alg_params = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': 'Campos_restantes_ab67611e_24e1_40ef_ac3f_ce096f92e095',
            'INPUT_RASTER': 'popd_1800AD_4e3576d5_2aef_45a9_a767_3a357db5d6e9',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media a nivel pais
            'OUTPUT': parameters['Popd1800']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Popd1800'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # popd 1900
        alg_params = {
            'COLUMN_PREFIX': 'popd1900',
            'INPUT': 'Campos_restantes_ab67611e_24e1_40ef_ac3f_ce096f92e095',
            'INPUT_RASTER': 'popd_1900AD_605dfe9d_6a92_4489_b8d4_2dfa901cc0a8',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media a nivel pais
            'OUTPUT': parameters['Popd1900']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Popd1900'] = outputs['EstadsticasDeZona']['OUTPUT']
        return results

        # popd2000
        alg_params = {
            'COLUMN_PREFIX': 'popd2000',
            'INPUT': 'Campos_restantes_ab67611e_24e1_40ef_ac3f_ce096f92e095',
            'INPUT_RASTER': 'popd_2000AD_ac642b7f_86ba_4d87_a40f_2ae470d699fa',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media a nivel pais
            'OUTPUT': parameters['Popd2000']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Popd2000'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

##################################################################
# Guardar registro en archivo .csv
##################################################################        
       
        alg_params = {
            'OUTPUT': 'C:/Users/catal/OneDrive - Facultad de Cs Económicas - UBA/UdeSA/Herramientas computacionales/Clase 4/output/raster_statics.csv',
            'USE_HTML': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GuardarRegistroEnArchivo'] = processing.run('native:savelog', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

    

 
