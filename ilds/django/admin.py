import csv

from .model import ModelFields

from django.http import HttpResponse


class ExportCsvMixin:
    """
    导出 CSV 格式文件的动作

    支持自定义的内容：
    # 设置导出 Csv 文件的编码
    csv_charset = 'gb2312'
    # 自定义导出 ForeignKey 字段内容
    related_fields = {'ForeignKey字段': {'fields': ['字段1', '字段2'], }}
    # 排除导出字段
    csv_export_exclude = []
    """

    def export_as_csv(self, request, queryset):
        if getattr(self, 'using', None):
            queryset = queryset.using(self.using)

        meta = self.model._meta
        related_fields = getattr(self, 'related_fields', {})
        export_exclude = getattr(self, 'csv_export_exclude', [])

        # 获取需要导出的 ForeignKey 字段
        for related_field, data in related_fields.items():
            if getattr(meta.concrete_model, related_field, None):
                cg_model = getattr(meta.concrete_model, related_field).field.related_model
                # 另外一种获取模型的方法
                # [field for field in meta.fields if field.name == 'cg_hetong_bianhao'][0].remote_field.model
                m = ModelFields(cg_model)
            else:
                raise ValueError(f'没有找到 {related_field} 模型')
            data['names'] = []
            for field in data['fields']:
                verbose = m.field_to_verbose(field)
                if verbose is None:
                    raise ValueError(f'没有找到 {field} 字段')
                # 写入标题
                data['names'].append(verbose)

        field_names = []
        # 写入标题
        field_verbose_name = []

        for field in meta.fields:
            if field.name in export_exclude or field.verbose_name in export_exclude:
                continue
            field_names.append(field.name)
            if field.name in related_fields:
                field_verbose_name.extend(related_fields[field.name]['names'])
            else:
                field_verbose_name.append(field.verbose_name)

        response = HttpResponse(content_type='text/csv', charset=getattr(self, 'csv_charset', 'utf-8'))
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_verbose_name)
        for obj in queryset:
            rows = []
            for field in field_names:
                if field in related_fields:
                    related_obj = getattr(obj, field, None)
                    if related_obj:
                        for related_field in related_fields[field]['fields']:
                            val = getattr(related_obj, related_field)
                            rows.append(val)
                    else:
                        rows.extend(['' for _ in related_fields[field]['fields']])
                else:
                    val = getattr(obj, field)
                    rows.append(val)
            writer.writerow(rows)

        return response

    def export_all_as_csv(self, request, queryset):
        return self.export_as_csv(request, self.model.objects.all())

    # Export Selected
    export_as_csv.short_description = "导出已选中（csv）"
    export_all_as_csv.short_description = "导出全部（csv）"
