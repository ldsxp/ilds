import csv

from django.http import HttpResponse


class ExportCsvMixin:
    """
    导出 CSV 格式文件的动作

    支持自定义的内容：
    # 设置导出 Csv 文件的编码
    csv_charset = 'gb2312'
    """

    def export_as_csv(self, request, queryset):
        if getattr(self, 'using', None):
            queryset = queryset.using(self.using)

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        # 写入标题
        field_verbose_name = [field.verbose_name for field in meta.fields]

        response = HttpResponse(content_type='text/csv', charset=getattr(self, 'csv_charset', 'utf-8'))
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_verbose_name)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_all_as_csv(self, request, queryset):
        return self.export_as_csv(request, self.model.objects.all())

    # Export Selected
    export_as_csv.short_description = "导出已选中（csv）"
    export_all_as_csv.short_description = "导出全部（csv）"
