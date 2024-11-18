import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {ProductPart} from "@/interfaces/Product/Parts";
import {CameraProductPartInterface} from "@/interfaces/Product/Camera";

function getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
}

export const parseMaterials = (materials: string) => {
    return Object.fromEntries(
        materials.split('_').slice(1).map(pair => pair.split('-').map(Number))
    );
};

export const parseMaterialsWithDefaults = (
    materials: string | undefined,
    material_parts: ProductPart[]
) => {
    // Сначала парсим переданную строку материалов
    const parsedMaterials = materials ? Object.fromEntries(
        materials.split('_')
            .slice(1)
            .map(pair => pair.split('-').map(Number))
    ) : {};

    // Проходим по всем material_parts и заполняем отсутствующие или null значения
    material_parts.forEach(part => {
        // Если для данного part.id нет значения или оно null
        if (!parsedMaterials[part.id] && part.material_groups[0]?.materials[0]) {
            parsedMaterials[part.id] = part.material_groups[0].materials[0].id;
        }
    });

    return parsedMaterials;
};

export const generateMaterialsSlug = (materials: SelectedMaterialsInterface) => {
    return 'materials_' + Object.entries(materials).map(([part, material]) => `${part}-${material}`).join('_');
}

export const setFirstMaterials = (material_parts: ProductPart[]) => {
    const initialMaterials: SelectedMaterialsInterface = {};

    material_parts.forEach(part => {
        initialMaterials[part.id] = part.material_groups[0].materials[0].id;
    });
    return initialMaterials;
}


export const setInitialMaterials = (material_parts: ProductPart[]) => {
    const initialMaterials: SelectedMaterialsInterface = {};

    material_parts.forEach(part => {
        const length = part.material_groups[0].materials.length
        const randomIndex = getRandomInt(length)
        initialMaterials[part.id] = part.material_groups[0].materials[randomIndex]?.id;
    });
    console.log('material_parts', material_parts)
    console.log('initialMaterials', initialMaterials)
    return initialMaterials;
}


export const CameraImageFromMaterials = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return parts.map(part => {
        const partId = part.part.id
        return part.materials.find(material => material.material == selectedMaterials[partId]) || {
            image: '',
            thumbnails: {s: '', m: ''}
        }
    })
}


export const getThumbnailS = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return CameraImageFromMaterials(parts, selectedMaterials).map(part => part.thumbnails.s)
}

export const getThumbnailM = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return CameraImageFromMaterials(parts, selectedMaterials).map(part => part.thumbnails.m)
}