import {ProductPartsInterface} from "@/interfaces/Materials";
import {SkuInterface} from "@/interfaces/Product";


export const chooseInitialMaterials = (parts: ProductPartsInterface[], materialGroupId?: number, materialId?: number) => {
    return parts.reduce((dict, part) => {
        let selectedMaterialId: number|null = null;

        if (materialGroupId && materialId) {
            const selectedMaterialGroup = part.material_groups.find(group => group.id === materialGroupId);
            if (selectedMaterialGroup) {
                const selectedMaterial = selectedMaterialGroup.materials.find(material => material.id === materialId);
                selectedMaterialId = selectedMaterial ? selectedMaterial.id : null;
            }
        } else {
            selectedMaterialId = part.material_groups[0].materials[0].id;
        }

        // Add entry to the dictionary with part id as key and selected material id as value
        dict[part.id] = selectedMaterialId ? selectedMaterialId : 0;
        return dict;
    }, {} as { [key: number]: number }); // Initialize the accumulator as an empty object
}
