from django.core.management.base import BaseCommand
from django.utils import timezone
from nse.models import NseSettings
from nsepython import nse_optionchain_scrapper
import pandas as pd

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        res = NseSettings.objects.all()
        self.stdout.write("Process start time %s" % time)
        for i in res:
            print(i.client)
            a = nse_optionchain_scrapper(i.nse_list)

            res_ce = []
            res_pe = []
            filter_ce = []
            filter_pe = []
            output_res = []

            def form_res(data):
                res = {}
                if data:

                    for key in data.keys():
                        res[key] = data[key]
                return res

            for data in a["records"]['data']:
                res_ce.append(form_res(data.get('CE')))
                res_pe.append(form_res(data.get('PE')))

            for data in a['filtered']['data']:
                filter_ce.append(form_res(data.get('CE')))
                filter_pe.append(form_res(data.get('PE')))

            ce = pd.DataFrame(res_ce)
            pe = pd.DataFrame(res_pe)
            fil_ce = pd.DataFrame(filter_ce)
            fil_pe = pd.DataFrame(filter_pe)
            file_name = i.path
            with pd.ExcelWriter(file_name) as writer:
                ce.to_excel(writer, sheet_name='CE')
                pe.to_excel(writer, sheet_name='PE')
                fil_ce.to_excel(writer, sheet_name='FILTERED_CE')
                fil_pe.to_excel(writer, sheet_name='FILTERED_PE')
            print('Completed')
        self.stdout.write("Process end time %s" % time)