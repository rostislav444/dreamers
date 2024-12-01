from django.utils.html import format_html


def blender_material_preview(obj):
    if obj.preview and obj.color:
        # Создаем контейнер с позиционированием
        return format_html("""
            <div style="
                position: relative;
                width: 120px;
                height: 120px;
            ">
                <img src="{}" style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: {};
                    opacity: 0.75;
                "></div>
            </div>
        """, obj.preview.url, obj.color.hex)
    elif obj.color:
        return format_html(
            '<div style="background-color: {}; width: 120px; height: 120px;"></div>',
            obj.color.hex
        )
    elif obj.preview:
        return format_html(
            '<img src="{}" style="width: 120px; height: 120px; object-fit: cover;">',
            obj.preview.url
        )
    return '-'