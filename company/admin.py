from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    site_header = 'Trang Quản lý'
    site_title = 'Trang Quản lý'
    index_title = 'Công ty TTT'

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            if app['app_label'] == 'summary':
                modelpop = list()
                modelpoplist = ('Position', 'Deparment', 'DateLog',
                                'TBTCType', 'TBTCBrand', 'TBTCManage',
                                'TBVTType', 'TBVTBrand', 'TBVTManage',
                                'UnitMeasure',
                                )
                for model in app['models']:
                    if model['object_name'] in modelpoplist:
                        modelpop.append(app['models'].index(model))
                modelpop.sort(reverse=True)
                for i in modelpop:
                    app['models'].pop(i)

        return app_list
