import {ProductPartsInterface} from "@/interfaces/Materials";
import {SkuInterface} from "@/interfaces/Product";
import {selectedMaterialsInterface} from "@/components/App/Product/index";

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

export const findSkuWithMaterialsSet = (selectedMaterials: selectedMaterialsInterface, skuList: SkuInterface[]): SkuInterface => {
    for (const sku of skuList) {
        let isMatch = true;

        for (const materialId in sku.materials) {
            if (selectedMaterials[materialId] !== sku.materials[materialId]) {
                isMatch = false;
                break;
            }
        }

        if (isMatch) {
            return sku; // Return the matching SKU
        }
    }

    throw new Error('No matching SKU found'); // Throw an error if no matching SKU is found
}
