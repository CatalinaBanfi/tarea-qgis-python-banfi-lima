        ## En este modelo vamos a utilizar el shapefile "WLDS" obtenido del modelo 1 y el shapefile "10m-admin-0-countries" 
        ## con las fronteras de los países, obtenido de Natural Earth Data, para un archivo CSV con el número de idiomas por país.
        
        # Definimos las rutas para los inputs y los outputs del modelo.
        
        mainpath = "/Maestría UdeSA/Materias UdeSA/Herramientas computacionales/4. Python + GIS"
        inpath = "{}/input".format(mainpath)
        outpath = "{}/output".format(mainpath)
        wlds = "{}/clean/clean.shp".format(outpath)
        admin = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(inpath)
        outcsv = "{}/languages_by_country.csv".format(outpath)
        
        # a) Utilizamos el algoritmo "fix geometries" en el shapefile WLDS. 
        
        fg1_dict = {
            'INPUT': wlds,
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', fg1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']

        # b) Utilizamos el algoritmo "fix geometries" en el shapefile 10m-admin-0-countries. 
        fg2_dict = {
            'INPUT': admin,
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', fg2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        # c) Realizamos la intersección entre las dos layer obtenidas en los pasos anteriores.
        
        int_dict = {
            'INPUT': outputs['FixGeometriesWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['FixGeometriesCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Intersection'] = processing.run('native:intersection', int_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Intersection']['OUTPUT']

        # d) Usamos el algoritmo statistics by categories en la intersección del punto c), guardando el resultado como archivo CSV.
        sbc_dict = {
            'CATEGORIES_FIELD_NAME': 'ADMIN',
            'INPUT': outputs['Intersection']['OUTPUT'],
            'VALUES_FIELD_NAME': '',
            'OUTPUT': outcsv
        }
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', sbc_dict, context=context, feedback=feedback, is_child_algorithm=True)
 
