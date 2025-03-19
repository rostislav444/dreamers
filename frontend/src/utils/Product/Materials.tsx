import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {ProductPart} from "@/interfaces/Product/Parts";
import {CameraProductPartInterface} from "@/interfaces/Product/Camera";
import {log} from "console";

function getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
}

export const parseMaterials = (materials: string) => {
    return Object.fromEntries(
        materials.split('_').slice(1).map(pair => pair.split('-').map(Number))
    );
};

export const parseMaterialsWithDefaults = (material_parts: ProductPart[], materialsString?: string) => {
    // Parse URL materials into a map of partId -> materialId
    const materialMap = new Map(
        materialsString?.split('_')
            .map(pair => pair.split('-').map(Number))
            .map(([partId, materialId]) => [partId, materialId]) || []
    );
    
    return Object.fromEntries(
        material_parts.map(part => {
            // Function to get default material (first in first group)
            const getDefault = () => ({
                partId: part.id,
                group: part.material_groups[0].name,
                material: part.material_groups[0].materials[0].id,
                material_name: part.material_groups[0].materials[0].name
            });
            
            // If no URL material for this part, use default
            const materialId = materialMap.get(part.id);
            if (!materialId) return [part.blender_name, getDefault()];
            
            // Find the material in available groups
            const foundGroup = part.material_groups.find(group => 
                group.materials.some(m => m.id === materialId)
            );
            
            // If found matching material, use it; otherwise use default
            if (foundGroup) {
                const material = foundGroup.materials.find(m => m.id === materialId)!;
                return [part.blender_name, {
                    partId: part.id,
                    group: foundGroup.name,
                    material: materialId,
                    material_name: material.name
                }];
            }
            
            return [part.blender_name, getDefault()];
        })
    );
};

export const generateMaterialsSlug = (materials: SelectedMaterialsInterface) => {
    return 'materials_' + Object.entries(materials).map(([part, material]) => `${part}-${material}`).join('_');
}


export const setInitialMaterials = (material_parts: ProductPart[]) => {
    const initialMaterials: SelectedMaterialsInterface = {};

    material_parts.forEach(part => {
        const materialGroup = part.material_groups[getRandomInt(part.material_groups.length)]
        const randomIndex = getRandomInt(materialGroup.materials.length)

        if (materialGroup.materials[randomIndex]) {
            initialMaterials[part.blender_name] = {
                partId: part.id,
                group: materialGroup.name,
                material: materialGroup.materials[randomIndex].id,
                material_name: materialGroup.materials[randomIndex].name
            }
        }
    });
    return initialMaterials;
}


export const CameraImageFromMaterials = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return parts.map(part => {
        return part.materials.find(material => material.material == selectedMaterials[part.part.blender_name]?.material) || part.materials[0]
    })
}


export const getThumbnailS = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return CameraImageFromMaterials(parts, selectedMaterials).map(part => part.thumbnails.s)
}

export const getThumbnailM = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return CameraImageFromMaterials(parts, selectedMaterials).map(part => part.thumbnails.m)
}